# Cold Reading Report — Kaledathela Setting & *Shuttered Lamp* (v1 -> v2)

Conducted via `backlot.reader` with two isolated `research` subagents pointed strictly at scratch packs outside `/home/eleanor/fablepaint` (`coldread_kal_stills` and `coldread_kal_film`), after sealing maker predictions in `SEALED_KAL.md`.

---

## 1. Score Against Sealed Intent (`INTENT.md`)

### A. Concept Plates (`concept_sheet.png`, `east_bayou.png`, `west_wastes.png`) — Reader `ae6067d3`
| # | Intended Beat | Score | Evidence from Unedited Narration |
|---|---|---|---|
| 1 | Giant banded primary planet + straight cyan subspace ring-corridor | **Landed** | *"A huge, diagonally banded purple gas giant... Cutting diagonally across the sky in both views is a straight, narrow cyan-and-blue conduit threaded through grey elliptical hoops (`0xC RAIL`)."* |
| 2 | Two Texases: East Texas piney/cypress bayou + refineries vs. West Texas caprock desert + pumpjack | **Landed** | *"East Texas/Gulf bayous ('Piney Slough'), cypress swamps, stilt shacks, and refinery gas flares in the East (`K1`), paired with West Texas/Panhandle caprock mesas, nodding oil pumpjacks, utility-pole highways, and storm cellars in the West (`K2`)."* |
| 3 | Four ruin strata stacked in one frame | **Half / Landed** | Identified all 4 strata accurately, **but noted** that without `K0`'s label, the purple ground `WORM-RIB` and cyan sky `0xC RAIL` did not share a visible material/colour link, and `K2`'s sky-rail touched the corner of the highway cross-overpass. |
| 4 | Chromatic law: Inquisition (`0xA` white crosses/cones + `0xD` visors/locks) hunting contraband green witches (`0x5–0x7`) & shuttered `0xF` shelter lamps | **Landed** | *"Because flora is violet, green exists only on witches... The Inquisition hunts via automated spectral/color scanning for green pixels... Warm amber-yellow (`0xF`) belongs solely to the Coven's hidden shelters."* (Caught Hunter's tiny `DISH RIFLE` using `0xC` cyan against our own `B+C = WORM BORDER` legend!) |

### B. Scored Concept Film (*Shuttered Lamp*, 32 s) — Reader `2ab682c0`
| # | Intended Beat | Score | Evidence from Unedited Narration |
|---|---|---|---|
| 1 | Shot 1 (0–8 s): West Texas desert, nodding pumpjack, sky-corridor transit at 4 s, cross-topped convoy reaching checkpoint at 6 s | **Landed (with scale/pop notes)** | Read the planet, sky-tube, nodding pumpjack + steam puffs (`2s`, `6s`), cyan streak (`4s`), and cross-topped patrol (`6s`), **but caught** that the checkpoint crossbar (`1` on `1` before `4s`) appeared to pop in at `4.0 s` and the convoy was too small near the horizon. |
| 2 | Shot 2 (8–16 s): East Texas bayou, flares, cross pylon; Pastor & Hunter on overpass while two drones scan swamp & dark stilt shack (`0 FOUND`) | **Half** | Read Pastor, operator, overpass, flares, cross pylon, stilt shack, and `0x5..0x7` / `0xF` scans, **but mistook** the two hovering Censer-Drones for *"stationary T-topped masts"* because they overlapped the vertical refinery flare pipes and barely translated horizontally, and noted no parked convoy truck on the overpass. |
| 3 | Shot 3 (16–24 s): Underground Worm-rib vault, 3 green witches round one `0xF` lamp; 18 s warning; 20 s Runner shutters lamp into darkness | **Half (critical timing catch!)** | Read the vault, 3 witches, `0xF` lamp, Worm-tap CRT, and `20.0 s` blackout leaving pinpoint eyes, **but caught a major staging flaw**: the white searchlight poured into the lit vault at `18.0 s` *two full seconds before* the lamp went dark at `20.0 s`, and Runner never walked over to physically shutter the lamp! |
| 4 | Shot 4 (24–32 s): Exterior night, patrol recedes, 26 s hatch opens (`0xF`), 28 s green ward on Worm-rib, 30 s sky link | **Landed (with motion notes)** | Read the surface vault under the rib, `26.0 s` relit `0xF` grate, `28.0 s` green wand-to-rib activation, and `30.0 s` cyan link to the sky-tube, **but noted** 1-frame character pops at `26 s`/`30 s`, instant static beams instead of travelling beams, and asked how a ground truck cast a steep top-down beam into a flat ground grate in Shot 3. |

---

## 2. Gap vs. Sealed Predictions (`SEALED_KAL.md`)
- **What we predicted accurately:** We predicted the film reader would question *how* the Shot 3 lantern closed at `20.0 s` without Runner physically stepping to the pedestal, and whether the Shot 4 cellar exit felt abrupt.
- **What our maker's eye missed completely until cold reading:**
  1. **The `18.0–20.0 s` searchlight contradiction in Shot 3:** Because we knew `18.0 s` meant "approaching warning", we overlooked that drawing the white beam *inside* the vault while the `0xF` lamp was still blazing meant the patrol had line-of-sight on the open lamp for 48 frames!
  2. **Drone + flare-pipe overlap in Shot 2:** We knew `DRONE_INQ` was a quadcopter, so our brain separated it from the grey refinery stack behind it; a fresh viewer saw a T-bar mounted on a grey pole!
  3. **How Shot 3's top-down beam enters a flat ground grate:** Having a **flying Censer-Drone** pass directly over the ceiling grate in Shot 3 (`20.25..23.8 s`)—and fly away toward the receding convoy in Shot 4 (`24.0..26.0 s`)—solves both Shot 3's top-down beam angle and Shot 2->3->4 visual continuity!
  4. **Tangencies in `plates.py`:** `K2`'s sky-rail touching the highway cross-overpass corner, and `HUNTER`'s `DISH RIFLE` using `0xC` cyan.

---

## 3. v2 Revision Changes Applied
1. **`kit_kal.py`:**
   - `PASTOR` given a gaunt shadowed face (`8`/`9`) under his wide preacher brim so **`COLLAR 0xA` is strictly his stark white clerical collar** + cross-crozier.
   - `HUNTER`'s `DISH RIFLE` lengthened and re-keyed to `9` steel + `0xA` dish + `0xD` emitter (**zero `0xC` cyan**, preserving `B+C` exclusively for the Worm-Border).
   - Dormant `0xB`/`0xC` insulator nodes added to ancient `WORM-RIB` segments so ground ribs and sky-corridor clearly share one ancient lineage.
2. **`plates.py` (v2):**
   - `K0`: Dithered `0xA` Censer cone (`CONE 0xA`) + dormant `0xC` nodes on Stratum 1 ribs.
   - `K1`: Separated left Censer drone from sky-rail and flare pipe; replaced single low arch with a taller broken double-arch aqueduct.
   - `K2`: Shifted `worm_vp` away from the highway cross-gate (`x=418`, zero tangency); wired a visible Worm-tap conduit from the Worm-rib base into the storm-cellar bulkhead.
3. **`film.py` (v2):**
   - **Shot 1:** Concrete checkpoint gantry visible from `0.0 s`; larger 3-truck convoy (`Pastor + 2 Hunters`) drives right under the checkpoint arch at `6.0 s` and advances into the foreground.
   - **Shot 2:** Pastor's cross-topped truck parked on the overpass behind Hunter & Pastor; refinery flare pipes moved clear of the flying Censer-Drones (which have animated rotor blurs, fly smoothly across open sky/water, and bank West at `14.0 s`).
   - **Shot 3:** At `18.0 s`, **only** the Worm-tap monitor flashes `0xD` red (`DRONE INBOUND`) while **Runner physically walks left (`18.1..19.9 s`)** to the central pedestal and pulls the iron hood down at **`20.0 s`**. Only *after* the vault is dark (`20.25..23.8 s`) does a **Censer-Drone** pass visibly across the ceiling grate above, sweeping full-depth dithered `0xA` beams to the floor while the spider remains as a dark silhouette!
   - **Shot 4:** Both the receding Censer-Drone and red-taillight Pastor truck depart (`24–26 s`); at `26.0 s` the cellar doors swing open and Signal & Bayou **climb smoothly up** out of the glowing `0xF` stairwell; at `28.0 s` the green wand beam **travels upward** and ignites the Worm-rib segments sequentially; at `30.0 s` a green/cyan ward canopy + sky-tether **grows smoothly** from the rib to the Worm-Border.
