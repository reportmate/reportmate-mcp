# reportmate-mcp

A [Model Context Protocol](https://modelcontextprotocol.io) server for [ReportMate](https://reportmate.app). It exposes your device fleet to AI agents (Claude and others) as a small, curated set of read-only tools — so you can ask your fleet questions in natural language: *"which Macs are missing FileVault?"*, *"what changed on device 0F33V9G25083HJ?"*, *"show stale check-ins."*

Built on [FastMCP](https://github.com/jlowin/fastmcp). It is a thin layer over the ReportMate REST API (`/api/v1/*`) — the same language as the API, so request/response models can be shared over time.

## Tools

Read-only and intent-shaped (not one-per-endpoint), to keep the agent's toolset legible:

- `search_devices(query, limit)` — list/filter the fleet
- `get_device(serial_number)` — full record (all modules) for one device
- `get_device_module(serial_number, module)` — one module document for one device
- `module_report(module)` — fleet-wide report for a module (inventory, installs, applications, system, management, identity, hardware, peripherals, security, network)
- `fleet_summary()` — high-level counts and health
- `application_usage()` — fleet-wide app utilization
- `recent_events(limit)` — recent errors / warnings / check-ins
- `api_health()` — API readiness incl. a database probe

Mutations (archive/delete) are intentionally omitted from the default server.

## Configure

A scoped API key is the preferred credential; the shared client passphrase also works:

```
export REPORTMATE_API_URL=https://api.reportmate.app
export REPORTMATE_API_KEY=rm_yourclient_yoursecret
```

```
export REPORTMATE_PASSPHRASE=your-passphrase
```

A read-scoped key is the right fit — this server exposes only read tools.

## Run

```
uv run reportmate-mcp
```

Or via container:

```
docker run --rm -e REPORTMATE_API_URL -e REPORTMATE_API_KEY ghcr.io/reportmate/reportmate-mcp
```

Register it with an MCP client (e.g. Claude Desktop) by pointing the client at the `reportmate-mcp` command with the environment variables set.

## License

AGPL-3.0-or-later. A commercial license is available — see [COMMERCIAL-LICENSE.md](COMMERCIAL-LICENSE.md).
