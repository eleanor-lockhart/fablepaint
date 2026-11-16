# NIGHT SERVICE: opening sequence (prototype). Production brief, revision 2

Sixty-two seconds. An anime-style opening that introduces the world and the cast of
`world/night-service/BIBLE.md` (read it first; it is short). Directed by the main session; each unit below is
animated by one agent; the theme is written by another. Revision 2 follows three independent reviews of the
storyboard (`review_storyboard.json`).

**The minute has to tell its own story to someone who has not read the bible.** In order, on screen:
a light stays lit only while someone minds it (Orrin) · when a house's light goes out it walks away in the chest of
a pale figure, and those figures are going to the boat (Marisol, Dee, Red) · a power company replaces minded lights
with light nobody is behind (Lang) · its machine runs on a cable, with a cold eye (No. 4) · the whales cut the
cable; the eye turns green; a window opens in its chest · everyone, in a row, one lit window each.

## Grid

1280 x 720. **12 poses a second** (shot on twos, like the paper boxes). **120 beats a minute, 4/4.**
One beat = 6 poses = 0.5 s. One bar = 24 poses = 2 s. Thirty-one bars = 744 poses = 62 s.
Cuts fall on bar lines unless a unit says otherwise. Picture and music share this grid and never see each other's
files: land your accents on the poses given here and they will be in sync.

## Units

| module (`op/shots/`) | bars | global poses | seconds | N | what |
|---|---|---|---|---|---|
| `a_open` | 1-4 | 0-95 | 0-8 | 96 | cold open, then the title |
| `b_keeper_dee` | 5-8 | 96-191 | 8-16 | 96 | Orrin the Keeper; Dee the Deckhand |
| `c_marisol_red` | 9-12 | 192-287 | 16-24 | 96 | Marisol the Lookout; Red the Signal Maintainer |
| `d_prechorus` | 13-16 | 288-383 | 24-32 | 96 | the crossing; the heron; Vesper Lang and light nobody is behind |
| `e_no4` | 17-19 | 384-455 | 32-38 | 72 | the break (black), then No. 4 revealed |
| `f1_pod` | 20-21 | 456-503 | 38-42 | 48 | the pod goes in; the cable is cut |
| `g1_walk` | 22-23 | 504-551 | 42-46 | 48 | the night shift walking across the moon |
| `g2_lights` | 24-25 | 552-599 | 46-50 | 48 | minder, light, minder, light: one cut a beat |
| `f2_window` | 26-27 | 600-647 | 50-54 | 48 | the eye turns green; a window opens in No. 4's chest |
| `h_lineup` | 28-31 | 648-743 | 54-62 | 96 | the lineup, windows lighting one by one; the end card, held |

## The storyboard (pose numbers are local to each unit, starting at 0)

**a_open.** 0-47: black. Far off, one tiny warm light (Tern Point) blinks at poses 0 and 12. Then on each of four
ticket-punches, poses **24, 30, 36, 42**, one lit window snaps on in the dark: only the window, no figure, at the
chest positions and in the window colours of Orrin, Red, Dee and Marisol standing in a row. 48-95: on pose **48**
the picture opens: the night harbour, the four now visible as dark shapes round their windows, and the title
**NIGHT SERVICE** large, with the sigil. The tagline SOMEBODY HAS TO STAY UP. arrives on pose 72. The title is
fully readable for at least 3 seconds.

**Introductions (b and c): the pattern.** Each introduction is two framings of one set with a hard cut on the bar
line (local pose 24, or 72). Bar one is the *place*: wide, the figure no more than a third of the frame height, the
shot's one light the biggest thing in the picture. Bar two is the *person*: a cut-in on the same figure at about
twice the size (`C.figure(..., size=860, ground=980)`: cut above the knee, the window near the middle of the
frame). The name card starts on the cut: `C.name_card(img, name, C.clamp01((i - start) / 16), side)` with start 24
or 72. Figure on one side, card on the other: Orrin figure right, card `'l'`; Dee figure left, card `'r'`;
Marisol figure right and flipped to face left, card `'l'`; Red figure left, card `'r'`. Nothing pale and nothing
that moves may pass behind a card (roughly x 84-620, y 450-615, or the mirror of that on the right).

