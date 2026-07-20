"""ReportMate MCP server."""

# Calendar version, YYYY.MM.DD.HHMM (UTC) — the convention for every
# ReportMate binary. This literal is the source of truth used at runtime
# (User-Agent, server version) so the exact zero-padded form is preserved.
# Python packaging (importlib.metadata) PEP 440-normalizes the installed
# package version separately (e.g. 2026.07.20.0038 -> 2026.7.20.38); do not
# read the version from there for display.
__version__ = "2026.07.20.0057"
