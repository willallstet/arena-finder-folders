import asyncio
import os
import sys
import traceback

try:
    from dotenv import load_dotenv
    
    # Load environment variables from .env file
    load_dotenv()
except ImportError:
    # dotenv is optional, continue without it
    pass

from tools.search.arena import ArenaTool, ArenaToolInput


async def main() -> None:
    
    arena_tool = ArenaTool()
    # Get access token from environment variable (loaded from .env file if dotenv is installed)
    access_token = os.getenv("ARENA_ACCESS_TOKEN")
    if not access_token:
        print("Error: ARENA_ACCESS_TOKEN environment variable not set.", file=sys.stderr)
        print("Get an access token from https://dev.are.na/oauth/applications", file=sys.stderr)
        sys.exit(1)
    tool_input = ArenaToolInput(user_id="will-allstetter", access_token=access_token)
    result = await arena_tool.run(tool_input)
    # Print all block titles
    for block in result.results:
        print(f"Title: {block.title}")
        print(f"Description: {block.description}")
        print(f"URL: {block.url}")
        print("---")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

