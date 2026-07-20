"""Unit tests for the ReportMate MCP server.

No network: the API client is monkeypatched, so these exercise config
resolution, tool registration, and request shaping without a live API.
"""

import asyncio

import pytest

from reportmate_mcp import __version__
from reportmate_mcp.config import Config


class TestConfig:
    def test_api_key_preferred(self, monkeypatch):
        monkeypatch.setenv("REPORTMATE_API_URL", "https://api.example.com/")
        monkeypatch.setenv("REPORTMATE_API_KEY", "rm_a_b")
        monkeypatch.setenv("REPORTMATE_PASSPHRASE", "pp")
        cfg = Config.from_env()
        assert cfg.api_url == "https://api.example.com"  # trailing slash trimmed
        assert cfg.auth_header() == {"X-API-Key": "rm_a_b"}

    def test_passphrase_fallback(self, monkeypatch):
        monkeypatch.setenv("REPORTMATE_API_URL", "https://api.example.com")
        monkeypatch.delenv("REPORTMATE_API_KEY", raising=False)
        monkeypatch.setenv("REPORTMATE_PASSPHRASE", "pp")
        cfg = Config.from_env()
        assert cfg.auth_header() == {"X-Client-Passphrase": "pp"}

    def test_missing_url_raises(self, monkeypatch):
        monkeypatch.delenv("REPORTMATE_API_URL", raising=False)
        monkeypatch.setenv("REPORTMATE_API_KEY", "rm_a_b")
        with pytest.raises(RuntimeError, match="REPORTMATE_API_URL"):
            Config.from_env()

    def test_missing_credential_raises(self, monkeypatch):
        monkeypatch.setenv("REPORTMATE_API_URL", "https://api.example.com")
        monkeypatch.delenv("REPORTMATE_API_KEY", raising=False)
        monkeypatch.delenv("REPORTMATE_PASSPHRASE", raising=False)
        with pytest.raises(RuntimeError, match="no credential"):
            Config.from_env()


class TestServer:
    async def test_expected_tools_registered(self):
        from reportmate_mcp import server

        tools = server.mcp.list_tools()
        if asyncio.iscoroutine(tools):
            tools = await tools
        names = {getattr(t, "name", t) for t in tools}
        assert names == {
            "search_devices",
            "get_device",
            "get_device_module",
            "module_report",
            "fleet_summary",
            "application_usage",
            "recent_events",
            "api_health",
        }

    def test_ten_modules(self):
        from reportmate_mcp import server

        assert len(server.MODULES) == 10
        assert "installs" in server.MODULES and "network" in server.MODULES

    async def test_module_report_builds_expected_path(self, monkeypatch):
        from reportmate_mcp import server

        calls = {}

        class FakeClient:
            async def get(self, path, params=None):
                calls["path"] = path
                return {}

        monkeypatch.setattr(server, "client", lambda: FakeClient())
        await server.module_report("/installs/")
        assert calls["path"] == "/api/v1/installs"


def test_version_is_calendar_stamp():
    # YYYY.MM.DD.HHMM, zero-padded — not PEP 440-normalized.
    parts = __version__.split(".")
    assert len(parts) == 4
    assert parts[0] == "2026" and len(parts[3]) == 4
