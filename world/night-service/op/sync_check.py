"""Is the picture on the music?   uv run python world/night-service/op/sync_check.py     (after build.py)

Nobody here can watch the film with the sound on, so this measures it. For every sync point in the brief it
reports what the picture did on that pose (how much of the frame changed against the pose before, compared with
the poses around it) and what the sound did at that instant (the strongest onset within 60 ms, and how far off
it is). It also draws both on one timeline: op/review/sync.jpg.

A picture accent "lands" if the change on its pose is clearly bigger than its neighbours'. A sound accent
"lands" if there is an onset above the detector's threshold within 40 ms."""
import sys, json, math
from pathlib import Path
import numpy as np
import cv2
from scipy import signal
HERE = Path(__file__).resolve().parent
from backlot import sound as sd

FPS = 12
SYNC = [(2.0, 'punch: window 1'), (2.5, 'punch: window 2'), (3.0, 'punch: window 3'), (3.5, 'punch: window 4'), (4.0, 'TITLE HIT'),
        (6.0, 'tagline'), (10.0, 'lamp starts to sink'), (11.0, 'lamp flares'), (12.5, 'Dee punch'), (13.5, 'Dee punch'), (14.5, 'Dee punch'), (15.5, 'Dee punch'),
        (16.5, 'light leaves the house'), (18.0, 'cut: Marisol close'), (21.5, 'mast drops to green'), (22.0, 'cut: Red close'), (24.0, 'pre-chorus: the crossing'),
        (26.0, 'cut: heron'), (27.0, 'heron blinks'), (28.0, 'cut: Lang'), (28.5, 'Lang tap 1'), (29.0, 'Lang tap 2'), (29.5, 'Lang tap 3'), (30.0, 'Lang tap 4'),
        (30.5, 'Lang tap 5'), (31.0, 'Lang tap 6'), (32.0, 'BREAK: black'), (33.0, 'cold eye opens'), (34.0, 'CHORUS: No. 4'), (36.0, 'tilt lands'),
        (38.0, 'cut: the pod'), (41.5, 'CABLE SNAPS'), (42.0, 'cut: the walk'), (46.0, 'cut 1'), (46.5, 'cut 2'), (47.0, 'cut 3'), (47.5, 'cut 4'),
        (48.0, 'cut 5'), (48.5, 'cut 6'), (49.0, 'cut 7'), (49.5, 'cut 8'), (50.0, 'cut: No. 4 head'), (50.5, 'eye turns green'), (52.0, 'WINDOW OPENS'),
        (54.0, 'lineup: Orrin'), (54.5, 'Red'), (55.0, 'Dee'), (55.5, 'Marisol'), (56.0, 'Passenger'), (56.5, 'Lang'), (57.0, 'No. 4, far off'), (58.0, 'END CARD')]

def picture(frames_dir):
    """Per pose: how much changed against the pose before. Returns (mean change, local change) arrays; local is the
    99.5th percentile of 16-px block changes, which sees a small light coming on that the mean cannot."""
    files = sorted(Path(frames_dir).glob('f_*.png')); prev = None; mean, local = [], []
    for f in files:
        g = cv2.resize(cv2.imread(str(f)), (640, 360), interpolation=cv2.INTER_AREA).astype(np.float32) / 255.0
        g = cv2.GaussianBlur(g, (0, 0), 1.5)                                  # take the film grain out of the measurement
        if prev is None: mean.append(0.0); local.append(0.0)
        else:
            d = np.abs(g - prev).mean(2); mean.append(float(d.mean()))
            b = d[:352].reshape(22, 16, 40, 16).mean((1, 3)); local.append(float(np.percentile(b, 99.5)))
        prev = g
    return np.array(mean), np.array(local)

def onsets(wav, hop=240):
    """Spectral-flux onset envelope at 5 ms hops."""
    x, sr = sd.read_wav(wav); mono = x.mean(1)
    f, t, Z = signal.stft(mono, sr, nperseg=1024, noverlap=1024 - hop, window='hann', padded=False, boundary=None)
    S = np.log1p(np.abs(Z) * 50); flux = np.maximum(np.diff(S, axis=1), 0).sum(0)
    flux = flux - signal.medfilt(flux, 41); t = t[1:] - 512 / sr + hop / sr
    env = np.sqrt(signal.convolve(mono ** 2, np.ones(480) / 480, 'same'))
    return t, np.maximum(flux, 0), flux.std() * 1.5, env, sr

