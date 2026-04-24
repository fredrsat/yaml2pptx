from __future__ import annotations

from pathlib import Path

from typer.testing import CliRunner

from yaml2pptx.cli import app

runner = CliRunner()


class TestGenCommand:
    def test_generate_simple(self, tmp_yaml, tmp_path):
        p = tmp_yaml(
            'slides:\n  - layout: "Title Slide"\n    title: "Hello"\n'
        )
        result = runner.invoke(app, ["gen", str(p), "-o", str(tmp_path / "out.pptx")])
        assert result.exit_code == 0
        assert "Generated" in result.stdout
        assert (tmp_path / "out.pptx").exists()

    def test_validate_only(self, tmp_yaml):
        p = tmp_yaml('slides:\n  - layout: content\n')
        result = runner.invoke(app, ["gen", str(p), "--validate-only"])
        assert result.exit_code == 0
        assert "Valid" in result.stdout

    def test_invalid_yaml(self, tmp_yaml):
        p = tmp_yaml("{{invalid")
        result = runner.invoke(app, ["gen", str(p)])
        assert result.exit_code == 1
        assert "Error" in (result.stdout + result.stderr)

    def test_file_not_found(self):
        result = runner.invoke(app, ["gen", "/nonexistent.yaml"])
        assert result.exit_code != 0


class TestInspectCommand:
    def test_inspect(self, default_template):
        result = runner.invoke(app, ["inspect", str(default_template)])
        assert result.exit_code == 0
        assert "Title Slide" in result.stdout
        assert "idx=" in result.stdout

    def test_inspect_specific_layout(self, default_template):
        result = runner.invoke(
            app, ["inspect", str(default_template), "--layout", "Title Slide"]
        )
        assert result.exit_code == 0
        assert "Title Slide" in result.stdout

    def test_inspect_layout_not_found(self, default_template):
        result = runner.invoke(
            app, ["inspect", str(default_template), "--layout", "Nonexistent"]
        )
        assert result.exit_code == 1


class TestInitCommand:
    def test_init_default(self, tmp_path):
        out = tmp_path / "presentation.yaml"
        result = runner.invoke(app, ["init", "-o", str(out)])
        assert result.exit_code == 0
        assert out.exists()
        content = out.read_text()
        assert "slides:" in content
        assert "title_slide" in content

    def test_init_with_name(self, tmp_path):
        out = tmp_path / "test.yaml"
        result = runner.invoke(
            app, ["init", "--name", "My Deck", "-o", str(out), "--slides", "3"]
        )
        assert result.exit_code == 0
        content = out.read_text()
        assert "My Deck" in content
