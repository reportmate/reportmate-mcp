"""Runtime configuration, resolved from the environment."""

from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Config:
    """Target and credentials for the ReportMate API.

    A scoped API key (``REPORTMATE_API_KEY``, sent as ``X-API-Key``) is the
    preferred credential — revocable and scope-limited. The shared client
    passphrase (``REPORTMATE_PASSPHRASE``, sent as ``X-Client-Passphrase``)
    is accepted as a fallback. A read-scoped key is the right fit for this
    server, which exposes only read tools.
    """

    api_url: str
    api_key: str | None
    passphrase: str | None

    @classmethod
    def from_env(cls) -> "Config":
        api_url = os.environ.get("REPORTMATE_API_URL")
        if not api_url:
            raise RuntimeError(
                "REPORTMATE_API_URL not set (e.g. https://api.reportmate.app)"
            )
        api_key = os.environ.get("REPORTMATE_API_KEY")
        passphrase = os.environ.get("REPORTMATE_PASSPHRASE")
        if not api_key and not passphrase:
            raise RuntimeError(
                "no credential: set REPORTMATE_API_KEY (preferred) or "
                "REPORTMATE_PASSPHRASE"
            )
        return cls(
            api_url=api_url.rstrip("/"),
            api_key=api_key,
            passphrase=passphrase,
        )

    def auth_header(self) -> dict[str, str]:
        if self.api_key:
            return {"X-API-Key": self.api_key}
        return {"X-Client-Passphrase": self.passphrase or ""}
