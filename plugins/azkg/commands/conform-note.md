---
description: Restructure a note to follow standard repository format
---

# Conform Note

Restructure a note to follow the standard repository format as defined in CLAUDE.md and README.md.

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

**IMPORTANT**: Transform the provided note to follow the question-oriented content synthesis approach defined in `_shared_content_synthesis.md`.

The target structure should be:

```markdown
---
tags: [domain, technology, content-type]
last_refresh: YYYY-MM-DD  # Optional, preserve if exists
source: <original_url_or_path>  # Optional, preserve if exists
---

# Note Title (Based on Central Question)

## Central Question

**Question**: [The single overarching question this note addresses]

**Executive Summary**: 2-3 paragraphs previewing key insights and how the content resolves the central question.

## Part I: [Domain Question 1]

### [Specific Question 1.1]

**Question**: [Clear, specific question from this section]

**Answer**: [Comprehensive response including:
- Direct answer to the question
- Supporting evidence from content (specific quotes, examples, data)
- Technical details and concrete information
- Implications and connections to broader themes]

### [Specific Question 1.2]

**Question**: [Next specific question]

**Answer**: [Evidence-based response...]

## Part II: [Domain Question 2]

### [Specific Question 2.1]

**Question**: [Clear question]

**Answer**: [Comprehensive response with content evidence...]

[Continue with additional parts and sections as needed]

## Resolution: [Answer to Central Question]

Synthesize domain insights to definitively resolve the central question posed at the beginning.

## Related Concepts

### Prerequisites
- [[note]] - Why it's needed first

### Related Topics
- [[note]] - Why it connects

### Extends
- [[note]] - What this builds upon

### Extended By
- [[note]] - What builds upon this

### Examples
- [[note]] - Concrete implementation

### Alternatives
- [[note]] - Different approach

## References

[1] <https://example.com>
[2] <https://example.com>
```

## Steps

### 1. Read and Analyze

- Read the specified note file
- Identify existing sections and their purpose
- Analyze the content to identify:
  - The central question the note addresses
  - Domain areas and their questions
  - Specific questions within each section
- Preserve all valuable content

### 2. Fix YAML Frontmatter

- Ensure proper YAML format with `tags: [tag1, tag2, tag3]`
- Preserve `last_refresh` if it exists
- Ensure tags follow conventions: lowercase with hyphens

### 3. Restructure Title and Central Question

- Ensure single H1 title (update to reflect central question if needed)
- Add "## Central Question" section immediately after title
- Identify and state the single overarching question the note addresses
- Create executive summary (2-3 paragraphs) previewing key insights

### 4. Transform Main Content to Question-Answer Format

**Apply question-oriented synthesis** (from `_shared_content_synthesis.md`):

- Organize existing content into Part I, Part II, etc. (domain questions)
- Within each part, create subsections with specific questions
- For each subsection:
  - **Question**: State the specific question clearly
  - **Answer**: Provide comprehensive response with evidence from content
- Preserve all substantive content, reorganized into Q&A format
- Maintain technical details, examples, and concrete information
- Add "## Resolution" section that synthesizes insights to answer central question

### 5. Fix References Section

- Change "Citations:" to "## References"
- Remove any "---" separator lines between content and references
- Remove attribution lines like "Answer from Perplexity: pplx.ai/share"
- Keep all citation links properly formatted
- Ensure References section comes AFTER Related Concepts

### 6. Preserve Related Concepts

- The "## Related Concepts" section contains typed relationships - be careful when editing
- This section IS the knowledge graph - relationships live directly in markdown files
- Ensure it appears before References section
- When conforming structure, preserve all existing relationships exactly as they are

### 7. Final Structure Check

The final order should be:

1. YAML frontmatter
2. Title (H1)
3. ## Central Question (H2) with executive summary
4. ## Part I, Part II, etc. (H2) - Domain questions with Q&A subsections
5. ## Resolution (H2) - Answer to central question
6. ## Related Concepts (H2) - preserve existing relationships
7. ## References (H2)

## Execution

1. Use Read tool to load the note
2. Use Edit tool to make surgical changes OR Write tool if complete restructure needed
3. Preserve all wikilinks in format `[[note]]` NOT `[[note.md]]`
4. Maintain all existing content - only reorganize, don't remove substance

## Important Rules

- **Preserve content**: Only reorganize, don't delete valuable information
- **Preserve Related Concepts**: Keep all existing relationships exactly as written
- **Maintain wikilinks**: Use `[[note]]` format
- **Keep citations**: Transform format but preserve all references
- **Clean formatting**: Remove extraneous separators and attribution lines
- **Consistent headings**: Use H2 (##) for major sections

## Example Transformations

**Before:**

```markdown
# Some Note

Lots of intro text...

## Content

...

Citations:
[1] https://example.com

---

Answer from Perplexity: pplx.ai/share

## Related Concepts
...
```

**After:**

```markdown
---
tags: [relevant, tags]
---

# Some Note

Brief summary extracted from intro.

## Content

...

## Related Concepts
...

## References

[1] <https://example.com>
```

Execute this transformation for the note file specified by the user.
