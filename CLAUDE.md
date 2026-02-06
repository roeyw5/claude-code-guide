# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A shareable collection of Claude Code skills, hooks, and educational examples. Everything lives under `.claude/` so skills and hooks work immediately when you clone the repo — no copying required.

## Repository Structure

- `README.md` — Comprehensive guide to Claude Code fundamentals (memory, context, plan mode, skills, sub-agents, hooks)
- `.claude/skills/` — Reusable skills in `<name>/SKILL.md` format, usable as `/slash-commands`
- `.claude/hooks/` — Security hooks (Node.js) for blocking dangerous commands and protecting secrets
- `.claude/agents/` — Specialized agents (used by the article-review skills)
- `examples/` — Documentation and sample output for complex multi-component setups (e.g., article-review-team)
- `images/` — Diagrams referenced by the README

## Key Conventions

- Skills follow the `<name>/SKILL.md` directory convention with YAML frontmatter and optional `$ARGUMENTS` support
- Related skills/agents are grouped with a shared prefix (e.g., `article-review-*`)
- Hook scripts follow the PreToolUse pattern, log to `~/.claude/hooks-logs/`, and use configurable severity levels
- All example content uses generic placeholders (NAME1, NAME2, etc.) — no real names or company-specific references

## Working With This Repo

No build or test commands. Changes are typically documentation edits, new skill files, or hook scripts. When adding new skills, create a `<name>/SKILL.md` folder under `.claude/skills/`. When adding hooks, add `.js` files under `.claude/hooks/`.
