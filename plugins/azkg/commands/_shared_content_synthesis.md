# Shared Content Synthesis Instructions

**This file contains common instructions for all content ingestion commands** (`/youtube-transcript`, `/scrape-url`, `/process-pdf`). These steps apply AFTER content has been acquired, regardless of source.

## Universal Content Processing Pipeline

### Phase 1: Question-Oriented Content Synthesis

Apply the methodology from `thinking_question_content_synthesis.md`:

**Step 1: Central Question Discovery**
- Identify the single overarching question the content addresses
- Consider title, description, opening/closing statements
- This becomes the note's organizing principle

**Step 2: Domain Question Extraction**
- Identify major question domains by analyzing topic transitions
- Look for transitional phrases: "Now let's talk about," "Another important point," "Moving on to"
- Group content segments into substantial domain areas

**Step 3: Specific and Atomic Question Decomposition**
- Break domain questions into specific questions (section level)
- Further decompose into atomic questions (evidence level)
- Extract specific details, examples, data points, and quotes from content

**Step 4: Progressive Answer Development**
- Build comprehensive answers using evidence from content
- Synthesize atomic answers into specific section responses
- Integrate specific answers to address domain questions
- Combine domain insights to resolve central question

### Phase 2: Note Structure and Metadata

**Generate note filename** (if not provided):
- Based on central question or primary topic
- Use lowercase with underscores
- Follow naming convention: `topic_subtopic.md` or `moc_topic.md`
- Examples: `agents_reasoning_patterns.md`, `python_async_programming.md`

**Determine appropriate tags**:
- 3-6 tags mixing dimensions:
  - Technology/Language (`#python`, `#rust`, `#typescript`)
  - Framework/Tool (`#mcp`, `#react`)
  - Domain/Discipline (`#agents`, `#llm`, `#writing`)
  - Content Type (`#guide`, `#reference`, `#pattern`)
  - Method/Thinking (`#first-principles`, `#systems-thinking`)

### Phase 3: MOC Integration

**Purpose**: Ensure every note is properly wired into the knowledge graph.

**Steps**:

1. **Read TOPICS.md** to understand existing MOC structure
   - 22 MOCs organized by domain (AI & ML, Development Platforms, etc.)
   - Each MOC listed with note count and brief description
   - Examples: `moc_agents`, `moc_python`, `moc_thinking`, `moc_mcp`

2. **Identify appropriate MOC(s)** based on:
   - Primary topic/domain from content
   - Tags assigned to the note
   - Technology stack or framework discussed
   - Cross-cutting themes (e.g., thinking patterns, development practices)
   - **Multiple MOCs are acceptable** if note spans domains

3. **Read target MOC file(s)** to understand organization
   - Check existing structure and categories within the MOC
   - Identify where the new note fits logically
   - Follow existing formatting patterns

4. **Update MOC file(s)** with Edit tool
   - Add wikilink `[[new_note]]` in appropriate section
   - Include one-line description of what note covers
   - Maintain alphabetical order or logical grouping
   - Update note count in MOC if present

5. **Create new MOC if needed**
   - Only if no existing MOC fits and topic is substantial
   - Follow naming convention: `moc_<topic>.md`
   - Include in TOPICS.md with description
   - **Rare** - usually existing MOCs cover most domains

### Phase 4: Relationship Discovery

**Identify connections to existing notes**:

1. **Search for related concepts**
   - Use Grep to find notes with similar tags
   - Search for wikilinks to related topics
   - Consider prerequisite chains and extensions

2. **Establish bidirectional relationships**
   - Add "Related Concepts" section to new note with:
     - **Prerequisites** - Must understand first
     - **Related Topics** - Connected ideas at same level
     - **Extends** - Builds upon another concept
     - **Examples** - Concrete implementations
   - Update related notes to link back (bidirectionality)
   - Always include "why" explanations for each relationship

3. **Ask user for confirmation** on suggested relationships
   - Present discovered connections
   - Allow user to approve/modify before updating

## Standard Note Structure

All notes follow this template:

```markdown
---
tags: [domain, technology, content-type]
source: <original_url_or_path>
date_added: <ISO_date>
# Additional metadata varies by source type:
# - YouTube: video_title, video_id, transcript
# - PDF: document_title, authors
---

# Note Title (Based on Central Question)

## Central Question

**Question**: [The single overarching question the content addresses]

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
- [[prerequisite]] - Why needed first

### Related Topics
- [[related]] - Connection explanation

### Extends
- [[base_concept]] - What this builds upon

## References

- [Original Source](<url_or_path>) - Source description
- Additional metadata specific to source type
```

## Critical Requirements

**Synthesis Over Analysis** (from `thinking_question_content_synthesis.md`):

- **DO NOT**: Simply analyze the question structure or list questions without substantial answers
- **DO**: Create complete educational document that systematically answers questions using evidence from content
- **DO**: Include specific details, quotes, examples, data points from content
- **DO**: Build understanding progressively from atomic to central question
- **DO**: Provide standalone educational value for readers learning the topic

**Answer Integration Pattern**:

Every question must be paired with comprehensive answers that include:
- Specific details, metrics, and examples from the content
- Direct quotes where appropriate (with timestamps/page numbers if available)
- Technical accuracy and precision
- Evidence-based reasoning with clear source attribution
- Standalone educational value

**MOC Integration Pattern**:

If creating `python_fastapi_patterns.md` from any source:

```markdown
# In moc_python.md, add to appropriate section:

### Web Frameworks
- [[python_fastapi_patterns]] - FastAPI design patterns and best practices from production use cases
```

## Common Tools to Use

- `Read` - Read TOPICS.md for MOC discovery, read target MOC files for structure
- `Grep` - Find related notes by tags/content, search for wikilinks
- `Write` - Create new note following question-oriented structure
- `Edit` - Update MOC files to include new note, update related notes for bidirectional relationships

## Example MOC Update Workflow

1. Read `TOPICS.md` → Identify `moc_python` and `moc_llm` as relevant
2. Read `moc_python.md` → Find "Libraries" section
3. Edit `moc_python.md` → Add `[[new_note]] - Brief description`
4. Read `moc_llm.md` → Find "Agent Systems" section
5. Edit `moc_llm.md` → Add `[[new_note]] - Brief description`

Result: New note is discoverable through two different MOC navigation paths.
