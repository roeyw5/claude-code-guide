# retro-game-planner

A Claude Code skill that takes you from "I want to make a game" to a reviewed design spec, a reviewed build plan and a ready-to-paste prompt for a fresh build session, for retro-style browser games.

It runs the pre-build process: discovery questions, clickable HTML mockups, game-loop and scoring decisions, an optional audit of your own content (for quiz and study games), the spec, an independent review, the plan, a second review, and the handoff. It does not build the game; the handoff prompt does that in a new session.

## Install

Copy this folder into `~/.claude/skills/` (or a project's `.claude/skills/`). Claude Code picks it up when you describe a game you want to make.

## Requirements

Plain Claude Code. Subagents are used for the reviews when available. Browser-based smoke tests in the build plan use a browser automation tool if the build session has one, and are skipped otherwise.

## Notice

This project is not affiliated with, endorsed by or sponsored by any game company or platform holder. It contains no game assets. The games it helps plan should use original names, characters, art and music. Product names that appear in the instructions (such as Chrome, Firefox, Node.js, Playwright, Google Fonts and Claude) are trademarks of their respective owners and are used only to identify those tools. The fonts named in the mockup starter (Pixelify Sans, Nunito) are third-party fonts under the SIL Open Font License and are loaded from Google Fonts, not bundled.
