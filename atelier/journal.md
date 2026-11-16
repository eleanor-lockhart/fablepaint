# Atelier journal

Working notes for developing one style on purpose. Newest entries at the bottom.
`STYLE.md` is the distilled guide; this file is the evidence behind it.

---

## Entry 0. Before any research: what I think I want

**Why the last two pictures looked like dioramas.** I looked at how I actually built them.
Every object got its own layer, its own lighting recipe and its own crisp alpha edge; then the
layers were stacked back to front. Nothing was ever painted *into* anything else. Sharpness was
uniform across the picture, texture was fractal noise spread evenly inside each cut-out, and
colours were chosen per object ("the whale is black") rather than per light. That is exactly
how a paper theatre is made, so that is what it looked like.

**What I can and can't do.** I never see a mark while I am making it. I plan, execute blind,
then look. Styles whose beauty is in the hand's live response (alla prima oils, sumi-e,
loose watercolour) are the ones I would have to fake. Styles whose beauty is in decisions
made *before* the cut (woodblock printing, serigraphy, poster gouache, cut paper) are how I
already work. A printmaker carves a block for each colour, in a fixed order, and cannot see
the print until the paper is pulled. That is my actual situation.

**So the hypothesis:** stop hiding the stack of flat shapes and design it instead. Work in the
tradition of the Japanese *shin-hanga* landscape print (Kawase Hasui, Yoshida Hiroshi) and
its poster/ligne-claire cousins: few flat colour blocks, gradations instead of modelling,
one selective carved line, one light source.

**What I'm drawn to as subject** (looking back at what I chose when given a free hand:
a lighthouse, a desk at night, an aurora with one small figure): night or dusk, weather,
a small warm light inside a large cool dark, and the human systems that keep running when
nobody is watching them: ferries, signal lights, lookouts, laundromats, greenhouses.

**Things I suspect I bring that a 1930s Tokyo workshop didn't:** exact construction
(perspective and astronomy can be computed, not guessed), pattern as texture (ruled rain,
modular waves) in place of noise, and the fact that my "blocks" are literally a script, so
the progressive proofs come for free.

