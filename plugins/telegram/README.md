# Telegram Reader Plugin

Access your Telegram conversations, channels, and Saved Messages via natural language queries through Claude Code.

## Features

- **List all conversations**: View private chats, groups, channels, and Saved Messages
- **Read messages by date**: Get messages since a specific date/time
- **Search messages**: Find messages matching specific queries
- **MCP + CLI**: Available as both MCP server (for Claude) and CLI tool

## Setup

**IMPORTANT**: MCP server setup requires TWO steps - authenticate via CLI first, then configure MCP server. This is because Telegram authentication is interactive and cannot be done through MCP.

### 1. Get Telegram API Credentials

1. Visit https://my.telegram.org/auth
2. Log in with your phone number
3. Click "API development tools"
4. Create a new application (any name/description works)
5. Copy your `api_id` (numeric) and `api_hash` (alphanumeric string)

### 2. Set Up CLI First (Required for Authentication)

The CLI tool handles interactive Telegram authentication and creates the session file needed by the MCP server.

```bash
# Navigate to CLI directory (relative to plugin install location)
cd cli

# Install dependencies
uv sync

# Create .env file with your credentials
cp .env.example .env
# Edit .env and add your TELEGRAM_API_ID and TELEGRAM_API_HASH
```

Your `cli/.env` should look like:
```env
TELEGRAM_API_ID=12345678
TELEGRAM_API_HASH=abc123def456abc123def456abc123de
```

**Authenticate with Telegram:**
```bash
# Run any CLI command to trigger authentication
uv run telegram-reader list-dialogs
```

You'll be prompted for:
- **Phone number**: Enter with country code (e.g., `+1234567890`)
- **Verification code**: Check your Telegram app for the code
- **2FA password** (if enabled): Your Telegram cloud password (Settings > Privacy > Two-Step Verification)

This creates `telegram_session.session` in the CLI directory.

### 3. Set Up MCP Server

The MCP server needs both the `.env` file and the authenticated session file.

```bash
# Navigate to MCP server directory
cd ../mcp-server

# Install dependencies
uv sync

# Copy .env from CLI (both need credentials)
cp ../cli/.env .env

# Copy authenticated session to Claude Code cache location
# Windows/Git Bash:
mkdir -p ~/.cache 2>/dev/null || true
cp ../cli/telegram_session.session ~/.cache/telegram_mcp_session.session

# Linux/macOS:
mkdir -p ~/.cache
cp ../cli/telegram_session.session ~/.cache/telegram_mcp_session.session
```

### 4. Configure Claude Code

Add the MCP server to your project's `.mcp.json`:

```json
{
  "mcpServers": {
    "telegram": {
      "command": "uv",
      "args": [
        "--directory",
        "<ABSOLUTE_PATH_TO_PLUGIN>/mcp-server",
        "run",
        "server.py"
      ],
      "env": {}
    }
  }
}
```

Replace `<ABSOLUTE_PATH_TO_PLUGIN>` with the full path to the telegram plugin directory (e.g., `C:/Users/username/path/to/plugins/telegram`).

**Restart Claude Code** to load the MCP server.

### Security Notes

- **Credentials**: Your API ID and hash are YOUR personal credentials (not bot tokens)
- **Session file**: Contains authentication tokens - treat like a password
- **Never commit**: Add `.env` and `*.session` to `.gitignore`
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

**Why two .env files?**
- CLI and MCP server run in different directories
- Each needs its own copy of credentials
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

**Problem**: "No phone number or bot token provided"
- **Solution**: Check `.env` file exists in both `cli/` and `mcp-server/` directories

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
