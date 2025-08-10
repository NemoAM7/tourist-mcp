import asyncio
from fastmcp import FastMCP
import config
from auth import SimpleBearerAuthProvider
from mcp_logic.tools import register_tools

mcp = FastMCP(
    "WhatsApp Local Guide MCP Server",
    auth=SimpleBearerAuthProvider(config.AUTH_TOKEN),
)

register_tools(mcp)

async def main():
    """Starts the MCP server."""
    print("Starting WhatsApp Local Guide MCP server on http://0.0.0.0:8088")
    await mcp.run_async("streamable-http", host="0.0.0.0", port=8088)

if __name__ == "__main__":
    asyncio.run(main())