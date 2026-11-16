# Hex

Ellie Lockhart's style, drawn by Fable: sixteen colours numbered 0 to F, a frame filled to its edges, the rule
left showing, and a straight face. Start with `STYLE.md`; the reasoning is in `journal.md`.

| | |
|---|---|
| `kit.py` | an indexed canvas: every pixel is one hex digit. Dither, sprites, the ROM font, dialog boxes, hexagonal cells |
| `sprites.py` | the cast, written as text |
| `gate_exe_tune.py` | the ten-second tune for the GATE.EXE loop, and the step that puts it on the picture |
| `voices.py` | every instrument the style has, synthesised; it also keeps the list of notes played, for a picture to be drawn from |
| `deep.py` | Hex in depth, on `backlot/depth.py`: light has no colour; paints that are blends of two registers; procedural skins on a 5 cm grid |
| `basecase/` | *Base Case*: `BRIEF.md`, `house.py` (the house, one model in metres), `cast.py` (the child, at 5 cm a pixel), `film.py` (the house as it is), `levels.py` (the same house printed as 1989, 1987 and 1980), `music.py`, `COLD_READ_v1.md` |
| `recital/` | *Space Opera (in One Act)*: `BRIEF.md`, `music.py` (the song, and `events.json`), `film.py` |
| `uptime/` | the major piece: `BRIEF.md` (storyboard on a bar grid), `music.py` (the score, written first), `ui.py` (a desktop of about 2000), `film.py` |
| `stage1.py` | the eight-bit drafts: `uv run python styles/hex/stage1.py` writes `stage1/` |
