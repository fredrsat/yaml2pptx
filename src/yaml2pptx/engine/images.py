"""Image insertion for python-pptx slides."""

from __future__ import annotations

from pathlib import Path

from pptx.util import Inches


def add_image_to_slide(
    slide,  # type: ignore[no-untyped-def]
    image_path: str,
    left: float | None = None,
    top: float | None = None,
    width: float | None = None,
    height: float | None = None,
) -> None:
    """Add an image to a slide."""
    path = Path(image_path)
    if not path.exists():
        raise FileNotFoundError(f"Image not found: {path}")

    img_left = Inches(left) if left is not None else Inches(1.0)
    img_top = Inches(top) if top is not None else Inches(2.0)
    img_width = Inches(width) if width is not None else None
    img_height = Inches(height) if height is not None else None

    slide.shapes.add_picture(str(path), img_left, img_top, img_width, img_height)
