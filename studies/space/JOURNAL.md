# Learning space

The second study on the roadmap. Ellie's brief: "thinking out physical environments you want to depict,
modeling them as vector/CAD images and also 3D spaces, and then translating that into perspective and motion in
your images/animation/worlds."

Goals and tests are in `../../ROADMAP.md`. This journal is the evidence, in the order things happened.

## Entry 0. Before any research or any tool: what I think I am doing, and a baseline

**Where I am.** Every picture so far is a flat stage seen square-on. Lit Window has a `camera()` that I used
for one ferry and one lookout, each as a single object set down on a painted ground. The opening has no space
at all: I put things at pixel positions that looked right, so the moon is a different size in every shot and
No. 4 is whatever height fitted the frame. The outside review asked three questions I could not answer: where
is the moon, how big is No. 4 beside a person, and what does a camera see when it moves.

**What I think the skill is.** Three things, and I only have part of the third.

1. *Thinking a place out*: deciding where things are and why, in metres, before drawing any of it.
2. *Holding it as one model* that can be looked at from above, from the side, and through a lens.
3. *Predicting what a camera will see*, well enough to choose the camera on purpose.

**The baseline.** For the prints I drew each subject from memory before looking at a reference, and kept the
drawing. The equivalent here: think a place out, describe three cameras in it, and write down *by feel* where
things will land in the frame. Then build the tool and score the guesses.

### Ebb Landing, thought out (metres; x east, y north, z up from tonight's water)

The Sound runs north and south. Ebb Landing is on its east shore, so the water and the far shore are to the
west and the hills are behind, to the east. The shoreline is the line x = 0.

- **The hill and the houses** rise to the east. The dead come down from there.
- **The Shore Line** (the railway) runs north and south along the foot of the hill at x = +35, and the road to
  the dock crosses it on the level. *So the dead have to cross the tracks to reach the boat.* That is why the
  Board is held at red from 1:10 to 1:35, and it took drawing a plan to see it. Signal 114.2 stands sixty
  metres south of the crossing.
- **The ticket office** is on land north of the road, eight metres square, with the union's drawer in it.
- **The trestle** runs straight out west from the shore for ninety metres, twelve wide, its deck five metres
  above the water on bents of four piles every seven and a half metres.
- **The waiting shed** stands on the trestle's south edge sixty to seventy metres out. One window.
- **The chain** where Dee punches tickets is across the deck at eighty-eight metres.
- **The transfer span** hinges at the end of the trestle and slopes down twenty-seven metres to the boat,
  hung from two towers fourteen metres tall with a beam across their tops.
- **Slip 3**: two wingwalls splayed like a funnel for the bow, and dolphins (lashed clusters of piles) further
  out on each side. The heron's dolphin is the outer one on the north side.
- **The *Kittiwake*** lies in the slip, bow to the span: fifty-two metres long, fourteen in the beam, car deck
  2.8 above the water, cabin above that, a wheelhouse at each end with its roof at 11.2, funnel top at 14.
  The funnel is 2.2 across, and the bible says the Cable is as thick as a ferry's funnel, so the Cable is 2.2.
- **Slips 1 and 2** are north of it: only their piles are left.
- **No. 4** stands in the Sound to the north-west, about five hundred metres from the end of the trestle,
  forty metres out of the water. Its cable runs east to **Substation 9**, on the shore three hundred metres
  north of the dock.
- **Tern Point** is two and a half kilometres to the south-south-west. **The far shore** is four and a half
  kilometres west, which from a standing eye is just at the horizon. It is never shown.
- **The night.** The boat sails at 1:35. For the moon to be low over the water in the west at that hour it
  must be a waxing moon a few days past first quarter, going down. Not a full moon: a full moon at 1:35 is
  high in the south. So the opening's big round moon over the water is the wrong moon for the hour.

### Three cameras and my guesses (written before doing any arithmetic)

Frame 1280 x 720, y measured down from the top.

**Shot 1. Wide, standing on the trestle.** Eye 1.6 above the deck, thirty metres out from shore, looking due
west and level, 28 mm lens (full-frame).

| what | my guess |
|---|---|
| the horizon | y = 360 |
| Dee at the chain (1.65 m tall, 58 m away): her height on screen | 70 px |
| the trestle's width (12 m) where she stands | 300 px |
| top of the span towers (19 m up, 87 m away) | y = 150 |
| top of the funnel | y = 250 |
| No. 4: where, and how tall | x = 1000, 200 px tall |
| the moon (15 degrees left of west, 9 degrees up): where, and how wide | x = 360, y = 200, 40 px wide |

**Shot 2. Long, from the door of the waiting shed, on Dee at the chain** (26 m away). 85 mm lens.

