# Kaledathela: a visual and thematic setting guide (for Hex)

Version 0.1. A setting for future Hex pieces — written as a **visual, spatial and musical grammar**, not a lore
bible. Names, histories and politics stay deliberately archetypical so each piece can invent only what its shot
needs. Built on top of `../STYLE.md` (Hex) and `../../../STYLE.md` (the house style).

---

## The premise in one picture

An Earth-sized, Earth-gravity **toxic megamoon** orbiting the giant **Kaledathela**, parked right against an
ancient **subspace tunnel border** built by the long-gone **Worms**. On the ground it looks like **Texas at night** —
wet, tangled **East Texas** where people and refineries crowd together; flat, scrub-and-mesa **West Texas** out in
the waste — built over the bones of several dead empires and currently held by an **authoritarian dominion**. A
**coven of witches** lives here in hiding, hunted by technologically armed religious inquisitors led by **The
Pastor**.

The tension in every frame is Hex's core tension turned into geography: **an indifferent toxic expanse + an actively
hostile perimeter overhead, set against one tiny, shuttered pocket of tended warmth (`register F`)**.

---

## 1. The sky (how you know it is not Earth)

Every exterior shot shows **Texas below** and **Kaledathela above**:

1. **The Primary (`Kaledathela`):** Huge (`20` to `30` degrees across — forty times Earth's moon), low, banded in
   bruised slate, violet and twilight (`registers 1, 2, 3, 8, 9`), half-eclipsed into a giant sickle or dome on the
   horizon. It does not move during a shot.
2. **The Worm-Border (the subspace route):** A ruled geometric scar cutting straight across the sky — a chain of
   ancient segmented rings and parallel containment rails (`register C` aqua filament inside `8`/`2` stone-metal
   ribs) converging to a vanishing point on the horizon, like an interstate border drawn across space. Now and then
   a 2-pixel vessel spark (`A`/`C`) drops in or slips out along the line without fanfare.
3. **Toxic air:** The horizon never clears to clean black or blue. Haze sits in chemical violet (`2`, `3`) and steel
   (`8`), with low bayou mist in the East and dry alkali dust in the West.

---

## 2. Two Texases on the ground

| | **The East** (populated, wet, vertical) | **The West** (desert & waste, dry, horizontal) |
|---|---|---|
| **Land & plants** | Stagnant dark bayous, sloughs, drainage canals. **Loblolly pines** (tall bare trunks for the lower two-thirds, irregular high crown tufts) and **bald cypress** (flared buttresses, conical knees in the water, hanging moss). **Zero green** — foliage is `0, 1, 2, 8`. | Flat **caprock mesas**, terraced scarps, alkali salt pans, caliche hardpan, **ocotillo, yucca and creosote** silhouettes. Sky takes two-thirds of the frame. |
| **Built world** | Petrochemical **cracking towers, pipe racks, flare stacks** (`E`/`D` waste flame), concrete highway overpasses on T-piers, corrugated-tin sheds, neon/LED **imperial broadcast crosses**, wet asphalt reflections. | Endless straight two-lane blacktop, wooden H-frame power lines, solitary **Lufkin pumpjacks** nodding in the dark (`curved horsehead, walking beam, rotary counterweight`), rusted tank batteries, dead cinderblock gas stations. |
| **Where the Coven hides** | *Inside the tangle:* stilt shacks deep in the cypress brake, culverts under highway interchanges, overgrown substations. | *Underground:* storm cellars, capped shafts, hollow Worm-conduits beneath the caliche, where one crack of `F` light shows for miles. |

---

## 3. Deep time: four strata in the dirt (never explained in text)

Any scene may stack two or more of these in the same frame without commentary:

1. **Worm architecture (oldest, non-human):** Enormous curved, segmented, jointless rings and parabolic ribs (`1, 2,
   8`) jutting out of desert hardpan or drowned in swamp water — the same geometry as the subspace border overhead.
2. **Fallen empires (two or three incompatible orders):** Toppled stone viaduct arches, cracked fluted domes, rusted
   orbital-tether stumps — quarried, tilted, and cut straight through by later roads and pipelines.
3. **Boomtown vernacular:** Corrugated tin, cinderblock, chain-link, oil pipe, wooden utility poles, faded signs.
4. **The Dominion (now):** Battered brutalist concrete pylons, radar dishes, highway gantries, and The Pastor's
   revivalist-surveillance towers bolted onto whatever stood there first.

---

## 4. The light and register code

Hex's sixteen registers (`0` to `F`) are strict law here. **Because toxic flora on the moon is indigo, slate and
violet (`1, 2, 3, 8`), witches really are the only green things in the world** — and The Pastor's instruments hunt
them by scanning for green registers (`0x5..0x7`) and un-registered warm lamps (`0xF`).

| who / what | registers | shape | behaviour | sound |
|---|---|---|---|---|
| **The Coven's shelter** | **`F` (`#ffd870`)** — *reserved, sole glow* | a shuttered slit, a trapdoor seam, a hooded lamp | still while safe; **shuttered dark** when hunters sweep | warm acoustic pluck, harp, hand-drum |
| **The Coven & hex-work** | **`5, 6, 7`** (`#2a7f6f`, `#6fd08c`, `#c8f08f`) | green skin/eyes; hexagonal ward-sigils; green terminal type | motionless until acting; instant when cast | whistle, low fiddle, tritone bell |
| **The Pastor & Hunters** | **`A` (`#e8ecf4`)** stark white + **`D` (`#e0407a`)** lock-on | **cross-slits**, hard conical searchlights, sweeping laser grids, white clerical collar | mechanical, unhurried sweep; HUD bounding boxes | 60 Hz hum, sustained organ/choir, sonar ping |
| **Refineries & waste** | **`E` (`#f08a30`)** + **`D` (`#e0407a`)** | ragged flare plumes, hazard beacons, sodium glare | restless, un-minded, reflected in oil/water | low sub rumble, steam hiss, pump clank |
| **The Worm-Border** | **`C` (`#59d8f0`)** + **`B` (`#3a78d8`)** | ruled parallel rails & segmented rings across the sky | invariant, indifferent | faint high glass harmonics |

---

## 5. Silhouettes (`kit_kal.py`)

- **The Pastor:** Tall, rigid, upright; **wide flat-brimmed West Texas preacher's hat** (`0` with `8` edge so it
  reads against night sky), ankle-length black cassock-duster, **2-pixel stark white clerical collar (`0xA`)** at
  the throat, carrying a **broadcast crozier / directional antenna** topped with a lit white-and-crimson cross.
