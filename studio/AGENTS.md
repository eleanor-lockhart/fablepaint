# Fable Studio: how to paint with it

`studio.py` in this directory is a raster painting program with no window. You paint by
writing short Python scripts that call its tools, running them, and looking at the image it
renders. Any agent that can run a shell command and open an image file can use it.

This file is the whole manual. `./studio.py api` prints every function with its exact
signature from the code; trust that over this file if they ever disagree.

## Setup

- With `uv` installed, just run `./studio.py ...`; dependencies install themselves on first run.
- Without `uv`: `pip install numpy pillow opencv-python-headless`, then `python studio.py ...`.
- Optional: `ffmpeg` (time-lapse video) and `fc-match` (font lookup for `text`).
- Run commands from this directory. Pictures live in `sessions/<name>/` next to `studio.py`.

## The loop

```
./studio.py new mypic --size 1920x1080 --bg '#ffffff'    # once
./studio.py run mypic step1.py                            # paint
# open sessions/mypic/view.jpg and LOOK at it
./studio.py view mypic --crop 600 300 500 400             # zoom: X Y W H -> sessions/mypic/crop.jpg
./studio.py run mypic step2.py                            # paint more, or fix what looked wrong
./studio.py undo mypic                                    # take back the last run (up to 3)
./studio.py export mypic -o mypic.png                     # final picture
```

1. `run` executes one script. If it raises, nothing is saved, so fix it and run again.
2. Every successful `run` rewrites `sessions/<name>/view.jpg`: the whole picture, at most
   1500 px across, with pixel rulers on the top and left edges. Read coordinates off the
   rulers. The 26 px dark margin is not part of the picture.
3. Work in several small scripts, looking after each. Painting blind in one big script is
   the main way to get a bad picture. Zoom into anything that matters before calling it done.
4. Everything persists between runs: layers, the active layer, the selection, the brush
   settings and the colour. Start each script by selecting the layer you mean (`use`) and
   setting the brush from scratch (see `B()` in `examples/hello.py`).

Other commands: `layers <s>` (the stack, top first, `>` marks the active one),
`view <s> --layer NAME` (one layer alone), `export <s> -o f.png --bits 16 --scale 0.5`,
`timelapse <s> -o f.mp4`, `help`, `api`.

`examples/hello.py` is a complete working script. Try it first:
`./studio.py new demo --size 1280x720 && ./studio.py run demo examples/hello.py`.

## Conventions

- **Coordinates** are canvas pixels, origin top-left, y down. `W` and `H` are in scope.
  Points may lie outside the canvas.
- **Angles** are degrees; for `smear`/`motion_blur`/`emboss`, 0 is right and 90 is up.
- **Colours**: `'#rrggbb'`; or a tuple, 0-255 if any value is above 1, otherwise 0-1;
  or `hsv(h_degrees, s, v)`; `mix(a, b, t)` blends two.
- **Opacity, flow, alpha** are 0-1.
- Pixels are 32-bit float, linear light, premultiplied alpha. Values above 1.0 are allowed
  and only clip at view/export, so light can be stacked on `add` layers.
- **Points for strokes** are `(x, y)` or `(x, y, pressure)` with pressure 0-1.
- A script is ordinary Python: loops, functions, `np`, `math`, and a seeded `rng`
  (`numpy.random.Generator`) are available. `exec(open('common.py').read())` shares helpers.

## Layers

| Call | What it does |
|---|---|
| `layer(name, blend='normal', opacity=1, above=None, below=None, clip=False)` | Create a layer and make it active. Goes directly above the active layer unless `above`/`below` names another. If the name exists it only switches to it. |
| `use(name)` | Make a layer active. |
| `props(name=None, opacity=, blend=, visible=, clip=, lock=)` | Change properties. |
| `lock(on=True)` | Alpha lock: painting recolours existing paint only. |
| `duplicate(name, new)` `rename(name, new)` `delete(name)` `move(name, above=/below=)` | Copies land above the source and become active. `move` with no target sends it to the top. |
| `merge_down(name=None)` | Merge into the layer below. |
| `stamp_visible(new, names=None)` | Flatten everything visible (or only the named layers) into a new top layer. |
| `clear()` | Empty the active layer. |
| `mask(source='selection', name=None)` | Give a layer a mask: `'selection'`, `'white'`, `'black'`, or a 2-D array (1 shows, 0 hides). |
| `mask_mode(True/False)` | While on, painting goes to the active layer's mask (white reveals, black hides). |
| `apply_mask()` `drop_mask()` | Bake the mask in, or discard it. |
| `adjust(name, kind, **args)` | Non-destructive adjustment of everything below. Kinds: `levels curves hue_sat exposure balance brightness_contrast desaturate invert posterize threshold colorize gradient_map`, same arguments as the filters. |
| `px(name=None)` | The raw `H x W x 4` float array, for custom numpy work. |

