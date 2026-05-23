#!/usr/bin/env python3
"""
html-guide build script.

Converts a markdown reference doc into a self-contained styled HTML file using
the Example B aesthetic (teal accent, step-cards, callouts, accordion).

This script handles the deterministic parts: parsing, plain sections, callouts,
tables, RTL detection, file I/O. SKILL.md asks Claude to optionally inspect the
output afterwards and enrich "How it works" diagrams or Troubleshooting tables
that benefit from custom rendering.

Usage:
    python3 build.py <input.md> [--output <output.html>] [--force]

If --output is omitted, writes to docs/guides/<input-stem>.html next to the input.
"""

from __future__ import annotations

import argparse
import html
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable


SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
TEMPLATE_PATH = SKILL_DIR / "template.html"

# Hebrew Unicode block. Used both to decide RTL and to lang-tag the output.
HEBREW_RE = re.compile(r"[֐-׿]")
HEBREW_RATIO_THRESHOLD = 0.30

STEP_HEADING_RE = re.compile(r"^step\s*\d+\b[:.\-\s]*", re.IGNORECASE)
NEEDS_HEADING_NAMES = {
    "prerequisites",
    "what you'll need",
    "what you will need",
    "requirements",
    "you'll need",
    "what you need",
    # Hebrew equivalents
    "מה צריך",
    "דרישות",
    "מה שצריך",
}
TROUBLE_HEADING_NAMES = {"troubleshooting", "פתרון בעיות"}
DIAGRAM_HEADING_NAMES = {"how it works", "איך זה עובד"}

CALLOUT_LABEL_TO_KIND = {
    "important": "warn",
    "warning": "warn",
    "warn": "warn",
    "caution": "warn",
    "heads up": "warn",
    "recommended": "ok",
    "tip": "ok",
    "success": "ok",
    "note": "info",
    "info": "info",
    "fyi": "info",
}


# ---------------------------------------------------------------------------
# Block model
# ---------------------------------------------------------------------------

@dataclass
class Block:
    """One ## section, plus the implicit pre-first-heading block (hero)."""
    heading: str | None  # None for the hero / pre-h2 lead-in
    level: int  # 1 for hero, 2 for normal sections
    lines: list[str] = field(default_factory=list)

    @property
    def heading_key(self) -> str:
        return (self.heading or "").strip().lower()


# ---------------------------------------------------------------------------
# Markdown parsing
# ---------------------------------------------------------------------------

def split_blocks(md: str) -> tuple[str, str, list[Block]]:
    """
    Split a markdown doc into (h1_title, lede_paragraph, sections).

    The hero is everything from the top until the first `##` heading:
        - the first `#` line becomes h1_title
        - the next non-empty paragraph becomes lede_paragraph
    Then each `##` heading starts a new Block.
    """
    lines = md.splitlines()
    h1 = ""
    lede_lines: list[str] = []
    sections: list[Block] = []
    current: Block | None = None
    seen_h1 = False
    in_code_fence = False

    for raw in lines:
        # Track fenced code blocks so we don't mis-parse `## foo` inside them.
        if raw.lstrip().startswith("```"):
            in_code_fence = not in_code_fence
            if current is not None:
                current.lines.append(raw)
            else:
                lede_lines.append(raw)
            continue

        if not in_code_fence and raw.startswith("# ") and not seen_h1:
            h1 = raw[2:].strip()
            seen_h1 = True
            continue

        if not in_code_fence and raw.startswith("## "):
            current = Block(heading=raw[3:].strip(), level=2)
            sections.append(current)
            continue

        if current is None:
            lede_lines.append(raw)
        else:
            current.lines.append(raw)

    # The lede is the first non-empty paragraph block in lede_lines.
    lede = ""
    para: list[str] = []
    for line in lede_lines:
        if line.strip() == "":
            if para:
                lede = " ".join(p.strip() for p in para)
                break
        else:
            para.append(line)
    if not lede and para:
        lede = " ".join(p.strip() for p in para)

    return h1, lede, sections


def is_hebrew(text: str) -> bool:
    """Return True if the text is predominantly Hebrew (RTL)."""
    if not text:
        return False
    letters = [c for c in text if c.isalpha()]
    if not letters:
        return False
    hebrew_count = sum(1 for c in letters if HEBREW_RE.match(c))
    return hebrew_count / len(letters) >= HEBREW_RATIO_THRESHOLD


# ---------------------------------------------------------------------------
# Section classification
# ---------------------------------------------------------------------------

