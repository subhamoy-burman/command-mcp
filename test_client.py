import asyncio
import subprocess
import time
import sys
import os
from contextlib import AsyncExitStack

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    # Create an exit stack for resource management
    async with AsyncExitStack() as exit_stack:
        # Start the MCP shell server as a subprocess
        print("Starting MCP shell server...")
        server_process = subprocess.Popen(
            [sys.executable, "shellserver.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdin=subprocess.PIPE,
            text=True
        )
        
        # Give the server a moment to start up
        print("Waiting for server to initialize...")
        await asyncio.sleep(2)
        
        try:
            # Set up server parameters
            server_params = StdioServerParameters(
                command=sys.executable,
                args=["shellserver.py"],
                env=None
            )

            # Connect to the server using stdio transport
            print("Connecting to server...")
            stdio_transport = await exit_stack.enter_async_context(stdio_client(server_params))
            stdio, write = stdio_transport
            
            # Initialize the client session
            session = await exit_stack.enter_async_context(ClientSession(stdio, write))
            await session.initialize()
            
            # List available tools
            response = await session.list_tools()
            tools = response.tools
            print(f"\nConnected to server with tools: {[tool.name for tool in tools]}")
            
            # Test the terminal tool
            print("\nTesting terminal tool...")
            try:
                # Try running a simple command
                print("Running 'dir' command...")
                result = await session.call_tool("terminal", {"command": "dir"})
                print(f"Response: {result.content}")
                
                # Try running an invalid command
                print("\nTrying invalid command...")
                result = await session.call_tool("terminal", {"command": "invalid_command"})
                print(f"Response: {result.content}")
            except Exception as e:
                print(f"Error: {e}")
            
            # Get server info
            print("\nGetting server info...")
            try:
                info = await session.get_resource("server://info")
                print(f"Server info: {info.content}")
            except Exception as e:
                print(f"Error getting server info: {e}")
                
        finally:
            # Clean up: terminate the server process
            print("Shutting down server...")
            server_process.terminate()
            try:
                server_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                print("Server didn't terminate gracefully, forcing...")
                server_process.kill()
            
            # Get any output from the server process
            stdout, stderr = server_process.communicate()
            if stdout:
                print("\nServer stdout:")
                print(stdout)
            if stderr:
                print("\nServer stderr:")
                print(stderr)

if __name__ == "__main__":
    asyncio.run(main())
