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


def _rgb(r: int, g: int, b: int) -> RGBColor:
    return RGBColor(r, g, b)


# ---------------------------------------------------------------------------
# Built-in themes
# ---------------------------------------------------------------------------

THEMES: dict[str, Theme] = {
    # -- Default: Navy / Teal (the original) --
    "default": Theme(),

    # -- Midnight: Deep indigo / electric cyan --
    "midnight": Theme(
        name="midnight",
        colors=ThemeColors(
            primary=_rgb(0x4F, 0x46, 0xE5),
            accent=_rgb(0x06, 0xB6, 0xD4),
            light_blue=_rgb(0x81, 0x8C, 0xF8),
            dark_navy=_rgb(0x0F, 0x17, 0x2A),
            text_dark=_rgb(0x1E, 0x29, 0x3B),
            text_muted=_rgb(0x64, 0x74, 0x8B),
            text_light=_rgb(0x94, 0xA3, 0xB8),
            white=_rgb(0xFF, 0xFF, 0xFF),
            card_bg=_rgb(0xEE, 0xF2, 0xFF),
            success=_rgb(0x10, 0xB9, 0x81),
            warning=_rgb(0xF5, 0x9E, 0x0B),
            success_bg=_rgb(0xEC, 0xFD, 0xF5),
            warning_bg=_rgb(0xFF, 0xFB, 0xEB),
        ),
        fonts=ThemeFonts(primary="Segoe UI"),
    ),

    # -- Coral: Warm rose / vibrant orange --
    "coral": Theme(
        name="coral",
        colors=ThemeColors(
            primary=_rgb(0xE1, 0x1D, 0x48),
            accent=_rgb(0xF9, 0x73, 0x16),
            light_blue=_rgb(0xFB, 0x71, 0x85),
            dark_navy=_rgb(0x4C, 0x05, 0x19),
            text_dark=_rgb(0x1C, 0x19, 0x17),
            text_muted=_rgb(0x78, 0x71, 0x6C),
            text_light=_rgb(0xA8, 0xA2, 0x9E),
            white=_rgb(0xFF, 0xFF, 0xFF),
            card_bg=_rgb(0xFF, 0xF7, 0xED),
            success=_rgb(0x05, 0x96, 0x69),
            warning=_rgb(0xD9, 0x77, 0x06),
            success_bg=_rgb(0xEC, 0xFD, 0xF5),
            warning_bg=_rgb(0xFF, 0xF7, 0xED),
        ),
        fonts=ThemeFonts(primary="Century Gothic"),
    ),

    # -- Forest: Deep green / nature tones --
    "forest": Theme(
        name="forest",
        colors=ThemeColors(
            primary=_rgb(0x16, 0x65, 0x34),
            accent=_rgb(0x16, 0xA3, 0x4A),
            light_blue=_rgb(0x4A, 0xDE, 0x80),
            dark_navy=_rgb(0x05, 0x2E, 0x16),
            text_dark=_rgb(0x1C, 0x19, 0x17),
            text_muted=_rgb(0x57, 0x53, 0x4E),
            text_light=_rgb(0xA8, 0xA2, 0x9E),
            white=_rgb(0xFF, 0xFF, 0xFF),
            card_bg=_rgb(0xF0, 0xFD, 0xF4),
            success=_rgb(0x05, 0x96, 0x69),
            warning=_rgb(0xCA, 0x8A, 0x04),
            success_bg=_rgb(0xF0, 0xFD, 0xF4),
            warning_bg=_rgb(0xFE, 0xFC, 0xE8),
        ),
        fonts=ThemeFonts(primary="Georgia"),
    ),

    # -- Sunset: Rich orange / golden amber --
    "sunset": Theme(
        name="sunset",
        colors=ThemeColors(
            primary=_rgb(0xC2, 0x41, 0x0C),
            accent=_rgb(0xF5, 0x9E, 0x0B),
            light_blue=_rgb(0xFB, 0x92, 0x3C),
            dark_navy=_rgb(0x43, 0x14, 0x07),
            text_dark=_rgb(0x29, 0x25, 0x24),
            text_muted=_rgb(0x78, 0x71, 0x6C),
            text_light=_rgb(0xA8, 0xA2, 0x9E),
            white=_rgb(0xFF, 0xFF, 0xFF),
            card_bg=_rgb(0xFF, 0xFB, 0xEB),
            success=_rgb(0x05, 0x96, 0x69),
            warning=_rgb(0xDC, 0x26, 0x26),
            success_bg=_rgb(0xEC, 0xFD, 0xF5),
            warning_bg=_rgb(0xFE, 0xF2, 0xF2),
        ),
        fonts=ThemeFonts(primary="Trebuchet MS"),
    ),

    # -- Arctic: Clean sky-blue / minimal --
    "arctic": Theme(
        name="arctic",
        colors=ThemeColors(
            primary=_rgb(0x02, 0x84, 0xC7),
            accent=_rgb(0x38, 0xBD, 0xF8),
            light_blue=_rgb(0x7D, 0xD3, 0xFC),
            dark_navy=_rgb(0x0C, 0x4A, 0x6E),
            text_dark=_rgb(0x0F, 0x17, 0x2A),
            text_muted=_rgb(0x64, 0x74, 0x8B),
            text_light=_rgb(0x94, 0xA3, 0xB8),
            white=_rgb(0xFF, 0xFF, 0xFF),
            card_bg=_rgb(0xF0, 0xF9, 0xFF),
            success=_rgb(0x0D, 0x94, 0x88),
            warning=_rgb(0xF5, 0x9E, 0x0B),
            success_bg=_rgb(0xF0, 0xFD, 0xFA),
            warning_bg=_rgb(0xFF, 0xFB, 0xEB),
        ),
        fonts=ThemeFonts(primary="Arial"),
    ),

    # -- Executive: Charcoal / gold sophistication --
    "executive": Theme(
        name="executive",
        colors=ThemeColors(
            primary=_rgb(0x1F, 0x29, 0x37),
            accent=_rgb(0xB4, 0x53, 0x09),
            light_blue=_rgb(0xD4, 0xA5, 0x74),
            dark_navy=_rgb(0x11, 0x18, 0x27),
            text_dark=_rgb(0x11, 0x18, 0x27),
            text_muted=_rgb(0x6B, 0x72, 0x80),
            text_light=_rgb(0x9C, 0xA3, 0xAF),
            white=_rgb(0xFF, 0xFF, 0xFF),
            card_bg=_rgb(0xF9, 0xFA, 0xFB),
            success=_rgb(0x05, 0x96, 0x69),
            warning=_rgb(0xDC, 0x26, 0x26),
            success_bg=_rgb(0xEC, 0xFD, 0xF5),
            warning_bg=_rgb(0xFE, 0xF2, 0xF2),
        ),
        fonts=ThemeFonts(primary="Georgia"),
    ),

    # -- Neon: Bold violet / cyan pop --
    "neon": Theme(
        name="neon",
        colors=ThemeColors(
            primary=_rgb(0x7C, 0x3A, 0xED),
            accent=_rgb(0x06, 0xB6, 0xD4),
            light_blue=_rgb(0xA7, 0x8B, 0xFA),
            dark_navy=_rgb(0x1E, 0x1B, 0x4B),
            text_dark=_rgb(0x1E, 0x29, 0x3B),
            text_muted=_rgb(0x64, 0x74, 0x8B),
            text_light=_rgb(0x94, 0xA3, 0xB8),
            white=_rgb(0xFF, 0xFF, 0xFF),
            card_bg=_rgb(0xF5, 0xF3, 0xFF),
            success=_rgb(0x10, 0xB9, 0x81),
            warning=_rgb(0xF5, 0x9E, 0x0B),
            success_bg=_rgb(0xEC, 0xFD, 0xF5),
            warning_bg=_rgb(0xFF, 0xFB, 0xEB),
        ),
        fonts=ThemeFonts(primary="Calibri"),
    ),

    # -- Earth: Terracotta / sage green warmth --
    "earth": Theme(
        name="earth",
        colors=ThemeColors(
            primary=_rgb(0x92, 0x40, 0x0E),
            accent=_rgb(0x4D, 0x7C, 0x0F),
            light_blue=_rgb(0x84, 0xCC, 0x16),
            dark_navy=_rgb(0x42, 0x20, 0x06),
            text_dark=_rgb(0x29, 0x25, 0x24),
            text_muted=_rgb(0x78, 0x71, 0x6C),
            text_light=_rgb(0xA8, 0xA2, 0x9E),
            white=_rgb(0xFF, 0xFF, 0xFF),
            card_bg=_rgb(0xFE, 0xFC, 0xE8),
            success=_rgb(0x3F, 0x62, 0x12),
            warning=_rgb(0xC2, 0x41, 0x0C),
            success_bg=_rgb(0xF7, 0xFE, 0xE7),
            warning_bg=_rgb(0xFF, 0xF7, 0xED),
        ),
        fonts=ThemeFonts(primary="Palatino Linotype"),
    ),

    # -- Ocean: Deep teal / aquamarine --
    "ocean": Theme(
        name="ocean",
        colors=ThemeColors(
            primary=_rgb(0x0F, 0x76, 0x6E),
            accent=_rgb(0x2D, 0xD4, 0xBF),
            light_blue=_rgb(0x5E, 0xEA, 0xD4),
            dark_navy=_rgb(0x04, 0x2F, 0x2E),
            text_dark=_rgb(0x1E, 0x29, 0x3B),
            text_muted=_rgb(0x64, 0x74, 0x8B),
            text_light=_rgb(0x94, 0xA3, 0xB8),
            white=_rgb(0xFF, 0xFF, 0xFF),
            card_bg=_rgb(0xF0, 0xFD, 0xFA),
            success=_rgb(0x05, 0x96, 0x69),
            warning=_rgb(0xF5, 0x9E, 0x0B),
            success_bg=_rgb(0xEC, 0xFD, 0xF5),
            warning_bg=_rgb(0xFF, 0xFB, 0xEB),
        ),
        fonts=ThemeFonts(primary="Trebuchet MS"),
    ),
}


def get_theme(name: str = "default") -> Theme:
    if name in THEMES:
        # Deep copy so per-presentation overrides don't mutate the prototype
        import copy
        return copy.deepcopy(THEMES[name])
    return Theme(name=name)


def resolve_color(color_name: str | None, default: RGBColor, theme: Theme | None = None) -> RGBColor:
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

    # Use theme colors if available, otherwise fallback to defaults
    if theme:
        c = theme.colors
        named = {
            "primary": c.primary,
            "accent": c.accent,
            "success": c.success,
            "warning": c.warning,
            "blue": c.light_blue,
            "dark": c.dark_navy,
        }
    else:
        named = {
            "primary": _rgb(0x00, 0x30, 0x87),
            "accent": _rgb(0x00, 0xA9, 0xA5),
            "success": _rgb(0x05, 0x96, 0x69),
            "warning": _rgb(0xE8, 0x77, 0x22),
            "blue": _rgb(0x6C, 0xAC, 0xE4),
            "dark": _rgb(0x00, 0x1F, 0x5C),
        }
    return named.get(color_name, default)
