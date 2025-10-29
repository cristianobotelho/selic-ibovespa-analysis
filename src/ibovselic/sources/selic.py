from __future__ import annotations

from datetime import datetime
from typing import List

import requests

from ..models import IndexResult, SelicResponse


SERIE_SELIC_MENSAL = 4390  # Percent per month, accumulated within the month
SERIE_SELIC_META_DIARIA = 432  # Percent per year, daily target defined by COPOM
SERIE_SELIC_META_MENSAL = 4392  # Percent per year, accumulated within the month

SGS_URL_TEMPLATE = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.{serie}/dados"
REQUEST_TIMEOUT = 20


def get_selic_series(start_year: int, end_year: int, serie: int = SERIE_SELIC_META_MENSAL) -> List[IndexResult]:
    """Fetch historical SELIC data for a given SGS serie identifier."""
    url = SGS_URL_TEMPLATE.format(serie=serie)
    params = {
        "formato": "json",
        "dataInicial": f"01/01/{start_year}",
        "dataFinal": f"31/12/{end_year}",
    }

    response = requests.get(url, params=params, timeout=REQUEST_TIMEOUT)
    response.raise_for_status()

    raw = response.json()
    if not isinstance(raw, list):
        return []

    results: List[IndexResult] = []
    for item in raw:
        record = SelicResponse(**item)
        parsed_date = datetime.strptime(record.data, "%d/%m/%Y").date()
        month_start = parsed_date.replace(day=1)

        results.append(
            IndexResult(
                date_reference=month_start,
                month=month_start.month,
                year=month_start.year,
                index="SELIC",
                value=record.valor,
            )
        )

    return results

