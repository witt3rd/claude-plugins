---
description: Display information about a Map of Content (MOC) file
---

# Graph MOC (Map of Content)

Display information about a specific MOC (Map of Content) file, which serves as a thematic navigation hub.

## 0. Locate AZKG Repository

**Check for AZKG_REPO_PATH environment variable:**

- Use bash conditional: `if [ -z "$AZKG_REPO_PATH" ]; then REPO_PATH=$(pwd); else REPO_PATH="$AZKG_REPO_PATH"; fi`
- **If AZKG_REPO_PATH is set:** Use that path as the repository root
- **If AZKG_REPO_PATH is not set:** Use current working directory (pwd)
- Store result as REPO_PATH for all subsequent file operations

**All file operations must use REPO_PATH:**

- Read: `Read(REPO_PATH/filename.md)` or `Read("$REPO_PATH/filename.md")`
- Write: `Write(REPO_PATH/filename.md)` or `Write("$REPO_PATH/filename.md")`
- Edit: `Edit(REPO_PATH/filename.md)` or `Edit("$REPO_PATH/filename.md")`
- Grep: `Grep(pattern, path=REPO_PATH)` or with explicit path
- Glob: `Glob(pattern, path=REPO_PATH)` or with explicit path

**Example usage:**

```
# Check environment variable
if [ -z "$AZKG_REPO_PATH" ]; then
  REPO_PATH=$(pwd)
else
  REPO_PATH="$AZKG_REPO_PATH"
fi

# Then use REPO_PATH for all operations
Read("$REPO_PATH/agents.md")
```

**Concrete examples:**

- If AZKG_REPO_PATH="/c/Users/dothompson/OneDrive/src/witt3rd/donald-azkg"
  → Read("/c/Users/dothompson/OneDrive/src/witt3rd/donald-azkg/agents.md")
- If AZKG_REPO_PATH is not set and pwd is /c/Users/dothompson/OneDrive/src/witt3rd/donald-azkg
  → Read("agents.md") or use full path from pwd

## Task

Show:

- MOC name and theme
- Total notes linked in this MOC
- List of all notes with their brief descriptions
- Section organization within the MOC

## Input

User provides the MOC name (e.g., "agents", "mcp", "python", "rust")

Common MOCs:

- agents_moc.md - AI agents and agentic systems
- mcp_moc.md - Model Context Protocol
- python_moc.md - Python development
- rust_moc.md - Rust programming
- typescript_moc.md - TypeScript and React
- windows_moc.md - Windows development
- writing_moc.md - Writing and communication
- csharp_moc.md - C# development

## Execution Steps

### 1. Normalize MOC Name

Ensure filename has `_moc.md` suffix:

- Input: "agents" → "agents_moc.md"
- Input: "agents_moc" → "agents_moc.md"
- Input: "agents_moc.md" → "agents_moc.md"

### 2. Verify MOC Exists

Use Glob to check if MOC file exists:

```bash
Glob "agents_moc.md"
```

If not found, list available MOCs and suggest closest match.

### 3. Read MOC Content

Use Read tool to get full MOC content.

### 4. Parse MOC Structure

Extract:

- **Title** (H1 heading)
- **Sections** (H2 headings)
- **Wikilinks** in each section
- **Brief descriptions** next to each wikilink

Example MOC structure:

```markdown
# Agents - Map of Content

## Core Concepts
- [[agents]] - AI agents powered by LLMs
- [[semantic_routing]] - Intelligent model selection

## Coding Assistants
- [[claude_code]] - Agentic AI coding assistant
- [[claude_code_agents]] - Subagent system
```

### 5. Count Notes

Count total wikilinks across all sections.

## Output Format

```
MOC: agents_moc.md
============================================================

Theme: AI agents and agentic systems
Total notes: 15

## Sections and Notes:

### Core Concepts (5 notes)
- [[agents]] - AI agents powered by LLMs for autonomous action
- [[semantic_routing]] - Intelligent model selection based on query
- [[react_agent_pattern]] - Design pattern for agent UIs
- [[llm_self_talk_optimization]] - Token-efficient agent communication
- [[agentic_development_context]] - Comprehensive development ecosystems

### Coding Assistants (5 notes)
- [[claude_code]] - Anthropic's agentic AI coding assistant
- [[claude_code_agents]] - Subagent system for parallel tasks
- [[claude_code_plugins]] - Extensibility via slash commands
- [[claude_code_hooks]] - Lifecycle event system
- [[zettelkasten_claude_plugin]] - Knowledge graph plugin

### Integration & APIs (2 notes)
- [[agent_mcp_apis]] - MCP APIs for agent tool integration
- [[adding_mcp_to_claude_code]] - Adding custom agents

### Related Topics (3 notes)
- [[mcp_overview]] - Protocol for agent tool integration
- [[react_framework]] - UI framework for agents

============================================================

💡 Next steps:
• Use `/graph-note [filename]` to explore any note in this MOC
• Use `/create-note` to add new notes to this domain
• Use `/search-notes #agents` to find all agent-tagged notes
```

## Use Cases

- **Explore a domain**: See all notes in a specific theme
- **Find related notes**: Discover notes you didn't know existed
- **Assess coverage**: Check if a topic area is well-covered
- **Navigate efficiently**: Jump to specific concepts in a domain
- **Plan additions**: Identify gaps where new notes are needed

## Tools Used

- **Glob** - Verify MOC file exists, list all MOCs
- **Read** - Get full MOC content
- **Parse logic** - Extract sections, wikilinks, descriptions

## Present Results

After displaying MOC information:

- Assess coverage (comprehensive vs sparse)
- Comment on organization (clear sections vs needs structure)
- Suggest if MOC is getting too large (might need splitting)
- Identify potential notes to add based on theme
- Note any wikilinks that point to non-existent notes

## If MOC Not Found

```
MOC not found: unknown_moc.md

Available MOCs:
- agents_moc.md - AI agents and agentic systems
- mcp_moc.md - Model Context Protocol
- python_moc.md - Python development
- rust_moc.md - Rust programming
- typescript_moc.md - TypeScript and React
- windows_moc.md - Windows development
- writing_moc.md - Writing and communication
- csharp_moc.md - C# development

Did you mean one of these?
```
