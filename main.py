#!/usr/bin/env python3
"""
Main entry point for the Luma API MCP server.
This can be run directly or through the MCP CLI.
"""

import asyncio
import os
import sys
from server import mcp


def main():
    """Start the MCP server using the standard MCP CLI runner."""
    # The mcp.run() method handles the asyncio event loop
    # and stdio transport automatically when run through MCP CLI
    mcp.run()


if __name__ == "__main__":
    # Check if LUMA_API_KEY is set
    if not os.environ.get('LUMA_API_KEY'):
        print("Warning: LUMA_API_KEY environment variable is not set!", file=sys.stderr)
        print("Set it with: export LUMA_API_KEY='your-api-key'", file=sys.stderr)
    
    main()