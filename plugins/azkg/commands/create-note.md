---
description: Create a new atomic note in the Zettelkasten knowledge graph
---

# Create Note

You are tasked with creating a new atomic note in the Zettelkasten knowledge graph. Follow these steps systematically:

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

## 1. Parse Input and Check for Duplicates

**Input format:** User provides either:

- A topic name: `/create-note semantic_routing`
- A descriptive phrase: `/create-note "Rust async runtime comparison"`

**Duplicate detection:**

- Search existing notes using Glob for similar filenames
- Search content using Grep for similar concepts
- If potential duplicate found, ask user:
  - "Found existing note `similar_note.md`. Would you like to:
    - Expand/refresh that note instead?
    - Create a new distinct note (explain the difference)?
    - Cancel?"

## 2. Generate Filename

**Naming convention:**

- `topic_specific_concept.md` - lowercase with underscores
- Descriptive, not generic: `python_mcp_sdk.md` NOT `sdk.md`
- No folder prefixes in filename
- All notes go in repository root

**Examples:**

- Input: "semantic routing" → `semantic_routing.md`
- Input: "Rust async runtime comparison" → `rust_async_runtime_comparison.md`
- Input: "First principles thinking" → `first_principles_thinking.md`

## 3. Research the Topic

**Use Perplexity for comprehensive research:**

- Formulate focused query: "Provide comprehensive, technical information about [TOPIC] including: definition, key concepts, how it works, common use cases, best practices, related technologies, and current state as of 2025. Focus on technical accuracy and concrete details."
- Use `mcp__perplexity-ask__perplexity_ask` tool
- Gather sufficient material for complete, self-contained note
- Capture citation sources for references section

**Research depth:**

- Note should be atomic (one concept) but complete
- Include enough context to be standalone
- Technical and specific, not superficial

## 4. Discover Relationships

**Analyze against existing knowledge graph using Grep and Read:**

**Prerequisites:** What must be understood first?

- Grep for foundational concepts this topic mentions
- Check existing notes for topics that should come before this
- Example: `mcp_security.md` requires `mcp_overview.md` first

**Related concepts:** What connects at the same level?

- Find complementary or adjacent topics via tag search
- Technologies that integrate or compare
- Example: `semantic_routing.md` relates to `agents.md`

**Extends:** What does this build upon?

- Specific notes this concept directly extends
- Base concepts or patterns this implements
- Example: `python_mcp_sdk.md` extends `mcp_overview.md`

**Examples:** What concrete implementations exist?

- Look for specific tool/framework notes
- Implementation patterns
- Example: `agents.md` has examples like `alita.md`

**Alternatives:** Different approaches to same problem?

- Competing technologies or patterns
- Different paradigms for same goal

## 5. Generate Tag Recommendations

**Read `tag_system.md` for complete tag catalog**

**Select 3-6 tags across multiple dimensions:**

1. **Technology/Language:** `#python`, `#rust`, `#typescript`, etc.
2. **Framework/Tool:** `#react`, `#mcp`, `#fastmcp`, etc.
3. **Domain/Discipline:** `#agents`, `#llm`, `#security`, etc.
4. **Content Type:** `#api`, `#guide`, `#pattern`, `#reference`, etc.
5. **Cross-cutting Themes:** `#async`, `#optimization`, `#testing`, etc.
6. **Method/Thinking:** `#first-principles`, `#systems-thinking`, etc.

**Tag format:** lowercase with hyphens in YAML array

```yaml
tags: [python, mcp, agents, sdk, api]
```

## 6. Write the Note

**IMPORTANT**: Follow the question-oriented content synthesis approach defined in `_shared_content_synthesis.md`.

**Note Structure Requirements:**

The note MUST follow this question-answering paradigm:

