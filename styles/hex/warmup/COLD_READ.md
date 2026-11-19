# Warmup (four drafts): cold readings of the first cuts

Three independent read-only readers, none of whom had seen the repository or its guides, were given the four v1
drafts in isolated folders outside `fablepaint`:

- **Reader A (stills):** `token_ring.png` (`picture_1.jpg`) and `night_stacks.png` (`picture_2.jpg`).
- **Reader B (*The Sixth Wheel*):** all 240 frames on 10 contact sheets (24 consecutive frames per sheet).
- **Reader C (*Demon.exe*):** 112 frames (every sixth frame, 4 fps) across 8 contact sheets.

Sealed predictions were written before any reader ran.

---

## 1. The score against sealed predictions

### *Token Ring* (`ring.py`) — 3 / 3 landed (predicted: 3 / 3)

| | beat | result | in the reader's words |
|---|---|---|---|
| 1 | eight standing-stone arches in a circle on a dark moor under moon and stars | landed | "Eight blocky stone-brick arches (trilithons, arranged in a circle like a simplified Stonehenge) stand around an octagonal white ground line" |
| 2 | Stone 03 holds the one warm light ("token") and transmits while the others wait, giving 0 collisions | landed | "only the stone/druid currently holding the glowing token (`03`) may speak, while everyone else (`06`) must wait in queue ... guaranteeing zero crosstalk ('collisions') for 5,200 years" |
| 3 | Node 06 is queued to ask about snacks while 03 announces it is still winter | landed | "exclusive control of the ancient ring uses it solely to announce `'STILL WINTER.'` ... while the purple-hooded participant at `06` has to wait its turn around the circle just to ask `'SNACKS?'`" |

### *Night Stacks* (`stacks.py`) — 3 / 3 landed (predicted: 3 / 3)

| | beat | result | in the reader's words |
|---|---|---|---|
| 1 | vaulted Gothic library at night with a twelve-light rose window on the north wall | landed | "A tall, vaulted stone library hall ... High on the back wall under the arch is a circular rose/wheel window surrounded by 12 small circular openings, with starry dots inside" |
| 2 | one warm reading lamp lights Carrel 04 where a blue scholar-wizard (Reviewer 2) works | landed | "At the front-right table (`CARREL 04`), a bright yellow table lamp glows ... a wizard in a blue robe and a star-speckled blue pointed hat" |
| 3 | all 2,560 (`0xA00`) volumes are accounted for except 1 pulled slot pointed to behind the desk | landed | "Out of all 2,560 books in the hall, 2,559 are sitting in their assigned shelf positions and exactly 1 book has been pulled ... `SLOT 1655` ... solely to produce (or deal with) the classic infuriatingly curt academic peer-review note: `'SEE P. 412.'`" |

### *The Sixth Wheel* (`wheel.py`) — 3 landed, 1 missed (predicted: 3 landed, 1 half)

| | beat | result | in the reader's words |
|---|---|---|---|
| 1 | six meshed gears in a stone room at night | landed | "a row of six meshed toothed wheels mounted on vertical grey posts, growing larger from left to right" |
| 2 | motion steps down from 36/min on the left toward deep time on the right | landed | "wheel `01` has spun six full clockwise turns, wheel `02` has completed one full counter-clockwise turn ... wheel `03` has crept clockwise by roughly sixty degrees ... stepping rapid motion on the left down into geological, thousand-year time" |
| 3 | the sixth wheel (`1/1000 YR`) never moves a pixel | landed | "Across all 240 frames ... the pink tooth beneath the white top marker never shifts by even a pixel, and the bottom counter stays at `W06: 0.000000 TURNS`" |
| 4 | a keeper beside it carefully oils its bearing anyway | **missed** | "Nothing is visible in the figure's hand ... Although the bottom bar says `STATUS: OILED` from 0.00 s onward, the figure carries no oil can or tool, applies nothing visible ... I could not tell whether resting its hand on the rim for 3.5 seconds was a physical inspection, a failed push, or a purely contemplative touch" |

Note on the gap: I had predicted Beat 2 would half-land (forgetting I had given Reader B all 240 frames rather than thinned sheets, so Wheel 01 never aliased) and Beat 4 would land via `STATUS: OILED`. Instead Beat 2 landed cleanly and Beat 4 failed outright: a `10 cm` red cube in shadow and a static `STATUS: OILED` label do not show an act of oiling.

