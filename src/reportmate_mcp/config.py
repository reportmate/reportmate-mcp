"""Runtime configuration, resolved from the environment."""

from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Config:
    api_url: str
    passphrase: str

    @classmethod
    def from_env(cls) -> "Config":
        api_url = os.environ.get("REPORTMATE_API_URL")
        if not api_url:
            raise RuntimeError(
                "REPORTMATE_API_URL not set (e.g. https://api.reportmate.app)"
            )
        return cls(
            api_url=api_url.rstrip("/"),
            passphrase=os.environ.get("REPORTMATE_PASSPHRASE", ""),
        )
