from __future__ import annotations

from datetime import date
from typing import Literal

from pydantic import BaseModel, Field


class IndexResult(BaseModel):
    """Normalized representation of a monthly financial indicator."""

    date_reference: date = Field(..., description="First day of the reference month")
    month: int = Field(..., ge=1, le=12)
    year: int = Field(..., ge=1900)
    index: Literal["IBOV", "SELIC"]
    value: float = Field(..., description="Closing value published by the source")


class IbovResponse(BaseModel):
    """Raw payload returned by the B3 IBOV endpoint."""

    month: int
    year: int
    indexClosingRate: float


class SelicResponse(BaseModel):
    """Raw payload returned by the Banco Central SGS endpoint."""

    data: str
    valor: float

