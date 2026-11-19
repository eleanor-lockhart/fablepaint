# Combat, Ballistics & Gothic Violence in Hex (`COMBAT.md`)

Version 1.0. Companion to [`STYLE.md`](STYLE.md) and [`../STYLE.md`](../STYLE.md). Defines how to stage **artistic /
soft-R** close-quarters combat, gunplay, hex-lethality, wounds, and structural destruction within Hex's strict
16-register palette—drawing kinetic grammar from *The Matrix* (lobby geometry, pulverized stone, suspended volleys) and
*The Raid: Redemption* (claustrophobic ruin breaches, stroboscopic darkness, visceral physical cost on both sides).

---

## 1. Tone & Rating Boundary (Artistic / Soft-R)

1. **Consequence, never spectacle-without-cost:** Violence is sharp, brief, legible, and irreversible within a scene.
   Every stone chip, spent casing, and dark blood pool **persists on the floor and walls** for the remainder of the
   shot (`Rule: Damage is permanent`).
2. **Graphic silhouette clarity over anatomical clutter:** At pixel / Stage-2 scale, gore works like gothic woodcuts,
   *Sin City*, or 1990s anime (*Ninja Scroll*): **gravity-curved fans of crimson droplets (`0xD` + `0x2`), stark
   muzzle-strobe cones (`0xA`, `>` shape — never `+` crosses), and dark pooling (`0x2`/`0x0`)**. **Never draw blood as
   a straight ruler-line**, or it will read like an Inquisition `0xD` targeting laser (`Rule 3: One look, one meaning`).
3. **Both sides bleed:** Hunters are disciplined, heavily armed zealots whose breaches shatter stone and kill; Witches
   survive only by turning darkness, architecture, and razor-precise hex-geometry against superior firepower—and they
   take real wounds and losses doing it.

---

## 2. Chromatic Law of Violence (All 16 Registers Accounted For)

**House Rule 2 still holds without exception:** **`Register F` (`#ffd870`) is NEVER used for muzzle flashes, explosions,
tracers, or sparks.** Even during a breach, `0xF` belongs exclusively to the Coven's shelter lamp—so when gunfire and
blood erupt near a shuttered `0xF` threshold, the viewer sees immediately what is at stake.

| Phenomenon | Active / Impact (`2–8 frames`) | Settled / Persistent (`rest of shot`) | Notes |
|---|---|---|---|
| **Muzzle flash & breach strobe** | **`A` (`#e8ecf4`)** cruciform/star flare | **`1` / `0`** darkness returns | In dark halls (`0, 1`), gunfire acts as stroboscopic photography, briefly throwing pillars & coats into `0xA`/`9` rim light. |
| **Propellant, brass & thermite** | **`E` (`#f08a30`)** arc + `9` smoke | **`8` (`#5a5f72`)** dead brass ticks on floor | Hot `2×1` casings eject in parabolic arcs (`0xE`) and cool to `8` on stone. |
| **Pulverized stone & dust** (*The Matrix*) | **`A` / `9`** chip burst | **`8` / `2`** carved craters in pillar + expanding Bayer-dithered `9 -> 2` dust | Columns physically lose silhouette chunks as rounds chew into them. |
| **Human / Hunter blood** | **`D` (`#e0407a`)** calligraphic spray / slash (`+ 1px A` under strobe) | **`2` (`#2e2a5e`) / `0`** dark wine pool with **`1px D` wet rim** | Poetic irony (`House Rule 3`): **`0xD` is both the Inquisition's target-lock laser AND mortal arterial blood.** |
| **Witch wound & fallen sister** | **`D` (`#e0407a`)** arterial spray + **`5` (`#2a7f6f`)** scattered hex-sparks | Skin dims from **`6` (`#6fd08c`) -> `4` (`#18404a` deep verdigris)** over a `2`/`D` blood pool | Proves witches are mortal flesh (`0xD` blood) while visibly registering extinguished/wounded green life (`6 -> 4`). |
| **Hex-combat geometry** | **`7` (`#c8f08f`)** razor edge + **`6`** lattice / wire | **`5` (`#2a7f6f`)** residual rune scar | Hexagonal bullet-catch planes (*Matrix* ripple rings), ceiling-drop wire snares, and close-quarters green-etched blades. |

