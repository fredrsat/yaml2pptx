from __future__ import annotations

from typing import Literal

from pydantic import BaseModel


class TextElement(BaseModel):
    text: str
    level: int = 0
    bold: bool | None = None
    italic: bool | None = None
    font_size: int | None = None


class ImageElement(BaseModel):
    path: str
    width: float | None = None
    height: float | None = None
    left: float | None = None
    top: float | None = None


class TableData(BaseModel):
    headers: list[str] | None = None
    rows: list[list[str]]
    style: str | None = None


class ChartSeries(BaseModel):
    name: str
    values: list[float | int]


class ChartData(BaseModel):
    type: Literal["bar", "column", "line", "pie", "scatter"]
    categories: list[str]
    series: list[ChartSeries]


class ShapeElement(BaseModel):
    type: Literal["image", "textbox"]
    path: str | None = None
    text: str | None = None
    left: float | None = None
    top: float | None = None
    width: float | None = None
    height: float | None = None
