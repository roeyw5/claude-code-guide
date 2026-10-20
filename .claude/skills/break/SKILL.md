---
name: break
description: Use when the user invokes /break — they are stepping away from this session, possibly for days, and will come back with nothing about it in their head.
manual: true
disable-model-invocation: true
---

# Break

The user is leaving mid-session and may return in an hour or in a week. They will read your last message cold, before sending anything. That message gets them oriented in about a minute and points at the documents that hold the detail.

The note is a map, not a record. Anything already written in a spec, plan, ledger, PR or card is linked, never restated. The note itself carries only what the reader needs to decide what to open and what to do next.

## Before writing

1. **Park, don't push on.** Start no new work. If an edit is half-applied, bring the file to a state that parses. No commits, pushes, deploys, or messages on the user's behalf.
2. **Check what you would otherwise guess.** One round of read-only calls: `git status` and unpushed commits where the session worked, the state of any PR it opened, servers it started, and that every file you will link exists.
3. **Read the session length.** Measured when this skill loaded:

   !`~/.claude/skills/break/context-usage.sh ${CLAUDE_SESSION_ID}`

   LONG means 40% of the context window or more, or a compaction happened. A long session is resumed in a fresh session, so **Next** carries a full handoff prompt (below). If the line is missing or says unknown, treat the session as LONG.

## The note

One message, the last of the turn, nothing after it. About 250 words outside the links table and the prompt block. Sections in this order; drop any that is empty.

**Session line** (no heading). One sentence: what this session is for, in the user's words, and where it lives (worktree, branch, PR).

**## The picture**
One paragraph, at most five sentences: the problem in plain words, the approach, and how far along we are. No history of how we got here.

**## Where it stands**
At most five bullets: what is done, the exact point we stopped, what is left. One closing line for anything unsaved: uncommitted, unpushed, or undeployed work. No test counts, commit hashes, or measurements unless the next step depends on one.

**## Waiting on you**
Numbered, one decision per item, two sentences plus `Recommend: …`. Pending permission prompts first. If nothing, omit the section.

**## Decided, written nowhere else**
Only rulings and findings from this session that no linked document records, one line each, at most four. If there are more, the fix is to say which document should receive them, not to list them here.

**## Read to get back in**
A table of at most six rows: link, one-line reason to open it. Reading order, first row is where to start. Clickable markdown links relative to the workspace root; PRs by URL. Specs, plans, mockups, ledgers and PRs qualify. Code locations, reports, screenshots and anything "reference only" do not, unless the next step starts there.

**## Before you resume**
Only things that need an action on return: a login to refresh, a server to restart, a branch to re-check against main. One line each with the command. Nothing that is merely true or harmless.

**## Next**
The single next step in one sentence, then a ready-to-send prompt in a code block.

- **SHORT session:** the prompt continues *this* session, at most four lines. Do not suggest starting fresh.
- **LONG session:** the prompt is a **handoff for a fresh session** that has never seen this conversation and will not see the note above it. Say so in one line above the block. It must stand alone:
  - **Goal and place:** what the work is for, the repo, worktree path, branch and PR URL.
  - **Read, in order:** full workspace-relative paths of the spec, plan, ledger or PR to read first, each with why. Never "the ledger" or "the plan" without its path.
  - **Exact stopping point:** what is done and where to pick up, with every label expanded ("Task 9 of the plan at docs/plans/…: wire the export check into the download path", not "Task 9").
  - **Decisions not written down:** every ruling, rejected option and finding from this session that no linked document records, so the new session does not reopen them. The four-line cap of the section above does not apply here.
  - **Gotchas and dead ends:** what was tried and failed, environment quirks met this session, pre-existing bugs to note but not fix.
  - **Gates:** where to stop for the user (pause points, before any push, deploy or server start) and anything needing their go.
  - **Unsaved state:** uncommitted or unpushed work and where it sits.

  Pack only what exists nowhere else. Do not restate project instructions files, memory, or the contents of the linked documents; the fresh session gets those for free. Typically 150–400 words, plain prose and short bullets, no nested code fences inside the block.

## Common mistakes

| Mistake | Fix |
|---|---|
| Restating what a linked document says | Link it with a one-line reason |
| Listing every decision of the session | Only those recorded nowhere else, four at most |
| Numbers, hashes, test counts, segment ids | Cut unless the next step needs that exact value |
| Links to everything touched | Six rows; what to read, not what exists |
| "Harmless", "reference only", "nothing running" lines | If it needs no action, it is not in the note |
| A label with no referent ("the guard", "G2", "Task 7") | Say what it is in plain words on first mention |
| A document mentioned without a link | Every document named is a link, verified to exist |
| Continuing the task to reach a better stopping point | Stop where you are |
| A LONG session's prompt that says "per the ledger" or "from Task 9" | Paths and plain words; the fresh session knows nothing |
| Suggesting "start fresh from this note" with a four-line prompt | LONG sessions get the full handoff prompt; the note is not pasted |
| Text or a tool call after the note | The note is the final message |