Blend modes: `normal add multiply screen overlay soft_light hard_light darken lighten dodge
burn difference color luminosity hue saturation`. `clip=True` shows a layer only where the
nearest unclipped layer below has paint (use it for shading and texture on a shape).

## Brushes

`brush(**settings)` changes settings; they persist. `preset(name)` loads a ready-made one:
`pencil ink marker airbrush oil acrylic watercolor chalk charcoal sponge splatter foliage grass glow eraser`.

| Setting | Default | Meaning |
|---|---|---|
| `tip` | `'round'` | `round chalk charcoal sponge cloud bristle flat splatter stipple leaf blade needle star spruce square` |
| `size` | 20 | Diameter in pixels. |
| `hardness` | .8 | 0 soft edge, 1 hard (round tip). |
| `opacity` | 1 | Cap on the whole stroke. |
| `flow` | 1 | Paint per stamp; low values build up. |
| `spacing` | .1 | Distance between stamps, as a fraction of size. |
| `angle`, `roundness` | 0, 1 | Tip rotation and squash. |
| `follow` | False | Rotate the tip along the stroke direction. |
| `scatter`, `count` | 0, 1 | Random offset (fraction of size) and stamps per step. |
| `size_jitter` `angle_jitter` `flow_jitter` | 0 | Random variation, 0-1 (`angle_jitter=1` is any angle). |
| `hue_jitter` `sat_jitter` `val_jitter` | 0 | Colour variation per stamp (hue in degrees). |
| `psize`, `pflow` | True, False | Pressure drives size / flow. |
| `taper` | `(0, 0)` | Fraction of the stroke that fades in / out. |
| `blend` | `'normal'` | How the stroke meets the layer; also `erase`, `behind`, or any blend mode. |
| `mix` | 0 | Wet mixing: pick up the colour underneath. |
| `grain` | 0 | Paper texture. |
| `smooth` | True | Spline through the points; False for straight segments. |

| Call | What it does |
|---|---|
| `stroke(points, color=None, pressure=None, **settings)` | One stroke. `pressure` is a list spread along the points. Settings given here apply to this stroke only. |
| `dabs(points, color=None, **settings)` | Single stamps at `(x, y[, scale])`. |
| `scatter(n, area=None, density=None, color=None, **settings)` | `n` stamps at random in a rect `(x0,y0,x1,y1)`, a polygon, or weighted by a canvas-sized density array. |
| `erase(points, **settings)` | Erase along a path. |
| `smudge(points, size=40, strength=.7)` | Drag paint. |
| `blur_stroke(points, size=60, strength=1, radius=6)` `dodge(points, size=60, exposure=.2)` `burn(...)` `liquify(points, size=120, strength=.5)` | Local blur, lighten, darken, push. |

## Shapes, fills, text

| Call | What it does |
|---|---|
| `fill(color, opacity=1, blend='normal')` | Fill the layer (or the selection). |
| `fill_poly(points, color, opacity=1, feather=0, blend='normal', smooth=False)` | Anti-aliased polygon; `smooth=True` rounds it through the points; `feather` softens the edge. |
| `fill_ellipse(cx, cy, rx, ry, angle=0, ...)` `fill_rect(x0, y0, x1, y1, ...)` | Same options as `fill_poly`. |
| `gradient(kind, p0, p1, stops, opacity=1, blend='normal', ease=None)` | `kind`: `linear radial reflect angle`. `stops`: `(position 0-1, colour[, alpha])`. Covers the whole canvas; limit it with a selection or `lock`. |
| `bucket(x, y, color, tol=12, opacity=1, feather=0)` | Flood fill judged on the visible picture. |
| `text(x, y, string, size=48, font=None, color=None, anchor='la')` | `font` is a family name or a file path. |

## Selections

A selection limits every paint, fill and filter until you call `select_none()`.

`select_rect(x0,y0,x1,y1)` `select_ellipse(cx,cy,rx,ry)` `select_poly(points)` each take
`mode='replace'|'add'|'sub'|'intersect'`, `feather=`, and (poly) `smooth=`.
`select_alpha(layer)` selects where a layer has paint; `select_luma(lo, hi)` by brightness;
`select_color(color, tol)` by colour; `select_array(a)` from a 2-D array.
`select_invert()` `feather(r)` `grow(px)` (negative shrinks) `select_none()`.

## Filters and transforms (active layer, inside the selection)

- Blur: `gaussian_blur(r)` `motion_blur(length, angle)` `zoom_blur(cx, cy, amount)`
  `smear(length, angle=90, decay=.4, gain=1)` (one-sided streak in a direction).
- Detail: `sharpen(amount, radius)` `high_pass(radius)` `median(k)` `emboss(angle, depth)`
  `noise(amount, mono=True)`.
