# Paperlight

Boxes of cut paper lit from behind and within, built at true size in Blender, photographed with
a real lens and animated on twos. Start with `STYLE.md`; the reasoning is in `journal.md`.

| | |
|---|---|
| `kit.py` | cut patterns: border, land, waves, firs, stars, lighthouse, lookout; `sheet()` makes a design cuttable |
| `studies/` | material and light tests |
| `works/<name>/scene.py` | a box: `test` (one frame), `render` (all frames to EXR), `finish` (lab, encode, review) |
| `works/*.mp4`, `*_still.png`, `*_making.jpg` | the finished loops, a still from each, and how each was made |

Run from the repository root: `uv run python styles/paperlight/works/lighthouse/scene.py test`.
