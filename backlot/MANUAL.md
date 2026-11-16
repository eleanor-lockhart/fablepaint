# backlot: a production pipeline for an agent artist

The paint programs (`../fpaint.py`, `../studio/`) make one picture at a time. `backlot` is the
rest of a studio: a model shop, a compositing desk, a lab, an animation stand and a screening
room. Everything is a plain Python function on numpy arrays, every stage reads and writes
ordinary files, and every stage has a way to *look* at what it did.

## Setup

```
uv sync                                   # once, in the repository root (or: pip install -e .)
uv run python backlot/tests/selftest.py   # 2D pipeline end to end, writes out/selftest/
uv run python -m backlot                  # the shell tools
```

The model shop needs Blender (tested with 5.2) on the PATH. It runs headless and uses the GPU
through OptiX if there is one. `out/` is scratch space and is not committed.

## The one convention

An **image** is a float32 array `H x W x 4`: linear light, premultiplied alpha. A **matte** is a
float32 array `H x W` in 0..1. Colours are written `'#rrggbb'` as they look on screen and are
converted on the way in. Values above 1.0 are normal until `lab.tonemap` brings them into range.

## Departments

| module | what it is for | the calls you will use most |
|---|---|---|
| `core` | files and colour | `load` `save` `canvas` `col` `resize` `read_exr` |
| `shapes` | a vocabulary of carved shapes as polygons | `setup(w, h, seed)` then `ribbon` `blob` `lens` `conifer` `cloudband` `ticks` `rain` `camera` ... |
| `draw` | mattes and fills in memory | `raster(polys, w, h)` `paint` `gradient` `fbm` `disc` `rect` `trace` `paperize` |
| `comp` | putting images together | `over` `blend` `stack`; mattes: `union` `intersect` `subtract` `xor` `grow` `feather` `outline`; `multiplane`; `drop_shadow` `light_wrap` `glow`; depth: `zmerge` `fog` `defocus` |
| `lab` | finishing | colour: `exposure` `white_balance` `cdl` `lift_gamma_gain` `curves` `split_tone` `tonemap`; lens: `bloom` `halation` `mist` `vignette` `aberration` `distort`; film: `grain` `weave` `flicker`; print: `paper` `misregister` `halftone` `quantize`; screen: `crt` |
| `anim` | time | `ease` `Track` `phase` `loop_noise` `on`; `render(fn, n, dir)` `motion_blur` `encode` `extract` |
| `screen` | seeing | `filmstrip` `onion` `motion_map` `flicker` `loop_seam` `scopes` `stats` `compare` `sheet` |
| `figure` | a jointed human in profile | `Figure()` `.joints(pose)` `.parts(pose)`; `Walk(fig, stride=...)` `.pose(g)`; `ik2` `periodic` `blend`; `gait_report` `draw_figure` `arcs` |
| `sound` | synthesis, mixing, mastering | instruments: `pluck` `bell` `glass` `epiano` `pad` `sub` `sea` `rain` `foghorn` `hum` `punch`; `Mix(dur).add(x, at, gain, pan_, send)` `.render(wet)`; `master` `loudness` `write_wav` `encode` `mux` |
| `score` | notes in bars and beats | `hz('D4')` `chord` `scale` `harmonic`; `Seq(bpm, beats)` `.note` `.chord` `.humanize` `.render(mix, tracks)`; `piano_roll` |
| `ear` | the listening room | `report(wav, out.jpg)` `measure` `ffmpeg_loudness`; calibrate with `backlot/tests/eartest.py` |
| `model` | the bridge to Blender | `Spec(...)` with `.material` `.sheet` `.panel` `.light` `.haze` `.camera` `.key` `.render`; `passes(exr)` |

## How a shot is put together

**2D (the animation stand).** Build plates once, write `frame(i)`, render, encode, look.

