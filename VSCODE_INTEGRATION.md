# VS Code Integration Guide

This document explains how to integrate the MCP Shell Server into VS Code.

## Adding to VS Code Settings

1. Open VS Code Settings (File > Preferences > Settings or Ctrl+,)
2. Click on the "Open Settings (JSON)" icon in the upper right corner
3. Add the following configuration to your `settings.json`:

```json
"mcp": {
  "servers": {
    "shell-server": {
      "command": "python",
      "args": ["path/to/shellserver.py"],
      "type": "stdio",
      "env": {}
    }
  }
}
```

Replace `"path/to/shellserver.py"` with the absolute path to your `shellserver.py` file.

## Using with VS Code Copilot

Once configured, you can use the shell server with Copilot in VS Code:

1. Open the Copilot Chat panel
2. Type commands that reference terminal operations
3. Copilot will use the shell server to execute terminal commands when needed

## Troubleshooting

If the shell server isn't working with VS Code:

1. Check the VS Code Developer Tools Console (Help > Toggle Developer Tools) for any error messages
2. Verify that the path to the shell server is correct
3. Make sure the MCP extension is enabled in VS Code
4. Try restarting VS Code after making changes to settings
