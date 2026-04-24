"""Icon library for yaml2pptx.

Provides named icons rendered as Unicode characters inside colored shapes.
Icons can be referenced by name in YAML: icon: "shield"
"""

from __future__ import annotations

from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Inches, Pt

# Icon mapping: name -> (character, recommended font)
# Uses characters that render well across platforms in PowerPoint
ICON_MAP: dict[str, tuple[str, str]] = {
    # Security & access
    "shield": ("⛨", "Segoe UI Symbol"),
    "lock": ("🔒", "Segoe UI Symbol"),
    "key": ("🔑", "Segoe UI Symbol"),
    "unlock": ("🔓", "Segoe UI Symbol"),

    # Technology
    "gear": ("⚙", "Segoe UI Symbol"),
    "server": ("☰", "Segoe UI Symbol"),
    "cloud": ("☁", "Segoe UI Symbol"),
    "database": ("⛁", "Segoe UI Symbol"),
    "code": ("⌨", "Segoe UI Symbol"),
    "network": ("⊞", "Segoe UI Symbol"),
    "chip": ("⬡", "Segoe UI Symbol"),

    # Communication & people
    "people": ("⚑", "Segoe UI Symbol"),
    "person": ("⚇", "Segoe UI Symbol"),
    "mail": ("✉", "Segoe UI Symbol"),
    "chat": ("⊡", "Segoe UI Symbol"),

    # Indicators & status
    "check": ("✓", "Segoe UI Symbol"),
    "cross": ("✗", "Segoe UI Symbol"),
    "warning": ("⚠", "Segoe UI Symbol"),
    "info": ("ℹ", "Segoe UI Symbol"),
    "star": ("★", "Segoe UI Symbol"),
    "flag": ("⚑", "Segoe UI Symbol"),

    # Business & analytics
    "chart": ("◫", "Segoe UI Symbol"),
    "target": ("◎", "Segoe UI Symbol"),
    "trend": ("⬆", "Segoe UI Symbol"),
    "money": ("◈", "Segoe UI Symbol"),
    "document": ("☷", "Segoe UI Symbol"),
    "folder": ("⊟", "Segoe UI Symbol"),

    # Science & health
    "brain": ("✧", "Segoe UI Symbol"),
    "heart": ("♥", "Segoe UI Symbol"),
    "health": ("✚", "Segoe UI Symbol"),
    "science": ("⚗", "Segoe UI Symbol"),
    "microscope": ("⊕", "Segoe UI Symbol"),

    # Nature & energy
    "lightning": ("⚡", "Segoe UI Symbol"),
    "globe": ("◉", "Segoe UI Symbol"),
    "sun": ("☀", "Segoe UI Symbol"),
    "leaf": ("❧", "Segoe UI Symbol"),

    # Navigation & actions
    "arrow_right": ("→", "Calibri"),
    "arrow_left": ("←", "Calibri"),
    "arrow_up": ("↑", "Calibri"),
    "arrow_down": ("↓", "Calibri"),
    "search": ("⊙", "Segoe UI Symbol"),
    "link": ("⊷", "Segoe UI Symbol"),
    "clock": ("⏱", "Segoe UI Symbol"),
    "rocket": ("▶", "Segoe UI Symbol"),

    # Shapes (simple fallbacks)
    "circle": ("●", "Calibri"),
    "square": ("■", "Calibri"),
    "diamond": ("◆", "Calibri"),
    "triangle": ("▲", "Calibri"),
}

# Aliases for convenience
ICON_MAP["gpu"] = ICON_MAP["chip"]
ICON_MAP["ai"] = ICON_MAP["brain"]
ICON_MAP["security"] = ICON_MAP["shield"]
ICON_MAP["settings"] = ICON_MAP["gear"]
ICON_MAP["users"] = ICON_MAP["people"]
ICON_MAP["time"] = ICON_MAP["clock"]
ICON_MAP["data"] = ICON_MAP["database"]
ICON_MAP["success"] = ICON_MAP["check"]
ICON_MAP["error"] = ICON_MAP["cross"]
ICON_MAP["alert"] = ICON_MAP["warning"]
ICON_MAP["plus"] = ICON_MAP["health"]


def get_icon(name: str) -> tuple[str, str]:
    """Get icon character and font by name.

    Returns (character, font_name). Falls back to filled circle if unknown.
    """
    return ICON_MAP.get(name.lower(), ("●", "Calibri"))


def get_icon_names() -> list[str]:
    """Return all available icon names (excluding aliases)."""
    return sorted(ICON_MAP.keys())


def add_icon_shape(
    slide,
    left: float,
    top: float,
    size: float,
    icon_name: str,
    bg_color: RGBColor | None = None,
    icon_color: RGBColor | None = None,
    icon_size: int | None = None,
) -> object:
    """Add a colored square with an icon character inside.

    Args:
        slide: The slide to add the icon to.
        left: Left position in inches.
        top: Top position in inches.
        size: Width and height of the square in inches.
        icon_name: Name of the icon from ICON_MAP.
        bg_color: Background color of the square.
        icon_color: Color of the icon character. Defaults to white.
        icon_size: Font size of the icon. Auto-calculated from size if not set.
    """
    from yaml2pptx.components.base import add_rect

    char, font = get_icon(icon_name)

    if icon_color is None:
        icon_color = RGBColor(0xFF, 0xFF, 0xFF)

    # Background square
    if bg_color:
        add_rect(slide, left, top, size, size, fill=bg_color)

    # Icon character centered in the square
    if icon_size is None:
        icon_size = int(size * 28)  # scale with shape size

    txBox = slide.shapes.add_textbox(
        Inches(left), Inches(top), Inches(size), Inches(size),
    )
    tf = txBox.text_frame
    tf.word_wrap = False
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    p.space_before = Pt(0)
    p.space_after = Pt(0)

    # Vertical centering via XML
    bodyPr = tf._txBody.find(qn('a:bodyPr'))
    if bodyPr is not None:
        bodyPr.set('anchor', 'ctr')

    run = p.add_run()
    run.text = char
    run.font.size = Pt(icon_size)
    run.font.name = font
    run.font.color.rgb = icon_color
    run.font.bold = False

    return txBox
