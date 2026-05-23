---
name: commit
description: Create a git commit with a clean, conventional message (feat/fix/docs/refactor/...) and a confirmation step before writing. Use whenever the user asks to commit, "make a commit", "save this", asks for a commit message, or wraps up a chunk of work — even if they don't say "conventional". Skip if the user is asking about commit history, blame, or anything other than creating a new commit.
---

Create a git commit for staged/unstaged changes with a concise, focused message.

## Instructions

1. Run `git status` to see current changes
2. Run `git diff --staged` and `git diff` to understand what changed
3. Stage all relevant changes (exclude unrelated files if any)
4. Show the proposed commit message and ask for confirmation before committing
5. Do not add the Claude Code footer or Co-Authored-By line

## Commit Message Format

```
<type>(<scope>): <subject>
```

- **type**: feat | fix | docs | style | refactor | test | chore | perf
- **scope**: component or area affected (optional but preferred)
- **subject**: imperative mood, max 50 chars, no period
- For complex changes, add a body explaining what/why (72-char lines) and reference issues

## Guidelines

- ONE commit per logical change
- Focus on WHAT changed and WHY, not HOW
- Skip obvious details - code speaks for itself
- Group related file changes into single commit
- If multiple unrelated changes exist, ask user how to handle

## Examples

Good:
- `feat(prediction): add batch processing chunk size config`
- `fix(auth): handle expired JWT token refresh`
- `docs(infra): add deployment runbook`
- `refactor(frontend): extract property card into shared component`

Bad:
- `updated files` (too vague)
- `Added null safety check to properties array in PropertyList.tsx and also fixed...` (too long)
- `WIP` (not descriptive)

$ARGUMENTS
