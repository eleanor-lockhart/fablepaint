# Warmup: four drafts in Hex (a second hand)

Written before building anything, after reading `AGENTS.md`, `STYLE.md`, `backlot/MANUAL.md`, `studio/AGENTS.md`,
and `styles/hex/STYLE.md` + `journal.md`. These four drafts exercise still construction, strict sixteen-register
printing (`stage2.py`), deep places and carved solids that turn (`backlot.space`, `backlot.depth`, `backlot.carve`,
`deep.py`, `puppet.py`), and a scored animation on a beat grid with synthesised voices and sync verification
(`kit.py`, `ui.py`, `voices.py`, `backlot.ear`, `backlot.sync`, `backlot.reader`).

## Shared rules kept across all four

- Sixteen registers (`0` to `F`), or fixed blends of two registers where stage 3 or 5 applies.
- Register `F` (`#ffd870`) is reserved for the one tended light in each piece and is the only thing that glows.
- Only the witch is green (`5`, `6`, `7`). Three of the four drafts do not have her in them and use no green at all
  outside the sixteen-register signature strip.
- Every frame is filled to its edges with structure; every piece leaves its rule showing in literal system type
  and signs itself with the sixteen registers in order.

---

## 1. *Token Ring* (`ring.py` -> `token_ring.png`, `token_ring_plan.png`)

**One sentence:** On a dark moor under winter stars, eight megalithic trilithons stand wired into a chalk octagon;
seven robed figures wait in the dark while the fourth holds the one lit lantern (`F`) that permits its holder to speak.

- **Stage:** Stage 2 (`640 x 360` strict sixteen registers, every pixel `0..F`, saved at `2x` = `1280 x 720`),
  printed from a 3D `backlot.space` + `backlot.depth` model in metres.
- **No witch:** Zero green registers anywhere in the scene (`SP.DRUID` mistletoe swapped to chrome/white).
- **Model:** Rolling moorland height field; eight sarsen trilithons on a `9.5 m` radius ring (`NODE 00` to `07`),
  joined by an inlaid chalk trench ring with clockwise markers; a cast point light at `NODE 04` throwing long
  radial shadows outward across the moor (with ambient floor above register `0` so shadows read as darkened ground,
  never holes).
- **Rule & gag:** `RING.SYS  NODES: 8  TOKEN: STONE 04  COLLISIONS (5200 YR): 0`, while `STONE 04` transmits
  `> STILL RAINING.` and `STONE 07` waits in queue.
- **What must land on a cold reading:**
  1. It is a ring of standing stones outdoors at night.
  2. One stone/figure holds a bright warm lantern while the others wait unlit.
  3. The circle operates as a pass-the-token communication ring where only the holder speaks and nothing collides.

---

## 2. *Night Stacks* (`stacks.py` -> `night_stacks.png`, `night_stacks_section.png`)

**One sentence:** At three in the morning inside a vaulted Gothic library, winter stars shine through a cusped rose
window onto 2,048 shelved volumes and one lit carrel (`F`) where Reviewer 2 has the single missing book open.

- **Stage:** Stage 2 (`640 x 360` strict sixteen registers, `2x` = `1280 x 720`), printed from a 3D Gothic vault
  built in metres on the `5 cm` grid.
- **No witch:** Zero green registers in the scene.
- **Model:** Pointed stone ribs, chequered flags, a compass-constructed twelve-light cusped rose window at the north
  wall, and sixteen bookcases holding `16 x 8 x 16 = 2,048` distinct book blocks on the `5 cm` grid — with exactly
  one gap on the shelf behind Carrel 04 and one open folio under the `F` desk lamp.
- **Rule & gag:** `STACKS.DB  2048 VOLS  SHELVED: 2047  IN USE: 1  VERDICT: REVISE & RESUBMIT`.
- **What must land on a cold reading:**
  1. A large vaulted Gothic library or hall with a circular rose window at the far end at night.
  2. One small warm reading lamp lighting a desk and scholar while the surrounding shelves sit in dark shadow.
  3. Every book is accounted for except the one open on the desk (and the academic / reviewer joke in the status).

---

## 3. *The Sixth Wheel* (`wheel.py` -> `sixth_wheel.mp4`, `sixth_wheel_still.png`, `sixth_wheel_plan.png`)

**One sentence:** In a stone clock room while snow falls outside, five meshed reduction shafts step a brisk drive
wheel down until the last wheel turns once in a thousand years, and a keeper with an oilcan oils its bearing anyway.

- **Stage:** Stage 5 (`backlot.space` + `backlot.depth` + `backlot.carve` + `puppet.py`, `1280 x 720`, `24 fps`,
  `10.0 s` = `240` frames, seamless loop).
