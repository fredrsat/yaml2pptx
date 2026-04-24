"""Card-based slide renderers: stat_cards, definition_cards, content_cards."""

from __future__ import annotations

from yaml2pptx.components.base import (
    add_footer,
    add_header,
    add_multiline_textbox,
    add_rect,
    add_slide_title,
    add_textbox,
)
from yaml2pptx.components.icons import add_icon_shape
from yaml2pptx.themes import Theme, resolve_color


def _card_positions(count: int, margin: float = 0.60, total_width: float = 12.13, gap: float = 0.25):
    """Calculate left positions and widths for evenly spaced cards."""
    card_width = (total_width - gap * (count - 1)) / count
    positions = []
    for i in range(count):
        left = margin + i * (card_width + gap)
        positions.append((left, card_width))
    return positions


def render_stat_cards(
    slide,
    theme: Theme,
    *,
    section: str = "",
    page: str = "",
    title: str = "",
    subtitle: str = "",
    cards: list[dict] | None = None,
    footnotes: list[str] | None = None,
    **kwargs,
) -> None:
    """Render a slide with statistic cards (big number + description)."""
    c = theme.colors
    s = theme.sizes

    add_header(slide, theme, section, page)
    add_slide_title(slide, theme, title, subtitle)

    if not cards:
        return

    positions = _card_positions(len(cards))
    card_top = s.content_top
    card_height = 3.80
    inner_pad = 0.30

    for i, (left, width) in enumerate(positions):
        card = cards[i] if i < len(cards) else {}

        # Card background
        add_rect(slide, left, card_top, width, card_height, fill=c.card_bg)

        # Top accent border
        add_rect(slide, left, card_top, width, s.card_border_height, fill=c.accent)

        inner_left = left + inner_pad
        inner_width = width - inner_pad * 2

        # Big stat number
        if card.get("stat"):
            add_textbox(slide, inner_left, card_top + 0.30, inner_width, 0.85,
                        text=card["stat"], font_size=54, bold=True, color=c.primary)

        # Label (below stat)
        if card.get("label"):
            add_textbox(slide, inner_left, card_top + 1.20, inner_width, 0.25,
                        text=card["label"], font_size=10, bold=True, color=c.accent)

        # Card title
        if card.get("title"):
            add_textbox(slide, inner_left, card_top + 1.55, inner_width, 0.40,
                        text=card["title"], font_size=15, bold=True, color=c.text_dark)

        # Description
        if card.get("description"):
            add_textbox(slide, inner_left, card_top + 2.05, inner_width, 1.55,
                        text=card["description"], font_size=10, italic=True, color=c.text_muted)

    # Footnotes
    if footnotes:
        add_multiline_textbox(slide, s.margin_left, 6.10, s.content_width, 0.95,
                              lines=footnotes, font_size=8, color=c.text_light)

    add_footer(slide, theme)


def render_definition_cards(
    slide,
    theme: Theme,
    *,
    section: str = "",
    page: str = "",
    title: str = "",
    subtitle: str = "",
    cards: list[dict] | None = None,
    callout: dict | None = None,
    **kwargs,
) -> None:
    """Render a slide with definition cards (term + explanation)."""
    c = theme.colors
    s = theme.sizes

    add_header(slide, theme, section, page)
    add_slide_title(slide, theme, title, subtitle)

    if not cards:
        return

    positions = _card_positions(len(cards))
    card_top = s.content_top
    card_height = 2.30
    inner_pad = 0.30

    for i, (left, width) in enumerate(positions):
        card = cards[i] if i < len(cards) else {}

        # Card background
        add_rect(slide, left, card_top, width, card_height, fill=c.card_bg)
        # Top accent border
        border_color = resolve_color(card.get("border_color"), c.primary)
        add_rect(slide, left, card_top, width, s.card_border_height, fill=border_color)

        inner_left = left + inner_pad
        inner_width = width - inner_pad * 2

        # Icon
        icon_name = card.get("icon", "")
        if icon_name:
            add_icon_shape(slide, inner_left, card_top + 0.30, 0.70,
                           icon_name=icon_name, bg_color=c.primary)
        else:
            add_rect(slide, inner_left, card_top + 0.30, 0.70, 0.70, fill=c.primary)

        # Term (large)
        if card.get("term"):
            add_textbox(slide, inner_left + 0.85, card_top + 0.30, inner_width - 0.85, 0.50,
                        text=card["term"], font_size=30, bold=True, color=c.primary)

        # Subtitle
        if card.get("subtitle"):
            add_textbox(slide, inner_left, card_top + 1.10, inner_width, 0.35,
                        text=card["subtitle"], font_size=14, bold=True, color=c.text_dark)

        # Description
        if card.get("description"):
            add_textbox(slide, inner_left, card_top + 1.45, inner_width, 0.70,
                        text=card["description"], font_size=11, color=c.text_muted)

    # Optional dark callout section at bottom
    if callout:
        _render_callout_bar(slide, theme, callout, top=4.55)

    add_footer(slide, theme)


