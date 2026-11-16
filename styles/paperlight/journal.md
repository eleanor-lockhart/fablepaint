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
