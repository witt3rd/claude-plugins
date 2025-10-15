"""Core Telegram API functionality shared between CLI and MCP server."""

import os
from datetime import datetime
from pathlib import Path
from typing import Optional

from loguru import logger
from telethon import TelegramClient
from telethon.tl.types import Channel, User


def get_credentials() -> tuple[int, str]:
    """Get Telegram API credentials from environment variables.

    Returns
    -------
    tuple[int, str]
        API ID and API hash.

    Raises
    ------
    ValueError
        If required environment variables are not set.
    """
    api_id_str = os.getenv("TELEGRAM_API_ID")
    api_hash = os.getenv("TELEGRAM_API_HASH")

    if not api_id_str or not api_hash:
        raise ValueError(
            "TELEGRAM_API_ID and TELEGRAM_API_HASH must be set in environment.\n"
            "Get these from https://my.telegram.org/auth"
        )

    try:
        api_id = int(api_id_str)
    except ValueError as e:
        raise ValueError(f"TELEGRAM_API_ID must be a number: {api_id_str}") from e

    return api_id, api_hash


async def list_all_dialogs(client: TelegramClient) -> list[dict[str, str | int]]:
    """List all dialogs (conversations) accessible to the authenticated user.

    Includes private chats, groups, channels, and Saved Messages.

    Parameters
    ----------
    client : TelegramClient
        Authenticated Telegram client.

    Returns
    -------
    list[dict[str, str | int]]
        List of dialog information dictionaries with keys:
        - id: Dialog ID
        - name: Dialog name
        - type: Dialog type (Saved Messages, Private Chat, Group, Channel)
        - username: Username if available
    """
    dialogs = []
    me = await client.get_me()

    logger.info("Fetching all conversations...")

    async for dialog in client.iter_dialogs():
        entity = dialog.entity

        # Determine dialog type
        if isinstance(entity, User):
            if entity.id == me.id:
                dialog_type = "Saved Messages"
            else:
                dialog_type = "Private Chat"
        elif isinstance(entity, Channel):
            if hasattr(entity, 'megagroup') and entity.megagroup:
                dialog_type = "Group"
            elif hasattr(entity, 'broadcast') and entity.broadcast:
                dialog_type = "Channel"
            else:
                dialog_type = "Chat"
        else:
            dialog_type = "Chat"

        dialog_info = {
            "id": dialog.id,
            "name": dialog.name,
            "type": dialog_type,
            "username": entity.username if hasattr(entity, 'username') and entity.username else None,
        }
        dialogs.append(dialog_info)
        logger.debug(f"Found {dialog_type}: {dialog_info}")

    logger.info(f"Found {len(dialogs)} conversations")
    return dialogs


async def get_messages_since(
    client: TelegramClient,
    dialog_identifier: str | int,
    since_date: datetime,
    limit: int = 100,
) -> list[dict[str, str | datetime | int]]:
    """Get messages from dialog since specified date.

    Parameters
    ----------
    client : TelegramClient
        Authenticated Telegram client.
    dialog_identifier : str | int
        Dialog username (e.g., '@channelname') or dialog ID.
    since_date : datetime
        Retrieve messages after this date/time.
    limit : int, optional
        Maximum number of messages to retrieve (default: 100).

    Returns
    -------
    list[dict[str, str | datetime | int]]
        List of message information dictionaries with keys:
        - id: Message ID
        - date: Message timestamp
        - text: Message content
        - sender: Sender ID
        Returns empty list if no messages found.

    Raises
    ------
    ValueError
        If dialog not found or not accessible.
    """
    logger.info(
        f"Searching for messages in {dialog_identifier} since {since_date} (limit: {limit})"
    )

    messages = []
    try:
        async for message in client.iter_messages(
            dialog_identifier,
            offset_date=since_date,
            limit=limit,
            reverse=True,  # Get oldest first (closest to since_date)
        ):
            message_info = {
                "id": message.id,
                "date": message.date,
                "text": message.text or "(no text content)",
                "sender": message.sender_id,
            }
            messages.append(message_info)

        logger.info(f"Found {len(messages)} messages since {since_date}")
        return messages

    except ValueError as e:
        raise ValueError(
            f"Could not access dialog '{dialog_identifier}'. "
            "Check that it exists and you have access to it."
        ) from e


async def search_dialog(
    client: TelegramClient,
    dialog_identifier: str | int,
    query: str,
    limit: int = 100,
) -> list[dict[str, str | datetime | int]]:
    """Search for messages in a dialog matching query.

    Parameters
    ----------
    client : TelegramClient
        Authenticated Telegram client.
    dialog_identifier : str | int
        Dialog username (e.g., '@channelname') or dialog ID.
    query : str
        Search query string.
    limit : int, optional
        Maximum number of messages to retrieve (default: 100).

    Returns
    -------
    list[dict[str, str | datetime | int]]
        List of matching message information dictionaries with keys:
        - id: Message ID
        - date: Message timestamp
        - text: Message content
        - sender: Sender ID
        Returns empty list if no matches found.

    Raises
    ------
    ValueError
        If dialog not found or not accessible.
    """
    logger.info(f"Searching for '{query}' in {dialog_identifier} (limit: {limit})")

    messages = []
    try:
        async for message in client.iter_messages(
            dialog_identifier,
            search=query,
            limit=limit,
        ):
            message_info = {
                "id": message.id,
                "date": message.date,
                "text": message.text or "(no text content)",
                "sender": message.sender_id,
            }
            messages.append(message_info)

        logger.info(f"Found {len(messages)} messages matching '{query}'")
        return messages

    except ValueError as e:
        raise ValueError(
            f"Could not access dialog '{dialog_identifier}'. "
            "Check that it exists and you have access to it."
        ) from e
