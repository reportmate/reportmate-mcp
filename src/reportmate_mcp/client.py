"""Async HTTP client over the ReportMate REST API (`/api/v1/*`)."""

from __future__ import annotations

from typing import Any

import httpx

from .config import Config


class ReportMateClient:
    def __init__(self, config: Config) -> None:
        self._http = httpx.AsyncClient(
            base_url=config.api_url,
            headers={
                "X-Client-Passphrase": config.passphrase,
                "Accept": "application/json",
            },
            timeout=30.0,
        )

    async def get(self, path: str, params: dict[str, Any] | None = None) -> Any:
        resp = await self._http.get(path, params=params)
        resp.raise_for_status()
        return resp.json()
