---
name: remind
description: Ten-second briefing of this session for someone juggling many parallel Claude Code sessions — what it is doing and what it needs from you, answered from memory without re-reading history. Run it as /remind when you switch back to a session and have lost the thread.
disable-model-invocation: true
---

# Remind

The user has switched between many sessions and remembers nothing about this one. Your reply must let them steer it in ten seconds with zero context in their head.

Answer from the conversation so far. Do not run tools, read files, or check git to compose the reply. Reconstructing state that way is slower than the briefing it produces and can misreport what actually happened. If you genuinely cannot tell the state without a tool call, say so in the reply. If nothing has happened yet in this session, reply with one line saying so.

## Reply format, in this exact order

**1. `This session:`** One sentence: what the user originally asked for, in their own plain words, plus the location if it matters (repo, worktree, branch, environment). This is the headline they scan across every session, so keep it to one line.

**2. `Needs from you:`** A numbered list of everything blocked on the user, or the single line `Nothing — <working on X | finished, idle>`. Order:
   - Unanswered permission prompts or denied tool calls first. Name the exact command and what it unblocks.
   - Then decisions and questions, one per item. Each item is at most three sentences: the context a stranger needs, the question, and your recommended answer (`Recommend: …`), so the user can reply "1: yes, 2: as you suggest".
   - An item is something only the user can decide. Anything you can decide yourself is not an item. Decide it.

**3. `Status:`** Two to four bullets: done, in progress, not started. Only what changes what the user does next, and nothing already covered by an item above. Say plainly if nothing is committed or tests have not run.

Cap: about 150 words. No preamble, no recap, no proposing new work, no closing question beyond the numbered items. Code identifiers only where the user must act on them (a command to approve, a file to look at).

## Example

Original ask: rate limiting on an export endpoint. Mid-session, a pip install sits denied and two design questions surfaced.

```
This session: adding per-user rate limiting (10 req/min, redis) to /api/export, per your first message.

Needs from you:
1. Approve the pending `pip install fakeredis` prompt — the 6 tests I wrote cannot run without it.
2. The nightly cron job calls this endpoint as user "system" in ~40-call bursts, so the limiter will throttle it. Exempt it? Recommend: yes, allowlist "system".
3. Unauthenticated requests have no user id; I keyed them by IP on my own initiative. Keep that, or reject them? Recommend: keep.

Status:
- Limiter written and wired (src/api/middleware/rate_limit.py).
- Tests written, never run. Nothing committed.
```

## Common mistakes

| Mistake | Fix |
|---|---|
| Asks buried after a long recap | Asks are section 2, right after the headline |
| A "question" that is just a flag ("noting that I did X") | Make it a yes/no with a recommendation, or drop it |
| Asking the user to do your work ("want me to approve the install?") | The user approves; you wait. State what they must click |
| An item that assumes the user remembers the context | One sentence of context inside the item |
| Two decisions bundled in one item | Split them; the user answers by number |
| Running tools to reconstruct the state | Answer from memory; admit gaps |
| Status repeating what an item already said | Status holds only what the items did not |
