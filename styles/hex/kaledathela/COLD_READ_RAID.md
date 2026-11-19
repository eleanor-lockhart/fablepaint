# Cold Reading Report — *Reliquary Drop* (`raid_film.py`, v1 -> v2)

Conducted via `backlot.reader` with an isolated `research` subagent (`1b0c2432`) pointed strictly at `coldread_raid_film` (128 frames across 8 sheets), after sealing predictions in `SEALED_RAID.md`.

---

## 1. Score Against Sealed Intent (`INTENT.md`)

| # | Intended Beat | Score | Evidence from Unedited Narration |
|---|---|---|---|
| 1 | Shot 1 (0–8 s): Cross-marked Reliquary dropship lands in rain (2 s), deploys 4 Hunters, arms charge (4 s), blows stone doorway (6 s), squad enters | **Landed** | *"An angular grey coffin-shaped craft with... a white Christian-style cross... and two bright orange downward-pointing trapezoids... four lined up side-by-side... At `6.00 s`, the lower half of the vertical grey barrier disappears... march rightward."* |
| 2 | Shot 2 (8–16 s): Colonnade gunfire erodes columns; Thorn killed at 10 s (`0xD` blood); Signal raises `0x6` bullet-catching lattice (12 s) and reverses volley (14 s), killing Hunter #1 & darkening hall | **Landed** | *"dark gaps get chewed into the grey stone... Thorn... collapses into a dark heap... tall vertical green oval... stopped bullets... flings four stacked yellow streaks backward... hall background darkens."* |
| 3 | Shot 3 (16–24 s): Bayou drops on line (16 s), pillar-vaults & slashes Hunter #2 (18 s); Runner's floor wire + Signal kill Hunter #3 while Runner takes a graze (20 s); Hunter #4 flees (22 s) | **Landed** | *"Bayou lowers on a thin vertical dark line... leaps upward and leftward... onto the side of the left column... curved pale-green `C` blade arc... Runner stretches a thin green horizontal wire... taking the third hunter's legs out while absorbing a graze... lone remaining gunman turns to face left."* |
| 4 | Shot 4 (24–32 s): Damaged dropship lifts off in rain (24 s); `0xF` sanctum opens over fallen Sister Thorn (26 s); Bayou plants green memorial blade lighting the overhead arch (30 s) | **Landed** | *"tilted, smoking craft rises... pale yellow-white light (`0xF`) spills... casting a warm yellow trapezoid over the dark fallen heap ('Sister Thorn')... upright pale-green cross-hilted blade... bright green lines spread through every segment of the curved purple arch."* |

---

## 2. Critical Shape & Continuity Catches Fixed in v2

1. **Shape Rule Discovered (`COMBAT.md` update — Blood vs. Lasers):**
   - *Reader catch:* `"Arterial blood spurts are drawn as straight, rigid diagonal bright-pink (0xD) rods—the exact same colour and thickness as the hunters' pink gun beams—so they look like stray laser bolts rather than blood."`
   - *v2 Fix in `kit_kal.py` & `COMBAT.md`:* Lasers stay thin straight lines; **`draw_blood_arc` now renders a gravity-curved parabolic fan of discrete liquid droplets (`0xD` + dark `0x2` crimson-violet core)** arcing downward onto the stone!
2. **Fallen Hunter Silhouette (`HUNTER_DOWN` vs. rubble):**
   - *Reader catch:* `"Dead hunters become tiny flat grey pancakes... nearly indistinguishable from the grey doorway rubble lump."`
   - *v2 Fix in `kit_kal.py`:* Redesigned `HUNTER_DOWN` with clear dark boots, coat torso, knocked-off wide-brim hat, and `0xD` chest wound, plus an intermediate crumpling pose before hitting the stone.
3. **Frame & Continuity Fixes in `raid_film.py` v2:**
   - **Shot 1:** Enclosed the building roof/wall behind the Worm-rib (`no starry sky inside the hall`); shut off VTOL flames once parked; Hunters step back to cover (`4.2–5.8 s`) and remain drawn across `6.00–6.15 s` (`zero missing frames`).
   - **Shot 2:** Added a physical ceiling floodlight fixture at `(290, 50)` keeping hall tone `1` steady across `8.0–14.0 s` (**stone column craters never reset at `12.0 s`**); aligned stone dust bursts to bullet height; sped reversed slugs to `0.15 s` (`frames 336–339`) with a 5th upward ricochet visibly shattering the ceiling floodlight!
   - **Shot 3:** Bayou drops behind Hunter #2's back and lands on his left side matching the `0x7` crescent slash; Runner's held lantern removed (`swap={0xF: None}`) with the `0xD` graze placed directly on her shoulder; at **`22.0 s`**, Bayou hurls a `0x7` green throwing-knife that visibly wounds Hunter #4's arm (`0xD` droplet arc + coat stain) so `1 WIA` happens on screen!
   - **Shot 4:** Wounded Hunter #4 scrambles up the folding ramp (`24.0–24.5 s`) as a green `0x6` bolt scorches the dropship's hull at `24.0 s` (trailing world-space drifting smoke); separated Bayou and Signal (`50 px` apart); animated Bayou's downward planting motion at `29.8–30.1 s`.
