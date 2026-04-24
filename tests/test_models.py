from __future__ import annotations

import pytest
from pydantic import ValidationError

from yaml2pptx.models.elements import ChartData, TableData, TextElement
from yaml2pptx.models.presentation import PresentationModel
from yaml2pptx.models.slides import SlideDefinition


class TestTextElement:
    def test_defaults(self):
        el = TextElement(text="hello")
        assert el.text == "hello"
        assert el.level == 0
        assert el.bold is None
        assert el.italic is None

    def test_with_formatting(self):
        el = TextElement(text="hello", level=1, bold=True, font_size=24)
        assert el.level == 1
        assert el.bold is True
        assert el.font_size == 24


class TestSlideDefinition:
    def test_minimal(self):
        slide = SlideDefinition(layout="content")
        assert slide.layout == "content"
        assert slide.title is None
        assert slide.content is None

    def test_content_normalization_strings(self):
        slide = SlideDefinition(layout="content", content=["hello", "world"])
        assert len(slide.content) == 2
        assert isinstance(slide.content[0], TextElement)
        assert slide.content[0].text == "hello"

    def test_content_normalization_dicts(self):
        slide = SlideDefinition(
            layout="content",
            content=[{"text": "indented", "level": 1}],
        )
        assert slide.content[0].level == 1

    def test_content_normalization_mixed(self):
        slide = SlideDefinition(
            layout="content",
            content=["plain", {"text": "indented", "level": 1}],
        )
        assert slide.content[0].text == "plain"
        assert slide.content[0].level == 0
        assert slide.content[1].text == "indented"
        assert slide.content[1].level == 1

    def test_left_right_normalization(self):
        slide = SlideDefinition(layout="two_column", left=["a"], right=["b"])
        assert slide.left[0].text == "a"
        assert slide.right[0].text == "b"


class TestTableData:
    def test_with_headers(self):
        table = TableData(headers=["A", "B"], rows=[["1", "2"]])
        assert table.headers == ["A", "B"]
        assert len(table.rows) == 1

    def test_without_headers(self):
        table = TableData(rows=[["1", "2"]])
        assert table.headers is None


class TestChartData:
    def test_valid(self):
        chart = ChartData(
            type="bar",
            categories=["Q1", "Q2"],
            series=[{"name": "Revenue", "values": [100, 200]}],
        )
        assert chart.type == "bar"
        assert len(chart.series) == 1

    def test_invalid_type(self):
        with pytest.raises(ValidationError):
            ChartData(
                type="invalid",
                categories=["Q1"],
                series=[{"name": "X", "values": [1]}],
            )


class TestPresentationModel:
    def test_minimal(self):
        model = PresentationModel(slides=[{"layout": "content"}])
        assert len(model.slides) == 1
        assert model.template is None

    def test_full(self):
        model = PresentationModel(
            template="test.pptx",
            output="out.pptx",
            metadata={"title": "Test", "author": "Author"},
            defaults={"font_size": 18},
            layout_map={"title_slide": "Title Slide"},
            slides=[
                {"layout": "title_slide", "title": "Hello"},
                {"layout": "content", "content": ["bullet"]},
            ],
        )
        assert model.template == "test.pptx"
        assert model.metadata.title == "Test"
        assert model.defaults.font_size == 18
        assert len(model.slides) == 2

    def test_no_slides_fails(self):
        with pytest.raises(ValidationError):
            PresentationModel()
