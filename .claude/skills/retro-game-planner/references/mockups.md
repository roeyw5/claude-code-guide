# Mockups (phase 3)

Mockups are throwaway HTML files the person opens in their browser. They exist to make decisions, not to become the game.

## Offering

The first time something visual comes up (a screen, layout, art style, font), ask in its own short message: "This might be easier if I show you. Want me to make a mockup page you can open in your browser?" If they decline, stay in text.

## Making one

- Start from `assets/mockup-starter.html` (a battle/dialog scene on the left, a text panel on the right, a palette and two fonts wired up). Copy it into the game folder under `mockups/` with a descriptive name (`battle-screen.html`, `battle-screen-v2.html`). Never overwrite an earlier version.
- Tell them the full path and to open it in a browser. If a browser automation tool is available, you can screenshot it yourself to check it before telling them.
- Put 2-3 options side by side on one page, each labelled with a letter and a one-line description of what the player experiences.
- **Use real content, including the worst case.** Show the longest real item from their data, not a short placeholder. Most layout decisions are made by the worst case.
- Draw sprites inline as tiny SVG pixel grids (`shape-rendering="crispEdges"`), so nothing is downloaded.

## Lessons that recur

- **Era look is not era screen size.** People who name an old handheld usually mean its charm, not a 160x144 box in a four-shade yellow-green palette. Ask whether they want it to "look old" or "feel nostalgic"; the brighter colours of later 32-bit handhelds often land better.
- **Separate text from the scene on desktop.** A fixed-size scene (for example 600x400) on the left and a flexible text panel on the right reads far better than text overlaid on the scene, and long text then just makes the panel taller.
- **Cap the width.** Without a max width (1200-1280px) the scene stretches on wide monitors. Fix the scene's pixel size; let only the text panel flex.
- **Two fonts:** a pixel font for game chrome (HUD, labels, dialog) for nostalgia, and a readable font for anything the player must read carefully (questions, long dialog, explanations). Show 2-3 readable-font candidates side by side and let them pick.
- **Show states, not just screens:** before and after answering, a "choose two" variant, the end screen.

## Afterwards

Record the chosen mockup files in the spec as the approved direction, and list every element in them that was later retired (an HP bar, a hint item), so the builder does not resurrect it. The spec wins over the mockups.
