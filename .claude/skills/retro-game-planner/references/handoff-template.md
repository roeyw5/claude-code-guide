# Handoff (phase 7)

The handoff prompt goes inline in your reply, in a code block, ready to paste into a fresh session. Do not save it to a file unless asked.

## What goes in it

Only what the fresh session cannot read anywhere else. It will read the spec and plan, and any instruction files in the folder, on its own. So the prompt carries:

- The folder path and the order to read things: spec first, then plan.
- **Step 0:** a fresh-eyes review of the plan against the current folder and data, fixing the plan in place before building.
- How to execute: task by task with a fresh subagent per task and a fresh reviewer after each, if the session supports subagents; otherwise inline, task by task, running each task's tests before moving on. If the session can pick models, the reviewer should be a different model than the implementer.
- **Rulings:** the options the person rejected during design, so the builder does not resurrect them (especially anything still visible in a mockup).
- **Exceptions granted for this run only:** for example "run all tasks without pausing", "push to origin main after each task, never force". Never invent permissions the person did not give.
- **Never stall:** on an ambiguity, pick the option most consistent with the spec's anti-goals, record it in README's "Deviations from spec", continue. Stop only for something destructive, a credential, or anything outside the game folder.
- **Reviewer brief:** reviewers refute rather than confirm, and check every domain fact in the content files (jokes fine, wrong facts are defects) and, for study games, every authored line against the question bank for hints.
- Gotchas discovered during design that are not written in the spec or plan.
- **The morning report:** what shipped per task (with commit ids), the final test count, each smoke as PASS / FAIL / NOT RUN, the deviations, what was skipped, which content files the person should proofread, and how to play.

## Pre-launch checklist (give this to the person, outside the prompt)

1. Start the session in the game folder.
2. Pick the model (the strongest available for an unattended multi-hour build).
3. If the plan uses a browser tool through a project MCP server, approve it at session start and check one call works (for example open about:blank).
4. Use an auto / pre-approved permission mode, or the run stalls on the first prompt.
5. Keep the machine awake and plugged in.
6. If the plan pushes to a remote, make sure the remote exists and the session's git credentials work.
7. Expect hours, not minutes. For scale: a 9-task plan run with a fresh implementer and a reviewer per task, plus a final whole-build review, took a little over 3 hours, with 3 of the 9 tasks needing one fix round.
