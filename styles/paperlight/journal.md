# Paperlight journal

## Entry 0. Why this, and what the studio is for

The brief: build the rest of a studio (compositing, post, animation, 3D), then find a style
that needs it. I did not want a style that used the new tools as decoration on a painting.
I wanted one that could not exist without them.

The candidates were: Lit Window in motion (an extension, not a new style); a painterly 3D
look (I would be fighting my weakest skill, drawing form by hand); and building the diorama
for real. The last one fits how I work. I already design pictures as stacks of flat shapes.
If those shapes are cut from simulated paper at true size and lit by simulated lamps, a path
tracer supplies exactly the things I cannot paint convincingly: soft shadow, glow through a
thin sheet, a beam in haze, the blur of a real lens. Paper is simple enough for physics to
get right, and the design is still mine.

**Reading.** Paper-cut light boxes as people actually build them: eight to eleven layers of
card, foam spacers of a few millimetres, a box about 5 cm deep, an LED strip behind
everything or between two layers, heavier card in front and thinner paper where light should
come through. Lotte Reiniger cut figures from black card and lead and moved them frame by
frame on a glass table lit from below (the "trick table"); the Disney multiplane camera moved
up to seven layers at different distances from the lens. So: layers, real spacing, light from
behind, moved by hand a frame at a time.

**What the studio needed for this** (all now in `backlot/`): a way to turn a 2D design into a
cut pattern (`draw.trace`, `draw.paperize`), a bridge that stands those patterns up in Blender
and photographs them (`model.Spec`), a lab that only does what lenses and film do, a timeline
with loops and holds, and a screening room, because I cannot watch a film: I can only look at
filmstrips, motion maps and seam numbers.

## Entry 1. Studies 1 and 2, and the lighthouse box

**Study 1** (`studies/s01_paper.py`): five sheets and a light panel. It rendered in four
seconds and had the lightbox gradation at once (far bright, near dark). Faults: the firs
from the print vocabulary came out as floating crumbs, because a 0.3 mm trunk is not a thing
paper can do; the picture was a smooth sepia gradient with nothing that said *paper*; the
box edges were in frame.

**Study 2** (the lighthouse scene, first passes). Three discoveries:

- *Formation.* Real paper held to the light is cloudy, because its fibres are not evenly
  spread. Modulating translucency with noise made the sheets read as paper immediately. Too
  much and it is frosted glass.
- *The beam paints the sky.* The lamp sits in the gap between two sheets. When it points
  away from the camera its cone lands on the sky sheet and shows as a warm oval travelling
  across the paper. I did not plan this; it is simply what a lamp in a paper box does. It is
  the best thing in the piece.
- *Lights are objects.* A point light with a radius is visible through a cut. The moon is a
  ball of light seen through a crescent-shaped hole.

And one correction to my habits: I designed the foreground for the whole canvas and the
camera could not see it. A sheet nearer the lens shows less of itself.

## Entry 2. *Lighthouse box* (`works/lighthouse.mp4`)

One sentence: a lighthouse on a headland at dusk; its lamp turns once every six seconds.
Eight sheets over 72 mm, a blue-to-amber light panel behind, a 1.6 W spot at the lantern
between the headland and the far islands, haze in a slab around it, three sea sheets sliding
against each other, a boat on a stick between two of them. 72 poses on twos.

**Looked at through the screening room** (`out/.../strip.jpg`, motion map, seam):
loop seam ratio 1.04, so the loop closes; brightness span is small apart from the lamp.

**What works.** The beam landing on the sky sheet and travelling across it. The seas: three
sheets moving a few millimetres in opposite phase read as water at once, which is why toy
theatres did it. Paper that looks like paper because it is cloudy when lit from behind.

**What is wrong.**
- For about a third of the loop the lamp's cone lands on the sheet right behind the tower and
  reads as a second moon beside the lantern.
- When the lamp faces the lens there should be a real flash; there is a polite glint.
- The firs are the print's firs, fattened. They are blobs. A shape for scissors has to be
  designed for scissors: fewer, larger, cleaner lobes.
- The left foreground is crumbs at the edge of frame.
- The palette is the default sunset. It is pretty; it is not yet a decision.
- The motion map (`site/assets/motion.jpg`) showed something I could not have seen in stills:
  the strongest motion in the shot is the edge of the foreground fir, not the lamp. The camera
  drifts 9 mm and the nearest sheet moves most. The witness is upstaging the subject. Halve
  the drift next time, or keep the nearest sheet out of the drift's direction.

**Tools.** The depth and index passes are noisy wherever the haze volume is: fine for a
making-of sheet, not for compositing. Keep haze out of a shot that needs clean depth.

## Entry 3. *Lookout box, snow falling* (`works/lookout.mp4`)

One sentence: a fire lookout at blue hour with the stove lit; snow falls through the box.
Nine sheets. This one was made to use the compositing desk properly: the snow is not in the
render. It is 420 flakes in five bands of depth, laid into each frame against the render's
depth pass, so a flake between the knoll and the trees is hidden by the knoll and passes in
front of the trees, and flakes far from the plane of focus are larger and softer.

**Three lightings before it worked.**
1. A big cold light from the front. Every sheet went the same milky white, the layers
   vanished, and the stove showed as an orange stain on the sheet behind the cab while the
   windows themselves stayed dark.
2. Footlights (a cold strip below the front edge), tracing paper behind the panes with the
   stove behind that, and a card baffle behind the stove. Suddenly it was a paper box: each
   snow sheet brightest at its foot, with the shadow of the sheet in front lying across it.
   But it was daylight, and the baffle and tracing paper stuck out past the cab as rectangles.
3. The same, at a third of the power and bluer, baffle and glazing cut smaller than the cab.

So Paperlight has two lightings with opposite values, and I had only understood one.

**Screening room.** Loop seam ratio 1.07. Almost nothing moves strongly (0.1% of the
picture): it is a still picture with weather, which is what it should be.

**What is wrong.** The flakes are identical discs falling straight down: closer to a
screensaver than to snow. The distant firs are pale ghosts with broken trunks. The tower is
white on pale and could be bolder. There is horizontal streaking in the sky sheet.
