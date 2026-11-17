"""Checks for the sixteen-colour print, on the real stills: python check.py"""
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent; sys.path.insert(0, str(HERE)); sys.path.insert(1, str(HERE.parent)); sys.path.insert(2, str(HERE.parents[2]))
import numpy as np
import game as G, stage2 as S2, film as F
for n, st in (('jetty', {}), ('beacon', dict(lamp=True, lever=True, dial=6)), ('lookout', dict(lamp=True, lit=True)), ('glass', dict(lit=True)), ('book', {}), ('sea', dict(lamp=True, lit=True))):
    idx, c = G.still(n, **st)
    assert idx.max() < 16 and all(max(t) < 16 for t in c.tables), 'every pixel of a still, and every colour it can cycle to, should be one of the sixteen registers'
    assert np.array_equal(c.at(idx, 3), c.at(idx, 11)), 'colour cycling should come round in eight ticks'
    assert not c.slot.any() or not np.array_equal(c.at(idx, 0), c.at(idx, 1)), 'a still with water in it should change from one tick to the next'
idx, c = G.still('glass', lit=True); assert set(np.unique(idx)) >= {5, 6}, 'the witch should still be green in the print'
idx, c = G.still('lookout', lamp=True, lit=True); assert not ({5, 6, 7} & set(np.unique(idx))), 'and nothing else should be'
a, b = G.still('jetty')[0], G.still('path')[0]
assert np.array_equal(S2.dissolve(a, b, 0.0), a) and np.array_equal(S2.dissolve(a, b, 1.01), b) and .4 < (S2.dissolve(a, b, .5) == b).mean(), 'a dissolve should begin as one still, end as the other, and be about half of each in the middle'
assert max(F.frame(i).max() for i in (0, 500, 1000, 1500, 1900)) < 16, 'every pixel of a finished frame (the hand and the log too) should be a register'
print('keepalive: sixteen registers in every pixel; only the witch is green; the sea comes round in eight ticks; the dissolve is whole at both ends')
