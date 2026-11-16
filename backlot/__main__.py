"""python -m backlot <tool> ...   quick looks from the shell.

  strip  FRAMES OUT.jpg [n]      filmstrip of a frame folder / glob / pattern
  motion FRAMES OUT.jpg          motion heat map + statistics
  seam   FRAMES                  loop-seam ratio and flicker numbers
  scopes IMAGE OUT.jpg           histogram, waveform, vectorscope
  stats  IMAGE [crop]            value masses, chroma, warm share, detail
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
else:
    print(__doc__)
