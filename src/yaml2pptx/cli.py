"""CLI interface for yaml2pptx."""

from __future__ import annotations

import logging
import platform
import subprocess
import time
from pathlib import Path
from typing import Optional

import typer

import yaml

from yaml2pptx.components.renderer import render_presentation
from yaml2pptx.engine.generator import GenerationError, generate
from yaml2pptx.engine.template import TemplateError, TemplateManager
from yaml2pptx.parser.yaml_parser import YamlParseError, parse_yaml
from yaml2pptx.themes import Theme, get_theme

logger = logging.getLogger("yaml2pptx")

app = typer.Typer(
    name="yaml2pptx",
    help="Generate PowerPoint presentations from YAML files.",
    no_args_is_help=True,
)


@app.command()
def gen(
    input_yaml: Path = typer.Argument(..., help="Path to YAML presentation file"),
    output: Optional[Path] = typer.Option(None, "--output", "-o", help="Output .pptx path"),
    template: Optional[Path] = typer.Option(None, "--template", "-t", help="Override template"),
    validate_only: bool = typer.Option(False, "--validate-only", help="Only validate, don't generate"),
    open_file: bool = typer.Option(False, "--open", help="Open file after generation"),
) -> None:
    """Generate a PowerPoint presentation from a YAML file."""
    try:
        model = parse_yaml(input_yaml)
    except YamlParseError as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1)

    if template:
        model.template = str(template)

    if validate_only:
        typer.echo(f"Valid: {input_yaml}")
        return

    try:
        out = generate(model, output)
    except (GenerationError, TemplateError) as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1)

    typer.echo(f"Generated: {out}")

    if open_file:
        _open_file(out)


@app.command()
def inspect(
    template_pptx: Path = typer.Argument(..., help="Path to a .pptx template file"),
    layout: Optional[str] = typer.Option(None, "--layout", help="Show specific layout only"),
) -> None:
    """Inspect a PowerPoint template's layouts and placeholders."""
    try:
        tm = TemplateManager(template_pptx)
    except TemplateError as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1)

    if layout:
        for info in tm.get_layouts_info():
            if info.name.lower() == layout.lower() or str(info.index) == layout:
                typer.echo(f"[{info.index}] \"{info.name}\"")
                for ph in info.placeholders:
                    typer.echo(f"  - idx={ph.idx}, type={ph.type}, name=\"{ph.name}\"")
                return
        typer.echo(f"Layout '{layout}' not found.", err=True)
        raise typer.Exit(1)

    typer.echo(f"Template: {template_pptx.name}")
    typer.echo(tm.format_inspect())


@app.command()
def init(
    name: str = typer.Option("Presentation", "--name", help="Presentation name"),
    template: Optional[str] = typer.Option(None, "--template", help="Template to reference"),
    slides: int = typer.Option(5, "--slides", help="Number of placeholder slides"),
    output: Path = typer.Option(Path("presentation.yaml"), "--output", "-o", help="Output YAML path"),
) -> None:
    """Create a starter YAML presentation file."""
    lines = []
    if template:
        lines.append(f'template: "{template}"')
    lines.append(f'output: "{name.lower().replace(" ", "_")}.pptx"')
    lines.append("metadata:")
    lines.append(f'  title: "{name}"')
    lines.append('  author: ""')
    lines.append("slides:")
    lines.append(f'  - layout: title_slide')
    lines.append(f'    title: "{name}"')
    lines.append(f'    subtitle: ""')

    for i in range(1, slides):
        lines.append(f"  - layout: content")
        lines.append(f'    title: "Slide {i + 1}"')
        lines.append(f"    content:")
        lines.append(f'      - "Point 1"')
        lines.append(f'      - "Point 2"')

    output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    typer.echo(f"Created: {output}")


