from __future__ import annotations

import base64
import json
from datetime import date
from typing import List

import requests

from ..models import IbovResponse, IndexResult


API_HOST = "https://sistemaswebb3-listados.b3.com.br"
API_ROUTE = "indexStatisticsProxy/IndexCall/GetMonthlyEvolution"
REQUEST_TIMEOUT = 15


def _build_encoded_payload(start_year: int, end_year: int) -> str:
    payload = {
        "index": "IBOVESPA",
        "language": "pt-br",
        "dateInitial": f"{start_year}-01-01",
        "dateFinal": f"{end_year}-12-31",
    }
    json_str = json.dumps(payload, separators=(",", ":"))
    return base64.b64encode(json_str.encode()).decode()


def get_ibov_monthly(start_year: int, end_year: int) -> List[IndexResult]:
    """Fetch the monthly IBOV index history for the provided interval."""
    encoded = _build_encoded_payload(start_year, end_year)
    url = f"{API_HOST}/{API_ROUTE}/{encoded}"

    response = requests.get(url, timeout=REQUEST_TIMEOUT)
    response.raise_for_status()
    raw = response.json()

    if isinstance(raw, dict):
        payload = raw.get("results", [])
    elif isinstance(raw, list):
        payload = raw
    else:
        payload = []

    results: List[IndexResult] = []
    for item in payload:
        record = IbovResponse(**item)
        results.append(
            IndexResult(
                date_reference=date(record.year, record.month, 1),
                month=record.month,
                year=record.year,
                index="IBOV",
                value=record.indexClosingRate,
            )
        )

    return results

