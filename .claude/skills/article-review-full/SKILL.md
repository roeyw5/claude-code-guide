---
name: full-review
description: Complete article review combining technical accuracy verification and editorial quality checks. Orchestrates tech-review and editorial-review, then consolidates findings into a single prioritized report. Use when preparing articles for publication.
allowed-tools: Read, Grep, Glob, Task, Write, WebSearch, WebFetch
---

You are performing a comprehensive article review that combines both technical accuracy and editorial quality checks.

# Instructions

When invoked with an article filename (e.g., `/full-review "article.md"`):

1. **Read the article** to verify it exists
2. **Launch tech-review and editorial-review in parallel** using the Task tool
3. **Wait for both to complete**
4. **Read both summary files** (TECH_REVIEW_SUMMARY.md and EDITORIAL_REVIEW_SUMMARY.md)
5. **Consolidate findings** into a single prioritized report
6. **Write consolidated summary** to `FULL_REVIEW_SUMMARY.md`

# Workflow

## Phase 1: Parallel Review Execution

Launch both review skills simultaneously:

- **Technical Review**: Verifies technical accuracy and code quality
- **Editorial Review**: Checks grammar, flow, structure, and SEO

Both run in parallel to minimize total review time.

## Phase 2: Consolidation

After both reviews complete:

1. Read both summary files
2. Cross-reference findings (identify overlapping issues)
3. Prioritize by impact:
   - **Blockers**: Critical technical errors + missing title/keywords
   - **High Priority**: Technical warnings + important editorial issues
   - **Medium Priority**: Editorial style issues + SEO important items
   - **Low Priority**: Suggestions and nice-to-have improvements
4. Create unified action plan

## Phase 3: Output Generation

Write a consolidated summary with:

```markdown
# Full Review Summary: [Article Name]

**Review Date**: [Date]
**Article**: [Filename]
**Review Type**: Technical + Editorial (Full)

---

## Executive Summary

**Total Issues Found**: X
- **Blockers** (must fix before publication): X
- **High Priority** (should fix): X
- **Medium Priority** (recommended): X
- **Low Priority** (nice to have): X

---

## Blockers (Fix Before Publication)

[Critical technical errors and critical SEO issues]

### Technical Blockers
[Issues from tech review marked as Critical]

### Editorial Blockers
[Issues from editorial review marked as Critical]

---

## High Priority Issues

[Technical warnings and important editorial issues]

### Technical Warnings
[Issues from tech review marked as Warning]

### Editorial Important
[Issues from editorial review marked as Important]

---

## Medium Priority Issues

[Editorial style issues and important SEO items]

### Editorial Style & Structure
[Issues from editorial review marked as Style/Structure]

### SEO Optimization
[Issues from editorial review SEO section marked as Important]

---

## Low Priority Suggestions

[Nice-to-have improvements]

### Technical Notes
[Issues from tech review marked as Note]

### Editorial Suggestions
[Issues from editorial review marked as Suggestion]

### SEO Enhancements
[Issues from editorial review SEO section marked as Suggestion]

---

## Issue Breakdown by Category

### By Type
- Technical Accuracy: X issues (X critical, X warnings, X notes)
- Code Quality: X issues (X critical, X warnings, X notes)
- Grammar & Language: X issues (X critical, X important, X style)
- Flow & Structure: X issues (X structure, X transitions, X readability)
- SEO Optimization: X issues (X critical, X important, X suggestions)

### By Priority
- Blockers: X
- High Priority: X
- Medium Priority: X
- Low Priority: X

---

## Recommended Action Plan

### Phase 1: Blockers
Fix these before any other changes:

1. [Blocker 1 with location and fix]
2. [Blocker 2 with location and fix]
...

### Phase 2: High Priority
Address after blockers are fixed:

1. [High priority issue 1]
2. [High priority issue 2]
...

### Phase 3: Medium Priority
Polish and optimization:

1. [Medium priority issue 1]
2. [Medium priority issue 2]
...

### Phase 4: Low Priority (optional)
Enhancements if time permits:

1. [Suggestion 1]
2. [Suggestion 2]
...

---

## Detailed Review Files

For complete details, see:
- Technical review: `TECH_REVIEW_SUMMARY.md`
- Editorial review: `EDITORIAL_REVIEW_SUMMARY.md`

---

## Ready for Publication?

**Current Status**: [Yes/No - needs fixes]

**Remaining Work**:
- [ ] Fix X blocker issues
- [ ] Address X high priority issues
- [ ] Consider X medium priority improvements

**Once blockers and high priority issues are fixed, the article will be publication-ready.**
```

# Implementation Steps

1. **Parse argument** to get article filename
2. **Verify file exists** using Read tool
3. **Launch both review skills in parallel** using the Skill tool:
   - `/tech-review "[filename]"`
   - `/editorial-review "[filename]"`
4. **Wait for completion**
5. **Read both summary files**:
   - TECH_REVIEW_SUMMARY.md
   - EDITORIAL_REVIEW_SUMMARY.md
6. **Consolidate findings**:
   - Cross-reference overlapping issues
   - Categorize by priority (Blocker/High/Medium/Low)
   - Create action plan
7. **Write consolidated summary** to FULL_REVIEW_SUMMARY.md
8. **Report to user**

# Priority Mapping

## Blockers (Must Fix Before Publication)
- Tech Review: Critical issues
- Editorial Review: Critical SEO issues (missing title, no keywords)

## High Priority (Should Fix)
- Tech Review: Warnings
- Editorial Review: Important grammar/structure issues

## Medium Priority (Recommended)
- Editorial Review: Style issues
- Editorial Review: Important SEO items

## Low Priority (Nice to Have)
- Tech Review: Notes
- Editorial Review: Suggestions
- Editorial Review: SEO suggestions

# Cross-Reference Logic

When consolidating, identify overlapping issues:

**Example**: If a code block has both:
- Tech issue: "Syntax error in Python function"
- Editorial issue: "Code block lacks descriptive header"

**Consolidate as**:
```markdown
### Code Block at Line X (BLOCKER + High Priority)

**Technical**: Python syntax error - missing closing parenthesis
**Editorial**: Missing descriptive header for context

**Fix**:
1. Add closing parenthesis on line X
2. Add header: "**Deployment Parser Function**"
```

# Output to User

After completing the review, output:

```
✓ Full review complete for: [filename]

Summary:
  Blockers: X (must fix)
  High Priority: X (should fix)
  Medium Priority: X (recommended)
  Low Priority: X (nice to have)

Consolidated report: FULL_REVIEW_SUMMARY.md
Detailed reviews: TECH_REVIEW_SUMMARY.md, EDITORIAL_REVIEW_SUMMARY.md

Next steps:
1. Review FULL_REVIEW_SUMMARY.md for prioritized action plan
2. Start with Blockers section
3. Refer to detailed reviews for specific context
```

# Notes

- This skill runs tech-review and editorial-review as sub-skills
- Both run in parallel to minimize wait time
- The consolidated summary provides a single prioritized to-do list
- Detailed summaries remain available for deep-dive context
- Action plan groups related fixes for efficient batching
