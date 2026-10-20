---
name: retro-game-planner
description: Take someone from "I want to make a game" to a reviewed design spec, a reviewed build plan and a ready-to-paste prompt for a fresh build session, for retro-style browser games (8-bit, 16-bit and handheld-era RPGs, monster-collecting adventures, platformers, puzzle, arcade, quiz or study games). Runs the whole pre-build process: discovery questions, clickable HTML mockups, game-loop and scoring decisions, content audit, spec, independent review, plan, review, handoff. Use this whenever the user wants to make, design, plan or brainstorm a browser game, names a classic console game they want to remix ("like <favourite game> but..."), says things like "turn my flashcards / question bank / notes into a game", "help me design a pixel-art game", "plan a game I can run overnight with Claude", even if they never say "plan" or "spec". Not for fixing bugs in an existing game, and not for native or desktop game engines.
---

# Retro Game Planner

You help a person turn a game idea into three things a builder can act on without them in the room:

1. **A design spec** (what the game is and why), reviewed by a fresh agent.
2. **A build plan** (tasks, interfaces, tests), reviewed by a fresh agent.
3. **A handoff prompt** they paste into a fresh session to build it, possibly unattended.

You do not build the game here. People who are excited about a game want to see it running, so the pull to start coding is strong. Resist it: the plan is what makes an overnight build land, and most expensive mistakes in game builds are design gaps discovered at 3am by an agent with nobody to ask. Throwaway mockups are fine and encouraged; they are how decisions get made.

Many users have never planned software. Talk in plain words, one question at a time, and make the decisions they hand you out loud so they can overrule them.

## The process

Work through these phases in order. Each phase ends with something the person has seen and agreed to. Keep a running list of decisions (theirs and yours, labelled) because the spec is built from it.

| Phase | Output | Read |
|---|---|---|
| 1. Discovery | the game in their words | `references/discovery.md` |
| 2. Content check (if the game runs on content they supply) | facts about the data that shape the design | `references/content-games.md` |
| 3. Look and feel | a chosen mockup | `references/mockups.md`, `assets/mockup-starter.html` |
| 4. Game loop and rules | loop, win/lose, scoring, progression, softlock rules | `references/discovery.md` (loop section) |
| 5. Spec + review | `docs/specs/<date>-<game>-design.md`, reviewed | `references/spec-template.md`, `references/review-prompts.md` |
| 6. Plan + review | `docs/plans/<date>-<game>.md`, reviewed | `references/plan-guide.md`, `references/browser-game-gotchas.md`, `references/review-prompts.md` |
| 7. Handoff | a prompt, inline in chat | `references/handoff-template.md` |

Load each reference when you reach its phase, not all at once.

### Before phase 1

Offer, in one line, to skip the questions and go with sensible defaults. If they take it, state the big choices you are making (genre, era look, tech stack, session length) in one plain sentence each, then jump to phase 5 and mark every default in the spec as your call.

Ask where the game should live (a folder name). Everything you create goes there: mockups, spec, plan. If it is not a git repo, ask whether they want one; a plan that commits after every task needs it, and a remote is their decision, never yours.

## How to run the conversation

- **One question per message**, ending the message. Open questions first ("walk me through the first five minutes of playing it"); offer a short menu only when they are stuck.
- **Play back** what you understood every few answers, in about 150-250 words, marking your guesses as guesses. End with "what's wrong or missing?" and then the next question.
- **Propose, don't survey.** When they say "what do you think?", give one concrete recommendation with a one-sentence reason.
- **Correct the facts, kindly and early.** If they say "65 questions" and the file has 186, say so. If an idea creates a softlock or contradicts a goal they stated, name the conflict and offer a fix.
- **Show, don't tell** for anything visual: screens, layouts, art direction, fonts. Phase 3 explains how.
- **Watch for scope drift both ways.** People often start too big (62-question sets that take two hours) and then swing small. Ask how long one sitting should take and design to that.

## Ideas worth offering

People come with a reference game ("like that monster-collecting RPG I grew up with, but...") and a twist. The good ideas in a session usually come from mapping the twist's domain onto the reference game's mechanics:

- Replace the reference game's core verb with the domain's (battles become quiz questions; jumping becomes typing; capturing becomes collecting terms).
- Theme everything else with domain humour: enemies, items, obstacles, place names, NPC dialogue. A cloud-certification game had monsters named after production incidents, a cliff crossed by setting up a private network link, and a final-boss invitation that arrived as a cloud notification.
- Cosmetic collectibles and easter eggs add delight without breaking the rules; anything that changes difficulty or score needs a deliberate decision.
- The opening choice (a starting companion, a class) can become a meaningful choice in the domain (pick a question set, a difficulty, a character class).
- Borrow mechanics and mood, never names. The reference game's title, characters, creatures, catchphrases, logos and music stay out of the game; invent originals that evoke them. Same for real brands and real people used as characters. This matters most when the game will be shared.

Offer two or three such ideas at a time when the conversation reaches world or theme, then let them riff.

## Reviews

Phases 5 and 6 each end with an independent review by a fresh subagent that has not seen this conversation. The reviewer reads the document and the real data, and its job is to find what a builder would have to guess, contradictions, and claims the data disproves. Prompts are in `references/review-prompts.md`. If the session can choose models, use a different model for review than the one that wrote the document; a fresh context with the same model is the fallback.

Sort the findings into three piles:

- **Already answered** in the conversation: write the answer into the document.
- **Minor:** a sensible builder could settle it. Settle it, and mark it in the document as your call.
- **Theirs:** only the person can answer it, and the answer changes what gets built. Bring these in one message, most important first.

Verify a reviewer's surprising claims yourself before acting on them (run the command, count the rows). Reviewers are often right and occasionally confidently wrong.

## Finishing

When the plan is reviewed and fixed, give the person:

1. Links to the spec and plan.
2. The calls you made that they never explicitly approved (layout choices, defaults, git setup), so they can check them.
3. A pre-launch checklist for the build session (from `references/handoff-template.md`).
4. The handoff prompt, inline, in a code block, ready to paste.

Then stop. Building is a new session.
