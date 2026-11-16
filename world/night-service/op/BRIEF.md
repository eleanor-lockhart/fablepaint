# NIGHT SERVICE: opening sequence (prototype). Production brief

Sixty seconds. An anime-style opening that introduces the world and the cast of
`world/night-service/BIBLE.md` (read it first; it is short). Directed by the main session;
each unit below is animated by one agent; the theme is written by another.

## Grid

1280 x 720. **12 poses a second** (shot on twos, like the paper boxes). **120 beats a minute, 4/4.**
One beat = 6 poses = 0.5 s. One bar = 24 poses = 2 s. Thirty bars = 720 poses = 60 s.
Cuts fall on bar lines unless a unit says otherwise. Picture and music share this grid and never
see each other's files: if you land your accents on the poses given here, they will be in sync.

## Units

| module (`op/shots/`) | bars | global poses | seconds | N | what |
|---|---|---|---|---|---|
| `a_open` | 1-4 | 0-95 | 0-8 | 96 | cold open, then the title |
| `b_keeper_dee` | 5-8 | 96-191 | 8-16 | 96 | introductions: Orrin the Keeper, Dee the Deckhand |
| `c_marisol_red` | 9-12 | 192-287 | 16-24 | 96 | introductions: Marisol the Lookout, Red the Signal Maintainer |
| `d_prechorus` | 13-16 | 288-383 | 24-32 | 96 | the passengers, the boat, the heron, Vesper Lang and cheap light |
| `e_no4` | 17-19 | 384-455 | 32-38 | 72 | the break (everything goes dark), then No. 4 revealed |
| `f1_pod` | 20-21 | 456-503 | 38-42 | 48 | the pod goes in; the cable is cut |
| `g_walk_montage` | 22-25 | 504-599 | 42-50 | 96 | the night shift walking in step; the three lights, one cut a beat |
| `f2_window` | 26-27 | 600-647 | 50-54 | 48 | a window opens in No. 4's chest |
| `h_lineup` | 28-30 | 648-719 | 54-60 | 72 | the lineup, windows lighting one by one; end title |

## The storyboard (local pose numbers inside each unit)

**a_open.** 0-47: black. Far off, one tiny warm light (Tern Point) blinks at poses 0 and 12. Then on each of
four ticket-punches, poses **24, 30, 36, 42**, one lit window snaps on in the dark: only the window, no figure,
at the chest positions and in the window colours of keeper, red, dee, marisol standing in a row. 48-95: the hit.
On pose **48** the picture opens: the night harbour, the four figures now visible as dark shapes round their
windows, and the title **NIGHT SERVICE** large, with the sigil. The tagline SOMEBODY HAS TO STAY UP. arrives at
pose 72. The title must be fully readable for at least 3 seconds.

**b_keeper_dee.** 0-47, Tern Point: the lighthouse on its headland (tower, gallery, lantern, a wedge of light
turning through the dark), stars; Orrin walks left to right along the ground in front of it in his own walk, a
foot down on every beat. `name_card('keeper', t)` from pose 20 to 47. 48-95, the car deck of the M/V *Kittiwake*:
steel deck, a chain across, one work lamp; Dee stands at the chain, cigarette ember glowing; pale passengers
shuffle in from the right in a queue; on poses **54, 66, 78, 90** she punches a card and a small window-shaped
chad of light drops. `name_card('dee', t)` from 68 to 95.

**c_marisol_red.** 0-47, Mount Vesper: the lookout tower among firs under stars; Marisol on the catwalk raises
her binoculars (blend her arms from hanging to her standing pose with `binoculars=True` over poses 6-18); far
off on a dark hillside one small yellow light walks slowly downhill. `name_card('marisol', t)` from 20 to 47.
48-95, the shore line: rails, a signal mast with its lamp at RED, rain; Red stands by the track holding her red
lantern; behind her two or three pale passengers walk across the track left to right. `name_card('red', t)`
from 68 to 95.

**d_prechorus.** Four cuts of one bar each. 0-23, Ebb Landing: five or six passengers in a line shuffling right
along the dock, windows very bright, the heron on its pile at the left. 24-47, the crossing, wide: the
*Kittiwake*, a long low silhouette with rows of lit windows, moving slowly right to left across the water in
rain, her light broken on the water under her, Tern Point blinking small in the distance. 48-71, the heron,
close and perfectly still; at pose **60** its eye blinks once; nothing else moves (this stillness is the joke
and the rule: nothing counts unless the heron saw it). 72-95, Vesper Lang, close, tablet held up and lighting
her from below; behind her the warm lights of the far shore flip to cold white one after another, left to right,
one every 3 poses; a cold-lit sign: CONTINUITY. A compact `name_card('lang', t)` from 78 to 95.

**e_no4.** 0-23, the break: on pose 0 a hard cut to total black. Hold black. On pose **12** one small green slit
of light opens, upper centre: an eye. Hold. 24-71, the reveal: on pose **24** the harbour under a huge moon, and
No. 4 standing knee-deep in the Sound, far too tall for the frame (`no4(...)` with height 900 or more). The
camera tilts from its legs at the waterline up to its head and shoulders against the moon, arriving by about
pose 58 and holding; green eye; the cable trailing down into the water; the ferry tiny beside its shin for
scale. End with the caption NO. 4 and, smaller, THE LINEMAN.

