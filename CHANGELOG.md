# Changelog

All notable changes to click-to-mcp will be documented in this file.

## [0.2.1] — 2026-05-15

### Added

- Comprehensive pytest test suite (12 tests): TestAdapter, TestServer, TestDiscover
- MCP integration examples: `examples/api_contract_guardian_mcp.py`, `examples/quick_start.py`
- Blog-style README with MCP workflow sections for Claude Code, Cursor, and Cline/VS Code
- Install-from-GitHub instructions as primary path (PyPI blocked by hCaptcha)
- "How It Works" table mapping Click concepts to MCP equivalents

### Changed

- Replaced script-style tests with proper pytest test functions
- README restructured with agent integration workflows as primary value proposition

## [0.1.0] — 2026-05-14

### Added

- Initial release
- Auto-discover installed Click/typer CLIs via `console_scripts` entry points (`click-to-mcp discover`)
- Serve any discovered CLI as an MCP server over stdio (`click-to-mcp serve <name>`)
- Built-in demo server (`click-to-mcp demo`)
- `serve_stdio()` — library API to wrap a Click/typer app as an MCP server
- `run()` — high-level library API with auto-detection
- Full MCP protocol: `initialize`, `tools/list`, `tools/call`
- Parameter introspection: maps Click options, arguments, types, enums, defaults, and help text to JSON Schema
- Nested command group support with prefixed tool names
- Dual Click and Typer framework compatibility
