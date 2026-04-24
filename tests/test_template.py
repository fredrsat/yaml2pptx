from __future__ import annotations

import pytest

from yaml2pptx.engine.template import TemplateError, TemplateManager


class TestTemplateManager:
    def test_load_default(self):
        tm = TemplateManager()
        layouts = tm.get_layouts_info()
        assert len(layouts) > 0

    def test_load_from_file(self, default_template):
        tm = TemplateManager(default_template)
        layouts = tm.get_layouts_info()
        assert len(layouts) > 0

    def test_file_not_found(self):
        with pytest.raises(TemplateError, match="not found"):
            TemplateManager("/nonexistent/template.pptx")

    def test_get_layout_by_name(self, default_template):
        tm = TemplateManager(default_template)
        layout = tm.get_layout("Title Slide")
        assert layout.name == "Title Slide"

    def test_get_layout_case_insensitive(self, default_template):
        tm = TemplateManager(default_template)
        layout = tm.get_layout("title slide")
        assert layout.name == "Title Slide"

    def test_get_layout_with_underscores(self, default_template):
        tm = TemplateManager(default_template)
        layout = tm.get_layout("title_slide")
        assert layout.name == "Title Slide"

    def test_get_layout_by_index(self, default_template):
        tm = TemplateManager(default_template)
        layout = tm.get_layout("0")
        assert layout.name == "Title Slide"

    def test_get_layout_with_map(self, default_template):
        tm = TemplateManager(default_template)
        layout = tm.get_layout("my_title", layout_map={"my_title": "Title Slide"})
        assert layout.name == "Title Slide"

    def test_get_layout_with_index_map(self, default_template):
        tm = TemplateManager(default_template)
        layout = tm.get_layout("my_layout", layout_map={"my_layout": 1})
        assert layout.name == "Title and Content"

    def test_get_layout_not_found(self, default_template):
        tm = TemplateManager(default_template)
        with pytest.raises(TemplateError, match="not found"):
            tm.get_layout("nonexistent_layout")

    def test_format_inspect(self, default_template):
        tm = TemplateManager(default_template)
        output = tm.format_inspect()
        assert "Title Slide" in output
        assert "idx=" in output

    def test_layouts_have_placeholders(self, default_template):
        tm = TemplateManager(default_template)
        layouts = tm.get_layouts_info()
        title_layout = [l for l in layouts if l.name == "Title Slide"][0]
        assert len(title_layout.placeholders) > 0
