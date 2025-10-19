# Process PDF and Create Note

Extract content from a PDF (URL or local file) and create a comprehensive knowledge graph note using question-oriented content synthesis.

## Usage

`/process-pdf <pdf_url_or_path> [note_filename]`

## Process

### Step 1: Content Acquisition (PDF-Specific)

**Access PDF content**:
- **If URL**: Use `mcp__firecrawl__firecrawl_scrape` with PDF parser
- **If local file**: Use `Read` tool (supports PDF)
- Extract text, structure, and key information

**Analyze document metadata**:
- Extract title, authors, publication date if available
- Identify document type (academic paper, guide, report, technical spec, etc.)
- Note any special structure (abstract, sections, references)

**Read the extracted content**:
- This is the raw content to be synthesized

### Step 2: Universal Content Processing

**Follow the shared content synthesis pipeline** documented in `_shared_content_synthesis.md`:

1. **Apply Question-Oriented Content Synthesis**
   - Phase 1: Central Question Discovery
   - Phase 2: Domain Question Extraction
   - Phase 3: Specific and Atomic Question Decomposition
   - Phase 4: Progressive Answer Development

2. **Generate note structure and metadata**
   - Determine filename based on central question
   - Assign 3-6 tags mixing dimensions
   - Create PDF-specific YAML frontmatter

3. **MOC Integration**
   - Read TOPICS.md to understand MOC structure
   - Identify appropriate MOC(s) for this note
   - Update MOC file(s) with wikilink and description

4. **Relationship Discovery**
   - Search for related notes in knowledge graph
   - Establish bidirectional relationships
   - Update related notes

## PDF-Specific Note Structure

```markdown
---
tags: [domain, topic, content-type]
source: <pdf_url_or_path>
document_title: "<title>"
authors: "<authors if applicable>"
date_added: <ISO_date>
---

# Note Title (Based on Central Question)

## Central Question

**Question**: [The single overarching question the document addresses]

**Executive Summary**: 2-3 paragraphs previewing key insights and how the document resolves the central question.

## Part I: [Domain Question 1]

### [Specific Question 1.1]

**Question**: [Clear, specific question from this section]

**Answer**: [Comprehensive response including:
- Direct answer to the question
- Supporting evidence from document (specific quotes, examples, data with page numbers)
- Technical details and concrete information
- Implications and connections to broader themes]

### [Specific Question 1.2]

**Question**: [Next specific question]

**Answer**: [Evidence-based response...]

## Part II: [Domain Question 2]

### [Specific Question 2.1]

**Question**: [Clear question]

**Answer**: [Comprehensive response with document evidence...]

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

- [Document Title](<source>) - Brief description
- Authors: <authors>
- Accessed: <date>
```

## Tools to Use

- `mcp__firecrawl__firecrawl_scrape` - For PDF URLs (with parser)
- `Read` - For local PDF files, read TOPICS.md and MOC files
- `Grep` - Find related notes in knowledge graph
- `Write` - Create new note following question-oriented structure
- `Edit` - Update MOC files to include new note, update related notes for bidirectional relationships

## Critical Requirements

See `_shared_content_synthesis.md` for complete requirements. Key points:

- **Synthesis Over Analysis**: Create complete educational document, not meta-analysis of question structure
- **Answer Integration Pattern**: Every question paired with comprehensive, evidence-based answers
- **MOC Integration**: Ensure note is wired into knowledge graph via appropriate MOC(s)
- **Bidirectional Relationships**: Update both new note and related notes for discoverability
