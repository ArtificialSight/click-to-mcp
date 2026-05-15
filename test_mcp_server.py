"""Test click-to-mcp MCP server protocol end-to-end."""
import sys, json, subprocess

sys.path.insert(0, r'C:\Users\home\OneDrive\Documents\GitHub\click-to-mcp')

test_msgs = [
    {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}},
    {"jsonrpc": "2.0", "id": 2, "method": "notifications/initialized", "params": {}},
    {"jsonrpc": "2.0", "id": 3, "method": "tools/list", "params": {}},
    {"jsonrpc": "2.0", "id": 4, "method": "tools/call", "params": {
        "name": "greet",
        "arguments": {"name": "World", "greeting": "Hi", "repeat": 1}
    }},
]

test_input = "\n".join(json.dumps(m) for m in test_msgs)

proc = subprocess.run(
    [sys.executable, "-c", """
import sys
sys.path.insert(0, r'C:\\Users\\home\\OneDrive\\Documents\\GitHub\\click-to-mcp')
from click_to_mcp import serve_stdio
from click_to_mcp.demo import cli
serve_stdio(cli, name='click-to-mcp-demo')
"""],
    input=test_input,
    capture_output=True,
    text=True,
    timeout=10
)

print("=== STDOUT ===")
print(proc.stdout)
if proc.stderr:
    print("=== STDERR ===")
    print(proc.stderr[:500])
print(f"=== Exit code: {proc.returncode} ===")

# Parse and check responses
lines = proc.stdout.strip().split("\n")
for line in lines:
    try:
        resp = json.loads(line)
        method = resp.get("id")
        if "result" in resp:
            r = resp["result"]
            if isinstance(r, dict) and "tools" in r:
                print(f"\nTools found: {len(r['tools'])}")
                for t in r["tools"]:
                    print(f"  - {t['name']}: {t.get('description', '')[:60]}")
            elif isinstance(r, dict) and "protocolVersion" in r:
                print(f"\nInitialize: protocol={r['protocolVersion']}, server={r.get('serverInfo',{})}")
            elif isinstance(r, dict) and "content" in r:
                print(f"\nTool result: {r['content'][0]['text'][:100]}")
    except json.JSONDecodeError:
        pass
