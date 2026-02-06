---
description: 'Cross-check technical claims or assumptions by getting a second opinion from another LLM. Use when you want to verify something discussed in the current session — e.g., "/doublecheck Redis SCAN is O(1) per call".'
---

# Double Check

Get a second opinion from another LLM to verify technical assumptions, claims, or decisions made during the current conversation.

## Prerequisites

Requires a CLI-accessible LLM. Default: `gemini`. Replace with any tool that accepts piped input (e.g., `llm`, `ollama run`, `sgpt`).

## Instructions

1. Identify the claim or assumption to verify — use `$ARGUMENTS` if provided, otherwise extract from conversation context
2. Build a verification prompt using the template below
3. Run it:
```bash
echo '<verification_prompt>' | gemini
```
4. Compare the response against our current understanding

## Prompt Template

```
I need you to verify the following technical claim. Be precise and cite official documentation where possible.

**Context:** [Brief description of what we're building or discussing]

**Claim to verify:** [The specific technical statement or assumption]

**Verification questions:**
1. Is this claim accurate? If not, what is correct?
2. Are there caveats, edge cases, or version-specific differences?
3. What does the official documentation say about this?

Please provide sources/links for your answers.
```

## Output Format

Present the response with a clear verdict:

- **Confirmed** — the claim holds, summarize supporting evidence
- **Partially correct** — note what's accurate and what needs correction
- **Contradicted** — explain the discrepancy, present both sides, and suggest how to resolve (e.g., check a specific doc page, test it, read source code)

$ARGUMENTS
