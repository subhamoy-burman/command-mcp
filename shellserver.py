"""
MCP Shell Server - Exposes a terminal tool for running commands
"""
import subprocess
import asyncio
import logging
from typing import Optional
from mcp.server.fastmcp import FastMCP, Context
import toml
import os
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("shellserver")

# Create an MCP server with the name "ShellServer"
mcp = FastMCP("ShellServer")

# Load configuration if available
config_path = "config.toml"
config = {}
if os.path.exists(config_path):
    try:
        config = toml.load(config_path)
    except Exception as e:
        print(f"Error loading config: {e}")

# Define allowed commands or use config
ALLOWED_COMMANDS = config.get("allowed_commands", ["dir", "ls", "echo", "pwd", "whoami", "python", "pip"])
MAX_OUTPUT_LENGTH = config.get("max_output_length", 4096)
TIMEOUT = config.get("timeout", 30)  # Timeout in seconds

@mcp.tool()
async def terminal(command: str, ctx: Context) -> str:
    """
    Run a command in the terminal and return the output.
    
    Args:
        command: The command to run
        
    Returns:
        The command output as a string
    """
    # Basic security check: only allow specific commands or command prefixes
    command_parts = command.strip().split()
    if not command_parts:
        return "No command specified"
        
    base_command = command_parts[0].lower()
    
    # Check if command is allowed
    if not any(base_command.startswith(allowed) for allowed in ALLOWED_COMMANDS):
        return f"Command '{base_command}' is not allowed. Allowed commands: {', '.join(ALLOWED_COMMANDS)}"
      # Log the command
    logger.info(f"Running command: {command}")
    ctx.info(f"Running command: {command}")
    
    try:
        # Run the command with a timeout
        process = await asyncio.create_subprocess_shell(
            command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        try:
            stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=TIMEOUT)
        except asyncio.TimeoutError:
            process.kill()
            await process.wait()
            return f"Command timed out after {TIMEOUT} seconds"
        
        # Decode and combine output
        stdout_str = stdout.decode('utf-8', errors='replace')
        stderr_str = stderr.decode('utf-8', errors='replace')
        
        combined_output = stdout_str
        if stderr_str:
            combined_output += f"\nErrors:\n{stderr_str}"
        
        # Truncate output if necessary
        if len(combined_output) > MAX_OUTPUT_LENGTH:
            truncated_output = combined_output[:MAX_OUTPUT_LENGTH]
            return f"{truncated_output}\n... Output truncated (total length: {len(combined_output)} characters)"
        
        return combined_output
    except Exception as e:
        return f"Error executing command: {str(e)}"

# Add server information resource
@mcp.resource("server://info")
def server_info() -> str:
    """Get information about the shell server"""
    return {
        "name": "MCP Shell Server",
        "version": "1.0.0",
        "description": "A server that allows running terminal commands through MCP",
        "allowed_commands": ALLOWED_COMMANDS,
        "max_output_length": MAX_OUTPUT_LENGTH,
        "timeout": TIMEOUT,
    }

if __name__ == "__main__":
    # Run the server
    mcp.run()