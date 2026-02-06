# Skills

Drop-in skills for Claude Code. Each folder is a `/slash-command`.

Since these live in `.claude/skills/`, they work immediately if you clone this repo. To use individual skills in another project, copy the folder:

```bash
cp -r commit/ /path/to/your-project/.claude/skills/commit/
```

## Standalone Skills

| Skill | Command | Description |
|-------|---------|-------------|
| `commit/` | `/commit` | Conventional commit messages with proper formatting |
| `doublecheck/` | `/doublecheck` | Cross-check technical claims using a secondary LLM |
| `update/` | `/update` | Update a PROGRESS.md file with session changes |
| `weekly-summary/` | `/weekly-summary` | Structured meeting summaries in Obsidian-compatible Markdown |

## Article Review System

These skills work together with 5 specialized agents (in `.claude/agents/article-review-*.md`) to provide comprehensive article reviews. See [examples/article-review-team/README.md](../../examples/article-review-team/README.md) for the full architecture guide.

| Skill | Command | Description |
|-------|---------|-------------|
| `article-review-tech/` | `/article-review-tech` | Technical accuracy verification |
| `article-review-editorial/` | `/article-review-editorial` | Grammar, flow, and SEO review |
| `article-review-full/` | `/article-review-full` | Orchestrates both tech + editorial in parallel |

## Skill Structure

Each skill follows the Claude Code convention:

```
skill-name/
├── SKILL.md              # Required — skill instructions and frontmatter
└── assets/               # Optional — templates, examples, scripts
```

The `SKILL.md` frontmatter controls behavior:

```yaml
---
name: skill-name
description: When Claude should invoke this skill
---
```
