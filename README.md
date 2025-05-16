# MCP Shell Server

A Python implementation of a Model Context Protocol (MCP) server that exposes a terminal command execution tool.

## Overview

This MCP Shell Server provides a secure way to execute terminal commands through the Model Context Protocol, allowing AI assistants and other MCP clients to interact with the command line in a controlled environment.

## Features

- 🔒 **Secure Command Execution**: Only allows predefined commands to be executed
- ⚙️ **Configurable**: Customize allowed commands, timeout settings, and output limits
- 🔄 **Async Processing**: Uses asyncio for efficient command execution
- 📋 **Robust Output Handling**: Properly captures stdout and stderr
- ⏱️ **Timeout Protection**: Prevents long-running commands from blocking the server
- 📝 **Comprehensive Logging**: Tracks all command executions

## Installation

### Prerequisites

- Python 3.8+
- Virtual environment (recommended)

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/mcp-shell-server.git
   cd mcp-shell-server
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   .\venv\Scripts\activate  # Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

The server can be configured using a `config.toml` file with the following options:

```toml
# Server configuration
[server]
host = "localhost"
port = 8080
debug = true

# Shell configuration
allowed_commands = [
    "dir",
    "ls",
    "echo", 
    # Add more allowed commands here
]
max_output_length = 8192
timeout = 30

# Security settings
[security]
require_auth = false
api_key = ""  # Set if require_auth is true
```

## Usage

### Running the Server

Start the server with:

```bash
python shellserver.py
```

Or use the MCP development mode:

```bash
mcp dev shellserver.py
```

### Testing with the Client

A test client is included to verify the functionality of the server:

```bash
python test_client.py
```

### Integrating with VS Code

You can add this server to your VS Code settings in `settings.json`:

```json
"mcp": {
    "servers": {
        "shell-server": {
            "command": "python",
            "args": ["shellserver.py"],
            "type": "stdio",
            "env": {}
        }
    }
}
```

## API

### Tools

#### `terminal`

Executes a terminal command and returns the output.

**Parameters:**
- `command` (string): The command to run

**Returns:**
- String containing command output

**Example:**
```python
result = await session.call_tool("terminal", {"command": "dir"})
```

### Resources

#### `server://info`

Returns information about the shell server.

**Returns:**
- JSON object with server details

## Security Considerations

- The server only allows execution of commands specified in the `allowed_commands` list
- Commands are run with the same permissions as the server process
- Consider setting `require_auth` to true and providing an API key for production use
- Review allowed commands carefully to prevent security vulnerabilities

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built with [Model Context Protocol (MCP)](https://modelcontextprotocol.io/)
- Inspired by the need for secure AI interaction with command-line tools
