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
            add_textbox(slide, inner_left, card_top + 0.25, inner_width, 1.10,
                        text=card["stat"], font_size=54, bold=True, color=c.primary)

        # Label (below stat)
        if card.get("label"):
            add_textbox(slide, inner_left, card_top + 1.40, inner_width, 0.25,
                        text=card["label"], font_size=10, bold=True, color=c.accent)

        # Card title
        if card.get("title"):
            add_textbox(slide, inner_left, card_top + 1.65, inner_width, 0.40,
                        text=card["title"], font_size=15, bold=True, color=c.text_dark)

        # Description — fill remaining card space
        if card.get("description"):
            desc_top = 2.10
            desc_height = card_height - desc_top - 0.10
            add_textbox(slide, inner_left, card_top + desc_top, inner_width, desc_height,
                        text=card["description"], font_size=10, italic=True, color=c.text_muted)

    # Footnotes (handle string input as single-item list)
    if footnotes:
        if isinstance(footnotes, str):
            footnotes = [footnotes]
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
    card_height = 3.80 if not callout else 2.80
    inner_pad = 0.30
    # Scale term font for narrow cards
    term_font = 20 if len(cards) >= 4 else 26

    for i, (left, width) in enumerate(positions):
        card = cards[i] if i < len(cards) else {}

        # Card background
        add_rect(slide, left, card_top, width, card_height, fill=c.card_bg)
        # Top accent border
        border_color = resolve_color(card.get("border_color"), c.primary, theme)
        add_rect(slide, left, card_top, width, s.card_border_height, fill=border_color)

        inner_left = left + inner_pad
        inner_width = width - inner_pad * 2

        # Icon
        icon_name = card.get("icon", "")
        if icon_name:
            add_icon_shape(slide, inner_left, card_top + 0.25, 0.60,
                           icon_name=icon_name, bg_color=c.primary)
        else:
            add_rect(slide, inner_left, card_top + 0.25, 0.60, 0.60, fill=c.primary)

        # Term (large)
        if card.get("term"):
            add_textbox(slide, inner_left + 0.75, card_top + 0.25, inner_width - 0.75, 0.65,
                        text=card["term"], font_size=term_font, bold=True, color=c.primary)

        # Subtitle
        if card.get("subtitle"):
            add_textbox(slide, inner_left, card_top + 0.95, inner_width, 0.35,
                        text=card["subtitle"], font_size=13, bold=True, color=c.text_dark)

        # Description — fill remaining card space
        if card.get("description"):
            desc_top = 1.35
            desc_height = card_height - desc_top - 0.10
            desc_font = 9 if callout else 10
            add_textbox(slide, inner_left, card_top + desc_top, inner_width, desc_height,
                        text=card["description"], font_size=desc_font, color=c.text_muted)

    # Optional dark callout section at bottom
    if callout:
        _render_callout_bar(slide, theme, callout, top=card_top + card_height + 0.15)

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
    card_height = 4.10 if not callout else 3.10
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

        # Description / points — constrained to card boundary
        body_top = 1.80
        body_height = card_height - body_top - 0.10

        if card.get("description"):
            add_textbox(slide, inner_left, card_top + body_top, inner_width, body_height,
                        text=card["description"], font_size=12, color=c.text_muted)

        if card.get("points"):
            add_multiline_textbox(slide, inner_left, card_top + body_top, inner_width, body_height,
                                  lines=card["points"], font_size=10, color=c.text_dark)

    # Optional callout — positioned below cards
    if callout:
        _render_callout_bar(slide, theme, callout, top=card_top + card_height + 0.20)

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
        add_textbox(slide, s.margin_left, 1.40, 12.10, 1.20,
                    text=message, font_size=28, color=c.text_dark)

    if not cards:
        add_footer(slide, theme)
        return

    positions = _card_positions(len(cards))
    card_top = 3.00
    card_height = 3.60
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
            add_textbox(slide, inner_left, card_top + 0.25, inner_width, 0.50,
                        text=card["title"], font_size=18, bold=True, color=c.text_dark)

        # Description — fill remaining card space
        if card.get("description"):
            desc_top = 0.80
            desc_height = card_height - desc_top - 0.10
            add_textbox(slide, inner_left, card_top + desc_top, inner_width, desc_height,
                        text=card["description"], font_size=12, color=c.text_muted)

    add_footer(slide, theme)


def _render_callout_bar(slide, theme: Theme, callout: dict, top: float = 4.55) -> None:
    """Render a dark callout bar with columns."""
    c = theme.colors
    s = theme.sizes
    # Ensure callout fits on slide (max bottom ~6.90 to leave room for footer)
    max_height = 6.90 - top
    height = min(callout.get("height", 1.80), max_height)
    add_rect(slide, s.margin_left, top, s.content_width, height, fill=c.dark_navy)

    # Label
    if callout.get("label"):
        add_textbox(slide, 0.85, top + 0.15, 11.63, 0.25,
                    text=callout["label"], font_size=10, bold=True, color=c.accent)

    # Columns
    columns = callout.get("columns", [])
    if columns:
        col_width = 11.00 / len(columns)
        for i, col in enumerate(columns):
            col_left = 0.85 + i * (col_width + 0.20)
            if col.get("title"):
                add_textbox(slide, col_left, top + 0.45, col_width, 0.35,
                            text=col["title"], font_size=13, bold=True, color=c.white)
            if col.get("description"):
                desc_h = height - 0.85 - 0.05
                add_textbox(slide, col_left, top + 0.80, col_width, desc_h,
                            text=col["description"], font_size=10, color=c.light_blue)
