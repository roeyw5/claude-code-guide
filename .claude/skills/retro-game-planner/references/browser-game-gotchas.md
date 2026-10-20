# Browser game gotchas

Fold the relevant ones into the plan's Global Constraints. Each one cost real time in a real build.

## Running from a file (double-click index.html)

- `file://` pages cannot `fetch()` local files and cannot load ES modules (`<script type="module">`, `import`). Use classic `<script src>` tags in dependency order, one global namespace, and ship data as `.js` files that assign to it.
- To unit-test that code in Node, have each file attach to `globalThis.NS = globalThis.NS || {}` and touch no `window`/`document`/`localStorage` at load time; Node tests can then `require()` the same file.
- Chrome gives all `file://` pages one shared `localStorage` origin: prefix every key with the game's name.
- Firefox only loads local fonts from the page's folder or below; keep fonts under the game folder (or embed them as base64).

## Fonts

- Bundle fonts locally if the game must work offline. Google Fonts' CSS API returns woff2 only for a browser User-Agent; pick the `latin` subset. Keep the licence file (most pixel fonts are SIL OFL).
- Canvas text does not wait for web fonts. Call `document.fonts.load('16px "Font Name"')` before the first draw, or the first frames use a fallback.
- Plan a fallback (system monospace / sans-serif) if the download fails during an unattended build.

## Rendering and input

- Keep the canvas at a fixed pixel size and scale with CSS and `image-rendering: pixelated`; never let it stretch to the window.
- Long text belongs in DOM, not canvas: it must wrap and, on short screens, scroll.
- Key auto-repeat fires repeated `keydown`s: track "pressed this frame" separately from "held". Lock input for a few hundred ms after a confirm so mashing Enter cannot double-submit or skip feedback. Lower-case letter keys (Caps Lock).
- Audio can only start after a user gesture; create the WebAudio context on the first key press.
- Letter shortcuts (B for bag, M for mute) keyed on `event.key` stop working under a non-Latin keyboard layout (Hebrew, Russian, Greek): map them by `event.code` (`KeyB`, `KeyM`) on both keydown and keyup.
- Some pixel fonts ship broken ligatures: Pixelify Sans drew "fi" and "fl" as a wrong glyph on canvas ("Security First" came out as "Security Arst"). Turn ligatures off in CSS (`font-variant-ligatures: none`) and break them in canvas strings (a zero-width non-joiner, written as the escape `\u200C`, between the letters).
- Never put the default focus of an end or results screen on an action that discards it ("Next level", "Play again"). The player arrives mashing Enter from the last fight; focus the review first.

## State and saving

- Wrap every storage read and write in try/catch; storage can be blocked, full, or hold garbage. The game must start fresh rather than crash.
- Stamp saves with a data version, so regenerating content discards stale saves instead of misreading them.
- Make recorded actions final: once an answer or move is saved, a reload must never re-ask or lose it. Hand resumed encounters only their unfinished parts, or a "record twice" guard turns into a softlock.
- Derive "this encounter is done" from the recorded result itself, not from a separate after-the-fight step: a reload between the two gives one trainer a second question.
- When a state change moves the player (a warp to the boss, a level exit), save the new position in the same write as the new state, before any fade or animation. Saving the phase first and the position after the fade left a window where a reload put the player outside a warp-only area with the invitation already used: an unfinishable run. Add a defensive normalise step on resume as well.
- Compute scores and badges from the saved run, never from what one screen collected: a resumed fight only sees its own remaining part.

## Tests and tooling

- `node --test tests/` treats `tests/` as a module and fails on Node 22; use `node --test "tests/*.test.js"`. Resolve paths with `__dirname`, since agent shells may reset the working directory.
- A deterministic build (same input, byte-identical output) is worth a test: it catches `Math.random()` or timestamps sneaking into generated data.
- Browser smoke tests need a browser tool in the build session (for example a Playwright MCP server). Project-scoped MCP servers need an interactive approval the first time, which an unattended session cannot give. Have the person approve it before they leave, and have the plan record smokes as NOT RUN (and continue) if no browser tool is available.
- If the browser tool refuses `file://` (the Playwright MCP does), serve the folder with `python3 -m http.server <port>` started in the background, never in the foreground (it blocks the agent). The `file://` path then goes untested: list "double-click index.html in Chrome and Firefox" as a manual check in the morning report.
- After editing a file during a smoke, hard-reload: Chrome serves cached scripts from the local server and the smoke tests the old code.
- The Playwright MCP writes its logs to `.playwright-mcp/` in the session's working directory. Start the build session inside the game folder and gitignore it, or the logs land in the parent folder.

## Unattended runs

- The run stalls on its first permission prompt unless the session runs in an auto or pre-approved permission mode.
- Anything that needs the network (fonts, CDNs) needs a stated fallback.
- Pushes and other remote writes need the person's explicit permission for that run, written into the handoff prompt with its limits (which remote, never force).