```markdown
---
tags: [tag1, tag2, tag3, tag4, tag5]
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
- Supporting evidence (specific quotes, examples, data from research)
- Technical details and concrete information
- Implications and connections to broader themes]

### [Specific Question 1.2]

**Question**: [Next specific question]

**Answer**: [Evidence-based response...]

## Part II: [Domain Question 2]

### [Specific Question 2.1]

**Question**: [Clear question]

**Answer**: [Comprehensive response with evidence...]

[Continue with additional parts and sections as needed]

## Resolution: [Answer to Central Question]

Synthesize domain insights to definitively resolve the central question posed at the beginning.

## Related Concepts

### Prerequisites
- [[prerequisite_note]] - Why it's needed first

### Related Topics
- [[related_note]] - Connection explanation

### Extends
- [[base_note]] - What this builds upon

## References

[1] Source URL from Perplexity research
[2] Source URL from Perplexity research
```

**Content Synthesis Guidelines** (from `_shared_content_synthesis.md`):

**DO**:
- Create complete educational document that systematically answers questions
- Include specific details, quotes, examples, data points from research
- Build understanding progressively from atomic to central question
- Provide standalone educational value for readers learning the topic
- Write for LLM context consumption and human reading
- Use wikilinks `[[note]]` to reference existing notes
- Include code examples where appropriate
- Be technical and specific with concrete, actionable information

**DO NOT**:
- Simply analyze the question structure or list questions without substantial answers
- Use vague generalities or hyperbolic language
- Include marketing claims or unsupported assertions

## 7. Add Bidirectional Relationships

**Update connected notes using Edit tool:**

For each relationship discovered:

1. **Read the target note** to find its "Related Concepts" section
2. **Add inverse relationship:**
   - If new note extends X → Add new note to X's "Extended By" section
   - If new note has prerequisite X → Add new note to X's "Extended By" or "Related Topics"
   - If new note relates to X → Add new note to X's "Related Topics"

**Example:**

```markdown
# In agents.md - add to "Related Topics" section:
- [[semantic_routing]] - Enables intelligent model selection for agent tasks
```

## 8. Update MOC Files

**Identify relevant MOC files using Glob:**

- Check tags to determine which MOCs apply
- Common MOCs: `agents_moc.md`, `mcp_moc.md`, `rust_moc.md`, `typescript_moc.md`, `python_moc.md`, `writing_moc.md`

**For each relevant MOC:**

- Read the MOC file
- Find appropriate section to add link
- Add wikilink with brief context: `- [[new_note]] - Brief description`
- Maintain MOC organization and structure
- Use Edit tool for surgical updates

## 9. Provide Summary

**Report to user:**

```
Created new note: `new_note.md`

**Tags:** tag1, tag2, tag3, tag4, tag5

**Relationships established:**
- Prerequisites: 2 notes
- Related concepts: 3 notes
- Extends: 1 note
- Examples: 2 notes

**Bidirectional links updated:**
- Updated 5 notes with inverse relationships

**MOCs updated:**
- moc_name_moc.md (added to "Section Name")
- other_moc.md (added to "Other Section")

**Next steps:**
- Review the note at `new_note.md`
- Use `/graph-note new_note.md` to verify relationships
- Use `/expand-graph new_note.md` to discover additional connections
```

## Important Constraints

**Critical rules:**

- ALWAYS use wikilink format `[[note]]` not `[[note.md]]`
- MAINTAIN bidirectionality - update both notes in every relationship
- ENSURE atomicity - one complete, usable concept per note
- NO hyperbolic language or marketing claims
- ALL notes go in repository root (no subdirectories)
- Use Write for new files, Edit for updating existing files
- Use Grep/Glob for discovery, Read for content analysis

**Tools to use:**

- **Write** - Create new markdown file
- **Edit** - Update existing notes (add relationships, update MOCs)
- **Read** - Read tag_system.md, MOC files, existing notes
- **Grep** - Search for similar concepts, find notes by tag
- **Glob** - Find MOC files, check for duplicates
- **mcp__perplexity-ask** - Research the topic

**Quality checks before writing:**

- Is this truly atomic (one concept)?
- Is it complete enough to stand alone?
- Are relationships meaningful and justified?
- Do tags span multiple dimensions?
- Is content technical and specific?

Execute these steps for the topic provided by the user.