@app.command()
def build(
    input_yaml: Path = typer.Argument(..., help="Path to YAML presentation file"),
    output: Optional[Path] = typer.Option(None, "--output", "-o", help="Output .pptx path"),
    theme_name: Optional[str] = typer.Option(None, "--theme", help="Theme name"),
    open_file: bool = typer.Option(False, "--open", help="Open file after generation"),
    watch: bool = typer.Option(False, "--watch", "-w", help="Watch for changes and rebuild"),
) -> None:
    """Build a presentation using the component-based renderer (themed slides)."""
    if watch:
        _watch_and_rebuild(input_yaml, output, theme_name, open_file)
        return
    try:
        text = input_yaml.read_text(encoding="utf-8")
    except (FileNotFoundError, PermissionError, OSError) as e:
        typer.echo(f"Error reading file: {e}", err=True)
        raise typer.Exit(1)

    try:
        data = yaml.safe_load(text)
    except yaml.YAMLError as e:
        typer.echo(f"Error parsing YAML: {e}", err=True)
        raise typer.Exit(1)

    if not isinstance(data, dict) or "slides" not in data:
        typer.echo("Error: YAML must contain a 'slides' key", err=True)
        raise typer.Exit(1)

    theme = get_theme(theme_name or data.get("theme", "default"))

    # Apply theme overrides from YAML
    theme_config = data.get("theme_config", {})
    if theme_config.get("organization"):
        theme.organization = theme_config["organization"]
    if theme_config.get("document_title"):
        theme.document_title = theme_config["document_title"]
    if theme_config.get("classification"):
        theme.classification = theme_config["classification"]
    if theme_config.get("footer"):
        theme.footer_text = theme_config["footer"]

    out_path = output or Path(data.get("output", "output.pptx"))

    try:
        out = render_presentation(
            slides_data=data["slides"],
            theme=theme,
            output_path=out_path,
            metadata=data.get("metadata"),
        )
    except (TypeError, ValueError, KeyError) as e:
        typer.echo(f"Error rendering presentation: {e}", err=True)
        logger.exception("Rendering failed")
        raise typer.Exit(1)
    except OSError as e:
        typer.echo(f"Error writing file: {e}", err=True)
        raise typer.Exit(1)

    typer.echo(f"Generated: {out}")

    if open_file:
        _open_file(out)


def _open_file(path: Path) -> None:
    system = platform.system()
    if system == "Darwin":
        subprocess.run(["open", str(path)])
    elif system == "Linux":
        subprocess.run(["xdg-open", str(path)])
    elif system == "Windows":
        subprocess.run(["start", str(path)], shell=True)


def _build_once(
    input_yaml: Path,
    output: Optional[Path],
    theme_name: Optional[str],
) -> Path | None:
    """Run a single build, returning output path or None on error."""
    try:
        text = input_yaml.read_text(encoding="utf-8")
        data = yaml.safe_load(text)
    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        return None

    if not isinstance(data, dict) or "slides" not in data:
        typer.echo("Error: YAML must contain a 'slides' key", err=True)
        return None

    theme = get_theme(theme_name or data.get("theme", "default"))

    theme_config = data.get("theme_config", {})
    if theme_config.get("organization"):
        theme.organization = theme_config["organization"]
    if theme_config.get("document_title"):
        theme.document_title = theme_config["document_title"]
    if theme_config.get("classification"):
        theme.classification = theme_config["classification"]
    if theme_config.get("footer"):
        theme.footer_text = theme_config["footer"]

    out_path = output or Path(data.get("output", "output.pptx"))

    try:
        out = render_presentation(
            slides_data=data["slides"],
            theme=theme,
            output_path=out_path,
            metadata=data.get("metadata"),
        )
        return out
    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        return None


def _watch_and_rebuild(
    input_yaml: Path,
    output: Optional[Path],
    theme_name: Optional[str],
    open_file: bool,
) -> None:
    """Watch a YAML file for changes and rebuild on save."""
    try:
        from watchdog.observers import Observer
        from watchdog.events import FileSystemEventHandler
    except ImportError:
        typer.echo("Error: watchdog not installed. Run: pip install yaml2pptx[watch]", err=True)
        raise typer.Exit(1)

    # Initial build
    out = _build_once(input_yaml, output, theme_name)
    if out:
        typer.echo(f"Generated: {out}")
        if open_file:
            _open_file(out)

    typer.echo(f"Watching {input_yaml} for changes... (Ctrl+C to stop)")

    class RebuildHandler(FileSystemEventHandler):
        def __init__(self):
            self._last_build = 0.0

        def on_modified(self, event):
            if event.src_path != str(input_yaml.resolve()):
                return
            # Debounce: skip if less than 1s since last build
            now = time.time()
            if now - self._last_build < 1.0:
                return
            self._last_build = now

            typer.echo(f"\nFile changed, rebuilding...")
            result = _build_once(input_yaml, output, theme_name)
            if result:
                typer.echo(f"Generated: {result}")

    observer = Observer()
    observer.schedule(RebuildHandler(), str(input_yaml.parent), recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(0.5)
    except KeyboardInterrupt:
        observer.stop()
        typer.echo("\nStopped watching.")
    observer.join()
