"""Main PPTX generation pipeline."""

from __future__ import annotations

import logging
from pathlib import Path

logger = logging.getLogger(__name__)

from yaml2pptx.engine.charts import add_chart_to_slide
from yaml2pptx.engine.images import add_image_to_slide
from yaml2pptx.engine.tables import add_table_to_slide
from yaml2pptx.engine.template import TemplateError, TemplateManager
from yaml2pptx.engine.text import populate_text_frame, set_title
from yaml2pptx.models.elements import TextElement
from yaml2pptx.models.presentation import PresentationModel


class GenerationError(Exception):
    pass


def generate(model: PresentationModel, output_path: str | Path | None = None) -> Path:
    """Generate a PPTX file from a PresentationModel."""
    tm = TemplateManager(model.template)
    prs = tm.prs

    # Defaults
    font_size = model.defaults.font_size if model.defaults else None
    font_name = model.defaults.font_name if model.defaults else None

    for slide_idx, slide_def in enumerate(model.slides):
        try:
            layout = tm.get_layout(slide_def.layout, model.layout_map)
        except TemplateError as e:
            raise GenerationError(f"Slide {slide_idx + 1}: {e}") from e

        slide = prs.slides.add_slide(layout)

        # Title
        if slide_def.title:
            set_title(slide, slide_def.title)

        # Subtitle (typically idx=1 on title slides)
        if slide_def.subtitle:
            _populate_subtitle(slide, slide_def.subtitle)

        # Content (body placeholder)
        if slide_def.content:
            _populate_body(slide, slide_def.content, font_size, font_name, placeholder_idx=1)

        # Two-column layout
        if slide_def.left:
            _populate_body(slide, slide_def.left, font_size, font_name, placeholder_idx=1)
        if slide_def.right:
            _populate_body(slide, slide_def.right, font_size, font_name, placeholder_idx=2)

        # Image
        if slide_def.image:
            add_image_to_slide(slide, slide_def.image)

        # Table
        if slide_def.table:
            add_table_to_slide(slide, slide_def.table)

        # Chart
        if slide_def.chart:
            add_chart_to_slide(slide, slide_def.chart)

        # Speaker notes
        if slide_def.speaker_notes:
            notes_slide = slide.notes_slide
            notes_slide.notes_text_frame.text = slide_def.speaker_notes

    # Metadata
    if model.metadata:
        if model.metadata.title:
            prs.core_properties.title = model.metadata.title
        if model.metadata.author:
            prs.core_properties.author = model.metadata.author
        if model.metadata.subject:
            prs.core_properties.subject = model.metadata.subject

    # Determine output path
    if output_path:
        out = Path(output_path)
    elif model.output:
        out = Path(model.output)
    else:
        out = Path("output.pptx")

    prs.save(str(out))
    return out


def _populate_subtitle(slide, subtitle_text: str) -> None:  # type: ignore[no-untyped-def]
    """Populate the subtitle placeholder."""
    for shape in slide.placeholders:
        if shape.placeholder_format.idx == 1 and not slide.shapes.title == shape:
            shape.text = subtitle_text
            return
    logger.warning("Subtitle placeholder not found on slide")


def _populate_body(
    slide,  # type: ignore[no-untyped-def]
    elements: list[TextElement],
    font_size: int | None,
    font_name: str | None,
    placeholder_idx: int = 1,
) -> None:
    """Populate a body placeholder with text elements."""
    for shape in slide.placeholders:
        if shape.placeholder_format.idx == placeholder_idx:
            populate_text_frame(shape.text_frame, elements, font_size, font_name)
            return
    logger.warning("Body placeholder (idx=%d) not found on slide", placeholder_idx)
