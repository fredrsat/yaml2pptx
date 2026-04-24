"""Title page slide renderer."""

from __future__ import annotations

from pptx.util import Pt

from yaml2pptx.components.base import add_rect, add_textbox
from yaml2pptx.themes import Theme


def render_title_page(
    slide,
    theme: Theme,
    *,
    category: str = "",
    title: str = "",
    subtitle: str = "",
    author: str = "",
    date: str = "",
    **kwargs,
) -> None:
    """Render a title page slide with decorative elements."""
    c = theme.colors
    s = theme.sizes

    # Dark background - critical for white text visibility
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = c.dark_navy

    # Decorative rectangles (bottom-right)
    add_rect(slide, 8.33, 4.70, 5.00, 2.80, fill=c.primary)
    add_rect(slide, 10.83, 6.10, 2.50, 1.40, fill=c.accent)

    # Decorative dot grid (5x3 grid of small squares)
    dot_size = 0.06
    dot_gap = 0.22
    for col in range(5):
        for row in range(3):
            add_rect(slide, 0.70 + col * dot_gap, 0.70 + row * dot_gap,
                     dot_size, dot_size, fill=c.light_blue)

    # Category line
    if category:
        add_textbox(slide, 0.90, 1.90, 10.0, 0.40, text=category,
                    font_size=12, bold=True, color=c.light_blue)

    # Main title
    add_textbox(slide, 0.90, 2.35, 11.0, 1.20, text=title,
                font_size=54, bold=True, color=c.white)

    # Subtitle
    if subtitle:
        add_textbox(slide, 0.90, 3.70, 11.0, 1.30, text=subtitle,
                    font_size=22, color=c.light_blue)

    # Divider line
    add_rect(slide, 0.90, 5.30, 1.20, 0.04, fill=c.accent)

    # Author
    if author:
        add_textbox(slide, 0.90, 5.45, 10.0, 0.35, text=author,
                    font_size=14, bold=True, color=c.white)

    # Date
    if date:
        add_textbox(slide, 0.90, 5.80, 10.0, 0.30, text=date,
                    font_size=12, color=c.light_blue)