**b_keeper_dee.** *Orrin, 0-47.* Wide (0-23): Tern Point, the lighthouse at the right third (tower, gallery,
lantern, a wedge of light turning through the dark), stars. Orrin walks in from the left toward it in his own
walk, a foot down on poses 0, 6, 12, 18, and stops on 24. Cut-in (24-47): Orrin facing the lamp, its light on him.
**The lamp follows his head, not the clock.** Over poses 24-29 he nods off (add about 30 to `head` and 6 to
`lean`: chin on chest) and over the same poses the lamp's light sinks to almost nothing; hold to 35 in near dark,
only his window lit. On pose **36** his head jerks up and the lamp flares back, brighter than before, for two
poses, then settles. This is rule 1 of the world in four seconds: play it clearly.
*Dee, 48-95.* Wide (48-71): the car deck of the M/V *Kittiwake*: steel deck, a chain across, one work lamp. Dee
stands at the chain, cigarette ember glowing. Pale passengers queue toward her **from the right, moving left**.
She punches a card on poses **54 and 66**. Cut-in (72-95): Dee and the first passenger; punches on **78 and 90**,
and here the chad that falls is big enough to see that it is the shape of a window, and lit.

**c_marisol_red.** *Marisol, 0-47.* Wide (0-23): Mount Vesper, the lookout tower among firs under stars. Marisol
stands on the catwalk **in front of the cab's lit band of windows** (this shot's one lamp), at least 200 px tall,
so her head and arms are cut out against it. On the facing hillside, middle distance, one small house with one lit
window. On pose **6** that window goes dark and in the same pose the same light is in the chest of a pale figure at
the door (`C.figure('passenger', ...)`, about 110 px, hat and suitcase): *the light has left the house.* It starts
walking downhill, right to left. Marisol's binoculars come up over poses 12-23 (three held keys: down, half, up;
her standing pose with `binoculars=True` is "up") and reach her eyes on the cut. Cut-in (24-47): Marisol,
binoculars up; and in a hard-edged round hole in the dark at upper left (centre about (330, 250), radius 170),
what she sees: the pale figure with its hat, its suitcase and its brilliant window, walking downhill.
*Red, 48-95.* Wide (48-71): the shore line: rails, a signal mast with its lamp at RED, rain. Red stands by the
track with her red lantern held low. Behind her, pale passengers cross the track **right to left**. On pose
**66** the mast lamp drops from red to green by itself (Continuity has automated it). Cut-in (72-95): over poses
72-78 Red swings the lantern up to head height at arm's length (`shN` 14 to 100, `elN` 10 to 20) and holds it:
she is the signal now. The rain inside the lantern's pool of light is red. The passengers keep crossing.

**d_prechorus.** Three cuts. *0-23, the crossing, wide:* the *Kittiwake*, a long low silhouette with rows of lit
windows, moving slowly right to left across the water in rain, her light broken on the water under her, Tern
Point blinking small in the distance. *24-47, the heron,* close and perfectly still. The rain keeps falling and
the water keeps twinkling behind it, and one pale figure's bright window crosses the far background right to
left, so that it is plainly the bird that is still and not the film. Its eye blinks once on pose **36** (closed
for two poses). *48-95, Vesper Lang:* medium shot, standing at the right third facing left as in the lineup,
figure about 600 px, tablet lit `C.COLD`. Behind her, across the upper two thirds, a terrace of six house windows,
each at least 40 x 56 px, warm (`C.LAMP`), each with a dark head-and-shoulders shape in it: somebody minding it.
On poses **54, 60, 66, 72, 78, 84** she taps the tablet and one window, left to right, flips to cold white
(`C.COLD`) and its head-and-shoulders shape is gone. Brighter, and nobody behind it. Above the terrace a cold-lit
sign: CONTINUITY. `C.name_card(img, 'lang', C.clamp01((i - 72) / 16), 'l')`.

**e_no4.** *0-23, the break:* on pose 0 a hard cut to `C.black()`. Hold. On pose **12** one small slit of COLD
white light opens, upper centre: an eye, the same white as the windows Lang has just switched (its cable is still
in). Put it at the exact pixels where No. 4's eye will be when the tilt below has arrived (`C.no4_eye`).
*24-71, the reveal:* on pose **24** the Sound under a huge moon and No. 4 standing knee-deep in it, far too tall
for the frame (`C.no4(..., height about 1300, eye=C.COLD)`), CONTINUITY stencilled on its chest, the ferry tiny
beside its shin. A pulse of cold light runs down the cable into its back on every beat. The camera tilts from its
legs at the waterline up to its head and shoulders against the moon over poses 24-47, eased, and **lands on pose
48**. Hold 48-71 with the caption NO. 4 and, smaller, THE LINEMAN.

