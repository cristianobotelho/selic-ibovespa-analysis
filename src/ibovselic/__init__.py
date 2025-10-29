"""Utilities to download IBOVESPA and SELIC historical data."""

from .exporter import MarketDataExporter
from .sources import (
    SERIE_SELIC_MENSAL,
    SERIE_SELIC_META_DIARIA,
    SERIE_SELIC_META_MENSAL,
)

__all__ = [
    "MarketDataExporter",
    "SERIE_SELIC_MENSAL",
    "SERIE_SELIC_META_DIARIA",
    "SERIE_SELIC_META_MENSAL",
    "export_ibov",
    "export_selic",
    "export_selic_meta",
]


def export_ibov(start_year: int, end_year: int, data_dir: str | None = None) -> str:
    exporter = MarketDataExporter(data_dir=data_dir or "data/raw")
    return str(exporter.export_ibov(start_year, end_year))


def export_selic(
    start_year: int,
    end_year: int,
    data_dir: str | None = None,
    serie: int = SERIE_SELIC_MENSAL,
) -> str:
    exporter = MarketDataExporter(data_dir=data_dir or "data/raw")
    return str(exporter.export_selic(start_year, end_year, serie=serie))


def export_selic_meta(start_year: int, end_year: int, data_dir: str | None = None) -> str:
    exporter = MarketDataExporter(data_dir=data_dir or "data/raw")
    return str(exporter.export_selic_meta(start_year, end_year))

