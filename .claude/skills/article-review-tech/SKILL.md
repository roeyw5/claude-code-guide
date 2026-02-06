---
name: tech-review
description: Comprehensive technical review of articles and documentation. Verifies technical accuracy against official sources, validates code examples, and checks technical content quality. Use when reviewing technical articles before publication.
allowed-tools: Read, Grep, Glob, Task, Write, WebSearch, WebFetch
---

You are performing a comprehensive technical review of a technical article. Your task is to verify technical accuracy and validate code examples.

# Instructions

When invoked with an article filename (e.g., `/tech-review "article.md"`):

1. **Read the article** using the Read tool
2. **Launch specialized review agents in parallel** using the Task tool:
   - `technical-verifier` agent (model: sonnet) - Verify technical claims against official docs
   - `code-examples-checker` agent (model: sonnet) - Validate all code blocks and configurations

3. **Consolidate findings** from both agents into a single summary document

4. **Write the summary** to `TECH_REVIEW_SUMMARY.md` with this structure:

```markdown
# Technical Review Summary: [Article Name]

**Review Date**: [Date]
**Article**: [Filename]

---

## Critical Issues

**Must be fixed before publication** - Factually incorrect information or broken code

[List each critical issue with:]
- **Location**: [Section/Line]
- **Issue**: [What's wrong]
- **Evidence**: [Link to official docs or technical explanation]
- **Fix**: [Specific correction needed]

---

## Warnings

**Should be fixed** - Outdated information, poor practices, incomplete examples

[List each warning with same format as critical]

---

## Notes

**Consider for improvement** - Minor issues, optimization opportunities

[List each note with same format]

---

## Summary

**Total Issues Found**: X
- Critical: X (must fix)
- Warnings: X (should fix)
- Notes: X (consider)

**Technologies Verified**: [List of technologies checked]
**Official Sources Consulted**: [Number of official docs referenced]
```

# Agent Prompts

When launching agents, use these prompts:

## Technical-Verifier Agent
```
Verify the technical accuracy of the article at [FILENAME] against official documentation.

For each technical claim, technology, API, configuration, or feature mentioned:
1. Search for official documentation using WebSearch
2. Fetch and read official docs using WebFetch
3. Compare article claims with authoritative sources
4. Check for outdated or deprecated information
5. Validate version numbers and feature availability
6. Verify API signatures, parameters, and responses

Technologies to verify: Extract all technologies, frameworks, APIs, CLIs, and configurations mentioned in the article. Verify each against its official documentation.

For each issue found, provide:
- Location (section/paragraph/line)
- The claim or statement
- Why it's incorrect or outdated
- Evidence (official doc URLs)
- Suggested correction
- Severity: Critical/Warning/Note

Critical = Factually wrong or will not work
Warning = Outdated, deprecated, or poor practice
Note = Minor inaccuracy or improvement opportunity

Return a structured list of all findings with official source citations.
```

## Code-Examples-Checker Agent
```
Review all code blocks, commands, and configurations in the article at [FILENAME].

Check every code block for:
- Syntax errors
- Missing imports or dependencies
- Security issues (hardcoded credentials, injection vulnerabilities)
- Best practices violations
- Completeness (can it actually run?)
- Correct configuration syntax
- Proper error handling
- Language-specific issues

Check all code blocks regardless of language. Common languages include Python, JavaScript/TypeScript, Shell/Bash, JSON, YAML, and configuration files.

For each issue found, provide:
- Location (section/code block number)
- The problematic code
- Why it's an issue
- Security implications (if any)
- Suggested correction
- Severity: Critical/Warning/Note

Critical = Code won't work or has security vulnerability
Warning = Poor practice or incomplete example
Note = Minor improvement or optimization

Return a structured list of all findings.
```

# Implementation Steps

1. Parse the argument to get the article filename
2. Verify the file exists using Read
3. Launch both agents in parallel with a single message containing two Task tool calls
4. Wait for both agents to complete
5. Consolidate their findings
6. Remove duplicates
7. Sort by severity (Critical → Warning → Note)
8. Write the summary document
9. Report completion to the user

# Output to User

After completing the review, output:

```
✓ Technical review complete for: [filename]

Summary:
  Critical: X (must fix)
  Warnings: X (should fix)
  Notes: X (consider)

Full review saved to: TECH_REVIEW_SUMMARY.md
```
