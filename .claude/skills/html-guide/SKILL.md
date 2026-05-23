---
name: html-guide
description: >
  Convert a markdown reference doc (setup guide, runbook, walkthrough, proposal)
  into a self-contained, visually styled HTML file with step-cards, callouts,
  needs-row, and a clean reading layout. Use this skill whenever the user asks
  to turn an .md file into a "nice looking" / "visual" / "printable" / "shareable"
  HTML version, build an HTML guide from markdown, or html-ify a doc for a
  non-technical reader to follow. Triggers on phrases like "make an HTML version
  of this guide", "html-ify this doc", "render this markdown as an HTML guide",
  "build a visual guide from <file.md>", "/html-guide <path>". The skill handles
  English LTR and Hebrew RTL automatically.
---

# html-guide

Turn a markdown doc into a styled, self-contained HTML page using a small bundled Python script for the deterministic conversion, then optionally enrich two special section types ("How it works" and "Troubleshooting") by hand because they benefit from layout decisions only you can make.

The aesthetic is fixed: white cards on a soft gray background, teal accent (`#0d9488`), system fonts, step-cards for `## Step N` headings, 3-card row for "What you'll need" / "Prerequisites", subtle shadows. The script picks `dir="rtl"` and `lang="he"` automatically when the source is predominantly Hebrew.

## Step 1: Resolve the input

If the user passed a path (`/html-guide path/to/file.md`), use it. If they passed nothing, ask whether they want to point at a file on disk or paste markdown content. If they paste content, write it to a tempfile under `/tmp/` first — the script reads from disk.

## Step 2: Run the build script

```bash
python3 ~/.claude/skills/html-guide/scripts/build.py <input.md>
```

The script defaults to writing `<repo>/docs/guides/<input-stem>.html` (it walks up from the input looking for a `docs/guides/` directory). Pass `--output <path>` to override, or `--force` to overwrite without prompting.

The script handles all the mechanical work:

- Parses the markdown (headings, paragraphs, lists, tables, fenced code, blockquotes).
- Detects Hebrew content and emits `<html dir="rtl" lang="he">` when >30% of letters are Hebrew. All directional CSS uses logical properties (`padding-inline-start`, `border-inline-start`), so RTL "just works."
- Classifies each `##` section by heading text:
  | Heading match | Rendering |
  |---|---|
  | `Step N`, `Step N: Title` | Step-card with circled number |
  | `Prerequisites`, `What you'll need`, `Requirements` | 3-card grid (one card per list item) |
  | Anything else | Plain `<h2>` + body |
- Converts callouts: `> **Important:** ...` → orange callout, `> **Tip:** ...` → green, `> **Note:** ...` → blue, etc.
- Escapes HTML, preserves code-block contents verbatim, renders tables with the styled wrapper.

Sections labeled "How it works" and "Troubleshooting" are rendered as plain sections by the script. You enrich them in Step 3.

## Step 3: Enrich the special sections (only if they benefit)

Read the script's output once. For each of these two cases, decide whether to upgrade the markup. **Skip this step entirely if neither pattern applies** — the plain rendering is fine for proposals, runbooks, and anything else without these specific shapes.

### Case A: "How it works" with an ASCII arrow diagram

If the source markdown's "How it works" section contains a single-line ASCII flow like `A --> B --> C`, replace the plain section with a CSS box diagram. The script will have rendered the ASCII inside a `<pre>` block; find it and replace with markup like:

```html
<div class="section-title">How it works</div>
<div class="diagram">
  <div class="diagram-box">
    <div class="title">Your computer</div>
    <div class="sub">DBeaver client</div>
  </div>
  <div class="diagram-arrow">→</div>
  <div class="diagram-box middle">
    <div class="title">EC2 backend</div>
    <div class="sub">backend-prod<br>(SSH tunnel entry)</div>
  </div>
  <div class="diagram-arrow">→</div>
  <div class="diagram-box">
    <div class="title">RDS database</div>
    <div class="sub">app-db<br>(production)</div>
  </div>
</div>
```

Use `.diagram-box.middle` (teal-tinted) for the centerpiece — usually the hop or the orchestrator. Keep node titles to 2–3 words and `.sub` lines to a short identifier + parenthetical hint.

Only do this for 3-node linear flows. Branching diagrams, multi-row diagrams, or anything with more than ~5 nodes won't fit the grid — leave those as `<pre>`.

### Case B: "Troubleshooting" table with Problem / Solution shape

If the source markdown has a `## Troubleshooting` table with two columns (typically "Problem" and "Solution"), the script renders it as a `<table>`. Upgrade it to a `<details>` accordion — easier to scan when there are many entries:

```html
<details>
  <summary>"Private key file does not exist"</summary>
  <p>Use the full path (<code>C:\Users\...</code>), not <code>~/.ssh/...</code>.</p>
</details>
<details>
  <summary>"Connection refused" on SSH</summary>
  <p>Check that the IP is reachable.</p>
</details>
```

One `<details>` per table row. The Problem cell becomes the `<summary>`, the Solution cell becomes the `<p>`. Preserve inline `<code>`, links, and `<strong>` from the script's output — don't strip formatting.

Only do this for genuine Problem/Solution pairs. A 2-column table that just happens to be under a "Troubleshooting" heading but isn't symptom/fix shaped should stay a table.

## Step 4: Write and report

After any Step 3 edits, write the final HTML to its target path (use Edit if the file already exists from Step 2, Write only if you skipped Step 3). Then tell the user:

- The output path as a clickable markdown link.
- A one-line "to view it: `xdg-open <path>`".
- A brief note of what (if anything) you upgraded in Step 3, so they know how much was script vs. judgment.

## Why this is structured as a script + judgment hybrid

The script handles 95% of the work because md→html is repetitive and deterministic — running an LLM through it every time wastes tokens and risks drift between runs. But two patterns (the diagram and the accordion) require deciding *whether* the source actually fits the richer markup. A blanket rule ("always make Troubleshooting an accordion") would produce ugly output when the table isn't really symptom/fix. That's the part that needs judgment, so it lives here in SKILL.md rather than in the script.

If you find yourself making the same Step 3 judgment over and over across runs, that's a signal the script should learn the pattern. Tell the user and propose moving the logic into `scripts/build.py`.

## Source files

- `scripts/build.py` — the Python build script. Self-contained, no third-party deps. Has `--output` and `--force` flags.
- `template.html` — the HTML scaffold with `{{LANG}}`, `{{DIR}}`, `{{TITLE}}`, `{{BODY}}` placeholders. All CSS is inline.

## Edge cases worth knowing

- **No `# h1`**: the hero section is skipped. The page falls back to using the input filename as the `<title>`.
- **Multi-paragraph lede**: only the first paragraph after the `# h1` becomes the `.lede`. Following paragraphs go into the body as plain `<p>`.
- **Mixed-language docs**: RTL detection is based on the *whole document*. A Hebrew doc with English code blocks will still be RTL (code blocks have `direction: ltr` baked into the CSS so they read correctly).
- **`## Step` headings without numbers** (`## Step: Save the key`): the script treats them as steps but uses `•` in the circle instead of a number. Probably not what the author wanted — gently suggest numbering.
- **Non-list "What you'll need"**: if the section has prose instead of `- items`, the 3-card grid doesn't apply and the section falls back to plain. The script handles this; you don't need to intervene.
