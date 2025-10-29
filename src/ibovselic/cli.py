from __future__ import annotations

import argparse
from pathlib import Path

from . import (
    SERIE_SELIC_MENSAL,
    SERIE_SELIC_META_DIARIA,
    SERIE_SELIC_META_MENSAL,
)
from .exporter import MarketDataExporter


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Download IBOVESPA and SELIC historical data as JSON files.",
    )
    parser.add_argument("--start-year", type=int, required=True, help="Initial year (inclusive)")
    parser.add_argument("--end-year", type=int, required=True, help="Final year (inclusive)")
    parser.add_argument(
        "--data-dir",
        type=Path,
        default=Path("data/raw"),
        help="Folder where the JSON files will be stored",
    )

    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument("--ibov", action="store_true", help="Export only IBOV data")
    group.add_argument("--selic", action="store_true", help="Export only SELIC data")
    group.add_argument("--selic-meta", action="store_true", help="Export only SELIC meta data")

    parser.add_argument(
        "--selic-serie",
        type=int,
        default=SERIE_SELIC_MENSAL,
        help="SGS serie code to use when exporting SELIC data",
    )

    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable debug logs for troubleshooting",
    )

    return parser


def main(args: list[str] | None = None) -> None:
    parser = build_parser()
    parsed = parser.parse_args(args=args)

    exporter = MarketDataExporter(data_dir=parsed.data_dir)
    if parsed.verbose:
        exporter.logger.setLevel("DEBUG")

    tasks_run = 0

    if parsed.ibov:
        exporter.export_ibov(parsed.start_year, parsed.end_year)
        tasks_run += 1

    if parsed.selic:
        exporter.export_selic(parsed.start_year, parsed.end_year, serie=parsed.selic_serie)
        tasks_run += 1

    if parsed.selic_meta:
        exporter.export_selic_meta(parsed.start_year, parsed.end_year)
        tasks_run += 1

    if tasks_run == 0:
        exporter.export_ibov(parsed.start_year, parsed.end_year)
        exporter.export_selic(parsed.start_year, parsed.end_year, serie=parsed.selic_serie)
        exporter.export_selic_meta(parsed.start_year, parsed.end_year)


if __name__ == "__main__":
    main()

