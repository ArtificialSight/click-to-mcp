"""Tests for the click-to-mcp list-tools feature (adapter-based)."""

from __future__ import annotations

import json

import pytest

from click_to_mcp.adapter import cli_to_mcp_tools, CliToolDef
from click_to_mcp.demo import cli as demo_cli


class TestListToolsAdapter:
    """Test the adapter's tool introspection — the core of the list-tools feature."""

    def test_demo_cli_has_calculate(self):
        tools = cli_to_mcp_tools(demo_cli)
        tool_names = [t.name for t in tools]
        assert any("calculate" in n for n in tool_names)

    def test_demo_cli_has_greet(self):
        tools = cli_to_mcp_tools(demo_cli)
        tool_names = [t.name for t in tools]
        assert any("greet" in n for n in tool_names)

    def test_tool_input_schema_has_type_object(self):
        tools = cli_to_mcp_tools(demo_cli)
        for tool in tools:
            assert tool.input_schema["type"] == "object"

    def test_required_params_marked(self):
        tools = cli_to_mcp_tools(demo_cli)
        # The calculate command should have required params (x, y)
        calc_tool = next((t for t in tools if "calculate" in t.name), None)
        assert calc_tool is not None
        assert len(calc_tool.input_schema.get("required", [])) >= 2

    def test_tool_names_are_valid_identifiers(self):
        """Tool names should be valid MCP tool names (no spaces)."""
        tools = cli_to_mcp_tools(demo_cli)
        for tool in tools:
            assert " " not in tool.name, f"Tool name '{tool.name}' contains spaces"

    def test_tool_descriptions_are_nonempty(self):
        tools = cli_to_mcp_tools(demo_cli)
        for tool in tools:
            assert tool.description.strip(), f"Tool '{tool.name}' has no description"

    def test_json_serializable_output(self):
        """Test that tool definitions can be serialized to JSON (for --json-output)."""
        tools = cli_to_mcp_tools(demo_cli, prefix="demo")
        output = []
        for tool in tools:
            output.append({
                "name": tool.name,
                "description": tool.description,
                "input_schema": tool.input_schema,
            })
        json_str = json.dumps(output, indent=2)
        parsed = json.loads(json_str)
        assert isinstance(parsed, list)
        assert len(parsed) > 0
        assert "name" in parsed[0]
        assert "input_schema" in parsed[0]

    def test_prefix_is_applied(self):
        """Prefixed tools should include the prefix in their name."""
        tools = cli_to_mcp_tools(demo_cli, prefix="myprefix")
        for tool in tools:
            assert tool.name.startswith("myprefix_"), f"Tool '{tool.name}' missing prefix"
