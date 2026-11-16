# NIGHT SERVICE on screen: a style guide

Version 2 (version 1 was a paragraph in the README and whatever `op/common.py` happened to do). Written after
the opening (`op/`), its outside review (`op/CRITIQUE.md`, 5 out of 10) and a cold reading of the revision.
Read the house style (`../../STYLE.md`) first; this adds what is particular to the film.

## The idea

Shadow theatre with lit windows. Everyone is a dark paper shape with one lit window in the chest, seen against
a night that is never quite black. The story is told by what the lights do. It is the chop in motion.

## The light code

Rule 3 of the house: one look, one meaning, said twice. The opening coded by colour alone, and two of the
colours were "white". From version 2 every kind of light differs in colour, in shape and in behaviour.

| who | colour | shape | behaviour | sound |
|---|---|---|---|---|
| the night shift (the living who mind a light) | warm, each their own: Orrin `#ffb347`, Dee `#ff9a3c`, Marisol `#ffe08a`, Red `#ff5a3c` | the four-pane window of the chop | breathes a little; dips when they tire | struck and decaying: pluck, bell, punch |
| the dead | the warmest and brightest thing on screen: candle white `#fff0c4`, whole figure pale warm paper | the same window, with a halo that trails behind them as they walk | never flickers; goes out only on the far shore | one glass tone |
| Continuity (the light nobody minds) | cold blue-white `#dbeeff` | a horizontal strip, a tube, never a window | dead steady, and comes on all at once | 720 Hz, sustained, and a hum |
| a Lineman | no window; one round eye | round | cold and steady while cabled; dark when cut; green and unsteady when it is its own | the hum, then silence, then a single struck note |
| the Light, the Board, the lantern | what they are in the world: lamp amber, signal red and green | their real shapes | they are *minded*: each is lit in the same shot as the person minding it | as the night shift |

**Decided here, not yet on screen:** the dead are warm (they carry the light that left a house window, and that
window was warm) and Continuity alone is cold; Continuity's light is a strip. The opening has the dead at
`#fff6cf` on blue-white paper and Lang's window as a cold window. Version 2 applies the table.

## Rules

1. **Black is black.** Figures `#080b11` for the far limbs, `#0e131c` for the body. No rim lines inside a
   figure in a wide shot: at that size they read as construction lines. Register every figure with the bloom
   as a shape to keep dark.
2. **A figure is read by its outline and its window,** so give the outline something to say: the hat, the
   thing carried, the stoop. Six people on one mannequin differ only by hat, and that is not enough (to be
   fixed by the bones study).
3. **Dark on dark is invisible.** A dark figure needs a lighter ground behind the part that acts: sky, water,
   a lit wall. Lang at her dark desk was nearly lost.
4. **The thing that acts is lit, or is the light.** Orrin dozing beside his lamp did not read in either
   version, because the eye goes to the lamp. Stage him lit by it, facing us, and let the head carry the lamp
   down with it.
5. **Screen direction:** the dead and the boat travel right to left (toward the far shore). The night shift
   work left to right. No. 4 faces left until its cable is cut.
6. **The heron is in every setting,** small, and it has seen whatever just happened.
7. **A prop has one model,** in the kit, before production starts: the Tern Point lens, the fire finder, the
   punch and its chad (the chad is the colour of the ticket it came from), the Board, the cable (as thick as a
   ferry's funnel, a jointed hose, with the light travelling inside it), No. 4.
8. **A place has one model** (`places/`, from the spatial study on). The moon is in one place in the sky for
   one night, No. 4 is forty metres tall in every shot, and a camera position is a point on a plan.
9. **Cards never type over the action they name.** The name arrives after the gesture has finished.
10. **A light event waits for the eye.** Not in the first second of a shot. Dim what competes with it, and
    hold the result for at least a second.
11. **Cuts are uneven.** Not more than three shots of the same length in a row.
12. **Grid.** 1280 x 720. From version 2: 24 frames a second; drawings change on twos (`anim.on(i)`), the
    camera, slides, rain and light ramps move on ones. A beat at 120 bpm is 12 frames.
13. **Finish once, in the master:** lens bloom (silhouette-safe), filmic tone, vignette, grain. A shot returns
    an unfinished linear frame.

## The kit

`op/common.py` is the opening's kit (palette, `harbour`, `light`, `sigil`, lettering and `name_card`, the cast
via `figure` and `walk_pose`, `no4`, `heron`, `begin` / `shadow` / `finish`). The cast is `cast.py`. What proved
general has moved to the library: `lab.bloom(protect=)`, `draw.font` and `draw.text`, `backlot.sync`,
`backlot.reader`. Version 2 gets a new kit built on those; the opening's stays as it shipped so the film can
be rebuilt.

## Faults seen so far (check a new shot against these)

- A bright thin line reads as a beam or a spear, not a cable. Thickness is identity.
- The viewer watches the lamp, not the dark man beside it.
- A light event six poses into a shot, with a brighter thing in frame, is not seen.
- A name card wiping in over the gesture it names.
- Far limbs lighter than the body: ghost legs. Bloom from a moon turning a torso olive grey.
- Walkers on a still ground: a treadmill. The deck has to stream past, with seams and posts to show it.
- A tilt at 115 pixels a pose on twelves: a strobe (`sync.travel` flags anything over 1% of the width a frame).
- A one-pose reversal (the lamp recovering for a single pose in the doze) reads as a fault (`sync.pops`).
- A crowd in front of the one person who acts. Three passengers, and they pass *behind* her.
- Cause in one shot and effect nine seconds later.
- The same prop drawn by three hands in three ways; the moon three sizes in three shots.
- A second drawing manner in the same film (the orca came from the print's landmarks and looks painted).
- `C.LAMP` at a gain under 2 blooms red only: a red fringe on the ferry's windows.
- Eleven two-second shots in a row. A four-second hold on a still end card.
- Two seconds of black with one faint point in it reads as "nothing has started".

## Changelog

- v1: the paragraph in `README.md` and the bible's "What it looks like".
- v2: after the opening. The light code as a table with shape and behaviour as well as colour; the dead made
  warm and Continuity made a strip; thirteen rules; the faults list from the review and the cold reading.
