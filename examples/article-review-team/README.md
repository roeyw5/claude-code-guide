# Article Review System for Claude Code

A comprehensive article review system that uses Claude Code skills and agents to perform technical accuracy verification, editorial review, and SEO optimization of markdown articles.

## Overview

This package provides an automated article review pipeline that combines:

- **Technical Review**: Verifies technical claims against official documentation and validates code examples
- **Editorial Review**: Checks grammar, flow, structure, and SEO optimization
- **Full Review**: Orchestrates both technical and editorial reviews in parallel

## Architecture

The system uses a hierarchical orchestration pattern where skills launch specialized agents:

```
/full-review
    |
    +-- /tech-review (skill)
    |       |-- technical-verifier (agent) - Verifies claims against official docs
    |       +-- code-examples-checker (agent) - Validates code blocks and commands
    |
    +-- /editorial-review (skill)
            |-- grammar-editor (agent) - Spelling, grammar, punctuation
            |-- flow-reviewer (agent) - Structure, transitions, readability
            +-- seo-optimizer (agent) - Title, headers, keywords, discoverability
```

### Components

| Component | Type | Model | Purpose |
|-----------|------|-------|---------|
| full-review | Skill | - | Orchestrates tech + editorial reviews |
| tech-review | Skill | - | Orchestrates technical verification |
| editorial-review | Skill | - | Orchestrates editorial checks |
| technical-verifier | Agent | sonnet | Verifies technical accuracy via web search |
| code-examples-checker | Agent | sonnet | Validates code syntax and security |
| grammar-editor | Agent | haiku | Checks grammar, spelling, clarity |
| flow-reviewer | Agent | sonnet | Analyzes document structure and flow |
| seo-optimizer | Agent | haiku | Optimizes for search discoverability |

## Installation

### Option 1: Project-Level Installation (Recommended)

Copy the `.claude` directory to your project root:

```bash
cp -r ~/article-review-package/.claude /path/to/your/project/
```

This makes the skills available only within that project.

### Option 2: User-Level Installation

Copy to your user Claude configuration to make skills available in all projects:

```bash
# Create directories if they don't exist
mkdir -p ~/.claude/skills ~/.claude/agents

# Copy skills and agents
cp -r ~/article-review-package/.claude/skills/* ~/.claude/skills/
cp -r ~/article-review-package/.claude/agents/* ~/.claude/agents/
```

## Usage

### Full Review (Recommended)

Run a complete technical and editorial review:

```
/full-review "article.md"
```

**Output**: Creates `FULL_REVIEW_SUMMARY.md` with prioritized findings from both reviews.

**Duration**: 5-10 minutes (runs tech and editorial reviews in parallel)

### Technical Review Only

Verify technical accuracy and code examples:

```
/tech-review "article.md"
```

**Output**: Creates `TECH_REVIEW_SUMMARY.md`

**What it checks**:
- Technical claims against official documentation
- API references and version numbers
- Code syntax and completeness
- Security issues in examples
- Dangerous commands that could harm users

### Editorial Review Only

Check grammar, flow, and SEO:

```
/editorial-review "article.md"
```

**Output**: Creates `EDITORIAL_REVIEW_SUMMARY.md`

**What it checks**:
- Grammar, spelling, punctuation
- Document structure and transitions
- Opening hook effectiveness
- Redundancy and dangling references
- Title optimization and keyword usage
- Readability and scannability

## Output Files

Each review generates a markdown summary file:

| Review | Output File | Contents |
|--------|-------------|----------|
| Full | `FULL_REVIEW_SUMMARY.md` | Consolidated, prioritized findings |
| Tech | `TECH_REVIEW_SUMMARY.md` | Technical accuracy issues |
| Editorial | `EDITORIAL_REVIEW_SUMMARY.md` | Grammar, flow, SEO issues |

### Issue Severity Levels

**Full Review** uses 4-tier prioritization:
- **Blockers**: Must fix before publication
- **High Priority**: Should fix
- **Medium Priority**: Recommended
- **Low Priority**: Nice to have

**Tech Review** uses 3-tier severity:
- **Critical**: Factually incorrect or broken code
- **Warning**: Outdated or poor practices
- **Note**: Minor improvements