- **No witch:** Zero green registers in the scene.
- **Mechanics & loop math:**
  - Shaft 1 (`DRIVE`): `6` full turns per loop (`+2160 deg`, `9 deg/frame`), `6` spokes.
  - Shaft 2 (`6:1`): `1` full turn per loop (`-360 deg`, `-1.5 deg/frame`), `6` spokes.
  - Shaft 3 (`6:1`): `1/6` turn per loop (`+60 deg`), built as one `60 deg` carved sector repeated six times
    (`D.turned`), so frame `240` matches frame `0` to the texel.
  - Shaft 4 (`6:1`): `1/36` turn per loop (`-10 deg`), `36`-tooth drum built from `10 deg` symmetry.
  - Shaft 5 (`WORM -> 1 / 1000 YR`): massive `2.6 m` wheel at right (`0.0000003 deg` in `10 s` = `0` pixels moved).
  - Keeper (`puppet.py`, chrome suit, oilcan): `10 s` periodic action under one tended brass lamp (`F`) hung beside
    Shaft 5 — leans in, oils the bearing twice, steps back to check the motionless wheel, and returns to rest.
- **What must land on a cold reading:**
  1. A row of connected gears stepping fast motion on the left down to slower and slower motion on the right.
  2. The last huge wheel does not visibly move at all (turns on a millennial timescale).
  3. A worker under the warm lamp carefully oils or tends the stationary wheel anyway.

---

## 4. *Demon.exe* (`demon_music.py`, `demon.py` -> `demon_exe.mp4`, `demon_poster.png`, `demon_score.jpg`, `demon_sync.jpg`)

**One sentence:** On a desktop running Maxwell's Demon, the witch sorts hot and cold molecules through a trapdoor
until the right-hand room warms enough to light its one window (`F`); when `SECOND_LAW.SYS` tells her to erase her
full 16-bit log and let the cold back in, she refuses to forget anything.

- **Stage:** Stage 3 desktop (`1280 x 720`, `24 fps`, `28.0 s` = `672` frames, `14` bars of `4/4` at `120 BPM`,
  `1 beat = 0.5 s = 12 frames`) framing a live Stage 1 chamber.
- **With the witch:** She stands in the gatehouse arch above the central partition (green `5`, `6`; her `0` hat set
  against a `2`/`3` stone arch so it never vanishes into void). Her pointer is green and never moves until she
  answers — in fact, she answers without moving it at all.
- **Beat grid (score written first):**
  - `0.0 s` (Bars 1–2): Equilibrium. Both chambers hold mixed hot (`E`/`D`, fast) and cold (`C`/`9`, slow)
    molecules (`0 C` left, `0 C` right). The small house at bottom-right has one dark window (`NEED +20 C`).
  - `4.0 s` (Bar 3): Sorting begins (`HOT -> RIGHT, COLD -> LEFT`). On `16` scheduled beats (`4.5, 5.0, 6.0, 6.5,
    7.5, 8.0, 9.0, 9.5, 10.5, 11.0, 12.0, 12.5, 13.5, 14.0, 15.0, 15.5 s`), exact constant-speed billiard
    trajectories bring a molecule to the hatch; the hatch opens for `6` frames, passes it, and logs `1..16` in
    `LOG.DAT`.
  - `16.0 s` (Bar 9): Right room reaches `+20 C`; the house window lights in `register F` (with `F` glow).
  - `18.0 s` (Bar 10): `SECOND_LAW.SYS` alert dialog: `MEMORY IS FULL (16 / 16 BITS). FORGET LOG AND LET THE COLD IN?`
    `[FORGET]` `[EQUALIZE]`. System pointer hesitates over both buttons (`19.0 s`, `20.5 s`).
  - `22.0 s` (Bar 12): `WITCH.EXE` opens in green: `I DO NOT FORGET THINGS.` `SECOND_LAW.SYS` turns grey, `LOG.DAT`
    expands to `16 / FOREVER`, four more sorts land on `23.0, 24.0, 25.0, 26.0 s`, and the `F` window stays lit.
- **What must land on a cold reading (6 beats):**
  1. Two rooms separated by a wall with a gate/trapdoor minded by the green witch.
  2. Fast/hot orange particles are sorted to the right and slow/cold blue ones to the left.
  3. Warming the right room causes the small dark house window to light up yellow.
  4. Each gate action fills a 16-slot memory/log until it hits `16/16`.
  5. A system dialog demands erasing/forgetting the log and equalizing the rooms.
  6. The witch refuses (`I DO NOT FORGET THINGS.`), expands the memory instead of erasing it, and keeps the room warm and lit.
