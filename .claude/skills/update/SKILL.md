---
name: update
description: Append a session-log entry and refresh the "Next" pointer in a PROGRESS.md file. Use whenever the user wants to log what was done this session, wrap up a working session, record progress, or "update progress" — even if they don't name the file. Skip if PROGRESS.md doesn't exist and the user hasn't asked to create one.
---

Update the PROGRESS.md file with changes made during this session.

## Instructions

1. Read the current PROGRESS.md file
2. Check git status and recent commits to see what changed
3. Review the conversation context for completed tasks, code reviews, or implemented stories
4. **Update the "Next" section** at the top with the next pending story/task
5. **Update/add to "Session Log"** - add entry for today or append to existing
6. Update the exercise status table if story progress has changed

## PROGRESS.md Structure

```markdown
# Project Name - Learning Progress

## Next

**Story N**: Brief description of next task

---

## Session Log

### YYYY-MM-DD (most recent first)
- What was done
- Another thing done

### Previous date
- ...
```

## Guidelines

- **Next section**: Always update with the next pending story from the backlog
- **Session Log**: Most recent date at top, append to today's entry if exists
- Keep entries concise - bullet points, no fluff
- Update exercise status (In Progress, Done) based on story completion
- If a backlog or artifacts directory exists, check it for the next pending story

$ARGUMENTS
