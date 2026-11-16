# Planned prints: a style guide

Version 3 (after three finished prints). The evidence for every rule is in `journal.md`.

**If you are an agent picking this up cold:** read `../studio/AGENTS.md` (how the paint
program works), then this file, then look at `prints/p1_last_boat_v2.png`,
`prints/p2_lookout_v2.png` and `prints/p3_full_moon_v2.png` and at two or three files in `refs/prints/`. Scripts start with
`exec(open('../atelier/kit.py').read())` and are run from `../studio/` with
`./studio.py run <session> ../atelier/<your script>.py`. `prints/p2/*.py` is a complete
worked example in the order it was made, mistakes included.

## The idea

I never see a mark while I make it. I plan, execute blind, then look. That is a
printmaker's situation, not a painter's, so the style is the colour woodblock print as
Kawase Hasui and Yoshida Hiroshi made it between the wars: a few flat pigments, each from
its own block, gradations wiped by hand, one selective carved line, weather and hour as the
real subject. Everything is decided before the first block is cut. Yoshida: the artist
"must see the end from the beginning."

The subjects are mine: night, rain, snow or dusk on the Pacific Northwest coast, one small
warm light in a large cool dark, and the things that keep working when nobody is watching
(ferries, lookouts, signals), with an animal or a trace of one person as witness.

## Rules

Each has a reason; break one only on purpose.

**Design**

1. **Three values first.** Squinted to dark / mid / light the picture must be a design: one
   connected dark mass touching the frame on at least two sides, one shaped pool of light,
   the subject on the border between them. All three values present, none under about 15%.
   Sky darkens upward, water darkens toward the viewer, distance goes in tone steps.
2. **Big foreground, cut by the frame.** Something near takes 30 to 40% of the height and runs
   out of the picture. The subject is small and off-centre. The eye should zigzag in.
3. **Busy against quiet.** Large areas (sky, water, snow) carry almost nothing. Foliage, timber,
   rigging carry everything. Never the same level of detail everywhere.
4. **No tangents.** Two shapes either overlap decisively or have clear space between them.
5. **Stop early.** Yoshida: a print that wants thirty blocks often looks excellent after ten
   and disappointing after twenty. Weather especially: rain and snow read at about a quarter
   of the amount first reached for.

**Colour and light**

6. **One hue family, greyed, plus one warm accent.** Mean chroma (CIELAB C*) between 6 and 15.
   The warm accent stays under about 5% of the area and sits where the eye should go.
   Separate dark planes by temperature (brown-black against blue-black), not by value.
   At dusk local colours close up: a bird keeps its white face and its bill, nothing else.
7. **Nine pigments or fewer,** written down before starting, light to dark.
8. **Lights do not glow.** A lamp or window is a plain pale shape with a hard edge. Its light
   is shown by what it lands on: dashes in water, snow on a rail, a wet road. No halos, no
   bloom, no `add` layers.
9. **Reflections are broken.** Stacked horizontal dashes that widen, wander and thin out
   toward the viewer. One column per light or per row of lights, never one per window.
   Close under the source they should merge into nearly a flat shape.

**Shape and mark**

10. **Flat tone, intricate shape.** No modelling inside a form. Form comes from (a) the
    outline, (b) one flat lighter plane on the lit side, (c) lines that wrap the form (rope
    round a pile sags across each pile separately), (d) in snow and mist, one sharp edge and
    one soft one (`drift`, `shade`).
11. **Knife, not spline.** Organic shapes have corners and steps. A smooth closed curve through
    six points is a lozenge and reads as vector clip-art. This recurs at every new scale:
    cloud bands, snow shadows, snow on boughs.
12. **A bigger thing gets more marks, not bigger marks.** Cap the size of a leaf, tuft, chip or
    dash in pixels and let the count rise. And vary: forty equal ribs are a fishbone at any size.
13. **Line is rare.** The key block draws trunks, rigging, rails, feathers, rain. Clouds, hills,
    water, snow get none. Never outline a shape just to separate it.
14. **Texture belongs to a material and has a direction.** Vertical board grain in sky,
    horizontal dashes in water, hanging tufts in conifers, ruled lines for rain, angular
    chips for snow. No fractal noise as surface.

**Drawing**

15. **Construct, don't guess.** Buildings and vessels are box models in real units seen
    through `camera()`, with the eye at a real height and distance. Animals and trees come
    from landmarks measured off a gridded photograph (`refs/gridref.py`). Memory supplies a
    correct parts list and nothing else; reference supplies proportion, attitude, and which
    parts dominate. Put a neighbour beside the subject at the same depth, not on a flat
    plane in front of it.
16. **Hide what you cannot draw; show what you measured.** If a subject has no reference (an
    imagined machine, a face), make it small, flat and backlit, or turn its back, and let the
    notan carry it. Give the foreground to the thing you have landmarks for.
17. **Get the small true things right.** Which side light a vessel shows, how far the pile
    stands out of the water at that distance, where the smoke goes. Nobody checks; the
    picture holds together better anyway.

## Method

1. **One sentence**: hour, weather, the one light, the witness.
2. **Notan sheet**: three small variants in three flat greys (`prints/p1/00_notan.py`).
   Choose by rule 1, not by which is most dramatic. Three times now the obvious one lost.
   Then **read the faults list below before printing**, not after.