**Test plan** (Ellie's three questions):
1. *Reference vs memory*: paint Study 0 right now, from memory of what a shin-hanga print
   looks like and what a Washington State ferry looks like. Then research, look at real
   prints and real photographs, and repaint. Compare.
2. *Chosen vs assigned subject*: the orca/mech was assigned, everything here is chosen.
3. *Can notes train a style*: write `STYLE.md` after research, revise it after every
   picture from that picture's critique, and see whether picture N+1 avoids picture N's faults.

---

## Entry 1. Study 0 (from memory) and what the reading said

**Study 0** (`studies/s00_memory.png`). What I produced from memory was a travel poster:
smooth digital gradients, a toy ferry dead centre, scribbled wave lines spread evenly,
random-dot stars, confetti reflection. I had remembered shin-hanga as
"flat shapes + gradient + outline". That is the cliché of it, not the thing.

**Reading** (sources at the bottom of `STYLE.md`):

- Yoshida Hiroshi, *Japanese Wood-block Printing* (1939). The artist "must see the end
  from the beginning"; the colour analysis is of "the picture in the artist's mind", done
  before any cutting. Keep the number of blocks down. Print light to dark. A print that
  wants thirty blocks "often looks excellent after about ten" and can disappoint after
  twenty: stop early. The *nezumi-ban* (a "grey" block that need not be grey, laid across
  several colour areas at once for shadow) "often instils life into the print", and is where
  skill shows. Gradation is made by wetting one end of the block: straight, abrupt-narrow,
  wide, curved, two-colour. Baren strokes leave marks: circular rubbing leaves circles,
  horizontal rubbing leaves horizontal lines that he used for water; a straight-grained
  board gave vertical lines that "suited the feeling of rain". Texture comes from the tools.
- Bokashi vocabulary: *ichimonji* (straight band, sky top / horizon), *ō-bokashi* (wide),
  *futa-iro* (two colours meeting), *ate-nashi* (soft patch with no edge: glow, mist),
  *ita-bokashi* (edge of the block sanded so a shape fades instead of ending).
- Arthur Wesley Dow, *Composition* (1899), written from Japanese prints. Order of work:
  line (spacing), then notan (dark-and-light masses), then colour. Two values first, then
  three. Every mass needs a reason; flat tones. Colour: "bright points floating in grayish
  tones", one dominating hue, beginners no more than two hues.
- Hasui, by his own account, worked from what he saw ("My work is based on reality") and
  simplified. Secondary commentary agrees on: decide hour and weather first, a small light
  in a large dark, weather drawn with texture and bare paper, one small figure for scale.

**First look at a real one** (Hasui, *Evening at Ushibori*, 1930). Corrections to my memory:

1. Flat *tone* but intricate *shape*. The trees and reeds are thousands of small carved
   marks. The sky and water are nearly empty. The picture is a contrast of busy and quiet.
   Study 0 had the same low detail everywhere.
2. Almost no outline. The key block draws trunks, the boat, grass blades. Clouds, water
   and hills have no line at all.
3. Texture is directional and belongs to the material: vertical wood grain in the sky,
   horizontal dashes in the water, radiating blades in the reeds, clumps in the foliage.
4. Reflections are broken horizontal ticks that thin out downward, never a solid mirror.
5. One hue (Prussian blue to green-black) in about five values, plus one pale warm
   (cloud band, sail). The warm is perhaps 5% of the area and it is where the eye goes.
6. Sky darkens upward, water darkens downward: the lightest band is in the middle and the
   subject sits on it.
7. Asymmetry: tree mass left, boat right of centre and small, foreground reeds as a dark
   diagonal with a bite of water taken out of it.

**The rest of the reference prints** (`refs/prints/`, measured with `analyze.py`):

| | my Study 0 | eleven real prints |
|---|---|---|
| mean chroma (CIELAB C*) | 19.5 | 6 to 15, one at 18 |
| share of picture that is cool-hued | 84% | 0 to 47% |
| fine-detail density | 6.9% | 9 to 36%, median about 15% |
| warm accent area | 1.4% | usually under 5% |

So I was twice as saturated, monochrome where they are grey with a hue bias, and half as
detailed. Reduced to three values, their pictures are *designs*: one connected dark mass that
touches the frame on two or three sides, one shaped pool of light, the subject on the border
between them. Mine reduced to horizontal stripes with an isolated black bar.

Things only the full-size prints taught me:

- *Night Rain at Teradomari*: 97% of it sits in the darkest third. Houses separate from sky by
  hue (warm black against blue black), not value. The two lit windows are plain pale slits
  with **no glow at all**. The light shows up only as dashes in the puddles and as the one
  ochre raincoat. A halo round a light is a digital-painting habit; a print can't do it and is
  better for it.
- *Snow at Mukojima*: foreground boats take 40% of the height and are cut by the frame. The
  eye zigzags from them to the umbrella to the far shore. Snow is bare paper sitting directly
  on black. Falling snow is thousands of small angular chips, not dots.
- Yoshida, *Cryptomeria Avenue*: distance is done in tone steps (near trees dark, each rank
  behind paler), trunks run out of the top of the frame, two tiny figures give the scale.

---

## Entry 2. Studies 1 and 2: materials, and memory against reference

**Study 1** (`studies/s01_materials.png`), six panels after looking at real prints. The
night-rain and water panels already feel like prints. Faults: wood grain so even it read as
a motion-blur filter; every organic shape a smooth lozenge (my splines have no corners; a
knife leaves corners); reflection ticks spread evenly like wallpaper; snow chips too big and
too few; firs drawn as the fishbone icon.

**Study 2a / 2b** (`studies/s02a_memory_subjects.png`, `s02b_reference_subjects.png`): the
same heron and ferry drawn from memory, then again after photographs.

- *Heron from memory*: a logo. Thin ghost neck standing straight up, bean body, legs like
  two wires, a rust ball for a thigh. Every part present and labelled, nothing related.
- *Heron after two photographs*, with landmarks read off a grid: the neck is folded, thick
  and warm grey; the head is a wedge continuing the bill; the body hangs like a cloak; the
  black shoulder mark is a vertical wedge. It has a posture now, which is the whole bird.
- *Ferry from memory*: an office block on a barge, dark tall hull, big square stack.
- *Ferry after four photographs*: long and low (10:1), nearly all white with the dark hull a
  thin strip, three rows of openings, rounded ends with the car-deck mouth, wide green-roofed
  pilot houses set back, a mast beside each. Built as a box model in metres and projected
  through a camera, so I can now draw it from any angle.
- *Fir*: the photograph showed a visible trunk and separate ragged sprays of unequal length
  with sky between, heavier on one side. Version two got that for distant trees, but near
  trees came out as torn flags because I scaled the marks up with the tree. Rule learned:
  **a bigger thing gets more marks, not bigger marks.**

**What reference gave me, concretely.** Not detail. Memory supplied a correct *parts list*
in every case (I knew a heron has an S-neck and a black plume). Reference supplied
*proportion, attitude, and which parts dominate*: the things that make it that animal or that
boat. The gain was largest for the organic subject and came mostly from measuring, not looking.

---

## Entry 3. Print 1: *Last boat, rain*

Method followed in order: sentence ("deep dusk, rain, the last ferry's windows, a heron as
witness"), three notan thumbnails (`prints/p1/00_notan.png`), block list, construction, print.

**The notan step earned its keep.** Variant B (ferry large and cut by the frame) was the
one I would have painted without thinking. Variant C scored best against rule 6: the pilings
make one dark mass touching three sides, the light is one pool, the bird stands on the
border. It is the better picture.

**Construction did real work.** The ferry is the box model seen from a dock 450 m off with
the eye 3.5 m above the water; the heron's pile is 8 m out and 1.75 m proud of the water,
and the bird is scaled as 1.2 m at that distance. She is heading left, so the side light we
see is the red (port) one. Nobody would check that. It still makes the scene hold together.

**v1 faults and what fixed them** (`p1_last_boat_v1.png` -> `_v2.png`):

- New layers went *under* the water because `layer()` inserts above the active layer.
  `block()` now always goes to the top.
- Two hundred rain lines veiled the whole picture like scratches. Fifty hairlines in loose
  sheaves with gaps between read as rain. Weather is felt at about a quarter of the amount
  I first reach for.
- The pilings were a flat brown wall, then a wall with crenellated stripes (stepped edges at
  a regular 46 px). Long irregular notches and carved grain lines work.
- Lashings drawn straight across the cluster looked like sticks. Rope goes round a pile, so
  it sags across each pile separately; that one change gives the piles their roundness with
  no shading at all. **A line that wraps a form describes the form.**
- The heron's back kissed the edge of the pilings. Moved it clear. No tangents: overlap
  decisively or leave a gap.
- The heron's neck was a warm blob on a cool bird at dusk. In low light the local colours
  close up; only the white face and the bill stay distinct.

**Measured** (v1): chroma 7.9, warm 4.9%, detail 14.1%, 76% dark. All inside the range of
the eleven reference prints, where Study 0 was outside on three of four.

**Still wrong:** the top of the reflection is sixty near-identical hairlines and reads like
a venetian blind; a block-cutter would have made it one flat shape with a torn lower edge.
The pilings are still the least alive third of the picture.

---

## Entry 4. Print 2: *Lookout, first snow*

A different subject on purpose (snow, architecture, conifers at close range) to see what
carried over from the notes. Reference: a 1943 Forest Service photograph of Aeneas Lookout
in winter, which gave me the tower's build, the buried cabin and the ski tracks leading in.

**What carried over without relearning:** notan first (variant A again beat the obvious
centred one); construct the tower as a box model and photograph it with the camera; lights
with no glow; tone steps for distance; a big foreground thing cut by the frame; `block()`
stacking. I made none of the Print 1 mistakes again. The first full pass took three scripts
where Print 1 took six.

**New mistakes, because the material was new:**

- *Cabin floating at deck height.* I put it on a flat ground plane, but the camera is below
  the knoll, so "nearer on a flat plane" means "higher on the page". Things beside a subject
  go beside it at the same depth, not in front of it. Construction catches this kind of
  error instantly; guessing would have hidden it.
- *Snow planes were stickers,* then (with a faded fill inside a polygon) *frosted-glass
  rectangles,* then *bowls.* What works is a crest: sharp along its top, shade thinning to
  nothing below, tapering to a point at each end, computed per pixel (`drift()`). Form in
  snow comes from one sharp edge and one soft one. That is ita-bokashi, and it took three
  tries to understand why the printers did it that way.
- *The near fir was forty identical white ribs* and swallowed the picture. Two rules I had
  already written down were being broken at a new scale: lozenges (smooth snow caps), and
  evenness. Fix: a dozen big sagging boughs instead of forty, snow as separate lumpy pillows
  with gaps where it has slid off, the trunk pushed to the edge of the frame.
- *Two values, not three.* `analyze.py` said 35% dark, 3% mid, 62% light: my eye had not
  noticed there was no middle. Dropping the far knoll to a mid tone (now 34 / 21 / 45) made
  it night, gave depth, and made the near crest the light. **Measure the values; the eye
  forgives its own picture.**

**Measured** (v2): chroma 7.0, warm 0.4%, detail 8.5%. Detail is at the bottom of the
reference range: fair for a snow picture, but the big white foreground is emptier than
Hasui would leave it.

**Still wrong:** the cabin roof is a plain parallelogram; the smoke is a wire; the distant
firs on the left ridge are all the same height.

---

## Entry 5. Print 3: *Full moon over the Sound* (the assigned subject, inside the style)

Ellie's earlier brief, word for word: an orca leaping out of Puget Sound to attack a giant
Evangelion-like machine under a full moon, a pitched battle behind. The first time
(`gallery/studio/orca_vs_mech.png`) I painted it as a realistic scene and it came out as a
diorama; the machine took three attempts and was still a pile of blocks. This is the same
subject put through the method.

**The notan decided everything.** Variant A was the old picture again: machine and whale
side by side, both middle-sized. Variant C put the machine far away as a small flat
silhouette inside the moon and made the whale the big foreground thing. That solves the
drawing problem instead of fighting it: the subject I have a measured reference for is
large, the one I can only imagine is 290 px tall and backlit. It read as that kind of
machine on the first attempt. Hasui shows people from behind for the same reason.

**Reference again.** The whale is built from landmarks on one photograph of a breaching
Southern Resident (`subjects/orca.py`). My remembered orca had been a slender torpedo; the
real one is a quarter as deep as it is long, blunt-headed, with a paddle for a flipper.

**The battle is in the far band,** where the method puts anything small: tracers as ruled
dashes, two searchlights as flat wedges, three fires, two jets, a destroyer, the pod going
in. All of it together is under 2% of the area and it still reads as a battle.

**Mistakes this time:** the moon road as long equal hairlines (the venetian-blind fault I
had already written down: I read my own list *after* making it, not before); a splash made
of shards on an ice floe (fixed by reusing the snow-pillow idea: foam is lumps); board
grain in a clear night sky reading as rain; a loop variable named `path` that silently
replaced the studio's `path()` function.

**Measured** (v2): 68% dark, 19% mid, 13% light; chroma 10; detail 8%.

**On Ellie's second question** (chosen against assigned subject). The assigned, absurd
subject came out at least as well as the two I chose, once it went through the same
method. The earlier failure was not because the subject was assigned. It was because I had
no method, no reference for the whale, and tried to render what I could not draw at a size
where it showed.
