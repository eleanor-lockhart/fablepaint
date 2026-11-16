# Paperlight: a style guide

Version 2 (after two studies and two boxes). Evidence in `journal.md`.
Tools: `../../backlot/` (read `backlot/MANUAL.md`), `kit.py` here. Blender does the light.

## The idea

A box of cut paper sheets standing one behind another, lit from behind and from within,
photographed with a real lens. It is the paper-cut light box (the craft) crossed with Lotte
Reiniger's trick table and the toy theatre, built at true size in millimetres and rendered by
tracing light, so everything paper does to light happens by itself: it glows where it is thin,
goes cloudy when backlit, throws soft shadows on the sheet behind, and shows a lamp's beam as
a moving patch on whatever the beam lands on.

Ellie said the earlier paintings looked like dioramas. Lit Window answered by flattening the
diorama into a print. Paperlight goes the other way and builds the diorama for real.

What I bring: the design of each sheet (the cut patterns come from the same carved-shape
vocabulary as the prints), exact construction, and the patience to move a lamp one frame at a
time. What the renderer brings: realism I cannot paint by hand, because paper is simple enough
for physics to get right.

## Rules

1. **Light is the pigment.** The paper is white, plus at most one dark card. All colour comes
   from where the lights are and what the light has passed through or bounced off.
2. **Only what could be on the table.** Sheets, card, tracing paper, lamps, a light panel,
   haze, a lens. The lab may do what a lens and film do (bloom, halation, mist, grain,
   vignette, weave) and nothing else. No painted glows, no flat-colour overlays.
   Anything added on the compositing desk (falling snow) must be something that could have
   been dropped into the box: it has a depth, it is hidden by every sheet nearer than that
   depth (use the render's depth pass), and it goes soft away from the plane of focus.
3. **A sheet is one connected piece, nothing thinner than a millimetre.** Run every sheet
   through `kit.sheet()`. Detail is made with *holes* (windows, stars, glazing bars), not lines.
4. **Depth is the composition.** Six to nine sheets. Decide first which of two lightings
   the box has, because it reverses the values:
   *lit from behind* (far is bright, near is a dark silhouette: the lighthouse), or
   *footlit* (a cold strip below the front edge: every sheet is white paper, brightest at its
   foot, with the shadow of the sheet in front lying across it: the lookout).
   Do not light the sheets flat from the front; it erases the layers.
5. **Design each sheet for its own window.** A nearer sheet shows less of itself
   (`kit.visible(depth)`). The foreground sheet is out of focus and should be bold.
6. **One reason to move.** Each piece has one light that changes or one mechanism that works
   (a lamp turning, seas sliding against each other, a boat rocking on its stick). Everything
   else holds still or drifts. Shot on twos: 12 poses a second.
7. **The loop closes.** Every motion is periodic in the loop length. Check `screen.loop_seam`.
8. **A real lens.** 85 mm at f/4 from about half a metre, focused on the subject's sheet.
9. **One warm light in a cool box** (kept from Lit Window), and here it may glow, because a
   lamp in haze behind paper really does.

## Method

1. One sentence: what the box shows, and what moves.
2. A depth plan: the sheets front to back, with what is cut in each and what light sits where.
3. Cut the sheets as mattes (`kit.py`), check what `paperize` dropped.
4. One test frame through `model.Spec(...).render`. Look. Fix lights before shapes.
5. Two or three frames at different moments of the motion. Look.
6. Render the loop; finish every frame in the lab; encode.
7. Screening room: filmstrip, motion map, loop seam. Then the critique in `journal.md`.

## Recipes that work

**Lit windows.** Cut the panes out of the sheet; put a piece of thin paper (tracing paper)
1 to 2 mm behind them; put a small warm point light 4 mm behind that; put a card baffle
behind the light, smaller than the building, so the light does not flood the sheet behind.

**Footlights.** An area strip 300 x 8 mm, 0.6 W, cold, at (0, -46, -74), aimed up into the box.

**Falling snow** (`works/lookout/scene.py`, `snow()`): flakes live in bands of depth between
the sheets; each band is drawn, blurred by its distance from the focus plane, multiplied by
`depth_pass > band_depth`, and laid over the frame, far bands first. Each flake falls a whole
number of screen heights per loop, so the loop closes.

**Lighthouse box**

- Canvas 1280 x 720 px at 4 px/mm (320 x 180 mm), border 70 px, sheets 10 to 14 mm apart.
- Back panel: emission strength 5, a gradation from amber at the bottom to deep blue at the top.
- Sky: an uncut sheet of thin paper (translucency .62) with pinholes of 0.4 to 0.8 mm for stars.
- Paper: translucency .42, formation .24 at scale 420. More formation looks like frosted glass.
- A spot lamp of 1.6 W with a 34 degree cone between two sheets, haze density 7 in a slab around it.
- A cold strip under the sea sheets (0.5 W), a little room light from the front (0.9 W area).
- Lab: bloom r14 .16 over 2.2; halation r9 .22 over 3; mist .10; filmic white 7; grain .028.

## Faults seen so far

- Thin trunks and tufts from the print vocabulary vanish or float when cut in paper.
- Sheets drawn for the whole canvas put their subject outside the camera's window.
- A square light panel behind a hole shows as a square. Use a ball of light (a point light
  with a radius is visible through the cut).
- Formation above about .4 turns paper into frosted glass and swallows the stars.
- Black card in front of soft paper reads as a void; use dark paper that takes a little light.
- A flat front light makes every sheet the same milky white and the box stops being a box.
- A baffle or a piece of tracing paper larger than the thing it hides shows as a rectangle.
- Haze makes the depth and index passes noisy. Keep haze out of shots that composite by depth.
- A lamp between two sheets throws a hot spot on the sheet just behind it that can read as a
  second moon. Give it more room behind, or accept it.
- White flakes over white paper are invisible; snow needs a dark sky or dark sheets behind it.

## Changelog

- v1: written after studies 1 and 2 and the lighthouse box.
- v2: after the lookout box. Two lightings named (back-lit and footlit); the rule for
  composited elements; recipes for lit windows, footlights and snow; five more faults.
