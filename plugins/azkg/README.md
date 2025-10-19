# Agentic-ZKG Plugin

**Agent-maintained Zettelkasten Knowledge Graph for Claude Code**

🚧 **Status: In Development** - Phase 1 implementation underway

## Overview

This plugin implements the [Agentic-ZKG paradigm](https://github.com/witt3rd/donald-azkg/blob/main/agentic_zkg.md) - agent-maintained knowledge graphs with conversational interface.

## Features

### 19 Slash Commands

**Core Knowledge Management (6):**
- `/create-note [topic]` - Research and create with auto-linking
- `/search-notes [query]` - Find notes by keyword
- `/expand-graph [note]` - Discover missing relationships
- `/learning-path [target]` - Generate prerequisite sequence
- `/graph-note [file]` - View relationships
- `/refresh-topic [file]` - Update with latest info

**Content Ingestion (4):**
- `/process-pdf <pdf_url_or_path>` - Extract PDF content and create knowledge graph notes
- `/scrape-url <url>` - Scrape web content and create knowledge graph notes
- `/youtube-transcript <youtube_url>` - Download YouTube transcripts and create notes
- `/telegram-next-message` - Process Telegram saved messages for knowledge capture

**Maintenance (3):**
- `/conform-note` - Restructure notes to question-oriented format
- `/rename-note` - Rename notes and update wikilinks
- `/graph-validate` - Run validation checks

**Analysis (2):**
- `/graph-stats` - Display knowledge graph statistics
- `/graph-moc` - Display MOC information

**Granular Operations (2):**
- `/graph-add-relationship` - Add typed bidirectional relationships
- `/update-note` - Update note metadata

**Shared Methodology:**
- All content ingestion commands use question-oriented content synthesis
- Follows methodology in `_shared_content_synthesis.md`
- Ensures consistent note structure across all sources

### MCP Server

Exposes knowledge graph as MCP resources and tools:
- Resources: `kg://notes`, `kg://note/{file}`, `kg://relationships/{file}`
- Tools: `search_knowledge`, `find_related`, `get_learning_path`

### Architecture

**Markdown-first** - No JSON graph, markdown is source of truth:
- Wikilinks `[[note]]` → implicit relationships
- YAML frontmatter → metadata
- "Related Concepts" sections → typed relationships
- MOC files → thematic organization

## Installation

```bash
/plugin marketplace add witt3rd/claude-plugins
/plugin install azkg@witt3rd
```

## Links

- [Agentic-ZKG Paradigm](https://github.com/witt3rd/donald-azkg/blob/main/agentic_zkg.md)
- [Implementation Vision](https://github.com/witt3rd/donald-azkg/blob/main/claude_plugin_azkg.md)
- [Marketplace](https://github.com/witt3rd/claude-plugins)

## License

MIT

## Command Documentation

For complete command specifications, implementation details, and usage examples, see:

**[COMMANDS.md](./COMMANDS.md)** - Comprehensive command reference with:
- All 19 command specifications
- Tier organization (Core, Content Ingestion, Maintenance, Analysis, Granular)
- Tool usage (Read, Write, Edit, Grep, Glob, Bash)
- Rationalization and recommendations
- Future command proposals

### Quick Reference

Commands are organized by usage frequency:

**Tier 1 - Core (Daily):** create-note, search-notes, expand-graph, learning-path, graph-note, refresh-topic

**Tier 1.5 - Content Ingestion (As Needed):** process-pdf, scrape-url, youtube-transcript, telegram-next-message

**Tier 2 - Maintenance (Weekly):** conform-note, rename-note, graph-validate

**Tier 3 - Analysis (Monthly):** graph-stats, graph-moc

**Tier 4 - Granular (Rarely):** graph-add-relationship, update-note