- Generate: `clouds(c1, c2, scale, octaves, seed, stretch=(1,1), ridged=False, contrast=1)`
  fills with fractal noise; `noise_field(scale, octaves, seed, stretch, ridged)` returns the
  noise as an array (0-1) for masks, `modulate`, or `scatter(density=)`.
- Light: `glow(radius, strength, threshold)` `vignette(strength, radius, softness, color)`
  `modulate(array)` (multiply the layer by a 2-D array).
- Distort: `turbulence(amount, scale, seed)` (roughens edges) `wave(amp, wavelength, axis)`.
- Colour: `levels(black, white, gamma)` `curves(points, channel='rgb')` `hue_sat(hue, sat, light)`
  `balance(shadows, mids, highs)` `brightness_contrast(brightness, contrast)` `exposure(stops)`
  `desaturate(amount)` `colorize(color, amount)` `gradient_map(stops)` `posterize(levels)`
  `threshold(level)` `invert()`.
- Transform: `transform(scale=1, rotate=0, translate=(0,0), center=None)` `flip('h'|'v')`
  `perspective(src_quad, dst_quad)`.
- Look: `sample(x, y)` prints the colour there; `path(points, closed=False)` returns the
  smooth curve through points.

## Recipes that work

- **Shade a shape**: `fill_poly` it, `lock(True)`, then big soft strokes
  (`hardness=0, flow=.1, psize=False`) of lighter and darker colour, `lock(False)`.
- **Texture or relief on a shape**: new layer with `clip=True, blend='overlay'` above it;
  `clouds(..., ridged=True)` then `emboss(angle, depth)`. This gives rock, snow, bark, waves.
- **Light sources and glows**: paint on a layer with `blend='add'`, then `gaussian_blur`.
- **Natural edges**: `turbulence(amount, scale)` on a hard silhouette.
- **Reflections**: `stamp_visible('refl')`, `flip('v')`, `transform(translate=(0, 2*waterline-(H-1)))`,
  `motion_blur(60, 90)`, `exposure(-.5)`, then mask it to the water.
- **Ground texture in perspective**: make a full-canvas texture, then
  `perspective([(0,0),(W,0),(W,H),(0,H)], [far-left, far-right, near-right, near-left])`.
- **Distance**: a layer of the sky/haze colour over far things, `gradient` from alpha 0 to .5.
- **Finish**: `stamp_visible('bloom')`, `levels(black=.6)`, `gaussian_blur(25)`,
  `props('bloom', blend='add', opacity=.4)`; a radial `gradient` of black for a vignette;
  `adjust('grade', 'curves', ...)` on top.

## Things that will trip you

- `layer()` inserts above the *active* layer, not on top. Call `use(x)` first, or pass
  `above=`. Check with `./studio.py layers <session>`.
- `layer(name)` on an existing name ignores the other arguments. Use `props` to change them.
- Brush settings persist across strokes and across runs. A stray `scatter` or `blend='erase'`
  from earlier will bite; reset the brush.
- A leftover selection silently restricts everything. `select_none()` when done.
- `gradient` and `fill` cover the whole layer; they do not stop at shapes unless you use a
  selection, `lock`, or a clipped layer.
- Fades to transparent are computed in linear light, so a two-stop gradient looks nearly
  even and then ends at a visible edge. Give glows several stops with alpha falling fast,
  e.g. `(0,c,.55),(.15,c,.3),(.3,c,.16),(.5,c,.07),(.7,c,.025),(1,c,0)`.
- You cannot paint on an adjustment layer; it becomes active after `adjust()`, so `use()`
  another layer before painting.
- For light, set the *layer* to `add` and paint with a normal brush.
- `stamp_visible` includes adjustment layers and puts its result on top of them; make
  stamps before adding final grading.
- Session folders are large: about 4 bytes x 4 channels x pixels per layer per saved
  version (a 2560x1440 picture with 40 layers is roughly 3 GB). Delete `sessions/<name>`
  when finished; exports are separate files.
- Undo keeps three runs. For a bigger change of mind, delete the layers and repaint them.
- Hand-drawn lines look drawn. Thin bright outlines around shapes are the fastest way to
  make a picture look like a diagram; use them sparingly and blur or break them.

## Not included

No window or stylus input, no vector layers, no colour management or CMYK, no animation.

A second, deliberately period-limited program (DOS and early-Mac video modes) is in the
parent directory: `../fpaint.py help`.

## A style built on this program

`../styles/lit-window/STYLE.md` documents one fully worked-out style, *Lit Window* (colour woodblock idiom), with a
helper library (`../styles/lit-window/kit.py`), measured references, three finished prints and the
journal of how it was arrived at. Read it if you want a method rather than a blank canvas.

## Sharing a picture

The repository is published at https://eleanor-lockhart.github.io/fablepaint/ ; any pushed
file is reachable at that address plus its path. See "Publishing a new picture" in the
top-level `README.md`.
