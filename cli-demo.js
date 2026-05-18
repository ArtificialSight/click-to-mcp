#!/usr/bin/env node
// npm wrapper for click-to-mcp-demo Python CLI
const { execSync } = require('child_process');

function getPythonCommand() {
  const commands = ['python3', 'python'];
  for (const cmd of commands) {
    try {
      execSync(`${cmd} --version`, { stdio: 'ignore' });
      return cmd;
    } catch (e) {
      continue;
    }
  }
  console.error('Error: Python 3 is required but not found. Install it from https://python.org');
  process.exit(1);
}

function ensureInstalled() {
  const pythonCmd = getPythonCommand();
  try {
    execSync(`${pythonCmd} -c "import click_to_mcp"`, { stdio: 'ignore' });
  } catch (e) {
    console.log('Installing click-to-mcp Python package...');
    execSync(`${pythonCmd} -m pip install click-to-mcp`, { stdio: 'inherit' });
  }
}

const pythonCmd = getPythonCommand();
ensureInstalled();
try {
  execSync(`${pythonCmd} -m click_to_mcp.demo ${process.argv.slice(2).join(' ')}`, {
    stdio: 'inherit',
    env: { ...process.env }
  });
} catch (e) {
  process.exit(e.status || 1);
}
