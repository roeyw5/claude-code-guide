# Plan guide (phase 6)

Save as `docs/plans/YYYY-MM-DD-<game>.md`. If the session has a dedicated plan-writing skill (for example superpowers `writing-plans`), use it and apply the game-specific points below on top. Otherwise follow this guide.

## What a plan is

The set of decisions the builder cannot make alone: which files, which names and signatures, which values from the spec, which tests prove each task. Not the code. A plan longer than the code it describes has written the code instead; a plan with lines like "handle edge cases" decided nothing.

## Header

- Goal (one sentence), architecture (2-3 sentences), tech stack, path to the spec ("read the spec in full first").
- **Unattended rule:** "Where this plan and the spec disagree, the plan wins; list each deviation in README's 'Deviations from spec'." A plan that says "stop and ask" stalls an overnight run.
- **Global constraints:** one line each, exact values (sizes, palettes, fonts, scoring formula, storage keys, git rules, the exact test command).
- **Review focus:** the five inputs or conditions most likely to bite a real player that no task's tests cover yet (reload mid-action, key mashing, odd selections, blocked storage, small windows). For each, add the pinning test to the task that owns the code.

## Tasks

Each task is the smallest unit with its own test cycle that a reviewer could reject on its own. For each: files (create/modify), an **Interfaces** block (what it consumes from earlier tasks and produces for later ones, with exact names and signatures), then steps: failing test (names and assertions with the spec's values), run and see it fail, implement (signature and file), run and see it pass, smoke if visual, commit.

A typical order for a browser game:

1. Data pipeline (if content-driven): curation file, build script, generated data, data tests.
2. Core logic with no DOM: run or level state, scoring, save/load, seeded randomness. Unit-tested.
3. Shell: page layout, fonts, input, scene manager, audio, a debug hook (`?debug=1`) that later smokes use to jump to states.
4. Art: palettes, sprites, tiles as data, with a sprite-sheet dev page.
5. World or levels: maps as data, movement, collision, a validator (reachability by BFS, density, unique ids).
6. Content: dialogue, puzzles, items, with a content validator (every referenced id exists). For study games, the task also checks every authored line against the question bank for lines that state an answer's deciding fact.
7. The main interaction screen (battle, level, puzzle).
8. Flow: progression, the final challenge, saving and resuming at every step.
9. End screen and a full-run smoke.

## Self-check before review

- Every spec section maps to a task.
- Every name used in a later task is defined, with the same spelling and signature, in an earlier task's Interfaces block. Name one owner for shared live state (for example `Game.state`), or two implementers will invent two.
- Every task's smoke only needs things built by that task or earlier.
- Every feature a task touches that arrives later has a stated stub. The world task places trainers before battles exist and shows a set name before the content file exists: say what it does meanwhile (a placeholder line through one named function the later task replaces, a fallback label), or each implementer invents its own.
- The test command actually works on this machine (run it once on an empty test).
- Read `browser-game-gotchas.md` and fold the relevant ones into Global Constraints.
