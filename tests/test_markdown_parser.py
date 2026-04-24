from __future__ import annotations

from yaml2pptx.parser.markdown_parser import RunSegment, parse_markdown


class TestParseMarkdown:
    def test_plain_text(self):
        segments = parse_markdown("hello world")
        assert len(segments) == 1
        assert segments[0].text == "hello world"
        assert not segments[0].bold
        assert not segments[0].italic

    def test_bold(self):
        segments = parse_markdown("hello **bold** world")
        assert len(segments) == 3
        assert segments[0].text == "hello "
        assert segments[1].text == "bold"
        assert segments[1].bold is True
        assert segments[2].text == " world"

    def test_italic(self):
        segments = parse_markdown("hello *italic* world")
        assert len(segments) == 3
        assert segments[1].text == "italic"
        assert segments[1].italic is True

    def test_code(self):
        segments = parse_markdown("use `pip install` here")
        assert len(segments) == 3
        assert segments[1].text == "pip install"
        assert segments[1].code is True

    def test_strikethrough(self):
        segments = parse_markdown("~~removed~~ text")
        assert len(segments) == 2
        assert segments[0].text == "removed"
        assert segments[0].strikethrough is True

    def test_link(self):
        segments = parse_markdown("see [docs](https://example.com) here")
        assert len(segments) == 3
        assert segments[1].text == "docs"
        assert segments[1].hyperlink == "https://example.com"

    def test_multiple_formats(self):
        segments = parse_markdown("**bold** and *italic* and `code`")
        assert len(segments) == 5
        assert segments[0].bold is True
        assert segments[2].italic is True
        assert segments[4].code is True

    def test_empty_string(self):
        segments = parse_markdown("")
        assert len(segments) == 1
        assert segments[0].text == ""

    def test_no_formatting(self):
        segments = parse_markdown("just plain text")
        assert len(segments) == 1
        assert segments[0].text == "just plain text"

    def test_bold_at_start(self):
        segments = parse_markdown("**bold** start")
        assert segments[0].text == "bold"
        assert segments[0].bold is True

    def test_bold_at_end(self):
        segments = parse_markdown("end **bold**")
        assert segments[-1].text == "bold"
        assert segments[-1].bold is True