**f1_pod.** 0-23: three dorsal fins cut right to left through the moon's path toward two dark columns at the
left (No. 4's shins), leaving pale wakes. 24-47: an orca rises in an arc beside the cable and takes it in its
teeth. On pose **42** the cable snaps: one or two poses of near-white flash, sparks, the two ends whipping apart.
The orca can be ported from `styles/lit-window/subjects/orca.py` (measured landmarks) or drawn as a clean
silhouette with its white patches; it must read as an orca.

**g_walk_montage.** 0-47, the walk: Orrin, Red, Dee and Marisol walk left to right in a row, each in their own
walk, a foot down on every beat (advance the stride phase by 1/12 a pose), the camera tracking with them so the
dock, piles and far shore slide past at different speeds; the heron goes by on a pile. 48-95, the three lights:
eight cuts of 6 poses, one a beat: the lighthouse beam / Marisol's brass fire finder with a walking light in
its sights / the Board at red / Dee's punch / the lamp flashing at the lens / the lookout's lit window in snow /
Red's lantern raised / the *Kittiwake*'s lit windows. Finished frames of the two paper boxes are on this machine
at `out/paperlight/lighthouse/frames/f_%04d.png` and `out/paperlight/lookout/frames/f_%04d.png` (1280x720,
72 each, load with `core.load`) and may be used as full-frame cuts; the rest are new close-ups.

**f2_window.** Close on No. 4's chest: large flat dark plates, seams, bolts. On pose **24** a window opens in the
plate: a slit of warm light that widens to a rectangle over about 6 poses, like a shutter. Warm light spills
onto the plates around it. Inside, faint scratched lines of handwriting (its logbook). Hold.

**h_lineup.** The lineup of `world/night-service/lineup.py` (heron, Orrin, Red, Dee, Marisol, a Passenger,
Vesper Lang; No. 4's boot behind them), starting with every window dark. The windows light one by one on poses
**0, 6, 12, 18, 24, 30** (Orrin, Red, Dee, Marisol, the Passenger, Lang); the heron's eye on 36; the title
NIGHT SERVICE and sigil arrive between 36 and 48; pose **48** is the last hit and everything holds; over the
final 12 poses the figures sink to black, leaving only the windows, the sigil, and SOMEBODY HAS TO STAY UP.

## Sync points for the music (seconds)

punches 2.0, 2.5, 3.0, 3.5 · title hit 4.0 · tagline 6.0 · Dee's punch 12.5, 13.5, 14.5, 15.5 · pre-chorus 24.0 ·
heron's blink 29.0 · hum rising under Lang 30-32 · BREAK: hard cut to silence 32.0 · the eye opens 33.0 ·
CHORUS hit 34.0 · cable snaps 41.5 · the walk 42-46, a step on every beat · montage, a cut on every beat 46-50 ·
half-time 50.0 · the window opens 52.0 · lineup windows 54.0, 54.5, 55.0, 55.5, 56.0, 56.5 · heron 57.0 ·
last hit 58.0 · picture ends 60.0 (the sound may ring to 62).

## The look (non-negotiable)

- Every person is a **dark paper shape with one lit window in the chest**. `C.figure()` does this. Warm windows
  are the night shift; the palest figures with the brightest windows are the dead; cold white light is
  Continuity; No. 4 has no window, only an eye (green when it is itself), until `f2_window`.
- Night. A few flat tones, big shapes, no outlines except the cut edge of card. One pool of light per frame.
  If a scene can be played with one lamp, play it with one lamp.
- Things that give off light are painted with `C.light()` and left alone. **Do not** bloom, tone-map, vignette
  or grain: the master does that to every frame (`C.finish`). The preview applies it for you.
- Keep the lower third quiet where a name card goes. Keep subjects off-centre. Leave dark space.
- Motion: holds are good. Ease every camera move (`C.ease`). Nothing moves without a reason. Things that
  twinkle (water, rain) change every second pose: seed them with `i // 2`.

## The contract for a unit

A file `world/night-service/op/shots/<module>.py` that defines `N` (the pose count above) and
`frame(i)` for `i` in `0..N-1`, returning a 1280x720 linear premultiplied RGBA float32 image, fully opaque.

- `import common as C` (the preview and the master put it on the path). Read `op/common.py`: `sky harbour light
  sigil text write name_card walker walk_pose figure no4 heron` and the palette. Read `backlot/MANUAL.md`, and
  `backlot/figure.py` if you pose people.
- `frame(i)` must be pure and deterministic: the same `i` always gives the same picture, in any order, in a
  forked worker. Build plates once at import. No `np.random` without a fixed seed. If you use `backlot.shapes`
  call `sh.setup(C.W, C.H, seed)` with a seed that depends only on what should change.
- Under about a second a frame.
- Only write your own module (and scratch under `out/op/<module>/`). Do not edit `common.py`, `cast.py`,
  `backlot/`, or anyone else's shot. If the kit lacks something, define it in your module and say so in your report.
- Everything is drawn in code. No downloaded or generated images.

**Preview and look:** `uv run python world/night-service/op/preview.py <module>` from the repository root, then
open `out/op/<module>/strip.jpg` (and single frames in `out/op/<module>/frames/`). Look, fix, repeat. At least
two rounds. Check your accents land on the poses above.
