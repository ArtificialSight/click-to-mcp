"""
click-to-mcp — Auto-wrap any Click/typer CLI as an MCP server.

Usage:
    from click_to_mcp import run
    from my_cli import cli_group
    run(cli_group, prefix="my-cli")
"""

from __future__ import annotations

from typing import Any

from .adapter import cli_to_mcp_tools, CliToolDef
from .server import serve_stdio

__version__ = "0.1.0"


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
    # Get description, handling TyperInfo objects
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


__all__ = ["cli_to_mcp_tools", "CliToolDef", "serve_stdio", "run"]
