# Telegram Reader Plugin

Access your Telegram conversations, channels, and Saved Messages via natural language queries through Claude Code.

## Features

- **List all conversations**: View private chats, groups, channels, and Saved Messages
- **Read messages by date**: Get messages since a specific date/time
- **Search messages**: Find messages matching specific queries
- **MCP + CLI**: Available as both MCP server (for Claude) and CLI tool

## Setup

**IMPORTANT**: The plugin comes pre-configured with APP_ID and APP_HASH. You only need to authenticate via CLI once to create the session file.

### 1. Authenticate via CLI (One-Time Setup)

The CLI tool handles interactive Telegram authentication and creates the session file at `~/.cache/telegram_mcp_session.session` - shared by both CLI and MCP server.

```bash
# Navigate to CLI directory (relative to plugin install location)
cd cli

# Install dependencies
uv sync

# Run any CLI command to trigger authentication
uv run telegram-reader list-dialogs
```

You'll be prompted for:
- **Phone number**: Enter with country code (e.g., `+1234567890`)
- **Verification code**: Check your Telegram app for the code
- **2FA password** (if enabled): Your Telegram cloud password (Settings > Privacy > Two-Step Verification)

This creates `~/.cache/telegram_mcp_session.session` which is automatically shared with the MCP server.

### 2. Done!

The MCP server is automatically configured when you install the plugin. Just **restart Claude Code** to load the MCP server.

No additional configuration needed - the plugin includes `.mcp.json` with APP_ID and APP_HASH pre-configured, and both CLI and MCP server share the same session file.

### Security Notes

- **APP_ID and APP_HASH**: These are application identifiers (like Telegram Desktop's app ID), not user credentials. They're safe to include in the plugin and shared by all users.
- **Session file**: Contains YOUR authentication tokens - treat like a password. Never commit or share this file.
- **Session location**: MCP server looks for session in `~/.cache/telegram_mcp_session.session`
- **Session expiry**: If session expires, re-authenticate via CLI and copy session file again

## Usage

### Via Claude Code (MCP Server)

Once configured, you can use natural language with Claude:

```
You: "Show me all my Telegram conversations"
Claude: [calls list_conversations()]

You: "What messages did I save yesterday?"
Claude: [finds Saved Messages ID, calls read_messages()]

You: "Search my Saved Messages for Python code examples"
Claude: [calls search_messages()]
```

**Available MCP Tools**:
- `list_conversations()` - List all chats, groups, channels
- `read_messages(dialog_id, since_date, limit)` - Read messages since date
- `search_messages(dialog_id, query, limit)` - Search for specific content
- `get_saved_messages_id()` - Quick access to Saved Messages ID

### Via CLI

The CLI provides direct command-line access:

#### List all conversations:

```bash
cd cli
uv run telegram-reader list-dialogs
```

Output:
```
ID              | Type            | Username             | Name
--------------------------------------------------------------------------------
264837327       | Saved Messages  | (no username)        | Saved Messages
-1001234567890  | Channel         | @mychannel           | My Channel Name
123456789       | Private Chat    | @username            | John Doe
```

#### Read messages since date:

```bash
# Using dialog ID
uv run telegram-reader read-message 264837327 --since 2025-10-01

# Using username
uv run telegram-reader read-message @mychannel --since "2025-10-01T14:30:00"
```

#### CLI Commands:

```bash
telegram-reader list-dialogs [--phone PHONE]
  List all conversations

telegram-reader read-message DIALOG [--since DATE] [--phone PHONE]
  Read messages from dialog since date

  DIALOG: Dialog ID or @username
  --since: ISO date (2025-10-01 or 2025-10-01T14:30:00)
```

## Architecture

```
plugins/telegram/
├── .claude-plugin/
│   └── plugin.json          # Plugin manifest
├── mcp-config.json          # MCP server configuration
├── mcp-server/              # MCP server (for Claude)
│   ├── server.py            # FastMCP implementation
│   ├── telegram_core.py     # Shared Telegram logic
│   ├── pyproject.toml       # Dependencies
│   └── .env                 # Credentials (copied from cli/.env)
├── cli/                     # CLI tool (standalone)
│   ├── src/telegram_reader/
│   │   └── cli.py           # Click-based CLI
│   ├── pyproject.toml       # Dependencies
│   ├── .env                 # Credentials (created from .env.example)
│   └── telegram_session.session  # Auth session (created on first run)
├── .env.example             # Credential template
└── README.md                # This file
```

**Design principles**:
- Shared logic in `telegram_core.py` (reusable)
- MCP server uses FastMCP for Claude integration
- CLI uses Click for user-friendly commands
- Telethon for MTProto access (full Telegram API)

**Credentials**:
- APP_ID and APP_HASH are embedded in both `mcp-server/.env` and `.mcp.json`
- No user configuration needed - works out of the box
- Session file is shared via `~/.cache/` location

## Telegram Concepts

- **Dialog**: Any conversation (private chat, group, channel, or Saved Messages)
- **Dialog ID**: Unique numeric identifier for each dialog
- **Saved Messages**: Your personal note-taking space (dialog with yourself)
- **Channel**: Broadcast-only communication (one-way)
- **Group**: Multi-user chat (two-way)
- **Private Chat**: One-on-one conversation

**Finding dialog IDs**: Use `list-dialogs` or `list_conversations()` to see all IDs.

## Telethon vs Bot API

This plugin uses **Telethon** (MTProto client) instead of Bot API because:

- ✅ Access to ALL your conversations (not just bot chats)
- ✅ Read Saved Messages (personal notes)
- ✅ Access to channels you follow
- ✅ Full message search and history
- ❌ Requires YOUR credentials (not a bot token)
- ❌ Needs authentication on first run

For bot-based applications, consider `python-telegram-bot` instead.

## Troubleshooting

### Authentication Issues

**Problem**: "SendCodeUnavailableError" or verification issues
- **Solution**: Restart authentication via CLI, make sure you're entering phone with country code (+1234567890)

**Problem**: "Password is required" (2FA)
- **Solution**: Enter your Telegram cloud password (Settings > Privacy > Two-Step Verification)

**Problem**: MCP server hangs on first call
- **Solution**: Session file not found. Re-authenticate via CLI and copy `cli/telegram_session.session` to `~/.cache/telegram_mcp_session.session`

### Session Issues

**Problem**: Repeated authentication requests from MCP server
- **Solution**: Check `~/.cache/telegram_mcp_session.session` exists and has correct permissions

**Problem**: "Session expired"
- **Solution**: Delete session file, re-authenticate via CLI, copy to `~/.cache/` again

### Message Access

**Problem**: "No messages found"
- **Solution**: Check dialog ID is correct (use `list-dialogs`), verify date format

**Problem**: "Could not access dialog"
- **Solution**: Ensure you have access to that conversation (not blocked/left)

## Setup Helper (Future Enhancement)

A CLI command could automate MCP setup:

```bash
# Future command (not yet implemented)
uv run telegram-reader setup-mcp
# Would: copy .env, copy session file, show .mcp.json config
```

## References

- [Telethon Documentation](https://docs.telethon.dev/)
- [Telegram API](https://core.telegram.org/api)
- [FastMCP Documentation](https://github.com/jlowin/fastmcp)
- [My Telegram API Credentials](https://my.telegram.org/auth)

## Related Knowledge Base Notes

- `[[telegram_bot_python]]` - Comprehensive Telegram API and SDK guide
- `[[python_mcp_sdk]]` - Building MCP servers with FastMCP
- `[[python_coding_standards]]` - Python best practices used in this plugin
