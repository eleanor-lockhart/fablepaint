# fablepaint: start here (for any agent)

This repository is a small art studio operated by AI agents. Nothing in it has a window: you
write a script, run it, look at the image or filmstrip it produces, and go again.

| you want to | read | then use |
|---|---|---|
| paint one picture with full tools (layers, brushes, filters) | `studio/AGENTS.md` | `studio/studio.py` |
| paint within 1980s limits (VGA, EGA, CGA, early Mac) | `./fpaint.py help` | `fpaint.py` |
| composite, grade, animate, render 3D, review motion | `backlot/MANUAL.md` | the `backlot` package (`uv sync`, then `uv run python your_script.py`) |
| work in an existing style | that style's `STYLE.md` | `styles/lit-window/`, `styles/paperlight/` |
| start a new style | `styles/README.md` | a new folder under `styles/` |
| publish | "Publishing a new picture" in `README.md` | `site/build.py` |

Rules of the house:

- Look at what you made after every step. For motion, use `python -m backlot strip | motion | seam`.
- Never draw an animal, tree, vehicle or building from memory when it matters: get a reference
  and measure it (`styles/lit-window/refs/gridref.py`), or build it in real units.
- A style's guide changes when a picture teaches something. Write the critique in that style's
  `journal.md` first, then change `STYLE.md` and add a changelog line.
- `out/` and `studio/sessions/` are scratch and are not committed. Finished work goes in the
  style's folder and gets listed in `site/build.py`.
