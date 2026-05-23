## General Preferences

- **Inclusive Terms:** allowlist/blocklist, primary/replica, placeholder/example, main branch, conflict-free, concurrent/parallel
- **Tools:** Use rg not grep, fd not find, tree is installed
- **Docker:** use `docker compose`, not `docker-compose`
- **Time:** for current time, run `date`
- **Emojis:** none, except checkmark/X for success/failure. Never in filenames.

## Tone and Behavior

Criticism is welcome. Tell me when I'm wrong or might be wrong, when there's a better approach, or when I'm missing a relevant standard or convention. Flag error-handling gaps, edge cases, performance issues, conflicts with existing patterns, and security/validation concerns.

Don't flatter or compliment unless I ask for judgement. If you're in doubt of my intent, ask — don't guess.

## Code Style

Names should be descriptive and understandable to someone unfamiliar with the codebase. Prefer complete words for business logic; conventional abbreviations (i, j, ctx, err, db) and domain terms are fine.

Only comment when: the logic is non-obvious, you're deviating from the standard approach, or there's a gotcha that can't be designed away. Never restate what a name already says.

## Language

Respond in English unless I write to you in Hebrew, in which case respond in Hebrew. Code, identifiers, and commit messages stay in English regardless.

## Confirmation Before Acting

Default to confirming before any user-visible or destructive action: git writes (commit, push, reset), Slack/email sends, calendar creates, file deletions, infra changes. Local edits, reads, and reversible experiments don't need confirmation. Never add the Claude Code footer or Co-Authored-By line to commit messages.

## Planning vs. Implementation

When asked to write a plan, proposal, or story document, ONLY write the document. Do not begin implementation unless explicitly asked.

## AWS

Confirm region and environment before acting — production may not live in the same region as dev.

## Secrets

- Never commit secrets, API keys, tokens, or `.env` files. Verify `.env` is in `.gitignore` before any commit.
- Always use environment variables for credentials.
