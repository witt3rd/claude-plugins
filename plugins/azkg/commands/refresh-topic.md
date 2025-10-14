---
description: Refresh a topic page with latest information from Perplexity
---

# Refresh Topic

You are tasked with refreshing a topic page with the latest information. Follow these steps:

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

## 1. Read the Topic File

- The user will provide a filename (e.g., `agents.md` or just `agents`)
- Read the file from REPO_PATH (not current directory)
- Parse the YAML frontmatter and main content

## 2. Formulate Perplexity Query

- Analyze the topic content to understand the main subject
- Extract key concepts, technologies, or themes
- Create a focused query to find:
  - Recent developments (last 6-12 months)
  - New research or papers
  - Updated best practices
  - Emerging trends
  - Deprecated or outdated information

Example query format: "What are the latest developments, research, and best practices for [TOPIC] as of 2025? Include any significant changes, new tools, or deprecated approaches."

## 3. Query Perplexity

- Use the `mcp__perplexity-ask__perplexity_ask` tool
- Provide a clear, focused query based on the topic analysis
- Request comprehensive, up-to-date information

## 4. Incorporate Updates

- Review the Perplexity response carefully
- Identify genuinely new or updated information that should be added
- For each update:
  - Determine the appropriate section to update
  - Maintain the existing structure and format
  - Add new information without removing valuable existing content
  - Preserve all existing citations and references
  - Add new citations for updated information if provided

## 5. Update Metadata

- Add or update the YAML frontmatter with:

  ```yaml
  last_refresh: 2025-10-11  # Use today's date
  ```

- Preserve all existing YAML fields (tags, etc.)
- Maintain YAML formatting

## 6. Write Updated File

- Use the Edit tool to make surgical updates to specific sections
- OR use the Write tool if comprehensive rewrite is needed
- Ensure all formatting is preserved (markdown, wikilinks, etc.)

## 7. Summary

- Provide a brief summary of:
  - What updates were found
  - Which sections were modified
  - Any significant new information added
  - Any outdated information identified (but keep unless contradicted)

## Important Notes

- **Preserve existing content**: Only add or update, don't remove unless information is clearly outdated or contradicted
- **Maintain structure**: Keep the same section organization
- **Keep relationships**: Don't modify the "Related Concepts" section
- **Respect format**: Maintain wikilink format `[[note]]`, YAML format, etc.
- **Be conservative**: Only incorporate high-quality, verifiable updates
- **No hyperbole**: Don't add marketing language or grandiose claims

Execute these steps for the topic file provided by the user.
