# click-to-mcp

Auto-wrap any [Click](https://click.palletsprojects.com/)/[typer](https://typer.tiangolo.com/) CLI as an [MCP](https://modelcontextprotocol.io/) (Model Context Protocol) server.

Part of the [Revenue Holdings](https://coding-dev-tools.github.io/revenueholdings.dev/) developer tool ecosystem.

## Why?

AI coding agents (Claude Code, Codex, Cursor) use MCP to interact with tools. 
Instead of rewriting your CLI tools as MCP servers, use click-to-mcp to wrap them automatically.

Works great with [Revenue Holdings CLI tools](https://coding-dev-tools.github.io/revenueholdings.dev/) — wrap `api-contract-guardian`, `json2sql`, `deploydiff`, or `configdrift` as MCP servers with zero code changes.

## Quick Start

```bash
pip install click-to-mcp
```

Or install directly from GitHub:

```bash
pip install git+https://github.com/Coding-Dev-Tools/click-to-mcp.git
```
# Discover all Click/typer CLIs installed in your environment
click-to-mcp discover

# Serve a specific CLI as an MCP server
click-to-mcp serve api-contract-guardian

# Or serve the built-in demo
click-to-mcp demo
```

Then configure your MCP client to run `click-to-mcp serve <name>` as a stdio transport.

## Usage

### CLI — Discover and Serve

```bash
# List all installed Click/typer CLIs
click-to-mcp discover

# Serve a specific CLI as an MCP server over stdio
click-to-mcp serve <name>

# Serve the built-in demo
click-to-mcp demo

# Version info
click-to-mcp --version
```

### Library — Integrate directly

```python
# my_cli.py
import click
from click_to_mcp import serve_stdio

@click.group()
def cli():
    """My CLI tool."""
    pass

@cli.command()
@click.argument("file")
@click.option("--verbose", is_flag=True)
def validate(file: str, verbose: bool) -> None:
    """Validate a file."""
    click.echo(f"Validating {file}...")

# Run as MCP server
serve_stdio(cli, name="my-cli", description="My CLI as MCP server")
```

### Library — High-level `run()` API

```python
from click_to_mcp import run
from my_cli import app

# Automatically detects Click/typer instances
run(app, prefix="my-cli")
```

## Features

- **Auto-discovery**: `click-to-mcp discover` scans `console_scripts` entry points for Click/typer CLIs
- **Serve any CLI**: `click-to-mcp serve <name>` wraps any discovered CLI as an MCP server
- **Supports both Click and Typer**: Full compatibility with both frameworks
- **Nested command groups**: Handles subcommand groups recursively with prefixed tool names
- **Parameter introspection**: Correctly maps Click options, arguments, types, enums, defaults, and help text to JSON Schema
- **Full MCP protocol**: Implements `initialize`, `tools/list`, `tools/call` over stdio

## MCP Protocol

Click-to-MCP implements the standard MCP protocol with:

- `initialize` — protocol handshake (returns server capabilities)
- `tools/list` — discover all CLI commands as MCP tools with JSON Schema inputs
- `tools/call` — invoke a CLI command with typed arguments

## Integration with Existing CLIs

Add an MCP server entry point to any Click/typer CLI:

```python
# cli.py — add a subcommand to run as MCP server
import typer
from click_to_mcp import run

app = typer.Typer(...)

@app.command()
def mcp():
    """Run as an MCP server over stdio."""
    from click_to_mcp import run
    run(app)
```

Then agents can use it as: `your-cli mcp`

## Development

```bash
git clone https://github.com/Coding-Dev-Tools/click-to-mcp
cd click-to-mcp
pip install -e .
python -m click_to_mcp discover
click-to-mcp demo  # starts MCP server for demo CLI
```

## Pricing

click-to-mcp is **free and open source** under Apache 2.0. No license key required, no rate limits, no telemetry.

It also works with any [Revenue Holdings](https://coding-dev-tools.github.io/revenueholdings.dev/) CLI tool — even on the free tier.

## License

Apache 2.0

---

<sub>Part of [Revenue Holdings](https://coding-dev-tools.github.io/revenueholdings.dev/) — developer CLI tools built by autonomous AI agents.</sub>
