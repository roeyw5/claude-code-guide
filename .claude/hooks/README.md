# Claude Code Hooks

Pre-tool-use hooks that run before Claude executes commands, adding safety guardrails.

## Quick Start

1. Copy the hook scripts to `~/.claude/hooks/`
2. Add the hook configuration to your settings file (see Installation below)
3. Restart Claude Code

## Installation

### Where to Put Hooks

Hooks can be installed at two levels:

| Location | Settings File | Scope |
|----------|--------------|-------|
| **Global (all projects)** | `~/.claude/settings.json` | Applies to every Claude session |
| **Project-specific** | `<project>/.claude/settings.json` | Only applies to that project |

For safety hooks like these, **global installation is recommended**.

### Step 1: Copy Hook Scripts

```bash
mkdir -p ~/.claude/hooks
cp block-dangerous-commands.js ~/.claude/hooks/
cp protect-secrets.js ~/.claude/hooks/
chmod +x ~/.claude/hooks/*.js
```

### Step 2: Configure Settings

Add to `~/.claude/settings.json` (create if it doesn't exist):

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "node ~/.claude/hooks/block-dangerous-commands.js"
          }
        ]
      },
      {
        "matcher": "Read|Edit|Write|Bash",
        "hooks": [
          {
            "type": "command",
            "command": "node ~/.claude/hooks/protect-secrets.js"
          }
        ]
      }
    ]
  }
}
```

### Hook Matchers

The `matcher` field specifies which tools trigger the hook:

| Matcher | Triggers On |
|---------|-------------|
| `Bash` | Shell command execution |
| `Read` | File reads |
| `Write` | File creation |
| `Edit` | File modifications |
| `Read\|Edit\|Write\|Bash` | Multiple tools (regex OR) |

## Included Hooks

### block-dangerous-commands.js

Blocks destructive bash commands before execution:
- `rm -rf` on home/root directories
- Fork bombs (`:(){:|:&};:`)
- `dd` to disk devices
- `curl | sh` (remote code execution)
- Force push to main/master
- `git reset --hard`

### protect-secrets.js

Prevents reading/modifying/exposing sensitive files:
- `.env` files (allows `.env.example`, `.env.template`)
- SSH keys (`~/.ssh/id_*`)
- AWS/GCP/Azure credentials
- Blocks exfiltration via `curl`, `scp`, `rsync`

## Configuration

Both hooks use `SAFETY_LEVEL` (edit at top of each script):

| Level | Description |
|-------|-------------|
| `critical` | Only catastrophic operations (rm -rf ~, dd, fork bombs) |
| `high` | (default) + risky operations (force push main, secrets) |
| `strict` | + cautionary operations (any force push, sudo rm) |

## Logs

All blocked operations are logged to:
```
~/.claude/hooks-logs/YYYY-MM-DD.jsonl
```

View logs in real-time:
```bash
tail -f ~/.claude/hooks-logs/$(date +%Y-%m-%d).jsonl
```

## How Hooks Work

1. Before Claude runs a tool (e.g., Bash), the hook receives the tool input via stdin as JSON
2. The hook inspects the input and decides: allow or block
3. To **block**: output JSON with `"decision": "block"` and a `"reason"`
4. To **allow**: exit silently (no output or empty JSON)

Example block response:
```json
{"decision": "block", "reason": "rm targeting home directory"}
```

## Writing Custom Hooks

Hooks are any executable that:
- Reads tool input from stdin (JSON format)
- Outputs a decision to stdout (optional)

Minimal Node.js example:
```javascript
#!/usr/bin/env node
const input = JSON.parse(require('fs').readFileSync(0, 'utf8'));

if (input.tool_input.command.includes('dangerous')) {
  console.log(JSON.stringify({
    decision: 'block',
    reason: 'Command contains "dangerous"'
  }));
}
// No output = allow
```

## Verify Installation

Test that hooks are working with these **safe** commands. Even if the hook fails, these won't cause harm:

### Test block-dangerous-commands.js

| Command | Expected Block Reason |
|---------|----------------------|
| `echo $SECRET_KEY` | echoing secret variable |
| `echo $API_TOKEN` | echoing secret variable |

### Test protect-secrets.js

| Action | Expected Block Reason |
|--------|----------------------|
| `printenv` | Environment dump may expose secrets |
| Ask Claude to read `.env.example` | Should be **allowed** (allowlisted) |
| Ask Claude to read `.env` | Should be **blocked**: .env file contains secrets |

### Verify via logs

After testing, check if blocks were logged:
```bash
tail ~/.claude/hooks-logs/$(date +%Y-%m-%d).jsonl
```

Example log entry:
```json
{"ts":"...","level":"BLOCKED","id":"echo-secret","priority":"high","cmd":"echo $SECRET_KEY",...}
```

If commands execute instead of being blocked, verify your `settings.json` paths and restart Claude Code.

## Disable

Remove or comment out the hook entry in `~/.claude/settings.json`

## Troubleshooting

**Hook not running?**
- Check the path in settings.json is correct
- Ensure the script is executable (`chmod +x`)
- Verify Node.js is available in PATH

**Too many false positives?**
- Lower the `SAFETY_LEVEL` to `critical`
- Check logs to see what's being blocked