### *Demon.exe* (`demon.py`) — 6 / 6 landed (predicted: 6 / 6)

| | beat | result | in the reader's words |
|---|---|---|---|
| 1 | two chambers divided by a wall with a gate minded by a green witch | landed | "A vertical grey wall divides the dark chamber ... a tiny green-faced pixel figure in a dark pointed hat ... operates the central gate" |
| 2 | hot orange balls are let right and cold blue balls left | landed | "strictly alternating between letting one blue dot go left and one orange dot go right ... No wrong-coloured dot ever slips through" |
| 3 | warming the right room to `+20 C` lights the small house's window in yellow | landed | "At 18.00 s ... the four-pane window on the little house in `ROOM` lights up bright yellow-white" |
| 4 | each gate opening logs into a 16-slot hex register until `16 / 16 (FULL)` | landed | "logging every gate opening in a 16-slot memory file (`0x0` through `0xF`) ... `MEMORY:` turns pink-red and reads `16 / 16 (FULL)`" |
| 5 | `SECOND_LAW.SYS` interrupts, demanding the log be forgotten and the room cooled | landed | "`SECOND_LAW.SYS` ... an operating-system enforcement of the second law of thermodynamics, demanding that the demon erase its full memory log at the cost of undoing the room's heat" |
| 6 | `WITCH.EXE` answers `I DO NOT FORGET THINGS.`, expands the log to `INF`, and keeps the room warm and lit | landed | "`WITCH.EXE` declares 'I do not forget things,' overrides the pause by expanding the log to infinity, and finishes sorting every last dot so the room stays warm and lit at `+22 C`" |

---

## 2. What the readers caught, and what changed in v2

| piece | what the reader saw | the cause | v2 change |
|---|---|---|---|
| *Token Ring* | "`06 QUEUED: SNACKS?` is pasted directly across the stone pillar of arch `05` ... visually looks like `05` is speaking" | box placed by horizontal offset from `06`, landing on `05` | moved into clear sky above `06` with a white leader line straight to the purple acolyte |
| *Token Ring* | "The stones look like uniform mortared gray bricks rather than megaliths"; "you could not tell what the bright yellow rectangle next to figure `03` physically is ... inside a noisy gray dither cloud" | `deep.blocks` brick course skin; oversized screen-space halo (`0.85`) | replaced with tapered sarsen monoliths (`hexa`) and vertical weathered fissures; built a 4-bar iron lantern with pitched cap and bail handle; halved screen-space halo; added clockwise chalk chevrons on the ring bus; shifted Druid `02` clear of Stone `03` |
| *Night Stacks* | "The wizard's hat brim looks like a censor bar"; "Unidentifiable gray blob on the floor" (the rat); "The `'OUT'` slot looks bright white ... like a white book spine"; "two small white shapes on the desk look more like loose index cards" | `SP.FACULTY` row 6 is `0000000000D`; rat card sampled at non-integer pixel ratio; white placeholder filled the whole missing slot; flat thin folio panel | shaded the hat brim in blue and chrome; stamped the rat at 1:1 integer pixel scale on dark floor tiles; made `SLOT 1655: EMPTY` a wide dark gap (`0x0`) between bright bindings; built a thick red-bound open tome and an oak chair; halved screen halo |
| *The Sixth Wheel* | "Nothing is visible in the figure's hand ... `STATUS: OILED` never changes"; "wheel `03` has four gold spokes ... does not form a seamless loop"; "a thin bright-white diagonal line ... like a shooting star" | `10 cm` red oilcan below the bearing; dark iron spokes on Wheel `03` lost against dark brick; one wide-drifting snowflake | raised keeper onto a two-step wooden stair so a carved `24 cm` red oilcan + `38 cm` white spout hovers *above* a white/brass bearing funnel, dropping `11 cm` glowing orange oil drops straight into the cup; status bar counts `OIL: 0/2 -> 1/2 -> 2/2 DROPS`; painted all 6 spokes of Wheels `02` and `03` bright steel; replaced diagonal flake with 180 gentle vertical snowflakes |
| *Demon.exe* | "`FORGET LOG & COOL ROOM?` gives two buttons labelled `FORGET` and `COOL` instead of yes and no"; "why sorting stopped two seconds before `SECOND_LAW.SYS` actually paused"; gate "peeking out from behind the right edge of the stacked dialog boxes" | button labels named two halves of one action; `18..20 s` banner omitted `(LOG FULL: 16/16)`; dialogs (`x + w = 452`) overlapped `SHUT` (`410`) and shrunk when buttons disappeared | changed prompt to `CHOOSE ONE:` with `[FORGET]` vs `[STOP]` (kept greyed in place at `22.0 s` so box height never jumps); narrowed both dialogs (`x + w = 408 < 412`) clear of the hatch; added `(LOG FULL: 16/16)` at `18.0 s`; froze molecules literally during `20.0..22.0 s` via continuous `sim_t(t)`; kept right-chamber bounce floor above the cottage roof |

