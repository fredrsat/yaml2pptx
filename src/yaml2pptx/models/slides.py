from __future__ import annotations

from pydantic import BaseModel, field_validator

from yaml2pptx.models.elements import (
    ChartData,
    ImageElement,
    ShapeElement,
    TableData,
    TextElement,
)


def _normalize_content(v: list | None) -> list[TextElement] | None:
    if v is None:
        return None
    result = []
    for item in v:
        if isinstance(item, str):
            result.append(TextElement(text=item))
        elif isinstance(item, dict):
            result.append(TextElement(**item))
        elif isinstance(item, TextElement):
            result.append(item)
        else:
            raise ValueError(f"Invalid content item type: {type(item).__name__}")
    return result


class SlideDefinition(BaseModel):
    layout: str
    title: str | None = None
    subtitle: str | None = None
    content: list[TextElement] | None = None
    left: list[TextElement] | None = None
    right: list[TextElement] | None = None
    image: str | None = None
    caption: str | None = None
    table: TableData | None = None
    chart: ChartData | None = None
    shapes: list[ShapeElement] | None = None
    speaker_notes: str | None = None

    @field_validator("content", "left", "right", mode="before")
    @classmethod
    def normalize_content_items(cls, v: list | None) -> list[TextElement] | None:
        return _normalize_content(v)
