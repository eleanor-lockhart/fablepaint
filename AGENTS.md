# fablepaint: start here (for any agent)

This repository is a small art studio operated by AI agents. Nothing in it has a window: you
write a script, run it, look at the image or filmstrip it produces, and go again.

| you want to | read | then use |
|---|---|---|
| know what the work here has in common, and how it is made and checked | `STYLE.md` (the house style) | |
| paint one picture with full tools (layers, brushes, filters) | `studio/AGENTS.md` | `studio/studio.py` |
| paint within 1980s limits (VGA, EGA, CGA, early Mac) | `./fpaint.py help` | `fpaint.py` |
| composite, grade, animate, render 3D, make sound, review motion and sync | `backlot/MANUAL.md` | the `backlot` package (`uv sync`, then `uv run python your_script.py`) |
| work in an existing style | that style's `STYLE.md` | `styles/lit-window/`, `styles/paperlight/` (Fable's own); `styles/hex/` (Ellie's, drawn by Fable: a different surface, do not mix them) |
| start a new style | `styles/README.md` | a new folder under `styles/` |
| add to the story world | `world/night-service/BIBLE.md`, then `LOG.md` | `world/night-service/cast.py` for the characters |
| make film for the story world | `world/night-service/STYLE.md` | `world/night-service/op/` is a worked example with its review |
| see what is being learned next, and the test for each study | `ROADMAP.md` | `studies/` |
| publish | "Publishing a new picture" in `README.md` | `site/build.py` |

Rules of the house:

- Look at what you made after every step, at the speed of the thing: `python -m backlot strip` for a shot's
  design, `python -m backlot run` for every event and camera move (consecutive frames), `motion | seam | travel`.
- Never draw an animal, tree, vehicle or building from memory when it matters: get a reference
  and measure it (`styles/lit-window/refs/gridref.py`), or build it in real units.
- One thing, one model: a place, prop or creature that appears twice is built once and looked at twice.
- You cannot see what your own picture says. Before calling a piece finished, write your verdict down, then
  have a cold reader narrate it (`backlot/reader.py`) and compare.
- A guide changes when a piece teaches something. Write the critique in that folder's journal first, then
  change its `STYLE.md` and add a changelog line. A library defect is fixed in the library, with a test, the
  day it is found.
- Every asset is made in code here. References are for looking and measuring. Nothing generated elsewhere
  goes into a finished piece.
- `out/` and `studio/sessions/` are scratch and are not committed. Finished work goes in its own folder and
  gets listed in `site/build.py`.
