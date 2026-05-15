"""Test MCP server mode on each CLI tool (fix src-layout)."""
import sys, json, subprocess

SRC_LAYOUTS = {
    "json2sql": "C:\\Users\\home\\OneDrive\\Documents\\GitHub\\json2sql\\src",
    "deploydiff": "C:\\Users\\home\\OneDrive\\Documents\\GitHub\\deploydiff\\src",
}

TOOLS = {
    "api-contract-guardian": {
        "import_path": "api_contract_guardian.cli",
        "attr": "app",
        "src_dir": None,
        "expected_tools": ["diff", "check", "migrate", "version", "mcp"]
    },
    "json2sql": {
        "import_path": "json2sql.cli",
        "attr": "app",
        "src_dir": SRC_LAYOUTS["json2sql"],
        "expected_tools": ["convert", "version", "mcp"]
    },
    "deploydiff": {
        "import_path": "deploydiff.cli",
        "attr": "main",
        "src_dir": SRC_LAYOUTS["deploydiff"],
        "expected_tools": ["preview", "cost", "rollback", "mcp"]
    },
}

for tool_name, info in TOOLS.items():
    print(f"\n{'='*60}")
    print(f"Testing MCP server for: {tool_name}")
    print(f"{'='*60}")

    test_msgs = [
        {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}},
        {"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}},
    ]
    test_input = "\n".join(json.dumps(m) for m in test_msgs)

    # Build the path setup
    path_setup = ""
    if info["src_dir"]:
        path_setup = f"sys.path.insert(0, r'{info['src_dir']}'); "

    cmd = (
        f"import sys; {path_setup}"
        f"from click_to_mcp import serve_stdio; "
        f"from {info['import_path']} import {info['attr']}; "
        f"serve_stdio({info['attr']}, name='{tool_name}')"
    )

    proc = subprocess.run(
        [sys.executable, "-c", cmd],
        input=test_input,
        capture_output=True,
        text=True,
        timeout=10
    )

    for line in proc.stdout.strip().split("\n"):
        try:
            resp = json.loads(line)
            if "result" in resp:
                r = resp["result"]
                if isinstance(r, dict) and "tools" in r:
                    tool_names = [t["name"] for t in r["tools"]]
                    print(f"  Tools ({len(r['tools'])}): {', '.join(tool_names)}")
                    for et in info["expected_tools"]:
                        found = any(et in tn for tn in tool_names)
                        print(f"    {et}: {'✓' if found else '✗'}")
                elif isinstance(r, dict) and "protocolVersion" in r:
                    print(f"  Initialize: OK (protocol {r['protocolVersion']})")
        except json.JSONDecodeError:
            pass

    if proc.stderr:
        stderr_clean = proc.stderr.strip()
        if stderr_clean:
            print(f"  Stderr: {stderr_clean[:200]}")

print("\nDone!")
