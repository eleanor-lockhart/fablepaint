"""backlot.sync: is the picture on the music, and did anything happen that nobody planned?

An agent cannot watch a film with the sound on, so this measures it. Give it the list of moments that are
meant to land (seconds, label), the folder of frames and the mixed sound.

    check(points, frames, wav)     per point: what the picture did on that frame, what the sound did at that instant
    events(points, frames, out)    a sheet of consecutive frames round every point: look at these, not at strips
    pops(points, frames)           large local changes that are NOT on the list: unplanned pops, forgotten cuts
    travel(frames)                 how far the whole picture slides per frame: the camera's speed, for strobing

What it cannot tell you: whether a viewer was looking there. "On time" is not "seen". An event lands for a
viewer when it happens to the brightest, simplest thing in the frame, is repeated, and takes long enough to
see. That needs a cold reader (backlot.reader), not this module.
"""
import json
from pathlib import Path
import numpy as np
import cv2
from scipy import signal

def picture(frames_dir, size=(640, 360), block=16):
    """Per frame: how much changed against the frame before. Returns (mean change, local change); local is the
    99.5th percentile of block changes, which sees a small light coming on that the mean cannot."""
    files = sorted(Path(frames_dir).glob('f_*.png')); prev = None; mean, local = [], []
    w, h = size; hb = (h // block) * block
    for f in files:
        g = cv2.resize(cv2.imread(str(f)), size, interpolation=cv2.INTER_AREA).astype(np.float32) / 255.0
        g = cv2.GaussianBlur(g, (0, 0), 1.5)                                  # take the film grain out of the measurement
        if prev is None: mean.append(0.0); local.append(0.0)
        else:
            d = np.abs(g - prev).mean(2); mean.append(float(d.mean()))
            b = d[:hb].reshape(hb // block, block, w // block, block).mean((1, 3)); local.append(float(np.percentile(b, 99.5)))
        prev = g
    return np.array(mean), np.array(local)

def onsets(wav, hop=240):
    """Spectral-flux onset envelope at 5 ms hops: (times, flux, threshold, loudness envelope, sample rate)."""
    from . import sound as sd
    x, sr = sd.read_wav(wav); mono = x.mean(1)
    f, t, Z = signal.stft(mono, sr, nperseg=1024, noverlap=1024 - hop, window='hann', padded=False, boundary=None)
    S = np.log1p(np.abs(Z) * 50); flux = np.maximum(np.diff(S, axis=1), 0).sum(0)
    flux = flux - signal.medfilt(flux, 41); t = t[1:] - 512 / sr + hop / sr
    env = np.sqrt(signal.convolve(mono ** 2, np.ones(480) / 480, 'same'))
    return t, np.maximum(flux, 0), flux.std() * 1.5, env, sr

def check(points, frames_dir, wav, fps=12, out_jpg=None, out_json=None, quiet=False):
    """For every (seconds, label): does the picture change on that frame clearly more than on its neighbours
    ("picture lands"), and is there a sound onset within 40 ms ("sound lands")? Writes a timeline picture and a
    json report, prints a table, returns the report."""
    mean, local = picture(frames_dir); n = len(mean)
    t, flux, thr, env, sr = onsets(wav)
    rows = []
    for s, label in points:
        p = int(round(s * fps))
        if p >= n: continue
        near = np.r_[local[max(1, p - 5):p], local[p + 1:p + 6]]; base = float(np.median(near)) if len(near) else 0.0
        pic = local[p] / max(base, 1e-4)
        m = (t >= s - .06) & (t <= s + .06); k = int(np.argmax(flux[m])); off = (t[m][k] - s) * 1000; strength = flux[m][k] / thr
        rows.append(dict(t=s, pose=p, what=label, picture_change=round(float(local[p]), 4), picture_vs_neighbours=round(float(pic), 1),
                         picture_lands=bool(pic >= 2.0 and local[p] > .004), sound_onset=round(float(strength), 1), sound_offset_ms=round(float(off)),
                         sound_lands=bool(strength >= 1.0 and abs(off) <= 40)))
    listed = {r['pose'] for r in rows}; order = np.argsort(-local)
    stray = [dict(pose=int(p), t=round(p / fps, 2), picture_change=round(float(local[p]), 4), on_beat=bool(p % 6 == 0)) for p in order[:60] if int(p) not in listed][:14]
    out = dict(points=rows, both=sum(r['picture_lands'] and r['sound_lands'] for r in rows), picture_only=[r['t'] for r in rows if r['picture_lands'] and not r['sound_lands']],
               sound_only=[r['t'] for r in rows if r['sound_lands'] and not r['picture_lands']], neither=[r['t'] for r in rows if not r['sound_lands'] and not r['picture_lands']],
               total=len(rows), unlisted_picture_changes=stray)
    if out_jpg:
        W, Hh = 1860, 150; dur = n / fps; X = lambda s: int(30 + (W - 60) * s / dur)
        img = np.full((Hh * 2 + 70, W, 3), 22, np.uint8)
        for b in range(0, int(dur) + 1, 2):
            cv2.line(img, (X(b), 20), (X(b), Hh * 2 + 40), (48, 48, 48), 1); cv2.putText(img, f'{b}', (X(b) + 2, Hh * 2 + 58), cv2.FONT_HERSHEY_SIMPLEX, .36, (170, 170, 160), 1, cv2.LINE_AA)
        lv = np.clip(local / max(np.percentile(local, 99.5), 1e-6), 0, 1)
        for p in range(1, n):
            cv2.line(img, (X(p / fps), 20 + Hh), (X(p / fps), 20 + Hh - int(lv[p] * (Hh - 8))), (150, 220, 255), 1)
        fv = np.clip(flux / max(np.percentile(flux, 99.9), 1e-6), 0, 1); cols = np.array([X(s) for s in t])
        for c in np.unique(cols):
            v = fv[cols == c].max(); cv2.line(img, (int(c), 40 + Hh), (int(c), 40 + Hh + int(v * (Hh - 8))), (120, 255, 170), 1)
        for r in rows:
            ok = r['picture_lands'] and r['sound_lands']; c = (90, 200, 90) if ok else ((60, 170, 255) if (r['picture_lands'] or r['sound_lands']) else (80, 80, 255))
            cv2.drawMarker(img, (X(r['t']), 30 + Hh), c, cv2.MARKER_DIAMOND, 9, 2)
        cv2.putText(img, 'picture: change against the pose before (local)   |   green: both land   orange: one lands   red: neither', (30, 14), cv2.FONT_HERSHEY_SIMPLEX, .42, (225, 225, 215), 1, cv2.LINE_AA)
        cv2.putText(img, 'sound: onset strength', (30, Hh * 2 + 36), cv2.FONT_HERSHEY_SIMPLEX, .42, (225, 225, 215), 1, cv2.LINE_AA)
        Path(out_jpg).parent.mkdir(parents=True, exist_ok=True); cv2.imwrite(str(out_jpg), img, [cv2.IMWRITE_JPEG_QUALITY, 90])
    if out_json:
        Path(out_json).parent.mkdir(parents=True, exist_ok=True); Path(out_json).write_text(json.dumps(out, indent=1))
    if not quiet:
        print(f'{"t":>5} {"pose":>4}  {"picture":>8} {"x nbrs":>6} {"":2} {"sound":>5} {"ms":>4} {"":2}  what')
        for r in rows:
            print(f'{r["t"]:5.1f} {r["pose"]:4d}  {r["picture_change"]:8.4f} {r["picture_vs_neighbours"]:6.1f} {"P" if r["picture_lands"] else ".":2} {r["sound_onset"]:5.1f} {r["sound_offset_ms"]:4d} {"S" if r["sound_lands"] else ".":2}  {r["what"]}')
        print(f'both land: {out["both"]}/{out["total"]}   picture only: {out["picture_only"]}   sound only: {out["sound_only"]}   neither: {out["neither"]}')
        print('largest picture changes not on the list:', [(s['t'], s['picture_change']) for s in stray[:8]])
    return out

def events(points, frames_dir, out_dir, fps=12, before=4, after=8, cols=6, cell_w=320):
    """A sheet of CONSECUTIVE frames round every listed moment.

    Review strips that sample every half second cannot show anything shorter than half a second, and most of
    what fails is shorter than that: a five-pose nod, a punch, a one-pose pop. Rule of the house: nothing is
    passed on strips alone; every event and every camera move is looked at on its own run of frames."""
    from . import core, screen
    Path(out_dir).mkdir(parents=True, exist_ok=True); n = len(list(Path(frames_dir).glob('f_*.png'))); made = []
    for s, label in points:
        p = int(round(s * fps)); ps = [q for q in range(p - before, p + after) if 0 <= q < n]
        if not ps: continue
        f = Path(out_dir) / f't{s:05.1f}_{"".join(ch if ch.isalnum() else "_" for ch in label)[:28]}.jpg'
        screen.sheet([core.load(f'{frames_dir}/f_{q:04d}.png') for q in ps], str(f), [f'{q}{"  <<" if q == p else ""}' for q in ps], cols=cols, cell_w=cell_w)
        made.append(str(f))
    return made

def _grey(f, size):
    return cv2.GaussianBlur(cv2.resize(cv2.imread(str(f)), size, interpolation=cv2.INTER_AREA).astype(np.float32) / 255.0, (0, 0), 1.5)

def _local(a, b, block=16):
    d = np.abs(a - b).mean(2); h, w = d.shape; hb = (h // block) * block
    return float(np.percentile(d[:hb].reshape(hb // block, block, w // block, block).mean((1, 3)), 99.5))

def pops(points, frames_dir, fps=12, floor=.03, undo=.35, allow=(), size=(640, 360)):
    """One-frame accidents: a frame that differs strongly from the one before it, after which the picture goes
    straight back to what it was (the change from the frame before to the frame after is less than `undo` of
    it). That is the signature of a shape that should not be there, and not of a light coming on, a cut or a
    move, which stay changed. Listed moments, the frame after each, and `allow` (frame numbers of deliberate
    flashes) are let through. Use it as a failing test: an empty list passes.
    A library bug once drew a black slab behind a walk for one pose in eighteen; this is what sees it."""
    files = sorted(Path(frames_dir).glob('f_*.png')); ok = set(allow)
    for s_, _ in points: ok |= {int(round(s_ * fps)), int(round(s_ * fps)) + 1}
    out = []; g = [None, None, None]
    for p, f in enumerate(files):
        g = [g[1], g[2], _grey(f, size)]                    # frames p-2, p-1, p
        if g[0] is None or (p - 1) in ok: continue
        into = _local(g[0], g[1]); across = _local(g[0], g[2])
        if into > floor and across < undo * into:
            out.append(dict(frame=p - 1, t=round((p - 1) / fps, 3), change=round(into, 4), undone_to=round(across, 4)))
    return out

def travel(frames_dir, size=(640, 360), confident=.3):
    """How far the whole picture slides between consecutive frames, in pixels of the full frame, by phase
    correlation. Returns the (dx, dy) steps as an array (zero where the frames do not match as a slide: cuts,
    flashes) and a summary with the largest step. A move that steps more than about 1% of the frame width per
    frame strobes: drawings may be held on twos, but the camera moves on ones."""
    files = sorted(Path(frames_dir).glob('f_*.png')); prev = None; out = []; scale = None
    win = cv2.createHanningWindow(size, cv2.CV_32F)
    for f in files:
        im = cv2.imread(str(f)); scale = scale or im.shape[1] / size[0]
        g = cv2.GaussianBlur(cv2.cvtColor(cv2.resize(im, size, interpolation=cv2.INTER_AREA), cv2.COLOR_BGR2GRAY).astype(np.float32), (0, 0), 1.2)
        if prev is None: out.append((0.0, 0.0))
        else:
            (dx, dy), resp = cv2.phaseCorrelate(prev, g, win)
            out.append((dx * scale, dy * scale) if resp > confident else (0.0, 0.0))
        prev = g
    a = np.array(out); step = np.hypot(a[:, 0], a[:, 1]); wpx = int(size[0] * (scale or 1))
    return a, dict(max_step=round(float(step.max()), 1), at=int(step.argmax()), percent_of_width=round(float(step.max()) / wpx * 100, 2),
                   moving_frames=int((step > .5).sum()), strobing_frames=int((step > .01 * wpx).sum()), frame_width=wpx)
