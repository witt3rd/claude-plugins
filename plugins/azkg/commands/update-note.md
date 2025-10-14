---
description: Update a note's metadata (title, tags, or summary)
---

# Update Note

Update a note's metadata (title, tags, or summary) in the YAML frontmatter.

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

## Input

User provides filename and fields to update:

- `/update-note agents.md --title "AI Agents: Autonomous Intelligence Systems"`
- `/update-note agents.md --tags "ai,agents,llm,autonomous"`
- `/update-note agents.md --summary "Brief new summary"`

Can update multiple fields in one command:

- `/update-note agents.md --title "New Title" --tags "new,tags"`

## Execution Steps

### 1. Normalize Filename

Ensure filename has `.md` extension.

### 2. Verify Note Exists

Use Glob to check note exists:

```bash
Glob "agents.md"
```

### 3. Read Current Note

Use Read tool to get full note content, including current YAML frontmatter.

### 4. Update YAML Frontmatter

Use Edit tool to update the specific fields:

**For title update:**

- No YAML field for title (title is the first `#` heading)
- Update the first `# Heading` line after YAML frontmatter

**For tags update:**

```yaml
---
tags: [old, tags]
---
```

becomes:

```yaml
---
tags: [new, tags, here]
---
```

**For summary update:**

- Summary is the first paragraph after title (not in YAML)
- Replace first paragraph after title heading

### 5. Report Changes

Show old vs new values for updated fields.

## Output Format

```
Updated Note: agents.md
============================================================

Title:
  Old: AI Agents
  New: AI Agents: Autonomous Intelligence Systems

Tags:
  Old: [agents, ai, llm]
  New: [ai, agents, llm, autonomous, architecture]

Summary:
  Old: AI agents are autonomous systems...
  New: AI agents are autonomous, goal-directed systems...

============================================================
✅ Metadata Updated!
============================================================

💡 Next steps:
• Review the updated note at agents.md
• Ensure title matches filename semantically
• Verify tags span multiple dimensions (see tag_system.md)
• Consider if related notes need similar updates
```

## Validation

Before updating:

- Note must exist
- At least one field (title, tags, or summary) must be specified

After updating:

- YAML frontmatter remains well-formed
- Tags follow naming convention (lowercase-with-hyphens)
- Title and summary are non-empty

## Tag Guidelines

When updating tags, follow best practices:

- **3-6 tags** per note (enough for discovery, not too many)
- **Mix dimensions**: technology + domain + content type
- **Lowercase with hyphens**: `first-principles` not `FirstPrinciples`
- **Specific over generic**: `mcp` better than `protocol`

See `tag_system.md` for complete tag catalog.

## Use Cases

- **Clarify title**: Make note title more specific or descriptive
- **Add tags**: Add missing tags to improve discoverability
- **Refine summary**: Update summary to better reflect current content
- **Standardize**: Ensure tags follow consistent naming conventions
- **Tag migration**: Update tags when tag system evolves

## Tools Used

- **Glob** - Verify note exists
- **Read** - Get current note content
- **Edit** - Update YAML frontmatter and note content
- **Parse logic** - Extract and modify YAML fields

## Important Notes

- Changes affect only metadata, not main content
- "Related Concepts" section is never modified by this command
- Title should semantically match filename (e.g., `agents.md` → "AI Agents")
- Tags should be comma-separated when provided
- Use `/conform-note` for structural changes beyond metadata