def classify(block: Block) -> str:
    """Return one of: step, needs, troubleshooting, diagram, plain."""
    key = block.heading_key
    if STEP_HEADING_RE.match(key):
        return "step"
    if key in NEEDS_HEADING_NAMES or any(name in key for name in NEEDS_HEADING_NAMES):
        return "needs"
    if key in TROUBLE_HEADING_NAMES:
        return "troubleshooting"
    if key in DIAGRAM_HEADING_NAMES:
        return "diagram"
    return "plain"


def extract_step_number(heading: str) -> str:
    """From 'Step 3: Save the key' return '3'; fallback to the raw heading."""
    m = re.match(r"step\s*(\d+)\b", heading.strip(), re.IGNORECASE)
    return m.group(1) if m else "•"


def strip_step_prefix(heading: str) -> str:
    """'Step 3: Save the key' → 'Save the key'."""
    return re.sub(r"^step\s*\d+\s*[:.\-]\s*", "", heading.strip(), flags=re.IGNORECASE)


# ---------------------------------------------------------------------------
# Inline markdown → HTML
# ---------------------------------------------------------------------------

def render_inline(text: str) -> str:
    """Convert inline markdown (bold, italic, links, code) to HTML.

    Order matters: code first (so its contents don't get bolded), then links,
    then bold/italic. Everything else is HTML-escaped.
    """
    placeholders: list[str] = []

    def stash(html_fragment: str) -> str:
        placeholders.append(html_fragment)
        return f"\x00{len(placeholders) - 1}\x00"

    # Inline code: `foo`
    def code_sub(m: re.Match[str]) -> str:
        return stash(f"<code>{html.escape(m.group(1))}</code>")

    text = re.sub(r"`([^`]+)`", code_sub, text)

    # Links: [label](url)
    def link_sub(m: re.Match[str]) -> str:
        label, url = m.group(1), m.group(2)
        return stash(
            f'<a href="{html.escape(url, quote=True)}">{html.escape(label)}</a>'
        )

    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", link_sub, text)

    # Escape the rest.
    text = html.escape(text)

    # Bold: **foo** — operate on escaped text, so we match literal asterisks.
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    # Italic: *foo* (single asterisks). Avoid matching across newlines.
    text = re.sub(r"(?<!\*)\*([^*\n]+)\*(?!\*)", r"<em>\1</em>", text)

    # Restore placeholders.
    def restore(m: re.Match[str]) -> str:
        return placeholders[int(m.group(1))]

    return re.sub(r"\x00(\d+)\x00", restore, text)


# ---------------------------------------------------------------------------
# Body rendering — turns a list of markdown lines into HTML fragments
# ---------------------------------------------------------------------------

def render_body(lines: list[str]) -> str:
    """
    Convert the body of a section (raw markdown lines) into HTML.

    Recognizes: paragraphs, fenced code blocks, ordered/unordered lists,
    blockquote callouts, and tables.
    """
    html_parts: list[str] = []
    i = 0
    n = len(lines)

    while i < n:
        line = lines[i]
        stripped = line.strip()

        # Blank line — skip
        if not stripped:
            i += 1
            continue

        # Fenced code block
        if stripped.startswith("```"):
            i += 1
            code_lines: list[str] = []
            while i < n and not lines[i].lstrip().startswith("```"):
                code_lines.append(lines[i])
                i += 1
            if i < n:
                i += 1  # consume closing fence
            code = html.escape("\n".join(code_lines))
            html_parts.append(f"<pre><code>{code}</code></pre>")
            continue

        # Blockquote / callout
        if stripped.startswith(">"):
            block_lines: list[str] = []
            while i < n and lines[i].strip().startswith(">"):
                block_lines.append(lines[i].strip().lstrip(">").lstrip())
                i += 1
            html_parts.append(render_callout(block_lines))
            continue

        # Table — at least two rows separated by a |-and-dash line
        if "|" in line and i + 1 < n and re.match(r"^\s*\|?[-:\s|]+\|?\s*$", lines[i + 1]):
            table_lines: list[str] = []
            while i < n and "|" in lines[i] and lines[i].strip():
                table_lines.append(lines[i])
                i += 1
            html_parts.append(render_table(table_lines))
            continue

        # Ordered list
        if re.match(r"^\s*\d+\.\s+", line):
            list_lines, consumed = collect_list(lines, i, ordered=True)
            html_parts.append(render_list(list_lines, ordered=True))
            i += consumed
            continue

        # Unordered list
        if re.match(r"^\s*[-*]\s+", line):
            list_lines, consumed = collect_list(lines, i, ordered=False)
            html_parts.append(render_list(list_lines, ordered=False))
            i += consumed
            continue

        # Otherwise: a paragraph (one or more consecutive non-blank lines)
        para_lines: list[str] = []
        while i < n and lines[i].strip() and not is_block_starter(lines[i]):
            para_lines.append(lines[i].strip())
            i += 1
        if para_lines:
            html_parts.append(f"<p>{render_inline(' '.join(para_lines))}</p>")

    return "\n".join(html_parts)