def main(frames_dir='out/op/full/frames', wav='out/op/music/night_service_op.wav'):
    mean, local = picture(frames_dir); n = len(mean)
    t, flux, thr, env, sr = onsets(wav)
    rows = []
    for s, label in SYNC:
        p = int(round(s * FPS))
        if p >= n: continue
        near = np.r_[local[max(1, p - 5):p], local[p + 1:p + 6]]; base = float(np.median(near)) if len(near) else 0.0
        pic = local[p] / max(base, 1e-4)
        m = (t >= s - .06) & (t <= s + .06); k = int(np.argmax(flux[m])); off = (t[m][k] - s) * 1000; strength = flux[m][k] / thr
        rows.append(dict(t=s, pose=p, what=label, picture_change=round(float(local[p]), 4), picture_vs_neighbours=round(float(pic), 1),
                         picture_lands=bool(pic >= 2.0 and local[p] > .004), sound_onset=round(float(strength), 1), sound_offset_ms=round(float(off)),
                         sound_lands=bool(strength >= 1.0 and abs(off) <= 40)))
    # the reverse question: the biggest picture changes that are NOT on the list (unplanned pops, or cuts I forgot)
    listed = {r['pose'] for r in rows}; order = np.argsort(-local)
    stray = [dict(pose=int(p), t=round(p / FPS, 2), picture_change=round(float(local[p]), 4), on_beat=bool(p % 6 == 0)) for p in order[:60] if int(p) not in listed][:14]
    out = dict(points=rows, both=sum(r['picture_lands'] and r['sound_lands'] for r in rows), picture_only=[r['t'] for r in rows if r['picture_lands'] and not r['sound_lands']],
               sound_only=[r['t'] for r in rows if r['sound_lands'] and not r['picture_lands']], neither=[r['t'] for r in rows if not r['sound_lands'] and not r['picture_lands']],
               total=len(rows), unlisted_picture_changes=stray)
    # the picture
    W, Hh = 1860, 150; dur = n / FPS; X = lambda s: int(30 + (W - 60) * s / dur)
    img = np.full((Hh * 2 + 70, W, 3), 22, np.uint8)
    for b in range(0, int(dur) + 1, 2):
        cv2.line(img, (X(b), 20), (X(b), Hh * 2 + 40), (48, 48, 48), 1); cv2.putText(img, f'{b}', (X(b) + 2, Hh * 2 + 58), cv2.FONT_HERSHEY_SIMPLEX, .36, (170, 170, 160), 1, cv2.LINE_AA)
    lv = np.clip(local / max(np.percentile(local, 99.5), 1e-6), 0, 1)
    for p in range(1, n):
        cv2.line(img, (X(p / FPS), 20 + Hh), (X(p / FPS), 20 + Hh - int(lv[p] * (Hh - 8))), (150, 220, 255), 1)
    fv = np.clip(flux / max(np.percentile(flux, 99.9), 1e-6), 0, 1); cols = np.array([X(s) for s in t])
    for c in np.unique(cols):
        v = fv[cols == c].max(); cv2.line(img, (int(c), 40 + Hh), (int(c), 40 + Hh + int(v * (Hh - 8))), (120, 255, 170), 1)
    for r in rows:
        ok = r['picture_lands'] and r['sound_lands']; c = (90, 200, 90) if ok else ((60, 170, 255) if (r['picture_lands'] or r['sound_lands']) else (80, 80, 255))
        cv2.drawMarker(img, (X(r['t']), 30 + Hh), c, cv2.MARKER_DIAMOND, 9, 2)
    cv2.putText(img, 'picture: change against the pose before (local)   |   green: both land   orange: one lands   red: neither', (30, 14), cv2.FONT_HERSHEY_SIMPLEX, .42, (225, 225, 215), 1, cv2.LINE_AA)
    cv2.putText(img, 'sound: onset strength', (30, Hh * 2 + 36), cv2.FONT_HERSHEY_SIMPLEX, .42, (225, 225, 215), 1, cv2.LINE_AA)
    (HERE / 'review').mkdir(exist_ok=True); cv2.imwrite(str(HERE / 'review' / 'sync.jpg'), img, [cv2.IMWRITE_JPEG_QUALITY, 90])
    (HERE / 'review' / 'sync.json').write_text(json.dumps(out, indent=1))
    print(f'{"t":>5} {"pose":>4}  {"picture":>8} {"x nbrs":>6} {"":2} {"sound":>5} {"ms":>4} {"":2}  what')
    for r in rows:
        print(f'{r["t"]:5.1f} {r["pose"]:4d}  {r["picture_change"]:8.4f} {r["picture_vs_neighbours"]:6.1f} {"P" if r["picture_lands"] else ".":2} {r["sound_onset"]:5.1f} {r["sound_offset_ms"]:4d} {"S" if r["sound_lands"] else ".":2}  {r["what"]}')
    print(f'both land: {out["both"]}/{out["total"]}   picture only: {out["picture_only"]}   sound only: {out["sound_only"]}   neither: {out["neither"]}')
    print('largest picture changes not on the list:', [(s['t'], s['picture_change']) for s in stray[:8]])
    return out

if __name__ == '__main__':
    main(*sys.argv[1:])
