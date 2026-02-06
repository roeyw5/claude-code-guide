---
name: weekly-summary
description: Creates structured meeting summaries in Markdown format, compatible with Obsidian and other knowledge base tools. Use when the user provides meeting notes, transcripts, or recordings and wants a formatted summary. Triggers include requests like "summarize this meeting", "create meeting notes", "weekly summary", "1:1 summary", "meeting recap", or any request to document a meeting in Markdown format.
---

# Weekly Summary Skill

Create structured meeting summaries in Markdown with callouts, tables, and tags. Compatible with Obsidian, Notion, and other Markdown-based knowledge bases.

## Output Format

Generate a `.md` file following this structure:

```markdown
# [Meeting Title]

> [!info] Meeting Details
> **Date:** YYYY-MM-DD
> **Participants:** [Names]
> **Type:** [Meeting Type]

---

## 1. [Topic Section]

### [Subsection if needed]
- Key point with **bold** for emphasis
- Another point

---

## Action Items

> [!todo] Action Items

| Action | Owner | Status |
|--------|-------|--------|
| Task description | Name | 🟡 Pending |

---

## Key Decisions

1. Decision one
2. Decision two

---

## Notes & Context

- Additional context points
- Background information

---

#meeting #weekly #[relevant-tags]
```

## Status Emoji Legend

| Status | Emoji |
|--------|-------|
| Pending | 🟡 |
| In Progress | 🟢 |
| Waiting | 🔵 |
| Planned | ⚪ |
| Idea Phase | 🟣 |
| Completed | ✅ |
| Blocked | 🔴 |

## Extraction Guidelines

1. **Topics**: Group discussion points into logical sections (3-7 sections typical)
2. **Action Items**: Extract ALL tasks mentioned with clear owner assignment
3. **Decisions**: Capture explicit agreements or conclusions reached
4. **Key Details**: Include specific numbers, dates, names, and deadlines
5. **Context**: Add relevant background that aids future reference

## Formatting Rules

- Use `> [!info]` for meeting metadata callout
- Use `> [!todo]` for action items callout
- Use `---` horizontal rules between major sections
- Use tables for action items (always include Owner and Status columns)
- Use numbered lists for decisions and ordered processes
- Use bullet lists for general points
- Add tags at the bottom relevant to the meeting content
- Use **bold** for emphasis on key terms, names, or numbers
- Use `code` formatting for technical terms, commands, or file names

## File Naming

Name output: `[meeting-type]_[YYYY-MM-DD].md`

Examples:
- `weekly_meeting_YYYY-MM-DD.md`
- `1on1_name_YYYY-MM-DD.md`
- `standup_YYYY-MM-DD.md`

## Language Handling

- If the source material is in a non-English language, produce the summary in English unless explicitly requested otherwise
- Preserve proper nouns, project names, and technical terms as-is
- Translate colloquialisms to clear English equivalents
