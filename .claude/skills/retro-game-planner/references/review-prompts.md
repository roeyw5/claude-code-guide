# Review prompts

Dispatch each as a fresh subagent that has not seen the conversation. Fill in the paths. All reviewers are read-only: tell them so, and tell them not to run git commands that change state. Their final message is their report.

## Content audit (phase 2, content-driven games)

```
You are auditing a <domain> question/content bank that will feed a study game. Default verdict for every item is KEEP; a drop needs a concrete reason.

File (read-only, do not modify anything): <path>. Fields: <fields>.

Check every item for: outdated facts (cite a source URL for each), a wrong answer key, broken or cut-off text, two equally defensible answers, duplicates or near-duplicates (keep the better-written one), and items far outside the stated scope.

Try to refute each of your own drop calls before reporting.

Report: a summary line; a table of proposed DROPs (id, category, one-sentence reason, source); a table of KEEP-with-note (id, the note a player should see); any key you think should change (old, new, source). Be terse.
```

## Spec builder-check (phase 5)

```
You are a talented browser-game engineer. You've been handed a design document and asked to plan the build. You cannot talk to its author.

Read <spec path>. Also check its claims against <data paths> and <mockup paths>; where prose and data disagree, the data wins: report the mismatch.

Report only the questions you would still need answered before planning well: places where you'd have to guess and a wrong guess would matter. For each, the question and why the answer changes the plan, ranked by importance. Also report internal contradictions and anything infeasible as written (for example, something that cannot work from file://), with evidence.

Skip what the document leaves to the builder, what you could decide yourself, and wording nitpicks. If nothing important is left, say "nothing important left".
```

## Plan review (phase 6)

```
You are reviewing an implementation plan that will be executed unattended by a fresh session with nobody to ask, so every gap becomes a guess at 3am.

Read in full: the spec <path>, the plan <path>, and the data <paths> (check every data claim the plan makes against it: counts, ids, strings, field names).

Refute the plan, don't confirm it: assume a defect until shown otherwise. Look for:
1. Spec requirements with no task, or tasks that contradict the spec.
2. Wrong data claims or arithmetic.
3. Interface mismatches between tasks (names, signatures, state fields), and shared state with no owner.
4. Tests that cannot pass as written, or pass without proving the behaviour.
5. Ordering problems: a task's test or smoke needs something only a later task builds.
6. Things that break an unattended run: steps needing a human, network steps without a fallback, tools that may not exist in the build session, commands that fail on this machine (run them), "stop and ask" instructions.
7. Places where the plan writes the code or decides nothing.

For each finding: severity (BLOCKER/MAJOR/MINOR), location, evidence (quote or computed value), concrete fix. Mark guesses UNVERIFIED. Most severe first. Then list what you verified as correct, so the executor can trust it.
```