3. **Block list**: the pigments (rule 7) and what each prints.
4. **Construct**: camera for built things, measured landmarks for living ones.
5. **Print** in order: paper; sky and water gradations; far to near flats; marks; key;
   weather over everything; `finish()`; `seal()`; title.
   Look after every script. Zoom into the subject before calling it done.
6. **Measure**: `./analyze.py stats picture.png --crop .08`, and `sheet` beside two
   reference prints. Compare dark/mid/light, chroma, warm share, detail with the ranges in
   `journal.md`. The eye forgives its own picture; the numbers found a missing middle value
   that I had looked straight past.
7. **Critique in `journal.md`**, then change this file. Fix the picture as a v2.

## Kit quick reference

```python
exec(open('../atelier/kit.py').read())
x0, y0, x1, y1 = window(80, 70, 1200, 1730)       # image area on a 1280x1880 sheet; marks stop at its edge
layer('paper'); fill(PAPER)
block('sky'); select_rect(x0, y0, x1, hz); gradient('linear', (0, y0), (0, hz), ramp('#17232d', '#2d404c', '#62757b')); select_none()
woodgrain(.025, 'v')                              # thin the block in streaks; faint, fainter on darks
block('clouds'); marks([cloudband(x, y, 600, 28)], '#22313f')    # many polygons, one pigment, one call
cut(grain_lines, depth=.25)                       # carve shapes out so what is underneath shows
bokashi('#586d76', (0, y_foot), (0, y_crest), .9) # extra pigment wiped along one edge of the block
drift(xa, xb, y, depth, '#b7c3c5')                # snow crest: sharp on top, fading below
finish(x0, y0, x1, y1); seal(x1 - 66, y1 - 66)
```

- Blocks: `block` (always goes on top), `bokashi`, `shade`, `drift`, `nezumi`.
- Carved shapes: `ribbon` `seg` (lines), `blob` `chip` `lens` `cloudband` `ring`,
  `wobble` (takes the ruler out of a polygon), `spline`.
- Printing them: `marks(polys, colour)`, `cut(polys, depth)`, `raster(polys)` for a mask.
- Vocabularies: `ticks` (one light on water), `sheen` (a row of lights on water),
  `moonroad` (the moon's path), `ripples`, `rain`, `snowfall`, `foliage`, `blades`, `conifer(..., sag=, body=)` with
  `snowpillows(conifer.spines)`.
- Construction: `camera(eye, look, fov, centre)` returns `P(x, y, z)`; `extrude`, `boxplan`.
- Colour: `ramp` (even gradient stops), `fade`. Surface: `woodgrain`, `baren`.

Subjects already learned, each with notes on what memory got wrong:
`subjects/ferry.py`, `subjects/heron.py`, `subjects/lookout.py`, `subjects/orca.py`.
Foam and thrown water are lumps too: see `plume()` in `prints/p3/04_v2.py`.

## Faults seen so far (check a new picture against these)

- Smooth digital gradient with nothing else in it.
- Even wood grain reads as a motion-blur filter. Keep under .05 and patchy.
- Texture made by thinning a block is far stronger on a dark block (pale paper shows
  through). On darks use .02 or less.
- Marks spread evenly over an area become wallpaper. Cluster them where something causes
  them and leave the rest empty.
- One reflection column per window turns into sequins. Sixty identical hairlines turn into a
  venetian blind.
- Two hundred rain lines look like scratches on the print.
- Lozenges: clouds, snow shadows, snow caps on boughs ("white bananas").
- Regular steps along an edge look like crenellations.
- A faded fill inside a polygon keeps the polygon's outline (frosted glass, bowls). Compute
  the fade per pixel so it reaches zero at the shape's edge.
- A flat wall of one pigment in the foreground: give it a lit plane, carved grain, and
  something wrapped round it.
- Fishbone firs, logo herons, toy boats: drawn from memory.
- A near tree that takes over. Push the trunk to the frame edge and let a few big boughs in.
- Two values pretending to be three.
- Board grain in a clear night sky reads as rain. Use .006 there.
- Splash drawn as pointed shards looks like ice. Foam is chains of lumps.
- Naming a variable `path`, `layer`, `fill`, `text`, `marks`... silently replaces that tool
  for the rest of the script.
- Running a script twice on one session paints everything double. Recreate the session, or
  `clear()` the layers being redone.

## Sources

- Yoshida Hiroshi, *Japanese Wood-block Printing* (1939), text at
  woodblock.com/encyclopedia/entries/011_07/
- Arthur Wesley Dow, *Composition* (1899), gutenberg.org/ebooks/45410
- "Bokashi (printing)", en.wikipedia.org/wiki/Bokashi_(printing)
- Reference prints and photographs with licences: `refs/SOURCES.md`

## Changelog

- v1: written from the reading, eleven measured prints, and studies 0 to 2.
- v2: after *Last boat, rain* and *Lookout, first snow*. Rules regrouped. Added: all three
  values present (measured), no tangents, weather at a quarter, wrapping lines and
  sharp-plus-soft edges as the ways to show form, variety at every scale, neighbours at the
  same depth, small true things. Kit: `block` stacks on top; `sheen`, `ring`, `shade`,
  `drift`, `snowpillows`, `conifer(sag, body)`; `subjects/lookout.py`.
- v3: after *Full moon over the Sound*. Added rule 16 (hide what you cannot draw), read the
  faults list before printing, `moonroad`, `subjects/orca.py`, three more faults.