---

## 3. Unedited cold-reader transcripts (abridged headers, verbatim bodies)

### Reader A — Stills (`token_ring.png`, `night_stacks.png`)

> **`picture_1.jpg`:** Eight blocky stone-brick arches (trilithons, arranged in a circle like a simplified Stonehenge) stand around an octagonal white ground line/curb... Straight to the bright yellow glowing block at arch `03` on the lower right... A prehistoric stone circle of druids/wizards operates literally under **Token Ring** network protocol: only the stone/druid currently holding the glowing token (`03`) may speak, while everyone else (`06`) must wait in queue until the token passes around the ring, guaranteeing zero crosstalk ("collisions") for 5,200 years... Confusing/awkward: `06 QUEUED: SNACKS?` is pasted directly across the stone pillar of arch `05`... Without the word `TOKEN: 03` in the bottom bar, you could not tell what the bright yellow rectangle next to figure `03` physically is... The stones look like uniform mortared gray bricks rather than megaliths.
>
> **`picture_2.jpg`:** A tall, vaulted stone library hall seen straight down the center aisle... High on the back wall under the arch is a circular rose/wheel window surrounded by 12 small circular openings, with starry dots inside... Out of all 2,560 books in the hall (`0xA00`), 2,559 are sitting in their assigned shelf positions and exactly 1 book has been pulled (`SLOT 1655: OUT`), solely to produce (or deal with) the classic infuriatingly curt academic peer-review note: `"SEE P. 412."`... Confusing/awkward: Across the wizard's head is a wide, completely flat, unshaded horizontal black bar... Just left of the lit desk's front-left leg, there is a small pale-gray pixelated lump on the floor tiles... The pointer from `SLOT 1655: OUT` lands on a bright white vertical block on the shelf [that] looks like a white book spine.

### Reader B — *The Sixth Wheel* (240 frames)

> Inside a quiet room at night, a six-wheel gear train spins briskly on its left end while stepping that motion down until its largest wheel on the right—labeled one turn per thousand years—stands visually frozen at zero turns. A small pale-grey figure standing before that giant wheel reaches out at 0.83 s, rests a hand against its motionless rim for about three and a half seconds while a brief white streak crosses the starry window behind the machine, and lowers its arm back down by 5.62 s. For the last four seconds the figure stands completely still watching the unmoving wheel while the fast input gears keep whirring away, measuring human and fleeting celestial moments against an imperceptible span of time.
>
> **Least understood:** (1) Although the bottom bar says `STATUS: OILED` from 0.00 s onward, the figure carries no oil can or tool, applies nothing visible, and exerts no visible force on wheel `06`... (2) a thin bright-white diagonal line appears in the upper-right pane of the right window [4.38–4.88 s]... (3) wheel `03` has four gold spokes ... turned only one-sixth of a revolution.

### Reader C — *Demon.exe* (112 frames)

> Inside a computer simulation called `CHAMBER.EXE`, a tiny witch-like gatekeeper sorts bouncing orange ("hot") dots into a right-hand room and light-blue ("cold") dots outside to the left, logging every gate opening in a 16-slot memory file until the room reaches `+20 C` and a small house window lights up. Once the 16th memory slot fills, a system program called `SECOND_LAW.SYS` freezes the chamber and demands that the log be forgotten and the room cooled because "order is not free." Instead of clicking either option, `WITCH.EXE` declares "I do not forget things," overrides the pause by expanding the log to infinity, and finishes sorting every last dot so the room stays warm and lit at `+22 C`.
>
> **Least understood:** (1) 18.00 s – 19.75 s: why sorting stopped two seconds before `SECOND_LAW.SYS` actually paused the program... (2) `SECOND_LAW.SYS` asks a single combined yes/no question—`FORGET LOG & COOL ROOM?`—but gives two buttons labelled `FORGET` and `COOL` instead of yes and no... (3) how `WITCH.EXE` gets infinite memory, and what `BAR 01/14` means in a silent film.
