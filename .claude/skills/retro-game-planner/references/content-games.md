# Games driven by the player's own content

Quiz games, vocabulary games, story games and level packs run on data the person supplies. The data's real shape should drive the design, so inspect it before mockups.

## 1. Measure the data

Run a short script (Python or Node, read-only) and report back in plain words:

- How many items, how they are grouped, which fields exist (and which do not: a "topic" field the design assumes may not exist).
- Variants that need their own UI: multi-answer questions ("choose two"), odd option counts, images, code blocks.
- **Length distribution:** median and maximum characters for each displayed field, and the single longest item. The longest item is the layout's real requirement.
- Formatting noise: stray newlines mid-sentence, HTML, typos.
- Any existing review notes or flags in the data.

Correct the person's mental model with the numbers ("it's 186 questions, not 65", "the longest question is 1,500 characters, so it can't fit a dialog box").

## 2. Decide the answering mechanic early

Free-text answers graded by an AI model sound great and add an API key, a running cost, latency and grading disputes. Multiple choice needs none of that. If the source has free-text answers and they want multiple choice, wrong options can be generated once at plan time and reviewed by the person, so the game itself needs no model.

## 3. Audit before splitting

Before the content is cut into levels or sets, dispatch a fresh subagent to audit it (prompt in `review-prompts.md`): stale facts, wrong answer keys, broken or cut-off items, duplicates, ambiguous items. It proposes; the person approves every drop. Record approved drops, text fixes and player-facing notes in the spec, and have the build apply them with a script from a small curation file, never by hand-editing the source.

## 4. Split deterministically

If content is grouped into sets or levels, a build script does it once with a fixed seed and writes a generated data file. Same membership every time; shuffle order per run if the person wants variety. Spread special variants (multi-answer, hard items) evenly. A data check script verifies counts, uniqueness, keys and that drops stayed dropped.

## 5. Size sets to a sitting

Set size times seconds-per-item should match how long they said one sitting is. Recompute the scoring examples for the final set sizes (with 14 items, 10 correct is 714 of 1000, which fails a 720 line).
