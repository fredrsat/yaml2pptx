"""Theme definitions for yaml2pptx.

A theme defines the visual style: colors, fonts, sizes, and spacing.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from pptx.dml.color import RGBColor
from pptx.util import Inches, Pt, Emu


@dataclass
class ThemeColors:
    primary: RGBColor = field(default_factory=lambda: RGBColor(0x00, 0x30, 0x87))
    accent: RGBColor = field(default_factory=lambda: RGBColor(0x00, 0xA9, 0xA5))
    light_blue: RGBColor = field(default_factory=lambda: RGBColor(0x6C, 0xAC, 0xE4))
    dark_navy: RGBColor = field(default_factory=lambda: RGBColor(0x00, 0x1F, 0x5C))
    text_dark: RGBColor = field(default_factory=lambda: RGBColor(0x1F, 0x29, 0x37))
    text_muted: RGBColor = field(default_factory=lambda: RGBColor(0x64, 0x74, 0x8B))
    text_light: RGBColor = field(default_factory=lambda: RGBColor(0x9C, 0xA3, 0xAF))
    white: RGBColor = field(default_factory=lambda: RGBColor(0xFF, 0xFF, 0xFF))
    card_bg: RGBColor = field(default_factory=lambda: RGBColor(0xF8, 0xFA, 0xFC))
    success: RGBColor = field(default_factory=lambda: RGBColor(0x05, 0x96, 0x69))
    warning: RGBColor = field(default_factory=lambda: RGBColor(0xE8, 0x77, 0x22))
    success_bg: RGBColor = field(default_factory=lambda: RGBColor(0xEC, 0xFD, 0xF5))
    warning_bg: RGBColor = field(default_factory=lambda: RGBColor(0xFF, 0xF7, 0xED))


@dataclass
class ThemeFonts:
    primary: str = "Calibri"
    mono: str = "Consolas"


@dataclass
class ThemeSizes:
    # Slide dimensions (widescreen 16:9)
    slide_width: int = 12192000   # 13.33 inches in EMU
    slide_height: int = 6858000   # 7.50 inches in EMU

    # Margins
    margin_left: float = 0.60
    margin_right: float = 0.60
    margin_top: float = 0.30
    content_width: float = 12.13  # usable width

    # Header area
    header_dot_size: float = 0.18
    header_dot_left: float = 0.60
    header_dot_top: float = 0.35
    section_label_left: float = 0.90
    section_label_top: float = 0.30
    page_num_left: float = 12.03
    page_num_top: float = 0.30

    # Title area
    title_top: float = 0.75
    title_height: float = 0.80
    subtitle_top: float = 1.40
    subtitle_height: float = 0.50

    # Content area
    content_top: float = 2.05
    content_bottom: float = 6.80

    # Footer
    footer_top: float = 7.15
    footer_height: float = 0.25

    # Card defaults
    card_gap: float = 0.25
    card_border_height: float = 0.08

    # Font sizes
    title_size: int = 28
    subtitle_size: int = 13
    section_label_size: int = 10
    page_num_size: int = 10
    footer_size: int = 9
    body_size: int = 13
    card_title_size: int = 18
    card_body_size: int = 12
    stat_size: int = 54
    big_letter_size: int = 68


@dataclass
class Theme:
    name: str = "default"
    colors: ThemeColors = field(default_factory=ThemeColors)
    fonts: ThemeFonts = field(default_factory=ThemeFonts)
    sizes: ThemeSizes = field(default_factory=ThemeSizes)

    # Footer template
    footer_text: str = ""
    organization: str = ""
    document_title: str = ""
    classification: str = ""


# Built-in themes
THEMES: dict[str, Theme] = {
    "default": Theme(),
}


def get_theme(name: str = "default") -> Theme:
    if name in THEMES:
        return THEMES[name]
    return Theme(name=name)


def resolve_color(color_name: str | None, default: RGBColor) -> RGBColor:
    """Resolve a color name or hex string to RGBColor.

    Supports:
      - None / empty -> default
      - Hex strings: "#00A9A5"
      - Named colors: "primary", "accent", "success", "warning", "blue", "dark"
    """
    if not color_name:
        return default
    if color_name.startswith("#"):
        hex_str = color_name.lstrip("#")
        return RGBColor(int(hex_str[0:2], 16), int(hex_str[2:4], 16), int(hex_str[4:6], 16))

    # Named color lookup (using default theme colors)
    named = {
        "primary": RGBColor(0x00, 0x30, 0x87),
        "accent": RGBColor(0x00, 0xA9, 0xA5),
        "success": RGBColor(0x05, 0x96, 0x69),
        "warning": RGBColor(0xE8, 0x77, 0x22),
        "blue": RGBColor(0x6C, 0xAC, 0xE4),
        "dark": RGBColor(0x00, 0x1F, 0x5C),
    }
    return named.get(color_name, default)
