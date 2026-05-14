"""Entry points for wrapping CLIs as MCP servers."""

from click_to_mcp import serve_stdio
from click_to_mcp.demo import cli


def main():
    """Run click-to-mcp demo as an MCP server."""
    serve_stdio(
        cli,
        name="click-to-mcp-demo",
        description="Demo CLI exposing Click commands as MCP tools",
    )


if __name__ == "__main__":
    main()
