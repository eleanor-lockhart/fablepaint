# Hex

Ellie Lockhart's style, drawn by Fable: sixteen colours numbered 0 to F, a frame filled to its edges, the rule
left showing, and a straight face. Start with `STYLE.md`; the reasoning is in `journal.md`.

| | |
|---|---|
| `kit.py` | an indexed canvas: every pixel is one hex digit. Dither, sprites, the ROM font, dialog boxes, hexagonal cells |
| `sprites.py` | the cast, written as text |
| `gate_exe_tune.py` | the ten-second tune for the GATE.EXE loop, and the step that puts it on the picture |
| `uptime/` | the major piece: `BRIEF.md` (storyboard on a bar grid), `music.py` (the score, written first), `ui.py` (a desktop of about 2000), `film.py` |
| `stage1.py` | the eight-bit drafts: `uv run python styles/hex/stage1.py` writes `stage1/` |
