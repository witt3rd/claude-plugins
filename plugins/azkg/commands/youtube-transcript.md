# YouTube Transcript and Create Note

Get transcript from a YouTube video using yt-dlp and create a comprehensive knowledge graph note using question-oriented content synthesis.

## Usage

`/youtube-transcript <youtube_url> [note_filename]`

## Process

### Step 1: Content Acquisition (YouTube-Specific)

**Extract video ID and metadata**:
- Parse video ID from YouTube URL
- Use `yt-dlp` to get video metadata (title, description, uploader, upload date)
- Command: `yt-dlp --skip-download --write-info-json <url>`

**Get transcript using yt-dlp**:
- Use `yt-dlp --write-auto-subs --sub-langs "en-US,en.*" --skip-download --sub-format vtt --convert-subs srt -o "attachments/%(id)s" <url>`
- This downloads English subtitles only, preferring en-US variant
- Save transcript to `attachments/<video_id>.srt` or `attachments/<video_id>.en.srt`
- If auto-generated subtitles unavailable, try manual subtitles with same `--sub-langs` flag
- If transcript unavailable, inform user and suggest alternatives

**Read the transcript**:
- Use Read tool to load transcript from `attachments/<video_id>.srt`
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
   - Create YouTube-specific YAML frontmatter

3. **MOC Integration**
   - Read TOPICS.md to understand MOC structure
   - Identify appropriate MOC(s) for this note
   - Update MOC file(s) with wikilink and description

4. **Relationship Discovery**
   - Search for related notes in knowledge graph
   - Establish bidirectional relationships
   - Update related notes

## YouTube-Specific Note Structure

```markdown
---
tags: [domain, topic, content-type]
source: <youtube_url>
video_title: "<title>"
video_id: "<video_id>"
transcript: "attachments/<video_id>.srt"
date_added: <ISO_date>
---

# Note Title (Based on Central Question)

## Central Question

**Question**: [The single overarching question the video addresses]

**Executive Summary**: 2-3 paragraphs previewing key insights and how the video resolves the central question.

## Part I: [Domain Question 1]

### [Specific Question 1.1]

**Question**: [Clear, specific question from this section]

**Answer**: [Comprehensive response including:
- Direct answer to the question
- Supporting evidence from transcript (specific quotes with timestamps if available)
- Technical details and concrete information
- Implications and connections to broader themes]

### [Specific Question 1.2]

**Question**: [Next specific question]

**Answer**: [Evidence-based response...]

## Part II: [Domain Question 2]

### [Specific Question 2.1]

**Question**: [Clear question]

**Answer**: [Comprehensive response with transcript evidence...]

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

- [Video Title](<youtube_url>) - Original video source
- [Transcript](attachments/<video_id>.srt) - Downloaded transcript (SRT format)
- Video ID: `<video_id>`
- Uploaded by: <uploader>
- Upload date: <upload_date>
- Accessed: <access_date>
```

## Tools to Use

- `Bash` - Run `yt-dlp` commands to download metadata and transcripts
- `Read` - Read downloaded transcript from attachments folder, read TOPICS.md and MOC files
- `Grep` - Find related notes in knowledge graph
- `Write` - Create new note following question-oriented structure
- `Edit` - Update MOC files to include new note, update related notes for bidirectional relationships

## Example yt-dlp Commands

```bash
# Get video metadata
yt-dlp --skip-download --write-info-json <youtube_url>

# Download auto-generated subtitles as SRT (English only, prefer en-US)
yt-dlp --write-auto-subs --sub-langs "en-US,en.*" --skip-download --sub-format vtt --convert-subs srt -o "attachments/%(id)s" <youtube_url>

# Try manual subtitles if auto-subs unavailable (English only, prefer en-US)
yt-dlp --write-subs --sub-langs "en-US,en.*" --skip-download --sub-format vtt --convert-subs srt -o "attachments/%(id)s" <youtube_url>

# List available subtitle languages
yt-dlp --list-subs <youtube_url>
```

## Critical Requirements

See `_shared_content_synthesis.md` for complete requirements. Key points:

- **Synthesis Over Analysis**: Create complete educational document, not meta-analysis of question structure
- **Answer Integration Pattern**: Every question paired with comprehensive, evidence-based answers
- **MOC Integration**: Ensure note is wired into knowledge graph via appropriate MOC(s)
- **Bidirectional Relationships**: Update both new note and related notes for discoverability
