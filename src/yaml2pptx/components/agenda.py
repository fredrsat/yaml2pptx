"""Agenda / table-of-contents slide renderer."""

from __future__ import annotations

from pptx.enum.text import PP_ALIGN

from yaml2pptx.components.base import (
    add_footer,
    add_header,
    add_line,
    add_slide_title,
    add_textbox,
)
from yaml2pptx.themes import Theme


def render_agenda(
    slide,
    theme: Theme,
    *,
    section: str = "AGENDA",
    page: str = "",
    title: str = "",
    subtitle: str = "",
    items: list[dict] | None = None,
    **kwargs,
) -> None:
    """Render an agenda slide with numbered items."""
    c = theme.colors
    s = theme.sizes

    add_header(slide, theme, section, page)
    add_slide_title(slide, theme, title, subtitle, title_size=36, title_top=0.80)

    if not items:
        return

    start_top = 2.30
    available = 4.20  # space before footer
    row_height = min(0.80, max(0.36, available / len(items)))
    num_left = s.margin_left
    title_left = 1.70
    desc_left = 6.30

    for i, item in enumerate(items):
        top = start_top + i * row_height

        # Separator line above (except first)
        if i > 0:
            add_line(slide, s.margin_left, top - 0.04, 12.10, color=c.text_light, weight=0.5)

        # Number
        num_text = item.get("number", f"{i + 1:02d}")
        add_textbox(slide, num_left, top, 1.0, 0.32, text=str(num_text),
                    font_size=18, bold=True, color=c.light_blue)

        # Title
        add_textbox(slide, title_left, top, 4.50, 0.32, text=item.get("title", ""),
                    font_size=14, bold=True, color=c.text_dark, alignment=PP_ALIGN.LEFT)

        # Description
        if item.get("description"):
            add_textbox(slide, desc_left, top, 6.30, 0.32, text=item["description"],
                        font_size=11, color=c.text_muted, alignment=PP_ALIGN.LEFT)

    # Final separator
    final_top = start_top + len(items) * row_height
    add_line(slide, s.margin_left, final_top - 0.04, 12.10, color=c.text_light, weight=0.5)

    add_footer(slide, theme)
