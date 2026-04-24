"""Lightweight Markdown parser that converts inline formatting to run segments.

Supports: **bold**, *italic*, `code`, [link](url), ~~strikethrough~~
Output: list of (text, formatting_dict) tuples for python-pptx run creation.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field


@dataclass
class RunSegment:
    text: str
    bold: bool = False
    italic: bool = False
    code: bool = False
    strikethrough: bool = False
    hyperlink: str | None = None
    formatting: dict = field(default_factory=dict)


# Pattern matches inline Markdown elements, ordered by priority
_INLINE_PATTERN = re.compile(
    r"(?P<bold_text>\*\*(?P<bold_inner>.+?)\*\*)"
    r"|(?P<strike_text>~~(?P<strike_inner>.+?)~~)"
    r"|(?P<code_text>`(?P<code_inner>[^`]+)`)"
    r"|(?P<link_text>\[(?P<link_label>[^\]]+)\]\((?P<link_url>[^)]+)\))"
    r"|(?P<italic_text>\*(?P<italic_inner>[^*]+)\*)"
)


def parse_markdown(text: str) -> list[RunSegment]:
    """Parse a string with inline Markdown into RunSegments."""
    if not text:
        return [RunSegment(text="")]

    segments: list[RunSegment] = []
    pos = 0

    for match in _INLINE_PATTERN.finditer(text):
        start, end = match.start(), match.end()

        # Add plain text before this match
        if start > pos:
            segments.append(RunSegment(text=text[pos:start]))

        if match.group("bold_inner") is not None:
            segments.append(RunSegment(text=match.group("bold_inner"), bold=True))
        elif match.group("strike_inner") is not None:
            segments.append(RunSegment(text=match.group("strike_inner"), strikethrough=True))
        elif match.group("code_inner") is not None:
            segments.append(RunSegment(text=match.group("code_inner"), code=True))
        elif match.group("link_label") is not None:
            segments.append(
                RunSegment(
                    text=match.group("link_label"),
                    hyperlink=match.group("link_url"),
                )
            )
        elif match.group("italic_inner") is not None:
            segments.append(RunSegment(text=match.group("italic_inner"), italic=True))

        pos = end

    # Add remaining plain text
    if pos < len(text):
        segments.append(RunSegment(text=text[pos:]))

    if not segments:
        segments.append(RunSegment(text=text))

    return segments
