# Skills

Drop-in skills for Claude Code. Each folder is a `/slash-command`.

Since these live in `.claude/skills/`, they work immediately if you clone this repo. To use individual skills in another project, copy the folder:

```bash
cp -r commit/ /path/to/your-project/.claude/skills/commit/
```

## Available Skills

| Skill | Command | Description |
|-------|---------|-------------|
| `commit/` | `/commit` | Conventional commit messages with a confirmation step before writing |
| `drawio/` | `/drawio` | Generate native `.drawio` XML diagrams for VS Code or app.diagrams.net |
| `html-guide/` | `/html-guide` | Convert a markdown runbook/guide into a styled, self-contained HTML page (handles LTR and Hebrew RTL) |
| `skill-creator/` | `/skill-creator` | Create, edit, and benchmark skills; optimize descriptions for triggering accuracy |
| `update/` | `/update` | Update a `PROGRESS.md` file with session changes |

## Skill Structure

Each skill follows the Claude Code convention:

```
skill-name/
├── SKILL.md              # Required — skill instructions and frontmatter
├── scripts/              # Optional — helper scripts the skill calls
├── references/           # Optional — extra docs loaded only when needed
└── assets/               # Optional — templates the skill writes into outputs
```

More elaborate skills in this repo (`skill-creator/`, `html-guide/`) bundle scripts and templates alongside `SKILL.md` — useful examples of progressive disclosure when the body alone isn't enough.

The `SKILL.md` frontmatter controls behavior:

```yaml
---
name: skill-name
description: When Claude should invoke this skill
---
```
