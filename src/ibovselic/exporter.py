from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Callable, Iterable, List, Sequence

from .models import IndexResult
from .sources import (
    SERIE_SELIC_MENSAL,
    SERIE_SELIC_META_MENSAL,
    get_ibov_monthly,
    get_selic_series,
)

FetchCallable = Callable[[int, int], Sequence[IndexResult]]


class MarketDataExporter:
    """Utility that batches API requests and stores them as JSON datasets."""

    def __init__(self, data_dir: Path | str = "data/raw", chunk_size: int = 10) -> None:
        self.data_dir = Path(data_dir)
        self.chunk_size = chunk_size
        self.data_dir.mkdir(parents=True, exist_ok=True)

        self.logger = logging.getLogger(self.__class__.__name__)
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s")
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

    # Public API -----------------------------------------------------------

    def export_ibov(self, start_year: int, end_year: int, filename: str = "history_ibov.json") -> Path:
        return self._export_series(
            start_year=start_year,
            end_year=end_year,
            fetcher=get_ibov_monthly,
            filename=filename,
            label="IBOVESPA",
        )

    def export_selic(
        self,
        start_year: int,
        end_year: int,
        filename: str = "history_selic.json",
        serie: int = SERIE_SELIC_MENSAL,
    ) -> Path:
        return self._export_series(
            start_year=start_year,
            end_year=end_year,
            fetcher=lambda a, b: get_selic_series(a, b, serie=serie),
            filename=filename,
            label=f"SELIC serie {serie}",
        )

    def export_selic_meta(
        self,
        start_year: int,
        end_year: int,
        filename: str = "history_selic_meta.json",
    ) -> Path:
        return self.export_selic(
            start_year=start_year,
            end_year=end_year,
            filename=filename,
            serie=SERIE_SELIC_META_MENSAL,
        )

    # Internal helpers ----------------------------------------------------

    def _export_series(
        self,
        start_year: int,
        end_year: int,
        fetcher: FetchCallable,
        filename: str,
        label: str,
    ) -> Path:
        self._validate_years(start_year, end_year)

        self.logger.info("Starting export for %s (%s-%s)", label, start_year, end_year)

        data: List[IndexResult] = []
        current = start_year
        while current <= end_year:
            block_end = min(current + self.chunk_size - 1, end_year)
            self.logger.info("Requesting block %s-%s", current, block_end)
            block_data = fetcher(current, block_end)
            data.extend(block_data)
            current = block_end + 1

        output_path = self.data_dir / filename
        self._write_json(output_path, data)
        self.logger.info("Done. Saved %s entries to %s", len(data), output_path.resolve())

        return output_path

    @staticmethod
    def _write_json(path: Path, items: Iterable[IndexResult]) -> None:
        serializable = [json.loads(item.model_dump_json()) for item in items]
        with path.open("w", encoding="utf-8") as handle:
            json.dump(serializable, handle, ensure_ascii=False, indent=2)

    @staticmethod
    def _validate_years(start_year: int, end_year: int) -> None:
        if start_year > end_year:
            raise ValueError("start_year must be less than or equal to end_year")
        if start_year < 1900:
            raise ValueError("start_year must be greater than or equal to 1900")

