"""Keepalive, to play: writes play/ (the stills, their colour cycling, the hot spots). play/index.html and
play/play.js are written by hand and are the whole game: about two hundred lines.

    python export.py
"""
import sys, json
from pathlib import Path
HERE = Path(__file__).resolve().parent; sys.path.insert(0, str(HERE)); sys.path.insert(1, str(HERE.parent)); sys.path.insert(2, str(HERE.parents[2]))
import numpy as np, cv2
from multiprocessing import Pool
import game as G, stage2 as S2

def todo():
    out = {}
    for l in (0, 1): out['jetty_%d' % l] = ('jetty', dict(lamp=bool(l))); out['path_%d' % l] = ('path', dict(lamp=bool(l)))
    out['shelter'] = ('shelter', {})
    for k in (0, 1): out['book_%d' % k] = ('book', dict(linked=bool(k))); out['glass_%d' % k] = ('glass', dict(lit=bool(k)))
    for d in range(10):
        for l, v in ((0, 0), (1, 1), (0, 1), (1, 0)): out['beacon_%d%d%d' % (l, v, d)] = ('beacon', dict(lamp=bool(l), lever=bool(v), dial=d))
    for l in (0, 1):
        for h in (0, 1): out['lookout_%d%d' % (l, h)] = ('lookout', dict(lamp=bool(l), lit=bool(h)))
    return out
def one(item):
    key, (node, st) = item; idx, cyc = G.still(node, **st); d = HERE / 'play' / 'img'; d.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(d / (key + '.png')), (S2.T16[idx][..., ::-1] * 255 + .5).astype(np.uint8), [cv2.IMWRITE_PNG_COMPRESSION, 9]); has = bool(cyc.slot.any())
    if has: cv2.imwrite(str(d / (key + '_c.png')), cyc.slot, [cv2.IMWRITE_PNG_COMPRESSION, 9])
    return key, [[int(v) for v in t] for t in cyc.tables] if has else None
if __name__ == '__main__':
    T = todo()
    with Pool(14) as pool: res = dict(pool.map(one, list(T.items())))
    spots = {n: {k: list(map(int, r)) for k, r in G.hotspots(n).items()} for n in G.NODES if n != 'sea'}; spots['book'] = {}
    json.dump(dict(palette=[[int(v) for v in c] for c in (S2.T16 * 255 + .5).astype(int)], cycles=res, spots=spots, back=G.BACK), open(HERE / 'play' / 'game.json', 'w'), separators=(',', ':'))
    print(len(res), 'stills;', sum(f.stat().st_size for f in (HERE / 'play' / 'img').glob('*.png')) // 1024, 'KB')
