"""
click-to-mcp — Auto-wrap any Click/typer CLI as an MCP (Model Context Protocol) server.

Usage:
    pip install click-to-mcp
    click-to-mcp discover            # List all Click/typer CLIs
    click-to-mcp serve <name>        # Serve a specific CLI as MCP
    click-to-mcp serve --all         # Serve first discoverable CLI
    click-to-mcp demo                # Run built-in demo

Or use as a library:
    from click_to_mcp import run, serve_stdio, cli_to_mcp_tools
    from my_cli import app
    run(app, prefix="my-cli")
"""

from __future__ import annotations

from typing import Any

from .adapter import cli_to_mcp_tools, CliToolDef
from .server import serve_stdio
from .discover import scan_entry_points, load_cli, find_our_clis, DiscoveredCLI

__version__ = "0.2.0"


def run(app: Any, prefix: str = "", name: str = "") -> None:
    """High-level entry point: serve a Click/typer app as an MCP server over stdio.

    This is the primary API for integrating click-to-mcp into your CLI tool.
    Call it from your mcp subcommand or mcp_server.py module.

    Args:
        app: A click.Group or typer.Typer instance.
        prefix: Optional tool name prefix (e.g. 'acg' for api-contract-guardian).
        name: Optional server name (defaults to app name or 'cli').
    """
    import inspect

    if not name:
        name = getattr(app, "name", None) or "cli"
    desc = ""
    if hasattr(app, "info"):
        info_desc = getattr(app.info, "help", None)
        if info_desc and "DefaultPlaceholder" not in str(type(info_desc)):
            desc = str(info_desc)
    if not desc:
        desc = getattr(app, "help", None) or ""
    if not isinstance(desc, str):
        desc = str(desc) if desc else ""

    serve_stdio(
        app,
        name=name,
        description=desc,
        prefix=prefix,
    )


__all__ = [
    "cli_to_mcp_tools", "CliToolDef", "serve_stdio", "run",
    "scan_entry_points", "load_cli", "find_our_clis", "DiscoveredCLI",
]
