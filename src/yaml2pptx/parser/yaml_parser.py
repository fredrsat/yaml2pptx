from __future__ import annotations

from pathlib import Path

import yaml
from pydantic import ValidationError

from yaml2pptx.models.presentation import PresentationModel


class YamlParseError(Exception):
    pass


def parse_yaml(yaml_path: str | Path) -> PresentationModel:
    """Parse a YAML file and return a validated PresentationModel."""
    yaml_path = Path(yaml_path)

    if not yaml_path.exists():
        raise YamlParseError(f"File not found: {yaml_path}")

    if yaml_path.suffix not in (".yaml", ".yml"):
        raise YamlParseError(f"Expected .yaml or .yml file, got: {yaml_path.suffix}")

    text = yaml_path.read_text(encoding="utf-8")

    try:
        data = yaml.safe_load(text)
    except yaml.YAMLError as e:
        raise YamlParseError(f"Invalid YAML: {e}") from e

    if not isinstance(data, dict):
        raise YamlParseError("YAML root must be a mapping")

    if "slides" not in data:
        raise YamlParseError("YAML must contain a 'slides' key")

    # Resolve relative paths against the YAML file's directory
    base_dir = yaml_path.parent

    if "template" in data and data["template"]:
        template_path = Path(data["template"])
        if not template_path.is_absolute():
            data["template"] = str(base_dir / template_path)

    for slide in data.get("slides", []):
        if isinstance(slide, dict) and slide.get("image"):
            image_path = Path(slide["image"])
            if not image_path.is_absolute():
                slide["image"] = str(base_dir / image_path)

    try:
        return PresentationModel(**data)
    except ValidationError as e:
        raise YamlParseError(f"Schema validation error:\n{e}") from e
