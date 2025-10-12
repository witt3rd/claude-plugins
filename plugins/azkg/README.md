# Agentic-ZKG Plugin

**Agent-maintained Zettelkasten Knowledge Graph for Claude Code**

🚧 **Status: In Development** - Phase 1 implementation underway

## Overview

This plugin implements the [Agentic-ZKG paradigm](https://github.com/witt3rd/donald-azkg/blob/main/agentic_zkg.md) - agent-maintained knowledge graphs with conversational interface.

## Features

### 13 Slash Commands

**Core (6):**
- `/create-note [topic]` - Research and create with auto-linking
- `/search-notes [query]` - Find notes by keyword
- `/expand-graph [note]` - Discover missing relationships
- `/learning-path [target]` - Generate prerequisite sequence
- `/graph-note [file]` - View relationships
- `/refresh-topic [file]` - Update with latest info

**Maintenance (3):**
- `/conform-note`, `/rename-note`, `/graph-validate`

**Analysis (2):**
- `/graph-stats`, `/graph-moc`

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