def is_block_starter(line: str) -> bool:
    s = line.lstrip()
    return (
        s.startswith("```")
        or s.startswith(">")
        or bool(re.match(r"^\d+\.\s+", s))
        or bool(re.match(r"^[-*]\s+", s))
    )


def collect_list(lines: list[str], start: int, *, ordered: bool) -> tuple[list[str], int]:
    """Collect contiguous list lines starting at `start`. Returns (lines, count)."""
    pattern = r"^\s*\d+\.\s+" if ordered else r"^\s*[-*]\s+"
    out: list[str] = []
    i = start
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            # Blank line — only break if the next non-blank isn't a continuation
            if i + 1 < len(lines) and re.match(pattern, lines[i + 1]):
                i += 1
                continue
            break
        if re.match(pattern, line) or (out and line.startswith(("  ", "\t"))):
            out.append(line)
            i += 1
            continue
        break
    return out, i - start


def render_list(lines: list[str], *, ordered: bool) -> str:
    tag = "ol" if ordered else "ul"
    pattern = r"^\s*(?:\d+\.|[-*])\s+"
    items: list[str] = []
    for line in lines:
        item = re.sub(pattern, "", line.strip())
        items.append(f"<li>{render_inline(item)}</li>")
    return f"<{tag}>\n" + "\n".join(items) + f"\n</{tag}>"


def render_table(lines: list[str]) -> str:
    rows = [parse_table_row(line) for line in lines if line.strip()]
    if len(rows) < 2:
        return ""
    header = rows[0]
    body = rows[2:]  # row 1 is the --- separator
    thead = (
        "<thead><tr>"
        + "".join(f"<th>{render_inline(c)}</th>" for c in header)
        + "</tr></thead>"
    )
    tbody_rows = "\n".join(
        "<tr>" + "".join(f"<td>{render_inline(c)}</td>" for c in row) + "</tr>"
        for row in body
    )
    return f"<table>\n{thead}\n<tbody>\n{tbody_rows}\n</tbody>\n</table>"


def parse_table_row(line: str) -> list[str]:
    stripped = line.strip()
    if stripped.startswith("|"):
        stripped = stripped[1:]
    if stripped.endswith("|"):
        stripped = stripped[:-1]
    return [cell.strip() for cell in stripped.split("|")]


def render_callout(lines: list[str]) -> str:
    """A blockquote becomes a callout. First **Label:** decides the kind."""
    text = " ".join(lines).strip()
    kind = "info"
    label_html = ""
    m = re.match(r"\*\*([^:*]+):\*\*\s*(.*)", text, re.DOTALL)
    if m:
        label = m.group(1).strip()
        body = m.group(2).strip()
        kind = CALLOUT_LABEL_TO_KIND.get(label.lower(), "info")
        label_html = f'<span class="callout-label">{html.escape(label)}</span>'
        text = body
    cls = "callout" if kind == "info" else f"callout {kind}"
    return f'<div class="{cls}">{label_html}{render_inline(text)}</div>'


# ---------------------------------------------------------------------------
# Section rendering
# ---------------------------------------------------------------------------

def render_hero(title: str, lede: str) -> str:
    if not title:
        return ""
    eyebrow = ""  # No eyebrow by default — Claude can fill it post-hoc if useful.
    lede_html = f'<p class="lede">{render_inline(lede)}</p>' if lede else ""
    return (
        '<header class="hero">\n'
        + (f'  <span class="eyebrow">{html.escape(eyebrow)}</span>\n' if eyebrow else "")
        + f"  <h1>{render_inline(title)}</h1>\n"
        + (f"  {lede_html}\n" if lede_html else "")
        + "</header>"
    )


