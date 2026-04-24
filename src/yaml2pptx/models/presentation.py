from __future__ import annotations

from pydantic import BaseModel

from yaml2pptx.models.slides import SlideDefinition


class PresentationMetadata(BaseModel):
    title: str | None = None
    author: str | None = None
    subject: str | None = None


class PresentationDefaults(BaseModel):
    font_size: int | None = None
    font_name: str | None = None


class PresentationModel(BaseModel):
    template: str | None = None
    output: str | None = None
    metadata: PresentationMetadata | None = None
    defaults: PresentationDefaults | None = None
    layout_map: dict[str, str | int] | None = None
    slides: list[SlideDefinition]