**f1_pod.** 0-23: three dorsal fins cut right to left through the moon's path toward two dark columns at the left
(No. 4's shins), leaving pale wakes; the cable comes down into the water beside the shins, a cold pulse running
down it on every beat. 24-47: an orca rises in an arc beside the cable and takes it in its teeth. On pose **42**
the cable snaps: one or two poses of near-white flash, sparks, the two ends whipping apart; after the flash the
cable is dark and there are no more pulses. The orca may be ported from `styles/lit-window/subjects/orca.py`
(measured landmarks, written for the paint program: adapt it) or drawn as a clean silhouette with its white
patches. It must read as an orca.

**g1_walk.** Orrin, Red, Dee and Marisol walk left to right across the frame in front of the huge low moon of
`e_no4` (`C.harbour(moon=...)`): four dark profiles, four windows, the moon's path on the water under their feet.
This is shadow theatre, which is what these puppets do best: it should be the brightest sustained frame of the
minute. Each walks their own walk, a foot down on every beat (`g = (i % 12) / 12`). Their feet are planted, so each
travels at `C.walk_speed(name, size)` px a pose, which differs: they do **not** hold formation. Marisol slowly
gains; Orrin slowly drops back. The camera travels at about the mean of Red and Dee, so the dock and its piles
slide past and the four drift against the frame. Far off and sliding by slowly, No. 4's two shins with the
severed cable hanging.

**g2_lights.** Eight cuts of 6 poses, a cut on every beat, alternating MINDER then LIGHT. Minders are at the
cut-in size of the introductions (`size=860, ground=980`), facing alternately right and left. Lights are ONE light
on `C.black()`, always at the same place and about the same size (centred near (640, 330), the lit shape about
100 px), with at most one dark shape round it to say what it is: no scenery. 0 Orrin, head up / 6 the lens of the
lamp / 12 Marisol, flipped, binoculars up / 18 the fire finder's brass ring with a walking pale figure in its
sights / 24 Red, lantern out at arm's length / 30 the Board, red / 36 Dee, flipped, the punch closing, a chad of
light falling / 42 the *Kittiwake*'s lit windows, close, sliding right to left: the boat sails. In every cut the
light is at double strength on its first two poses and then settles: each cut is struck on the beat like a note.
Do not use the paper-box renders.

**f2_window.** Pose 0: No. 4's head and shoulders against the moon, the framing `e_no4` ended on; the eye is dark;
the severed cable hangs from its back (`cable='cut'`), a few sparks. Pose **6**: the eye opens GREEN. Poses 8-22:
an eased tilt and push from the eye down to the chest (plates, seams, bolts, the stencilled CONTINUITY). Pose
**24**: a window opens in the chest plate: a slit of warm light that widens to a rectangle over about 6 poses,
like a shutter. Warm light spills onto the plates round it. Inside, scratched lines of handwriting; for the hold
(30-47) one line is legible: I AM TOLD I WROTE THE LAST ENTRY.

**h_lineup.** *0-47, the lineup,* after `world/night-service/lineup.py` (copy what you need; do not import it, it
renders when imported): on the dock in front of the Sound, left to right the heron on its pile (x about 90), Orrin,
Red, Dee, Marisol, a Passenger, Vesper Lang (flipped to face left), at about `size=390`, ground about 595, x about
211, 358, 506, 653, 819, 1024. Far out in the water behind them, upper right and clear of where the title will go,
No. 4 stands whole and dark (`C.no4(..., height about 380, cable='cut')`, eye and chest dark). The heron's eye is
lit from pose 0: it was already watching. Every window starts dark (`window=False, glow=0`). They light one by one
on poses **0, 6, 12, 18, 24, 30** (Orrin, Red, Dee, Marisol, the Passenger, Lang). On pose **36** the seventh: far
off, No. 4's eye goes green and the window in its chest lights, warm. Hold. *48-95, the end card:* pose **48** is
the last hit and a hard cut to the cold open in reverse: black; the seven windows only, small, six in a row low in
the frame and No. 4's apart and higher; the sigil; **NIGHT SERVICE**; SOMEBODY HAS TO STAY UP. Complete on pose 48
and held, unchanged, to pose 95.

## Sync points for the music (seconds)

punches 2.0, 2.5, 3.0, 3.5 · **title hit 4.0** · tagline 6.0 · Orrin's steps on the beats 8.0-9.5; the lamp sinks
10.0-10.9; **it flares at 11.0** · Dee's punch 12.5, 13.5, 14.5, 15.5 · the light leaves the house 16.5 · the mast
drops to green 21.5; Red's lantern is up by 22.5 · pre-chorus 24.0 · heron's blink 27.0 · Lang taps a window cold
at 28.5, 29.0, 29.5, 30.0, 30.5, 31.0; hum rising 28-32 · **BREAK: hard cut to silence 32.0** · the eye opens 33.0 ·
**CHORUS hit 34.0**; a cold pulse on every beat · the tilt lands 36.0 · **the cable snaps 41.5** · the walk 42-46,
a foot on every beat · minder/light, a cut on every beat 46.0-49.5 · half-time 50.0 · the eye turns green 50.5 ·
**the window opens 52.0** · lineup windows 54.0, 54.5, 55.0, 55.5, 56.0, 56.5 · No. 4's window 57.0 ·
**last hit and end card 58.0** · the end card holds, and the sound rings, to 62.0.

## The look (non-negotiable)

- Every person is a **dark paper shape with one lit window in the chest**. `C.figure()` does this. Warm windows
  are the night shift; the palest figures with the brightest windows are the dead; cold white light is
  Continuity; No. 4 has no window, only an eye: **cold white while its cable is in, green once the cable is cut**,
  and then, in `f2_window`, a window.
- Night. A few flat tones, big shapes, no outlines except the cut edge of card. One pool of light per frame.
  If a scene can be played with one lamp, play it with one lamp.
- **A figure is dark on dark, so a gesture only reads where the moving limb crosses the shot's one light.** Stage it
  there: Marisol's arms against the cab's lit windows, Dee's punch hand against the work lamp, walkers' legs
  against bright water.
- **Screen direction.** The dead and the boat only ever travel right to left. The night shift walk left to right,
  against them. No pale figure faces right except the Passenger in the lineup.
- **Nothing counts unless the heron saw it.** The heron is somewhere in every setting of every unit: small
  (`C.heron(..., s=0.05 to 0.12)`), standing on something, never moving, never centred, never under a card, never
  mentioned. Put it against something lighter than itself (sky, moon, water) or it disappears. In `d_prechorus` it
  has its own shot and in `h_lineup` its place in the line; everywhere else it is there to be found the second time.
- Things that give off light are painted with `C.light()` and left alone. **Do not** bloom, tone-map, vignette or
  grain: the master does that to every frame (`C.finish`). The preview applies it for you.
- Motion: holds are good. Ease every camera move (`C.ease`). Nothing moves without a reason. Things that twinkle
  (water, rain) change every second pose: seed them with `i // 2`.

## The contract for a unit

A file `world/night-service/op/shots/<module>.py` that defines `N` (the pose count above) and `frame(i)` for `i` in
`0..N-1`, returning a 1280x720 linear premultiplied RGBA float32 image, fully opaque.

- `import common as C` (the preview and the master put it on the path). Read `op/common.py`: `sky black harbour
  light sigil text write name_card walker walk_speed walk_pose figure no4 no4_eye no4_point heron` and the palette.
  Read `backlot/MANUAL.md`, and `backlot/figure.py` if you pose people (a pose is a dict of joint angles; blend two
  with `fg.blend(a, b, t)`).
- **A walker's feet are planted.** At one step a beat (`g = (i % 12) / 12`) its x must advance
  `C.walk_speed(name, size)` px a pose, or the ground under it must slide by exactly that, or it skates.
- `frame(i)` must be pure and deterministic: the same `i` gives the same picture, in any order, in a forked
  worker. Build plates once at import. No randomness without a fixed seed. If you use `backlot.shapes`, call
  `sh.setup(C.W, C.H, seed)` with a seed that depends only on what should change. `C.harbour` reseeds `sh` itself.
- Under about a second a frame.
- Only write your own module (and scratch under `out/op/<module>/`). Do not edit `common.py`, `cast.py`,
  `backlot/`, or anyone else's shot. If the kit lacks something, define it in your module and say so in your report.
- Everything is drawn in code. No downloaded or generated images.

**Preview and look:** `uv run python world/night-service/op/preview.py <module>` from the repository root, then open
`out/op/<module>/strip.jpg` and single frames in `out/op/<module>/frames/` (f_0000.png is pose 0). Look, fix,
repeat: at least two rounds. Open the exact frames your accents fall on and check they show what the storyboard says.

## Shared placements (so that units cut together)

- **No. 4 against the moon** (the frame `e_no4` lands on at its pose 48 and holds, and `f2_window` starts from):
  `FINAL = dict(cx=600, waterline=1560, height=1300, moon=(640, 400, 300))`, i.e.
  `C.no4(C.harbour(hz=1540, moon=(640, 400, 300), road=False), 600, 1560, 1300, eye=...)`. Its eye is then at
  `C.no4_eye(600, 1560, 1300)`, about (722, 445). `e_no4`'s tilt is the whole scene sliding down 1000 px: it starts
  with the waterline at y = 560 (and the moon still above the frame) and ends at `FINAL`.
- **The low moon of the walk** (`g1_walk`): `C.harbour(hz=470, moon=(640, 330, 250), shimmer=i // 2)`, dock top at
  about y = 600, figures about `size=300`.
- **Cut-in size** for people (introductions and `g2_lights`): `C.figure(..., size=860, ground=980)`.
- **The lights of `g2_lights`** are centred at (640, 330).