---

## 3. Kinetic Rhythm: Three-Phase Impact (`Anticipation -> Snap -> Hit-Stop`)

Never animate combat as continuous floaty translation or 1-frame teleports:

1. **Anticipation (`4–6 frames` / `0.17–0.25 s`):** Coat drop, pillar plant, rifle laser lock (`0xD` line tightening),
   or green `0x6` sigil coiling at a witch's wrist.
2. **Snap / Transit (`2–3 frames` / `0.08–0.12 s`):** High-velocity directional smear—a dark coat vaulting off a scarred
   stone column, a `0x7` blade arc, or an `0xA` ballistic trace.
3. **Hit-Stop (`4–6 frames` / `0.17–0.25 s`):** **Freeze both striker and target on the exact frame of impact** while
   secondary physics (`0xD` blood arc, `9` stone splinters, `0xE` brass, dust dither) continue expanding—locked to a
   sub-drop + metallic/flesh transient in the score.
4. **Collapse & Settle (`6–12 frames`):** Body drops smoothly to knees then stone; blood arc settles into a persistent
   `0x2`+`0xD` floor pool.

---

## 4. Asymmetric Tactics (`Inquisition` vs. `Coven`)

### The Inquisition (Industrial / Liturgical Breach — *The Raid*)
- **Reliquary Dropship:** Angular black-and-steel (`0, 1, 8, 9`) tilt-thruster assault craft bearing a stark `0xA` hull
  cross, `0xE` downward VTOL wash whipping rain/alkali dust sideways, and a rear ramp flooding `0xA` light around
  stacked `0xD` Hunter visors.
- **Fire-team Doctrine:** Shaped breaching charges (`0xE`/`0xA`) on ancient ruin arches, overlapping automatic
  flechette/dish-rifle cones (`0xA` strobes + `0xD` lasers) that chew stone cover apart, and low-flying Riot-Censers.

### The Coven (Architectural / Geometric Counter — *The Matrix* + Gothic Craft)
- **The Hex-Lattice Catch (`Signal`):** Snaps a flat `0x6`/`0x7` hexagonal plane across a corridor, arresting an entire
  volley of `0xE` slugs in concentric emerald ripple-rings before dropping them or reversing them back down the
  shooters' own `0xD` laser lines.
- **Pillar-Vault & Close Quarters (`Bayou`, `Runner`, `Thorn`):** Kill overhead lights first; use carved stone pillars
  and overhead Worm-ribs as vertical floor—dropping into dead-space behind rifle barrels with green-etched blades (`7`)
  and trip-snares (`6`).

---

## 5. Sound Palette for Combat (`voices.py` + `raid_music.py`)

- **Gunfire & Breaches:** Band-passed transient crack (`1.2–4.5 kHz`) layered over tight 55 Hz chest-thump (`kick`) and
  high metallic casing ticks (`7–10 kHz`), quantized or syncopated against `120–140 BPM` industrial/bodhran breakbeats.
- **Bullet-Catch / Hex-Blade:** Sudden high-pass vacuum suck + crystalline `glass` tritone shimmer (`D` + `Ab`) when
  slugs freeze in the green lattice; razor-sharp FM metallic *shing* (`2.4–6 kHz`) on blade arcs.
- **Casualties & Aftermath:** Never score a death with triumphant brass. Drop the percussion out under a low `D` minor /
  Phrygian organ/cello pedal and solitary Celtic `whistle` (`pietà coda`), letting rain and distant dropship turbines
  carry the weight.

---

## 6. Shared Code Entry Points (`styles/hex/kaledathela/`)

- **`kit_kal.py`:** Cast & combat sprites (`DROPSHIP` helper, `WITCH_THORN`, wounded/fallen swaps, `draw_blood_arc`,
  `draw_blood_pool`, `draw_scarred_pillar`, `draw_hex_lattice`).
- **`raid_plates.py`:** Generates `raid_sheet.png` (Fig. R0: Ballistic/Gore Register Atlas & Dropship) and
  `raid_tableau.png` (Fig. R1: *The Colonnade Breach* hero keyframe).
- **`raid_music.py` & `raid_film.py`:** 32.0-second scored confrontation film (`raid_concept.mp4`).
