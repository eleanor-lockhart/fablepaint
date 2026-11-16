"""python -m backlot <tool> ...   quick looks from the shell.

  strip  FRAMES OUT.jpg [n]      filmstrip of a frame folder / glob / pattern
  motion FRAMES OUT.jpg          motion heat map + statistics
  seam   FRAMES                  loop-seam ratio and flicker numbers
  scopes IMAGE OUT.jpg           histogram, waveform, vectorscope
  stats  IMAGE [crop]            value masses, chroma, warm share, detail
  travel FRAMES                  the camera's speed: largest slide of the whole picture between two frames
  run    FRAMES OUT.jpg START [n]  n consecutive frames from START on one sheet (look at events at their own speed)
"""
import sys, json
from . import screen
from .core import load
a = sys.argv[1:]
if not a:
    print(__doc__)
elif a[0] == 'strip':
    print(screen.filmstrip(a[1], a[2], n=int(a[3]) if len(a) > 3 else 12))
elif a[0] == 'motion':
    p, st = screen.motion_map(a[1], a[2]); print(p, json.dumps({k: round(v, 4) for k, v in st.items()}))
elif a[0] == 'seam':
    st = screen.flicker(a[1])[1]; st.pop('series')
    print(json.dumps({k: round(v, 5) for k, v in {**screen.loop_seam(a[1]), **st}.items()}))
elif a[0] == 'scopes':
    print(screen.scopes(load(a[1]), a[2]))
elif a[0] == 'stats':
    print(json.dumps({k: round(v, 3) for k, v in screen.stats(load(a[1]), float(a[2]) if len(a) > 2 else 0).items()}))
elif a[0] == 'travel':
    from . import sync
    print(json.dumps(sync.travel(a[1])[1]))
elif a[0] == 'run':
    from pathlib import Path
    s0, n = int(a[3]), int(a[4]) if len(a) > 4 else 12
    fs = sorted(Path(a[1]).glob('f_*.png'))[s0:s0 + n]
    print(screen.sheet([load(str(f)) for f in fs], a[2], [str(s0 + k) for k in range(len(fs))], cols=6, cell_w=320))
else:
    print(__doc__)