**Editorial Review** categorizes by type:
- **Grammar**: Critical / Important / Style
- **Flow**: Structure / Transition / Readability
- **SEO**: Critical / Important / Suggestion

## Agent Details

### technical-verifier

**Purpose**: Verifies technical claims against official documentation

**Key Features**:
- Fetch-first approach: Always fetches full documentation pages
- Prioritizes official sources (docs.anthropic.com, github.com/anthropics, etc.)
- Checks API signatures, version numbers, deprecated features
- Validates file paths and setting names

**Tools Used**: Read, Grep, Glob, WebSearch, WebFetch

### code-examples-checker

**Purpose**: Validates code examples, commands, and configurations

**Key Features**:
- Syntax validation across multiple languages (Python, JS, Shell, JSON/YAML)
- Security checks (hardcoded credentials, injection vulnerabilities)
- Dangerous command detection (rm -rf, chmod 777, etc.)
- Completeness verification (missing imports, dependencies)

**Tools Used**: Read, Grep, Glob

### grammar-editor

**Purpose**: Checks spelling, grammar, punctuation, and clarity

**Key Features**:
- Grammar and mechanics (subject-verb agreement, verb tense)
- Spelling and typo detection
- Clarity improvements (active voice, wordiness)
- Formatting consistency (commands, file paths, code elements)

**Tools Used**: Read, Grep, Glob

### flow-reviewer

**Purpose**: Analyzes document structure, transitions, and readability

**Key Features**:
- Opening hook evaluation (first 3 paragraphs critical)
- Section ordering and logical progression
- Redundancy detection between sections
- Dangling reference detection (promises without delivery)
- Cognitive load assessment

**Tools Used**: Read, Grep, Glob

### seo-optimizer

**Purpose**: Optimizes articles for search engines and discoverability

**Key Features**:
- Title optimization (50-60 characters, keyword placement)
- Header structure and keyword usage
- Meta description quality
- Content readability metrics
- Internal/external linking opportunities

**Tools Used**: Read, Grep, Glob

## Customization

### Modifying Agent Behavior

Edit the agent files in `.claude/agents/` to customize:

- **Severity thresholds**: Adjust what counts as Critical vs Warning
- **Check patterns**: Add domain-specific validation rules
- **Output format**: Modify the issue reporting structure

### Adding New Agents

1. Create a new `.md` file in `.claude/agents/`
2. Include the frontmatter:
   ```yaml
   ---
   name: my-agent
   description: What this agent does
   tools: Read, Grep, Glob
   model: haiku  # or sonnet
   ---
   ```
3. Add the agent instructions below the frontmatter
4. Reference the agent in a skill using the Task tool

### Creating New Skills

1. Create a directory in `.claude/skills/your-skill-name/`
2. Create `SKILL.md` with frontmatter:
   ```yaml
   ---
   name: your-skill
   description: What this skill does
   allowed-tools: Read, Grep, Glob, Task, Write
   ---
   ```
3. Add orchestration instructions that launch agents via Task tool

## Requirements

- Claude Code CLI or VS Code extension
- Claude Pro, Team, or Enterprise subscription (for web search capabilities)

## Example Workflow

1. Write your technical article in markdown
2. Run `/full-review "my-article.md"`
3. Review `FULL_REVIEW_SUMMARY.md` for prioritized issues
4. Fix Blockers first, then High Priority issues
5. Re-run review to verify fixes
6. Publish when no Blockers remain

## Troubleshooting

### Skills Not Appearing

- Verify files are in `.claude/skills/` with `SKILL.md` inside subdirectories
- Restart Claude Code after adding new skills
- Check frontmatter syntax (YAML between `---` markers)

### Agents Not Found

- Verify agent files are in `.claude/agents/`
- Check that agent names match references in skills
- Ensure frontmatter includes required fields (name, description, tools, model)

### Web Search Failures

- technical-verifier requires WebSearch/WebFetch tools
- Ensure you have Claude Pro, Team, or Enterprise subscription
- Some official docs may require direct URL fetching

## License

This package is provided as-is for use with Claude Code.