def render_step(block: Block) -> str:
    num = extract_step_number(block.heading or "")
    title = strip_step_prefix(block.heading or "")
    body = render_body(block.lines)
    return (
        '<section class="step">\n'
        f'  <div class="step-circle">{html.escape(num)}</div>\n'
        '  <div class="step-body">\n'
        f"    <h2>{render_inline(title)}</h2>\n"
        f"    {body}\n"
        "  </div>\n"
        "</section>"
    )


def render_needs(block: Block) -> str:
    """Turn a list of `- **Thing** — description` items into a 3-card grid."""
    items = extract_list_items(block.lines)
    if not items:
        # Fall back to a plain section.
        return render_plain(block)
    cards: list[str] = []
    for item in items:
        m = re.match(r"\*\*([^*]+)\*\*\s*[—–\-]?\s*(.*)", item.strip(), re.DOTALL)
        if m:
            head = m.group(1).strip()
            body = m.group(2).strip()
        else:
            head, body = item.strip(), ""
        cards.append(
            '  <div class="need-card">\n'
            f"    <h3>{render_inline(head)}</h3>\n"
            f"    <p>{render_inline(body)}</p>\n"
            "  </div>"
        )
    title_html = (
        f'<div class="section-title">{render_inline(block.heading or "")}</div>'
    )
    return f'{title_html}\n<div class="needs">\n' + "\n".join(cards) + "\n</div>"


def extract_list_items(lines: list[str]) -> list[str]:
    """Pull `- ...` items out of a section body."""
    out: list[str] = []
    for line in lines:
        m = re.match(r"^\s*[-*]\s+(.*)$", line)
        if m:
            out.append(m.group(1))
    return out


def render_plain(block: Block) -> str:
    heading_html = (
        f"<h2>{render_inline(block.heading)}</h2>\n" if block.heading else ""
    )
    return heading_html + render_body(block.lines)


def render_section(block: Block) -> str:
    kind = classify(block)
    if kind == "step":
        return render_step(block)
    if kind == "needs":
        return render_needs(block)
    # troubleshooting and diagram fall through to plain — SKILL.md tells Claude
    # to inspect those after the script runs and decide whether to enrich them.
    return render_plain(block)


# ---------------------------------------------------------------------------
# Assembly
# ---------------------------------------------------------------------------

def assemble(md_text: str, template: str, *, source_name: str) -> str:
    title, lede, sections = split_blocks(md_text)
    full_text = md_text  # use the full doc to decide RTL, not just hero
    rtl = is_hebrew(full_text)

    body_parts: list[str] = []
    if title:
        body_parts.append(render_hero(title, lede))

    for block in sections:
        body_parts.append(render_section(block))

    body_html = "\n\n".join(p for p in body_parts if p)

    lang = "he" if rtl else "en"
    direction = "rtl" if rtl else "ltr"
    page_title = title or source_name

    return (
        template
        .replace("{{LANG}}", lang)
        .replace("{{DIR}}", direction)
        .replace("{{TITLE}}", html.escape(page_title))
        .replace("{{BODY}}", body_html)
    )


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Convert markdown to styled HTML.")
    parser.add_argument("input", type=Path, help="Path to the source .md file")
    parser.add_argument(
        "--output", "-o", type=Path, default=None,
        help="Output path (default: docs/guides/<input-stem>.html next to input)",
    )
    parser.add_argument(
        "--force", "-f", action="store_true",
        help="Overwrite existing output without prompting",
    )
    args = parser.parse_args(list(argv) if argv is not None else None)

    if not args.input.exists():
        print(f"error: input file not found: {args.input}", file=sys.stderr)
        return 2

    if args.output is None:
        # Walk up to find docs/guides; default to a sibling .html otherwise.
        guides = find_guides_dir(args.input)
        if guides is not None:
            output = guides / f"{args.input.stem}.html"
        else:
            output = args.input.with_suffix(".html")
    else:
        output = args.output

    if output.exists() and not args.force:
        print(
            f"error: {output} already exists. Re-run with --force to overwrite.",
            file=sys.stderr,
        )
        return 3

    template = TEMPLATE_PATH.read_text(encoding="utf-8")
    md_text = args.input.read_text(encoding="utf-8")
    rendered = assemble(md_text, template, source_name=args.input.stem)

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(rendered, encoding="utf-8")
    print(str(output))
    return 0


def find_guides_dir(input_path: Path) -> Path | None:
    """Walk up from input_path to find a docs/guides dir; return it if found."""
    for parent in input_path.resolve().parents:
        candidate = parent / "docs" / "guides"
        if candidate.is_dir():
            return candidate
    return None


if __name__ == "__main__":
    sys.exit(main())
