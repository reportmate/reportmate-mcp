"""Entry point: `reportmate-mcp` or `python -m reportmate_mcp`."""

from .server import mcp


def main() -> None:
    # Defaults to stdio transport (how MCP clients like Claude Desktop launch it).
    mcp.run()


if __name__ == "__main__":
    main()
