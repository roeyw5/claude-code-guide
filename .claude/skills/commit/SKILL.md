---
description: 'Create a concise commit with recent changes'
---

Create a git commit for staged/unstaged changes with a concise, focused message.

## Instructions

1. Run `git status` to see current changes
2. Run `git diff --staged` and `git diff` to understand what changed
3. Stage all relevant changes (exclude unrelated files if any)
4. Create a commit with a concise message following conventional format

## Commit Message Format

```
<type>(<scope>): <subject>
```

- **type**: feat, fix, refactor, style, docs, test, chore
- **scope**: component or area affected (optional but preferred)
- **subject**: imperative mood, max 50 chars, no period

## Guidelines

- ONE commit per logical change
- Focus on WHAT changed and WHY, not HOW
- Skip obvious details - code speaks for itself
- Group related file changes into single commit
- If multiple unrelated changes exist, ask user how to handle
- If arguments are provided, use them as context for what to commit (e.g., specific files or a description of the change)

## Examples

Good:
- `feat(candidates): add search and filter functionality`
- `fix(candidates): add null safety for positions array`
- `refactor(ui): improve keyboard accessibility`

Bad:
- `updated files` (too vague)
- `Added null safety check to positions array in candidates.js and also fixed...` (too long)
- `WIP` (not descriptive)

$ARGUMENTS