| what | my guess |
|---|---|
| Dee's height on screen | 240 px |
| how much of the deck's width the frame takes in at her distance | 8 m |
| top of the span towers | out of the top of the frame |
| roof of the near wheelhouse | y = 150 |
| the heron on its dolphin (1 m tall, about 89 m away): how tall, and where | 12 px, x = 900 |

**Shot 3. High, from thirty metres up over the shore south of the road** (x = +40, y = -60), looking at the
seaward end of the trestle. 35 mm lens.

| what | my guess |
|---|---|
| the horizon | y = 120 |
| the trestle's ninety metres, end to end on screen | 500 px |
| the *Kittiwake*'s fifty-two metres on screen | 220 px |
| No. 4's head against the horizon | 30 px above it |
| the ticket office: where | bottom right, about x = 1050, y = 600 |

## Entry 1. The reading

What practitioners do, and the few numbers that matter. Sources at the end of the entry.

- **Layout, in Japanese animation.** One drawing per shot, made before any animation, that fixes the camera,
  the perspective, the staging and the background together. The "layout system" is credited to Miyazaki on
  *Heidi* (1974), with parallel experiments elsewhere (Shibayama's "movement layouts" on *Gamba*, 1975). It is
  the job a director of photography does on a set.
- **Oshii's rule.** On *Patlabor 2* Oshii asked his layout artists to imitate lenses, because animated films are
  "based on memories of live-action images" and so should obey the laws of the camera. Kon Satoshi drew a
  sequence to look like telephoto and wide-angle shots on purpose; the animation director says Oshii kept
  asking for the camera to go lower, since a low wide lens makes a space bigger. His layouts were published as
  a book called *Methods*. I have read about it, not read it.
- **The horizon is the eye.** The horizon line is at the camera's height. Every standing figure of the same
  height, on the same ground, is crossed by it at the same point of the body. One horizon per picture.
- **On a film set** the equivalent of a plan is the *overhead*: a bird's-eye drawing of the space with every
  camera setup marked and numbered, and the lens written beside it.
- **The giant moon.** Its size in the frame is set by the focal length. Its size *beside a person* is set only
  by how far away the person is: for the moon to be as tall as something, stand about 110 times that thing's
  size away from it. And it has to be on the horizon, because the camera is on the ground.
- **Moving the camera.** For a pan, not more than one frame-width in seven seconds (0.6% of the width per
  frame at 24), or it judders. The old animators' rule: camera moves on ones.
- **A ferry slip** is a trestle, a bridge seat, a transfer span that hinges down to the boat (hung from towers
  with counterweights on the old cable-operated kind), two wingwalls that funnel the bow in, and dolphins
  further out.

Sources: fullfrontal.moe on the layout system; animationobsessive.substack.com ("Life Under Martial Law") and
animetudes.com on *Patlabor 2*; artyfactory.com and startbaynotebooks.substack.com on the horizon and eye
level; neiloseman.com and jameskicklighter.com on overheads; photopills.com and garyhartblog.com on the moon;
red.com ("Panning Speed Best Practices"); Washington State Ferries *Terminal Design Manual* M 3082, chapters
600 to 650; the low-precision formulas for the sun and moon from the *Astronomical Almanac*.

## Entry 2. A tool, a place, and what the place knew that I did not

**The tool** is `backlot/space.py`. A `Set` holds solids in metres. `drawing()` turns it into a plan, an
elevation or a section as SVG. A `Camera` is a position, a direction and a focal length; `render()` shows the
set through it with hidden surfaces removed and gives back depth, a matte per solid, plane normals and a line
pass. `moon()` is a small almanac. Figures, No. 4 and the heron go into the set as flat paper cards standing
at a point and facing a compass bearing, so the set hides them properly and the camera sizes them.

**Is it right?** Two outside checks. The almanac puts the sun and moon 0.19 degrees apart at the instant of
greatest eclipse on 8 April 2024, and gives the right dates for this month's new, quarter and full moon. And
the same set through Blender's own camera agrees with my renderer on 99.98% of pixels or better in all three
baseline shots (`ebb_landing.py check`).

**The place** is `world/night-service/places/ebb_landing.py`, and everything in `places/ebb-landing/` comes
out of it: two plans, two elevations, a section through the trestle, a map of the Sound, a size sheet, layout
sheets and night frames for three cameras, a lens sheet, and eight seconds of film.

### The baseline, scored

`ebb_landing.py score`, against the guesses in entry 0.

| | by feel (entry 0) | with four rules (below) |
|---|---|---|
| where things are | off by 10.8% of the frame on average, worst 59% | 0.1%, worst 0.1% |
| how big things are | off by a factor of 1.8 on average | within 3% on average, worst 10% |
| the horizon | right, or within 3% | within 0.1% |

By feel I put the horizon in the right place and almost nothing else. With a wide lens I drew far things two to
four times too big (Dee 2.5x, No. 4 2x, the moon 4.2x). With a long lens I drew them too small (the heron at
0.4x). **My hand has one lens, about 50 mm, whatever lens I say I am using.** That is why the opening is flat:
things were placed as if by a wide lens and sized as if by a long one.

The four rules, which took a minute each to apply in my head for round two (`score2`, three new cameras, the
predictions written before it was run):

1. The focal length in pixels is 35.6 times the focal length in millimetres (for a 1280 frame).
2. A thing's size on screen is that, times its size, over its distance.
3. The horizon is at the centre of the frame, moved by the focal length times the tangent of the tilt.
4. The moon is the focal length in pixels over 110.

### What the place knew

1. **Why the Board is held at red.** The railway runs along the shore between the hill and the dock, so the
   dead, coming down from the houses, have to cross the tracks to reach the boat. It was in the bible as a rule
   and I had never seen that it was a fact about where things are.
2. **Which night it is.** For the moon to be low over the water at 1:35 it has to be a waxing moon going down
   in the west. The almanac says: the small hours of Friday 20 November 2026. At 1:35 a moon 77% lit stands 8.5
   degrees up and almost exactly due west, over the far shore, so the boat sails down the moon's own road. It
   sets at 2:32. The big round moon in the opening is the wrong moon for the hour.
3. **What the giant moon costs.** For four people to walk across a moon as big as the opening's, the lens is
   1,549 mm, the camera is 312 metres from them, and the moon has to be under one degree up, which that night
   is at 2:24:38. The camera has to be lower than they are, so it stands on the tide flat of Ebb Creek and
   they walk the railway trestle across its mouth, north, toward Substation 9. From there the frame is only
   four metres tall where they are: there is no water in it at all, only sky. The opening's "moonlit water
   between the piles" and its moon cannot be in the same shot.
4. **No. 4 gets in the way.** On the exact line from the moon through No. 4, its legs are wider than the moon
   and all that shows is a white slot between two pylons. The walkers cross ten metres south of that line, so
   that the moon sits between No. 4's hanging hand and its leg.
5. **How big No. 4 is.** Twenty-four Dees. In the opening's lineup it is about three.
6. **Where a camera cannot stand.** From the doorway of the waiting shed, where entry 0 put camera 2, the
   shed's own wall hides Dee. For the lens sheet, the 100 mm position was inside the shed and the 300 mm
   position had the shed between it and her.
7. **The Cable is 2.2 metres across,** because the bible says it is as thick as a ferry's funnel and the
   funnel had to be given a size.

### Two lenses (`ebb-landing/two_lenses.mp4`)

The same four people on the same trestle, six seconds apart. First a 35 mm lens walking beside them on the
tide flat, 26 metres off: they are 85 pixels tall, the moon is an eleven-pixel coin on the horizon with its
road on the water, and No. 4 stands beside it. Then the 1,549 mm lens, locked off: the moon is 500 pixels
wide and they walk through it.

Checked with the instruments: `sync.pops` empty. In the tracking shot the picture slides 0.8 pixels a frame
(the strobe limit is 7.7). No. 4 drifts toward the moon while the trestle's piles stream past and the moon
stays put, which is parallax that nobody animated.

- **Twos slip against a moving camera.** A drawing held for two frames while the camera moves every frame
  slides back and jumps forward. So the walkers are on ones in the tracking shot and on twos in the
  locked-off one. House rule 17 needed that second half.
- **`sync.travel` reads the figures when the background is plain.** In the locked-off shot it reports nine
  pixels a frame of "camera" movement. That is the walkers; the sky behind them has nothing to hold on to.

### My own verdict, written before anybody else has looked

What I think works: the plans and elevations read as a place; the long-lens frame is the best single image I
have made of this world and I did not design it, I found it; the lens sheet shows what a lens does.

What I think is weak:

- The night frames are flat tones on boxes. Surfaces have one texture (planks). The hill is a staircase.
- The pools of light cast no shadows, and a window lights the wall it is in: the *Kittiwake*'s cabin goes cream.
- A gibbous moon drawn truthfully looks like an egg. I do not know yet whether a viewer reads it as a moon.
- The figures are profile cards. Anything but a side view of a person is still impossible, so "a figure
  walking toward the lens" is not done; it needs the turnaround from the bones study.
- The wide shot has a dark bank filling its left edge, and the four figures are small and dark against a dark sky.
- No cold reader has seen any of it. The test "a stranger can list what is where" has not been run.
- The second round of guesses was arithmetic, not a better eye. I think that is the right lesson, and it is
  also what somebody would say who had not improved.

### Where the study stands against its goals

| goal | state |
|---|---|
| Think it out | by feel: 11% and a factor of 1.8. With the rules: 0.1% and within 10%. Target met, by arithmetic |
| One model per place | done for Ebb Landing: plans, elevations, section, shots and film from one file; agrees with Blender |
| One sky | done: the moon comes from the almanac in every frame; its size from the lens |
| Lenses on purpose | lens sheet done; camera plot on the plan done for three cameras; the two-lens film |
| Motion in depth | a tracking shot on ones, under the strobe limit. A figure walking toward the lens: not done |
| It reads | not tested |

Next: the cold reader, given three frames and asked to list what is where. Cast shadows, by letting Blender
light the same set. Tern Point and the tower on Mount Vesper. A crane and a push-in. And one picture that is
*finished*, not only correct.

## Entry 3. Flat drawings in deep places

Ellie's next assignment was this study's unfinished half, put plainly: learn to put 2D animation in 3D space
("2.5D", with perspective) and make something with it. The something is *Base Case* (`styles/hex/basecase/`,
and entry 6 of that style's journal). This entry is about the skill.

### What 2.5D is, by its history

Every one of these is a way of getting depth without modelling everything, and each is one rule:

| when | the trick | the rule under it |
|---|---|---|
| 1930s, the multiplane camera; 1980s, parallax scrolling | flat layers at different distances, slid by different amounts | apparent motion is one over distance |
| 1980, the first graphic adventures | a perspective drawing in lines, which never moves | a picture can be in perspective without being a space |
| 1984 to 1993, adventure games | a painted room with a hidden map of what is in front of what; a figure drawn smaller the higher up the screen she walks | size is one over distance; whoever is nearer covers |
| 1992 to 1993, Wolfenstein and Doom | walls as textured strips scaled by distance; everyone a flat picture that always faces you | a figure can be a card |
| 1996 to 2000, painted backgrounds with polygon figures, and paper figures in polygon rooms | one of the two is flat and the other is not, and the camera has to be told which | the flat thing must be lit and hidden by the same space as the solid thing |
| 2018 on, "HD-2D" | pixel-art figures and pixel-art textures in a lit, shadowed room, seen by a moving camera | all of the above at once |

So "2.5D" is not a look. It is a model that knows where things are, plus a decision, made once, about which
things are flat.

### The four rules I was missing

`backlot/space.py` could already say where a thing lands on the screen. What it could not do was make a flat
drawing belong in the place. `backlot/depth.py` adds that, and it comes to four rules:

1. **A texel is a size in the world.** Every surface is painted on one grid (5 cm) and every figure is drawn on
   the same grid. Then a brick, a stair tread and a shoe agree what a pixel is, at every distance, and the only
   way to make a figure bigger is to move the camera. (Before this I sized figures per shot.)
2. **Light is worked out per texel.** The lamps are summed at the middle of each texel, so the edge of a shadow
   is the same hard square as the paint under it. Screen-space light on world-space pixels looks like a filter
   laid over the picture. Shadows are depth maps: one down the beam of a torch, six round a bare bulb.
3. **A figure is a card.** A cut-out, standing in the set: the set hides it, lamps light it, and it casts a
   shadow shaped like itself. A card that casts and is not drawn gives a shadow of something that is not there.
4. **The camera moves; the paint stays.** Nothing is slid by hand. A camera move is a list of keys (where it
   stands, what it looks at, what lens) and the parallax is whatever follows.

Two things I got wrong on the way and now know:

- A camera tied to a walking figure steps when she steps. The first tracking shot strobed at 2.4% of the frame
  width a frame. The camera needs a path of its own, straight runs with the corners rounded off; then 0.45%.
- Dithering between levels of light, even on the texel grid, reads as dirt. Five or six flat steps read as light.

Tests in `backlot/tests/selftest.py`: a card twice as near slides twice as far; the texel under a pixel is the
5 cm square the pixel looks at; a lamp behind a wall lights nothing on this side; every pixel of one texel
gets one level; a hole in a card shows what is behind it.

### What the study's list looks like now

| goal | state |
|---|---|
| cast shadows | done, in my own renderer and not Blender's: texel-sharp, from fixed and moving lamps, and from cards |
| a crane and a push-in | done: the last shot of *Base Case* rises through the ground from the basement to the house; the push-in goes over a shoulder and through a screen |
| surfaces with more than one texture | done: eleven painted skins (block, brick, boards, siding, snow, earth in section) |
| a tracking shot in depth | done, with a figure walking in it: stairs, floor, round a desk |
| one model, more than one picture | further than planned: one house, four prints (now, 1989, 1987, 1980) from one file |
| a figure walking toward the lens | still not done. Cards face the lens, so she has a back view and a side view, and no turn between them |
| it reads (a stranger can say what is where) | tested as a story by a cold reader (see the Hex journal); not yet as a plan |
| Tern Point, Mount Vesper, the car deck | not done |

What is still by feel: how bright a lamp is and how far it reaches (I tuned them by looking); and how much of a
frame should be dark.
