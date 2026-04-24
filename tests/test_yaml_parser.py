from __future__ import annotations

from pathlib import Path

import pytest

from yaml2pptx.parser.yaml_parser import YamlParseError, parse_yaml


class TestParseYaml:
    def test_minimal(self, tmp_yaml):
        p = tmp_yaml('slides:\n  - layout: content\n    title: "Hello"\n')
        model = parse_yaml(p)
        assert len(model.slides) == 1
        assert model.slides[0].title == "Hello"

    def test_full_presentation(self, tmp_yaml):
        content = """
template: null
output: "test.pptx"
metadata:
  title: "Test"
  author: "Author"
slides:
  - layout: title_slide
    title: "Title"
    subtitle: "Sub"
  - layout: content
    title: "Bullets"
    content:
      - "Item 1"
      - text: "Item 2"
        level: 1
    speaker_notes: "Notes here"
"""
        p = tmp_yaml(content)
        model = parse_yaml(p)
        assert model.metadata.title == "Test"
        assert len(model.slides) == 2
        assert model.slides[1].content[0].text == "Item 1"
        assert model.slides[1].content[1].level == 1
        assert model.slides[1].speaker_notes == "Notes here"

    def test_file_not_found(self):
        with pytest.raises(YamlParseError, match="File not found"):
            parse_yaml("/nonexistent/file.yaml")

    def test_invalid_extension(self, tmp_path):
        p = tmp_path / "test.txt"
        p.write_text("slides: []")
        with pytest.raises(YamlParseError, match="Expected .yaml"):
            parse_yaml(p)

    def test_invalid_yaml(self, tmp_yaml):
        p = tmp_yaml("{{invalid yaml")
        with pytest.raises(YamlParseError, match="Invalid YAML"):
            parse_yaml(p)

    def test_no_slides_key(self, tmp_yaml):
        p = tmp_yaml("title: test\n")
        with pytest.raises(YamlParseError, match="'slides' key"):
            parse_yaml(p)

    def test_not_a_mapping(self, tmp_yaml):
        p = tmp_yaml("- item1\n- item2\n")
        with pytest.raises(YamlParseError, match="root must be a mapping"):
            parse_yaml(p)

    def test_template_path_resolution(self, tmp_path, default_template):
        # Create yaml in a subdirectory, template in parent
        sub = tmp_path / "sub"
        sub.mkdir()
        import shutil
        shutil.copy(default_template, sub / "my_template.pptx")
        yaml_file = sub / "test.yaml"
        yaml_file.write_text('template: "my_template.pptx"\nslides:\n  - layout: content\n')
        model = parse_yaml(yaml_file)
        assert Path(model.template).is_absolute()

    def test_table_slide(self, tmp_yaml):
        content = """
slides:
  - layout: content
    title: "Data"
    table:
      headers: ["A", "B"]
      rows:
        - ["1", "2"]
        - ["3", "4"]
"""
        p = tmp_yaml(content)
        model = parse_yaml(p)
        assert model.slides[0].table is not None
        assert model.slides[0].table.headers == ["A", "B"]
        assert len(model.slides[0].table.rows) == 2

    def test_chart_slide(self, tmp_yaml):
        content = """
slides:
  - layout: content
    title: "Chart"
    chart:
      type: bar
      categories: ["Q1", "Q2"]
      series:
        - name: "Rev"
          values: [100, 200]
"""
        p = tmp_yaml(content)
        model = parse_yaml(p)
        assert model.slides[0].chart is not None
        assert model.slides[0].chart.type == "bar"
