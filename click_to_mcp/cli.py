"""click-to-mcp meta-CLI — discover and serve Click/typer CLIs as MCP servers.

Usage:
    click-to-mcp discover            # List all discoverable CLIs
    click-to-mcp serve <name>        # Serve a specific CLI (stdio)
    click-to-mcp serve --all         # Serve all discoverable CLIs (stdio)
    click-to-mcp serve-http <name>   # Serve a CLI over HTTP+SSE
    click-to-mcp demo                # Run the demo CLI as MCP server (stdio)
    click-to-mcp demo-http           # Run the demo CLI as HTTP+SSE server
"""

from __future__ import annotations

import sys
from typing import Optional

import click

from . import serve_stdio, __version__
from .discover import scan_entry_points, load_cli


@click.group()
@click.version_option(version=__version__, prog_name="click-to-mcp")
def cli():
    """Auto-wrap any Click/typer CLI as an MCP (Model Context Protocol) server."""
    pass


@cli.command()
def discover():
    """List all installed Click/typer CLIs that can be served as MCP tools."""
    clis = scan_entry_points()

    if not clis:
        click.echo("No Click/typer CLIs found in installed packages.")
        click.echo("Install a Click/typer-based CLI and run this command again.")
        return

    click.echo(f"Found {len(clis)} Click/typer CLI(s):")
    click.echo("")

    for i, cli_info in enumerate(clis, 1):
        type_tag = "[Typer]" if cli_info.is_typer else "[Click]"
        summary = cli_info.summary[:80] if cli_info.summary else "(no description)"
        click.echo(f"  {i}. {type_tag} {cli_info.name}")
        click.echo(f"       Package: {cli_info.package_name} {cli_info.package_version}")
        click.echo(f"       Module:  {cli_info.module_path}:{cli_info.attr_name}")
        click.echo(f"       Summary: {summary}")
        click.echo("")

    click.echo("Usage:  click-to-mcp serve <name>")
    click.echo("        click-to-mcp serve --all")


@cli.command()
@click.argument("name", required=False, default=None)
@click.option("--all", "serve_all", is_flag=True, help="Serve all discoverable CLIs")
def serve(name: Optional[str], serve_all: bool):
    """Serve a CLI as an MCP server over stdio.

    Specify a CLI NAME from 'click-to-mcp discover', or use --all.
    """
    if not name and not serve_all:
        click.echo("Error: Specify a CLI name or --all", err=True)
        sys.exit(1)

    if serve_all:
        clis = scan_entry_points()
        if not clis:
            click.echo("No CLIs found to serve.", err=True)
            sys.exit(1)
        # Serve the first one as primary — MCP stdio is single-server.
        # For --all we could eventually multiplex, but for now serve the first.
        click.echo(f"Multiple CLIs found. Serving the first one: {clis[0].name}", err=True)
        target_cli = load_cli(clis[0].name)
        if target_cli is None:
            click.echo(f"Error: Could not load CLI '{clis[0].name}'", err=True)
            sys.exit(1)
        serve_stdio(target_cli, name=clis[0].name)
        return

    target_cli = load_cli(name)
    if target_cli is None:
        click.echo(f"Error: CLI '{name}' not found.", err=True)
        click.echo("Run 'click-to-mcp discover' to see available CLIs.", err=True)
        sys.exit(1)

    serve_stdio(target_cli, name=name)


@cli.command()
@click.argument("name", required=False, default=None)
@click.option("--host", default="127.0.0.1", help="Host to bind (default: 127.0.0.1)")
@click.option("--port", default=8000, type=int, help="Port to bind (default: 8000)")
@click.option("--all", "serve_all", is_flag=True, help="Serve all discoverable CLIs")
def serve_http(name: Optional[str], host: str, port: int, serve_all: bool):
    """Serve a CLI as an MCP server over HTTP+SSE.

    Specify a CLI NAME from 'click-to-mcp discover', or use --all.
    Requires optional HTTP dependencies: pip install 'click-to-mcp[http]'
    """
    if not name and not serve_all:
        click.echo("Error: Specify a CLI name or --all", err=True)
        sys.exit(1)

    # Try to import HTTP deps early for a clear error message
    try:
        from .http_server import serve_http as _serve_http
    except ImportError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)

    if serve_all:
        clis = scan_entry_points()
        if not clis:
            click.echo("No CLIs found to serve.", err=True)
            sys.exit(1)
        click.echo(f"Multiple CLIs found. Serving the first one: {clis[0].name}", err=True)
        target_cli = load_cli(clis[0].name)
        if target_cli is None:
            click.echo(f"Error: Could not load CLI '{clis[0].name}'", err=True)
            sys.exit(1)
        _serve_http(target_cli, name=clis[0].name, host=host, port=port)
        return

    target_cli = load_cli(name)
    if target_cli is None:
        click.echo(f"Error: CLI '{name}' not found.", err=True)
        click.echo("Run 'click-to-mcp discover' to see available CLIs.", err=True)
        sys.exit(1)

    _serve_http(target_cli, name=name, host=host, port=port)


@cli.command()
def demo():
    """Run the built-in demo CLI as an MCP server (stdio)."""
    from .demo import cli as demo_cli

    serve_stdio(demo_cli, name="click-to-mcp-demo")


@cli.command("demo-http")
@click.option("--host", default="127.0.0.1", help="Host to bind (default: 127.0.0.1)")
@click.option("--port", default=8000, type=int, help="Port to bind (default: 8000)")
def demo_http(host: str, port: int):
    """Run the built-in demo CLI as an HTTP+SSE MCP server.

    Requires optional HTTP dependencies: pip install 'click-to-mcp[http]'
    """
    try:
        from .http_server import serve_http as _serve_http
    except ImportError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)

    from .demo import cli as demo_cli

    _serve_http(demo_cli, name="click-to-mcp-demo", host=host, port=port)


def main():
    """Entry point for the click-to-mcp CLI."""
    cli()


if __name__ == "__main__":
    main()
