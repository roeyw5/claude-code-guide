---
name: editorial-review
description: Comprehensive editorial review of articles for grammar, flow, readability, and SEO optimization. Checks language quality, content structure, and discoverability. Use when polishing articles before publication.
allowed-tools: Read, Grep, Glob, Task, Write
---

You are performing a comprehensive editorial review of a technical article. Your task is to check grammar, flow, structure, and SEO optimization.

# Instructions

When invoked with an article filename (e.g., `/editorial-review "article.md"`):

1. **Read the article** using the Read tool
2. **Launch specialized review agents in parallel** using the Task tool:
   - `grammar-editor` agent (model: haiku) - Check spelling, grammar, punctuation, clarity, voice
   - `flow-reviewer` agent (model: sonnet) - Analyze structure, transitions, readability
   - `seo-optimizer` agent (model: haiku) - Review title, headers, keywords, discoverability

3. **Consolidate findings** from all agents into a single summary document

4. **Write the summary** to `EDITORIAL_REVIEW_SUMMARY.md` with this structure:

```markdown
# Editorial Review Summary: [Article Name]

**Review Date**: [Date]
**Article**: [Filename]

---

## Grammar & Language Issues

### Critical (Must Fix)
[Issues that confuse meaning or are factually wrong]

### Important (Should Fix)
[Grammatical errors, unclear sentences]

### Style Improvements
[Suggestions for better clarity and professionalism]

---

## Flow & Structure Issues

### Structure Problems
[Document organization, section ordering issues]

### Transition Issues
[Missing connections between sections]

### Readability Concerns
[Dense passages, confusing flow]

---

## SEO Optimization Opportunities

### Critical (Must Fix)
[Missing title, H1, or essential meta elements]

### Important (Should Fix)
[Significant optimization opportunities]

### Suggestions
[Nice-to-have improvements for better discoverability]

---

## Summary

**Total Issues Found**: X
- Grammar: X Critical, X Important, X Style
- Flow: X Structure, X Transitions, X Readability
- SEO: X Critical, X Important, X Suggestions

**Priority**: Fix Critical issues first, then Important, then consider Style/Suggestions.
```

# Agent Prompts

When launching agents, use these prompts:

## Grammar-Editor Agent
```
Review the article at [FILENAME] for grammar, spelling, punctuation, and clarity.

Check for:
- Spelling errors and typos
- Grammatical mistakes
- Punctuation issues
- Unclear or wordy sentences
- Inconsistent voice or tone
- Technical writing standards

For each issue found, provide:
- Location (section/paragraph)
- The problematic text
- Why it's an issue
- Suggested correction
- Severity: Critical/Important/Style

Return a structured list of all findings.
```

## Flow-Reviewer Agent
```
Analyze the article at [FILENAME] for structure, flow, and readability.

Check for:
- Document organization and section ordering
- Logical progression of ideas
- Paragraph and section transitions
- Readability and scannability
- Heading hierarchy
- Dense or confusing passages
- Opening hook effectiveness
- Conclusion strength

For each issue found, provide:
- Location (section/paragraph)
- The problematic area
- Why it's an issue
- Suggested improvement
- Severity: Structure/Transition/Readability

Return a structured list of all findings.
```

## SEO-Optimizer Agent
```
Review the article at [FILENAME] for SEO and discoverability.

Check for:
- Title optimization (should be compelling, include keywords)
- H1 heading (should match title intent)
- Header keyword usage (H2, H3)
- Keyword density and placement
- Meta description potential (first paragraph quality)
- Internal linking opportunities
- Tags and categories appropriateness
- Content readability metrics
- Search intent alignment

For each issue found, provide:
- Location
- The current state
- Why it matters for SEO
- Suggested optimization
- Severity: Critical/Important/Suggestion

Return a structured list of all findings.
```

# Implementation Steps

1. Parse the argument to get the article filename
2. Verify the file exists using Read
3. Launch all three agents in parallel with a single message containing three Task tool calls
4. Wait for all agents to complete
5. Consolidate their findings
6. Remove duplicates
7. Categorize by severity
8. Write the summary document
9. Report completion to the user

# Output to User

After completing the review, output:

```
✓ Editorial review complete for: [filename]

Summary:
  Grammar: X Critical, X Important, X Style
  Flow: X Structure, X Transitions, X Readability
  SEO: X Critical, X Important, X Suggestions

Full review saved to: EDITORIAL_REVIEW_SUMMARY.md
```