- **Witch Hunters & Censer-Drones:** Trenchcoat rangers with flat-brim helmets, crimson (`D`) visor slits and
  parabolic dish-rifles; hovering cruciform drones sweeping hard `A` cones downward with `D` target reticles.
- **The Coven (individuals, never a uniform copy):** Pointed or battered hats, ragged coats over work boots, green
  skin (`6`), tending jury-rigged field radios, Worm-stone taps, spiders, and one shuttered `F` lantern.

---

## 6. Staging rules for future videos

1. **Show the sky early, then play the ground.** One wide shot with the Primary and the Worm-border establishes the
   moon; nobody needs a caption explaining Kaledathela.
2. **Light is stealth.** Unlike `Uptime` (where the lit window defies the crowd openly), here `register F` is
   contraband warmth: shuttering a lamp before a white searchlight crosses the roof *is* an action scene.
3. **Machines keep rhythm; hunters sweep; witches wait.** Pumpjacks nod on a 4-second period; flare stacks flicker;
   searchlights pan on ones; a witch holds completely still until the frame she acts.
4. **Keep the deadpan.** High-tech religious telemetry (`PASTORAL SCAN: 0x06 NOT FOUND // AMEN`) and mundane Texas
   roadside grit sit side by side with a straight face — neither camp nor grimdark.

---

## 7. Combat, Ballistics & Soft-R Violence (`COMBAT.md`)

When a patrol turns into a breach or confrontation, follow [`COMBAT.md`](COMBAT.md):
- **Muzzle strobes & stone erosion (`0xA`, `9`, `8`):** Gunfire acts as stroboscopic flash lighting in dark ruins and
  permanently craters carved stone cover (*The Matrix* lobby grammar). Hot brass & VTOL thrusters use **`0xE`** —
  **never `0xF`**, which stays reserved for the defended shelter lamp even mid-firefight.
- **Arterial blood & mutual cost (`0xD` -> `0x2`):** Both sides take real casualties. Fresh arterial spray/slashes use
  calligraphic **`0xD`** (`#e0407a`, the Inquisition's own target-lock colour turned mortal) before settling into
  persistent dark `0x2` wine pools with a `1px 0xD` wet rim. When a witch is struck down, she bleeds `0xD` while her
  bright **`0x6` green skin dims to `0x4` (`#18404a`) deep verdigris**.

---

## 8. Reference Files for Agents (`styles/hex/kaledathela/`)

| File | Purpose |
|---|---|
| `STYLE.md` | Visual, chromatic, spatial & musical setting grammar (East/West Texas + Worm-Border + 4 strata) |
| `COMBAT.md` | Soft-R gothic combat, ballistics, destructible cover & chromatic blood/wound doctrine |
| `kit_kal.py` | Shared cast sprites (`PASTOR`, `HUNTER`, `DRONE_INQ`, `WITCH_SIGNAL`, `WITCH_BAYOU`, `WITCH_RUNNER`, `WITCH_THORN`, casualties) + `draw_sky_canvas`, `draw_loblolly`, `draw_cypress`, `draw_pumpjack_2d`, `draw_dropship`, `draw_scarred_pillar`, `draw_blood_arc`, `draw_blood_pool`, `draw_hex_lattice` |
| `plates.py` | Setting concept plates (`concept_sheet.png`, `east_bayou.png`, `west_wastes.png`) |
| `music.py`, `film.py` | *Shuttered Lamp* (`kaledathela_concept.mp4`, 32 s, `14/14` sync) — stealth & setting test (`BRIEF.md`, `COLD_READ.md`) |
| `raid_plates.py` | Combat concept plates (`raid_sheet.png`, `raid_tableau.png`) |
| `raid_music.py`, `raid_film.py` | *Reliquary Drop* (`raid_concept.mp4`, 32 s, `14/14` sync) — dropship breach & CQB test (`COLD_READ_RAID.md`) |
