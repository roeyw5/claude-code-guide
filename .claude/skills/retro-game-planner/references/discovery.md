# Discovery and game loop

## Territory to cover (never read this out as a list)

Pick the next question from whatever is least clear. Anchor questions in concrete moments.

**What it is**
- The reference game(s) and what exactly they loved about it: the walking around? the collecting? the battles? the music?
- The twist: what is different, and why does that make it worth building?
- Who plays: just them, friends, students, the public? This changes how careful the content must be. Trademarked names, characters, catchphrases and logos from the reference game, real brands' logos and real people should not appear in a shared game; plan original stand-ins.

**Why now / success**
- What does a good evening with this game look like? How long is one sitting?
- What would make them wince even if it technically works? (These become anti-goals: "looks too old", "too easy to cheat my own score", "a typo in a question".)

**Platform and controls**
- Desktop browser, phone, or both. Keyboard, mouse, touch, gamepad.
- Do not copy the reference hardware's limits by default. A classic 8-bit handheld screen is 160x144 pixels and its text box holds two short lines; a desktop browser does not need either. Ask which era's *look* they want (8-bit, 16-bit, later 32-bit handhelds) separately from screen size.

**Content**
- Does the game run on content they supply (questions, words, levels, story text)? If yes, get the files now and go to `content-games.md` before designing screens: the content's real shape decides the layout.

## The game loop (phase 4)

Settle each of these explicitly. The builder will otherwise guess.

1. **Core loop:** what the player does every 30 seconds, every 5 minutes, and once per session.
2. **Start:** title, new/continue, any meaningful first choice.
3. **Progression:** areas, levels, difficulty curve, what unlocks what.
4. **Win, lose, and end:** what ends a run, what the end screen shows, what happens next (replay, next level, next set).
5. **Failure handling:** what a wrong move costs. Can the player retry? Does a failure ever block progress?
6. **Scoring:** the exact formula and any pass line, with two worked examples (one just passing, one just failing).
7. **Items, collectibles, power-ups:** what each one does to difficulty or score. Cosmetic-only is a valid and often better answer.
8. **Persistence:** what survives closing the tab (current run, best scores, unlocks).
9. **Audio:** music, effects, mute key.

### Softlock check

Before leaving this phase, walk the rules looking for states the player cannot get out of:

- A gate that needs something the player may have permanently missed (a badge from a fight they lost and cannot redo).
- A required target the player cannot find (the last trainer hidden somewhere in a big map). Fix with counters, pointers, or by not requiring all of them.
- Resume after reload landing in a state the code did not expect (mid-battle, mid-dialog, after an answer was recorded but before the screen moved on).

Every gate should be either always solvable (retryable puzzles) or optional.

### Faithfulness check (for study, practice or simulation games)

If the score is meant to mean something outside the game (an exam score, a typing speed), anything that inflates it (hints, 50/50s, retries, helper items) breaks the point of the game. Ask explicitly, and record the answer as a rule.

The quiet version of a hint is authored flavour text. "Funny but accurate" NPC tips, puzzle replies and item descriptions in the same domain will, sooner or later, state the deciding fact of a question in the bank. In one build a guard dog outside the final boss explained exactly what the service it was named after does, one screen before the boss asked about that service. Make the rule explicit in the spec: flavour text may joke about the domain but must not state a fact that decides any answer in the bank, and the content task checks every line against the bank.

**Sharing.** If friends or the public will play it, ask how they will get it. A game built from separate files is a folder, not one HTML file: plan either a zip of the runtime files or a single-file build step. And check whether they may redistribute the content (practice-question banks often may not be shared).
