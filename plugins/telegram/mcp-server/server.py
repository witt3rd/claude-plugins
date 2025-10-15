#!/usr/bin/env python3
"""Telegram MCP Server - Access Telegram conversations via Model Context Protocol."""

import asyncio
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from fastmcp import FastMCP
from loguru import logger
from telethon import TelegramClient

from telegram_core import (
    get_credentials,
    get_messages_since,
    list_all_dialogs,
    search_dialog,
)

# Load environment variables
load_dotenv()

# Configure logger
logger.add(
    Path.home() / ".cache" / "telegram-mcp-server.log",
    rotation="10 MB",
    retention="7 days",
    level="INFO",
)

# Initialize FastMCP server
mcp = FastMCP("Telegram Reader")

# Global Telegram client (initialized on first use)
_client: TelegramClient | None = None
_client_lock = asyncio.Lock()


async def get_client() -> TelegramClient:
    """Get or create authenticated Telegram client.

    Returns
    -------
    TelegramClient
        Authenticated Telegram client instance.

    Raises
    ------
    ValueError
        If credentials are not configured.
    """
    global _client

    async with _client_lock:
        if _client is None or not _client.is_connected():
            api_id, api_hash = get_credentials()

            # Use session file in user's cache directory
            session_path = Path.home() / ".cache" / "telegram_mcp_session"

            _client = TelegramClient(str(session_path), api_id, api_hash)

            # Start client (will use existing session if available)
            await _client.start()
            logger.info("Telegram client connected")

    return _client


@mcp.tool()
async def list_conversations() -> str:
    """List all Telegram conversations accessible to the authenticated user.

    Includes private chats, groups, channels, and Saved Messages.

    Returns
    -------
    str
        Formatted list of all conversations with ID, type, username, and name.

    Examples
    --------
    User: "Show me all my Telegram conversations"
    Assistant calls: list_conversations()
    """
    client = await get_client()
    dialogs = await list_all_dialogs(client)

    if not dialogs:
        return "No conversations found."

    # Format as readable text
    lines = ["All your Telegram conversations:", "=" * 100]
    lines.append(f"{'ID':<15} | {'Type':<15} | {'Username':<20} | {'Name'}")
    lines.append("-" * 100)

    for dialog in dialogs:
        username = f"@{dialog['username']}" if dialog["username"] else "(no username)"
        lines.append(
            f"{dialog['id']:<15} | {dialog['type']:<15} | {username:<20} | {dialog['name']}"
        )

    lines.append("-" * 100)
    lines.append(f"\nTotal: {len(dialogs)} conversations")

    return "\n".join(lines)


@mcp.tool()
async def read_messages(
    dialog_id: int,
    since_date: str,
    limit: int = 50,
) -> str:
    """Read messages from a Telegram conversation since a specified date.

    Parameters
    ----------
    dialog_id : int
        The dialog ID from list_conversations().
    since_date : str
        ISO format date/time (e.g., "2025-10-01" or "2025-10-01T14:30:00").
    limit : int, optional
        Maximum number of messages to retrieve (default: 50, max: 200).

    Returns
    -------
    str
        Formatted list of messages with ID, date, sender, and content.

    Examples
    --------
    User: "Show me messages from my Saved Messages since October 1st"
    Assistant: First calls list_conversations() to find Saved Messages ID
    Then calls: read_messages(dialog_id=264837327, since_date="2025-10-01")

    User: "What did John say yesterday?"
    Assistant: Finds John's chat ID, then reads messages since yesterday
    """
    # Validate and parse date
    try:
        since_datetime = datetime.fromisoformat(since_date)
    except ValueError as e:
        return f"Error: Invalid date format '{since_date}'. Use ISO format like '2025-10-01' or '2025-10-01T14:30:00'"

    # Cap limit to reasonable maximum
    limit = min(limit, 200)

    client = await get_client()
    messages = await get_messages_since(client, dialog_id, since_datetime, limit)

    if not messages:
        return f"No messages found in dialog {dialog_id} since {since_date}"

    # Format messages as readable text
    lines = [f"Messages from dialog {dialog_id} since {since_date}:", "=" * 100]

    for msg in messages:
        lines.append(f"\nMessage ID: {msg['id']}")
        lines.append(f"Date: {msg['date']}")
        lines.append(f"Sender: {msg['sender']}")
        lines.append(f"Content:\n{msg['text']}")
        lines.append("-" * 100)

    lines.append(f"\nTotal: {len(messages)} messages")

    return "\n".join(lines)


@mcp.tool()
async def search_messages(
    dialog_id: int,
    query: str,
    limit: int = 50,
) -> str:
    """Search for messages in a Telegram conversation matching a query.

    Parameters
    ----------
    dialog_id : int
        The dialog ID from list_conversations().
    query : str
        Search query string to match in messages.
    limit : int, optional
        Maximum number of messages to retrieve (default: 50, max: 200).

    Returns
    -------
    str
        Formatted list of matching messages with ID, date, sender, and content.

    Examples
    --------
    User: "Search my Saved Messages for Python code"
    Assistant: First calls list_conversations() to find Saved Messages ID
    Then calls: search_messages(dialog_id=264837327, query="Python")

    User: "Find messages from Alice mentioning the meeting"
    Assistant: Finds Alice's chat ID, then searches for "meeting"
    """
    # Cap limit to reasonable maximum
    limit = min(limit, 200)

    client = await get_client()
    messages = await search_dialog(client, dialog_id, query, limit)

    if not messages:
        return f"No messages found in dialog {dialog_id} matching '{query}'"

    # Format messages as readable text
    lines = [f"Messages in dialog {dialog_id} matching '{query}':", "=" * 100]

    for msg in messages:
        lines.append(f"\nMessage ID: {msg['id']}")
        lines.append(f"Date: {msg['date']}")
        lines.append(f"Sender: {msg['sender']}")
        lines.append(f"Content:\n{msg['text']}")
        lines.append("-" * 100)

    lines.append(f"\nTotal: {len(messages)} messages")

    return "\n".join(lines)


@mcp.tool()
async def get_saved_messages_id() -> str:
    """Get the dialog ID for your Saved Messages.

    Convenience function to quickly find your Saved Messages chat.

    Returns
    -------
    str
        The dialog ID for Saved Messages, or error message if not found.

    Examples
    --------
    User: "What's my Saved Messages ID?"
    Assistant calls: get_saved_messages_id()
    """
    client = await get_client()
    dialogs = await list_all_dialogs(client)

    for dialog in dialogs:
        if dialog["type"] == "Saved Messages":
            return f"Your Saved Messages ID is: {dialog['id']}"

    return "Saved Messages not found. This shouldn't happen - try list_conversations() instead."


if __name__ == "__main__":
    # Run the MCP server
    mcp.run()
