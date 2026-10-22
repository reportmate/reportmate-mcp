# ReportMate MCP wiki

The MCP server exposes a ReportMate fleet to AI agents through the Model Context Protocol. It owns no data of its own: it is a read-only layer over the ReportMate REST API (`/api/v1/*`), and agents use its small set of intent-shaped tools to ask fleet questions in natural language.

## Read first

- [Project setup, configuration and tools](../README.md)
- [Tool definitions](../src/reportmate_mcp/server.py)
- [Runtime configuration](../src/reportmate_mcp/config.py)
- [Commercial licensing](../COMMERCIAL-LICENSE.md)

## Architecture

The server uses FastMCP and runs over stdio by default, which is how desktop MCP clients launch it. The [entry point](../src/reportmate_mcp/__main__.py) backs both the `reportmate-mcp` console script and `python -m reportmate_mcp`.

[`server.py`](../src/reportmate_mcp/server.py) registers eight tools: `search_devices`, `get_device`, `get_device_module`, `module_report`, `fleet_summary`, `application_usage`, `recent_events` and `api_health`. The tools are shaped around the questions people ask rather than mirroring every endpoint, so an agent sees a short, legible toolset. The ten collection modules (inventory, installs, applications, system, management, identity, hardware, peripherals, security and network) match the dashboard tabs. Archive and delete operations are deliberately left out.

[`client.py`](../src/reportmate_mcp/client.py) is a thin asynchronous httpx client with a 30-second timeout and a `reportmate-mcp/<version>` user agent. The server builds it lazily, so the package imports without environment variables set.

[`config.py`](../src/reportmate_mcp/config.py) reads `REPORTMATE_API_URL` and a credential from the environment. A scoped API key in `REPORTMATE_API_KEY` is sent as `X-API-Key` and is preferred; the shared client passphrase in `REPORTMATE_PASSPHRASE` is the fallback. A read-scoped key fits, because every tool only reads.

The version is a calendar stamp, `YYYY.MM.DD.HHMM` in UTC, kept in [`__init__.py`](../src/reportmate_mcp/__init__.py). The packaging build reads it from there, and the runtime uses that literal rather than the normalized package metadata.

The [Dockerfile](../Dockerfile) installs the package on a slim Python image with `reportmate-mcp` as its entry point. The [build workflow](../.github/workflows/build.yml) builds that image on pull requests and publishes it to GHCR from `main` and version tags.

## Development and verification

Use the [README](../README.md) for setup and running. Dependencies are managed with uv; the dev group adds pytest, pytest-asyncio and ruff.

```
uv sync --group dev
```

```
uv run ruff check .
```

```
uv run pytest -q
```

The [tests](../tests/test_mcp.py) need no network. They cover credential resolution, the exact set of registered tools, the module list, request path shaping and the version format, with the API client replaced by a fake. The [CI workflow](../.github/workflows/ci.yml) runs the same lint and tests on every pull request to `main`.

To try the server against a real API, set `REPORTMATE_API_URL` to an instance such as `https://api.example.com` with a read-scoped key, then run `uv run reportmate-mcp` or register the command with an MCP client.

## Documentation ownership

Keep this wiki as the entry point and update the linked pages where the facts belong: setup and the tool list in the README, tool behaviour in the docstrings in `server.py`. Examples use fictional data. Deployment inventories, credentials, provider mappings and organization-specific operations belong with their deployment owner.
