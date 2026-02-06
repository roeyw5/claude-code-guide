# Technical Review Summary: Claude Code Sandboxing

**Review Date**: 2026-01-04
**Article**: Claude Code Sandboxing.md

---

## Critical Issues

**Must be fixed before publication** - Factually incorrect information or broken code

### 1. Incorrect Incident Date

**Location**: Line 7, Opening paragraph
**Issue**: "On December 8, 2025, a developer named LovesWorkin posted on Reddit..."

**Problem**: The date is incorrect. According to multiple sources covering the incident, the article was published on December 16, 2025. The Hacker News discussion shows the Reddit post was made approximately 20 days before the December 16 reporting date, which would place it around late November 2025, not December 8.

**Evidence**:
- [GIGAZINE article published December 16, 2025](https://gigazine.net/gsc_news/en/20251216-claude-code-cli-mac-deleted/)
- [Hacker News discussion](https://news.ycombinator.com/item?id=46268222)

**Fix**: Either verify the exact Reddit post date or use more general language like "In late 2025" or "In November 2025." Remove the specific "December 8, 2025" date as it cannot be confirmed.

---

### 2. Misleading Sandbox Mode Description

**Location**: Lines 109-110, Step 2: Choose Your Mode
**Issue**: "1. **Sandbox BashTool, with auto-allow in accept edits mode** - Full autonomy..."

**Problem**: This conflates two separate features. According to official documentation, the two sandbox modes are:
1. Auto-allow mode (sandboxed commands run automatically)
2. Regular permissions mode (sandboxed commands still require approval)

The phrase "with auto-allow in accept edits mode" is not found in official documentation and creates confusion.

**Evidence**: [Claude Code Sandboxing Documentation](https://code.claude.com/docs/en/sandboxing)

**Fix**: Replace with accurate terminology:
```
1. **Auto-allow mode** - Sandboxed bash commands run automatically without permission prompts. Commands that cannot be sandboxed still require approval.
2. **Regular permissions mode** - All bash commands require permission, even when sandboxed.
```

---

### 3. Malformed Settings Path Reference

**Location**: Line 131
**Issue**: `"Add to your user settings (**`~/.claude/settings.json`**) or to your project's (**`.claude/settings.json`**`)` for team-wide enforcement."`

**Problem**: Malformed backtick sequence - extra closing backtick after the closing parenthesis.

**Fix**: Remove the stray backtick:
```
Add to your user settings (`~/.claude/settings.json`) or to your project's (`.claude/settings.json`) for team-wide enforcement.
```

---

## Warnings

**Should be fixed** - Outdated information, poor practices, incomplete examples

### 1. Unverified 84% Statistic Context

**Location**: Lines 20, 80
**Issue**: Uses "internal testing" when official documentation says "internal usage"

**Problem**: "Testing" implies controlled experiments, while "usage" refers to real-world operational experience. This is a subtle but meaningful distinction.

**Evidence**: [Anthropic engineering blog](https://www.anthropic.com/engineering/claude-code-sandboxing)
Official quote: "In our internal usage, we've found that sandboxing safely reduces permission prompts by 84%."

**Fix**: Change "internal testing" to "internal usage" to match official terminology.

---

### 2. VS Code Extension Sandboxing Availability Not Clarified

**Location**: Line 186
**Issue**: "The native sandboxing features described here are specific to Anthropic's Claude Code CLI. They may not be available in VS Code extensions..."

**Problem**: While correct, this could be more actionable. The VS Code extension does NOT support the `/sandbox` command.

**Evidence**: [Claude Code VS Code documentation](https://code.claude.com/docs/en/vs-code)

**Fix**: Replace with:
```
The native sandboxing features described here are specific to Anthropic's Claude Code CLI and are NOT available in the VS Code extension. To use sandboxing in VS Code, open the integrated terminal and run the `claude` CLI command directly. The CLI and extension share conversation history via `claude --resume`.
```

---

### 3. Windows Sandboxing Support Status Unclear

**Location**: Line 81
**Issue**: "**Catch:** Windows support planned but not yet available"

**Problem**: This is partially accurate but incomplete. Native sandboxing (using OS-level primitives) is not yet available for Windows, but Claude Code itself runs natively on Windows.

**Fix**: Clarify:
```
**Catch:** Native sandboxing (using OS-level security primitives) is not yet available for Windows. While Claude Code runs natively on Windows, Windows users should use Docker containers for sandboxed environments.
```

---

### 4. Devcontainer Template Location May Confuse Users

**Location**: Line 144
**Issue**: "Download Anthropic's [Dev Container template](https://github.com/anthropics/claude-code/tree/main/.devcontainer)"

**Problem**: The link points to a GitHub tree view, not a downloadable template. Users cannot "download" a single folder from GitHub's web interface.

**Fix**: Provide actionable instructions:
```
Clone Anthropic's repository and copy the .devcontainer folder:
```bash
git clone https://github.com/anthropics/claude-code.git
cp -r claude-code/.devcontainer /path/to/your/project/
```
Or download the three files individually from GitHub.
```

---

### 5. Vague "Sensitive Directories" Reference

**Location**: Line 54
**Issue**: "It can read most of your system to understand your environment, except certain sensitive directories blocked by default."

**Problem**: Doesn't specify which directories are blocked.

**Fix**: Add specificity:
```
It can read most of your system to understand your environment, with write access restricted to your current working directory. By default, Claude cannot modify system files in `/bin/`, shell configuration files like `~/.bashrc` and `~/.zshrc`, or directories you've explicitly denied. Custom denied paths can be configured via `sandbox.filesystem.deniedPaths` in `settings.json`.
```

---

### 6. Incomplete Configuration Example

**Location**: Section "Step 4: Fine-Tune Your Configuration"
**Issue**: Mentions `"allowUnsandboxedCommands": false` but doesn't show complete JSON structure

**Problem**: Users might not know the full structure needed, potentially creating invalid JSON.

**Fix**: Provide complete example:
```json
{
  "sandbox": {
    "allowUnsandboxedCommands": false
  }
}
```

---

## Notes

**Consider for improvement** - Minor issues, optimization opportunities

### 1. Claude Code Web Version Platform Support

**Location**: Line 92
**Issue**: "Run entirely in Anthropic's cloud at [claude.ai/code](https://claude.ai/code)."

**Enhancement**: Add important restrictions:
```
Run entirely in Anthropic's cloud at [claude.ai/code](https://claude.ai/code). Requires Claude Pro, Team, or Enterprise subscription. Currently in research preview and only supports GitHub repositories (GitLab and other platforms not supported).
```

---

### 2. iOS App Availability Not Mentioned

**Location**: Line 195
**Issue**: No mention of iOS app availability

**Enhancement**: Add to final recommendations:
```
- **Mobile:** Use Claude Code on iOS for coding on the go (research preview, requires Pro/Team/Enterprise subscription)
```

---

### 3. Settings Structure for `allowUnsandboxedCommands`

**Location**: Line 127
**Issue**: Setting structure incomplete - should be nested under `sandbox` object

**Fix**: Show correct nesting:
```json
{
  "sandbox": {
    "allowUnsandboxedCommands": false
  }
}
```

---

### 4. Security Warning Could Be Stronger

**Location**: Line 126
**Issue**: "`enableWeakerNestedSandbox: true` can help—but this considerably weakens security."

**Enhancement**: Expand explanation:
```
If you need Docker _inside_ a sandboxed environment, `enableWeakerNestedSandbox: true` can help—but this **considerably weakens security** by reducing filesystem and network isolation to maintain compatibility with nested containerization. Only use this in development environments with non-sensitive data.
```

---

### 5. Git Credentials Proxy Mechanism Unexplained

**Location**: Line 95
**Issue**: "Git credentials handled by secure proxy" - doesn't explain how

**Enhancement**: Clarify the mechanism:
```
**Result:** Zero local risk. Git operations use secure OAuth integration with GitHub - you never share credentials directly with Anthropic. Each session runs in an isolated cloud environment.
```

---

### 6. Missing Platform Context for File Paths

**Location**: Line 131
**Issue**: Uses Unix-style path (`~/`) without Windows equivalent

**Enhancement**: Add note:
```
Add to your user settings (`~/.claude/settings.json` on Linux/macOS)
```

---

### 7. Docker Socket Mount Warning Could Show Anti-Pattern

**Location**: Line 170
**Issue**: Warning about Docker socket mounting doesn't show what to avoid

**Enhancement**: Add example:
```yaml
# DON'T DO THIS unless you understand the security implications
volumes:
  - /var/run/docker.sock:/var/run/docker.sock
```

---

## Summary

**Total Issues Found**: 16
- Critical: 3 (must fix)
- Warnings: 6 (should fix)
- Notes: 7 (consider)

**Technologies Verified**: Claude Code CLI, Native sandboxing (Bubblewrap/Seatbelt), Docker containers, VS Code Dev Containers, Claude Code on the web

**Official Sources Consulted**: 8
- Claude Code Sandboxing Documentation
- Claude Code Settings Reference
- Anthropic Engineering Blog
- Claude Code VS Code Documentation
- Claude Code on the Web Documentation
- GitHub Repository
- GIGAZINE incident coverage
- Hacker News discussions

---

## Priority Recommendations

### Phase 1: Critical Fixes (30 minutes)
1. Fix incorrect incident date (line 7)
2. Correct sandbox mode terminology (lines 109-110)
3. Fix malformed backtick in settings path (line 131)

### Phase 2: Warnings (1 hour)
4. Change "internal testing" to "internal usage" (lines 20, 80)
5. Clarify VS Code extension limitations (line 186)
6. Update Windows sandboxing status (line 81)
7. Fix devcontainer download instructions (line 144)
8. Specify sensitive directories (line 54)
9. Add complete JSON configuration examples

### Phase 3: Enhancements (30 minutes)
10. Add platform restrictions for web version
11. Mention iOS app availability
12. Strengthen security warnings
13. Add platform-specific path notes

**Overall Assessment**: Technically sound article with strong content. Main issues are factual accuracy (date, terminology) and incomplete configuration examples. With recommended fixes, this will be publication-ready.