```python
from backlot import draw, comp, lab, anim, screen, shapes as sh
sh.setup(W, H, seed=3)
sky = draw.gradient(W, H, (0, 0), (0, H), '#101a2a', '#27405a', '#6c8794')
trees = comp.stencil(draw.raster(polys, W, H), '#0b1118')
def frame(i):
    p = anim.phase(i, N)                                  # 0..1 round the loop
    img = comp.multiplane([(sky, 50), (trees, 1.0)], cam=(40 * math.sin(2 * math.pi * p), 0))
    return lab.grain(lab.tonemap(lab.bloom(img)), frame=i)
pattern = anim.render(frame, N, 'out/shot/frames', workers=8)
anim.encode(pattern, 'shot.mp4', fps=24, loops=2)
```

**3D (the model shop).** Design sheets as mattes, cut them, light them, photograph them.

```python
S = model.Spec((1280, 720), ppm=4)                        # design pixels, pixels per millimetre
S.material('paper', kind='paper', translucency=.45, formation=.25)
S.material('back', kind='emit', strength=5, axis='Z', stops=[[0, '#ff8a3c'], [1, '#16286e']])
S.panel('back', (380, 240), (0, 86, 0), 'back')          # a light panel 86 mm behind the front
S.sheet('hills', matte, depth=40)                         # white in the matte is paper
S.light('lamp', pos=(-60, 52, 30), type='spot', power=1.6, color='#ffc27a', cone=34, rot=(90, 0, 0))
S.key('lamp', 'rotation_euler', [(1, [90, 0, 0]), (73, [90, 0, 360])])
S.haze((330, 30, 190), pos=(0, 54, 0), density=7)        # air, so a beam shows
S.camera(pos=(0, -545, 0), look=(0, 40, 0), lens=85, fstop=4, focus=(0, 46, 0))
frames = S.render('out/shot/exr', frames=range(1, 73), samples=110, res=(1280, 720))
p = model.passes(frames[0])                               # image, depth, index, emit, normal
```

Units are millimetres; X right, Z up, Y away from the camera. A sheet's `depth` is how far it
stands behind the front. `kind`: `paper` (diffuse plus translucent, cloudy when backlit), `card`
(opaque), `acetate`, `emit` (a light panel, optionally a gradation), `mirror`.
`S.key(target, path, keys)` animates anything: a sheet's `location` or `rotation_euler`, a light's
`data.energy`, `'cam'`, `'target'`, `'focus'`. About 6 seconds a frame at 1280x720 on an RTX 4070.

Then every frame goes through the lab and out through `anim.encode`, exactly as in 2D.

## Looking (do this after every step)

```
uv run python -m backlot strip  out/shot/frames out/strip.jpg 12     # twelve frames in a grid
uv run python -m backlot motion out/shot/frames out/motion.jpg       # where it moves, as heat
uv run python -m backlot seam   out/shot/frames                      # loop seam ratio, flicker
uv run python -m backlot scopes frame.png out/scopes.jpg             # histogram, waveform, vectorscope
uv run python -m backlot stats  frame.png                            # value masses, chroma, detail
```

`loop_seam` ratio near 1 means the loop point is no rougher than any other frame change.
`motion_map` softens frames first so film grain does not count as motion.

## Things that will trip you

- A sheet nearer the lens shows less of itself. Design each sheet for the window the camera has
  on it at that depth, not for the whole canvas.
- Paper cannot hold a strip thinner than about a millimetre and an unattached piece falls out.
  `draw.paperize(matte, min_width, anchor)` removes both and tells you how much was lost.
- Blender 5 renders multilayer EXR in several *parts*; `core.read_exr` reads them all.
- Light power is in watts at tabletop scale: 0.01 to 2, not hundreds.
- `anim.render` forks worker processes; build plates before calling it, not inside `frame`.
- Do the lens (`bloom`, `halation`) before `tonemap`, and `grain` after.

## Not included (yet)

3D LUT files, error-diffusion dither, sound, a non-linear editor (cut shots together with
ffmpeg's concat), and any window: nothing here is interactive.