def render_content_cards(
    slide,
    theme: Theme,
    *,
    section: str = "",
    page: str = "",
    title: str = "",
    subtitle: str = "",
    cards: list[dict] | None = None,
    callout: dict | None = None,
    **kwargs,
) -> None:
    """Render a slide with content cards (icon, title, subtitle, points list)."""
    c = theme.colors
    s = theme.sizes

    add_header(slide, theme, section, page)
    add_slide_title(slide, theme, title, subtitle, title_top=0.80)

    if not cards:
        return

    positions = _card_positions(len(cards))
    card_top = 2.40
    card_height = 2.60
    inner_pad = 0.30

    for i, (left, width) in enumerate(positions):
        card = cards[i] if i < len(cards) else {}

        # Card background
        add_rect(slide, left, card_top, width, card_height, fill=c.card_bg)

        inner_left = left + inner_pad
        inner_width = width - inner_pad * 2

        # Icon
        icon_name = card.get("icon", "")
        if icon_name:
            add_icon_shape(slide, inner_left, card_top + 0.30, 0.65,
                           icon_name=icon_name, bg_color=c.primary)
        else:
            add_rect(slide, inner_left, card_top + 0.30, 0.65, 0.65, fill=c.primary)

        # Card title
        if card.get("title"):
            add_textbox(slide, inner_left, card_top + 1.05, inner_width, 0.40,
                        text=card["title"], font_size=16, bold=True, color=c.text_dark)

        # Card subtitle (examples)
        if card.get("subtitle"):
            add_textbox(slide, inner_left, card_top + 1.45, inner_width, 0.30,
                        text=card["subtitle"], font_size=11, italic=True, color=c.accent)

        # Description / points
        if card.get("description"):
            add_textbox(slide, inner_left, card_top + 1.80, inner_width, 0.70,
                        text=card["description"], font_size=12, color=c.text_muted)

        if card.get("points"):
            add_multiline_textbox(slide, inner_left, card_top + 1.80, inner_width, 1.50,
                                  lines=card["points"], font_size=10, color=c.text_dark)

    # Optional callout
    if callout:
        _render_callout_bar(slide, theme, callout, top=5.30)

    add_footer(slide, theme)


def render_icon_cards(
    slide,
    theme: Theme,
    *,
    section: str = "",
    page: str = "",
    title: str = "",
    subtitle: str = "",
    message: str = "",
    cards: list[dict] | None = None,
    **kwargs,
) -> None:
    """Render a key-message slide with icon cards below (left accent border)."""
    c = theme.colors
    s = theme.sizes

    add_header(slide, theme, section, page)

    # Label above message
    if section:
        add_textbox(slide, s.margin_left, 0.90, 10.0, 0.35,
                    text=section.upper(), font_size=11, bold=True, color=c.accent)

    # Big message text
    if message:
        add_textbox(slide, s.margin_left, 1.40, 12.10, 2.20,
                    text=message, font_size=28, color=c.text_dark)

    if not cards:
        add_footer(slide, theme)
        return

    positions = _card_positions(len(cards))
    card_top = 4.20
    card_height = 2.60
    inner_pad = 0.35

    for i, (left, width) in enumerate(positions):
        card = cards[i] if i < len(cards) else {}

        # Card background
        add_rect(slide, left, card_top, width, card_height, fill=c.white)
        # Left accent border
        add_rect(slide, left, card_top, 0.08, card_height, fill=c.accent)

        inner_left = left + inner_pad
        inner_width = width - inner_pad * 2

        # Card title
        if card.get("title"):
            add_textbox(slide, inner_left, card_top + 0.90, inner_width, 0.50,
                        text=card["title"], font_size=18, bold=True, color=c.text_dark)

        # Description
        if card.get("description"):
            add_textbox(slide, inner_left, card_top + 1.45, inner_width, 1.0,
                        text=card["description"], font_size=12, color=c.text_muted)

    add_footer(slide, theme)


def _render_callout_bar(slide, theme: Theme, callout: dict, top: float = 4.55) -> None:
    """Render a dark callout bar with columns."""
    c = theme.colors
    s = theme.sizes
    height = callout.get("height", 2.15)
    add_rect(slide, s.margin_left, top, s.content_width, height, fill=c.dark_navy)

    # Label
    if callout.get("label"):
        add_textbox(slide, 0.85, top + 0.20, 11.63, 0.30,
                    text=callout["label"], font_size=10, bold=True, color=c.accent)

    # Columns
    columns = callout.get("columns", [])
    if columns:
        col_width = 11.00 / len(columns)
        for i, col in enumerate(columns):
            col_left = 0.85 + i * (col_width + 0.20)
            if col.get("title"):
                add_textbox(slide, col_left, top + 0.60, col_width, 0.40,
                            text=col["title"], font_size=13, bold=True, color=c.white)
            if col.get("description"):
                add_textbox(slide, col_left, top + 1.00, col_width, 1.05,
                            text=col["description"], font_size=11, color=c.light_blue)
