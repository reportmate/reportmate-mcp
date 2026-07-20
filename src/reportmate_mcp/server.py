"""ReportMate MCP server (FastMCP).

A curated, **read-only** set of tools over the ReportMate REST API. The tools
are intent-shaped (not one-per-endpoint) so an agent gets a small, legible
toolset. Mutations (archive/delete) are intentionally omitted from the default
server; add them behind an explicit opt-in if/when needed.
"""

from __future__ import annotations

from typing import Any

from fastmcp import FastMCP

from .client import ReportMateClient
from .config import Config

mcp = FastMCP("reportmate")

# The ten collection modules, matching the dashboard tabs. Fleet reports and
# per-device module documents both address a module by one of these names
# (nested variants like "installs/full" or "security/certificates" also work
# against the fleet report endpoint but are not enumerated here).
MODULES = (
    "inventory",
    "installs",
    "applications",
    "system",
    "management",
    "identity",
    "hardware",
    "peripherals",
    "security",
    "network",
)

_client: ReportMateClient | None = None


def client() -> ReportMateClient:
    """Lazily construct the API client so the module imports without env vars."""
    global _client
    if _client is None:
        _client = ReportMateClient(Config.from_env())
    return _client


@mcp.tool
async def search_devices(query: str = "", limit: int = 0) -> list[dict[str, Any]]:
    """List devices in the fleet, optionally filtered by a free-text query
    (matches serial, name, model, OS, etc.). Set limit to cap the result count
    (0 = all)."""
    data = await client().get("/api/v1/devices")
    devices = data.get("devices", data) if isinstance(data, dict) else data
    if query:
        q = query.lower()
        devices = [d for d in devices if q in str(d).lower()]
    if limit and limit > 0:
        devices = devices[:limit]
    return devices


@mcp.tool
async def get_device(serial_number: str) -> dict[str, Any]:
    """Return the full record for a single device (all modules) by serial
    number."""
    return await client().get(f"/api/v1/device/{serial_number}")


@mcp.tool
async def get_device_module(serial_number: str, module: str) -> Any:
    """Return one module document for a single device — e.g. module="installs"
    to see just the managed-install state, or "network", "security", etc."""
    return await client().get(f"/api/v1/device/{serial_number}/modules/{module}")


@mcp.tool
async def module_report(module: str) -> Any:
    """Fleet-wide report for one collection module: inventory, installs,
    applications, system, management, identity, hardware, peripherals,
    security, or network. Returns every device's data for that module."""
    m = module.strip().strip("/")
    return await client().get(f"/api/v1/{m}")


@mcp.tool
async def fleet_summary() -> dict[str, Any]:
    """High-level fleet counts and health (dashboard rollup)."""
    return await client().get("/api/v1/dashboard")


@mcp.tool
async def application_usage() -> Any:
    """Fleet-wide application usage/utilization report."""
    return await client().get("/api/v1/applications/usage")


@mcp.tool
async def recent_events(limit: int = 50) -> Any:
    """Most recent fleet events (errors, warnings, check-ins)."""
    return await client().get("/api/v1/events", params={"limit": limit})


@mcp.tool
async def api_health() -> dict[str, Any]:
    """API readiness, including a database-connectivity probe."""
    return await client().get("/api/v1/health/ready")
