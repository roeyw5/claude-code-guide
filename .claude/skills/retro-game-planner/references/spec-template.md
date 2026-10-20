# Spec template (phase 5)

Save as `docs/specs/YYYY-MM-DD-<game>-design.md` in the game folder. Write for a talented builder who will never talk to the person. Keep it to what the game is and why; the how belongs in the plan. Mark every decision as the person's or yours.

```markdown
# <Game title>: design

Status: <draft|reviewed>, <date>.

## 1. Intent
Who it is for, the reference game, the twist, and why it is worth building. What a good session feels like and how long it is.

## 2. Goals, non-goals, anti-goals
Goals. Non-goals (explicitly out of this version, including "later phase" ideas). Anti-goals: things that make it a failure even if it works (softlocks, a score that lies, the wrong look, trademarked names, characters or logos, real people, wrong facts).

## 3. Content (if any)
Source files and fields. Measured facts (counts, variants, longest item). Curation: approved drops, text fixes, player-facing notes, each by id. How content is split into sets or levels, and the split's determinism.

## 4. A session, start to finish
Numbered: title, first choice, the world or levels, encounters, the final challenge, the end screen.

## 5. Main screens
For each: layout with sizes (fixed vs flexible parts, max width), what each region shows, fonts, states (before/after an action). Approved mockup files, plus the list of mockup elements that were later retired. "Where a mockup and this spec disagree, the spec wins."

## 6. The world / levels
Areas, density ("something to interact with always on screen"), obstacles and puzzles and their rules (retryable, scored or not), items and collectibles and what they affect.

## 7. Rules and scoring
Formula, pass line, two worked examples. Failure handling. Softlock rules.

## 8. End screen
What it shows and what the player can do next.

## 9. How it is built
Tech stack and the reason, how it is run (double-click index.html? local server?), controls, persistence, audio, where authored content lives so the person can review it, and the data check script.

## 10. Left to the builder
The list of things the builder decides freely (names, art, jokes, map layouts).

## 11. Decisions log
Settled with the person. Your calls (to check while reading). Pending: should be "nothing" before the plan starts.
```

Before handing the spec over, check: every number in it was computed from the data, not remembered; every anti-goal has a rule somewhere that prevents it; "pending" is empty.
