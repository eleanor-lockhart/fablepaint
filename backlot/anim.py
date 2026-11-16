"""backlot.anim: time. Easing, keyframe tracks, seamless loops, stop-motion holds, a parallel
frame renderer, and encoders.

A shot is a function frame(i) -> image. Everything else here helps write that function or run it.
"""
import math, os, subprocess, shutil
from pathlib import Path
import numpy as np
from .core import F, save

# ---------------------------------------------------------------- easing and tracks
def ease(t, kind='inout'):
    """t in 0..1 -> eased 0..1. kinds: linear in out inout (cubic), expo, sine, back, snap."""
    t = float(np.clip(t, 0, 1))
    if kind == 'linear': return t
    if kind == 'in': return t ** 3
    if kind == 'out': return 1 - (1 - t) ** 3
    if kind == 'inout': return 4 * t ** 3 if t < .5 else 1 - (-2 * t + 2) ** 3 / 2
    if kind == 'expo': return 0 if t == 0 else 1 if t == 1 else (2 ** (20 * t - 10) / 2 if t < .5 else (2 - 2 ** (-20 * t + 10)) / 2)
    if kind == 'sine': return -(math.cos(math.pi * t) - 1) / 2
    if kind == 'back': c = 1.70158; return 1 + (c + 1) * (t - 1) ** 3 + c * (t - 1) ** 2
    if kind == 'snap': return 1.0 if t >= 1 else 0.0
    raise ValueError(kind)

class Track:
    """Keyframes: Track([(0, a), (24, b, 'out'), (48, c)])(frame) -> value. Values may be numbers or tuples.
    The ease named on a key shapes the move INTO that key."""
    def __init__(self, keys):
        self.keys = sorted([(k[0], np.asarray(k[1], float), k[2] if len(k) > 2 else 'inout') for k in keys], key=lambda k: k[0])
    def __call__(self, t):
        ks = self.keys
        if t <= ks[0][0]: return ks[0][1]
        if t >= ks[-1][0]: return ks[-1][1]
        for a, b in zip(ks, ks[1:]):
            if a[0] <= t <= b[0]:
                return a[1] + (b[1] - a[1]) * ease((t - a[0]) / (b[0] - a[0]), b[2])

def phase(i, n):
    """Frame i of an n-frame loop -> 0..1 (frame n would be 0 again)."""
    return (i % n) / n

def loop_noise(p, seed=0, harmonics=4, falloff=.6):
    """Smooth wandering value in about -1..1 that repeats exactly when phase p goes 0 -> 1."""
    r = np.random.default_rng(seed)
    ph, amp = r.uniform(0, 2 * math.pi, harmonics), falloff ** np.arange(harmonics)
    return float(sum(amp[k] * math.sin(2 * math.pi * (k + 1) * p + ph[k]) for k in range(harmonics)) / amp.sum())

def on(i, n=2):
    """Stop-motion hold: the pose index for frame i when shooting 'on twos' (n=2), threes, ..."""
    return i // n

# ---------------------------------------------------------------- rendering frames
_FN = None
def _work(job):
    i, path, bits = job
    img = _FN(i)
    if img is not None:
        save(path, img, bits=bits)
    return i

def render(fn, frames, out_dir, workers=8, pattern='f_%04d.png', bits=8, skip_existing=False):
    """Render fn(i) for each frame number in `frames` (an int n means range(n)) to out_dir, in parallel.
    fn may be any function or closure (worker processes are forked). Returns the file pattern."""
    global _FN
    import multiprocessing as mp
    frames = list(range(frames)) if isinstance(frames, int) else list(frames)
    out = Path(out_dir); out.mkdir(parents=True, exist_ok=True)
    jobs = [(i, str(out / (pattern % i)), bits) for i in frames if not (skip_existing and (out / (pattern % i)).exists())]
    _FN = fn
    if workers <= 1 or len(jobs) <= 1:
        for j in jobs: _work(j)
    else:
        with mp.get_context('fork').Pool(min(workers, len(jobs))) as pool:
            for _ in pool.imap_unordered(_work, jobs): pass
    return str(out / pattern)

def motion_blur(fn, i, samples=5, shutter=.5):
    """Average fn(t) over the shutter interval (in linear light): real motion blur for anything fn can draw at fractional time."""
    return sum(fn(i + shutter * (k / samples - .5)) for k in range(samples)) / samples

# ---------------------------------------------------------------- encoding
def encode(pattern, out, fps=24, crf=16, start=0, loops=1, audio=None, scale=None):
    """Frames (printf pattern) -> .mp4 (H.264, plays everywhere), .webm (VP9), .gif or .webp, chosen by extension.
    loops > 1 repeats the sequence that many times in the file (useful for short loops)."""
    out = Path(out); out.parent.mkdir(parents=True, exist_ok=True)
    src = ['-framerate', str(fps), '-start_number', str(start)] + (['-stream_loop', str(loops - 1)] if loops > 1 else []) + ['-i', pattern]
    vf = [f'scale={scale}:flags=lanczos'] if scale else []
    ext = out.suffix.lower()
    if ext == '.mp4':
        cmd = src + (['-i', str(audio)] if audio else []) + ['-vf', ','.join(vf + ['format=yuv420p']), '-c:v', 'libx264', '-crf', str(crf), '-preset', 'slow',
              '-movflags', '+faststart'] + (['-c:a', 'aac', '-b:a', '160k', '-shortest'] if audio else [])
    elif ext == '.webm':
        cmd = src + ['-vf', ','.join(vf + ['format=yuv420p']), '-c:v', 'libvpx-vp9', '-crf', str(crf + 14), '-b:v', '0']
    elif ext == '.gif':
        cmd = src + ['-vf', ','.join(vf + ['split[a][b];[a]palettegen=stats_mode=diff[p];[b][p]paletteuse=dither=bayer:bayer_scale=4']), '-loop', '0']
    elif ext == '.webp':
        cmd = src + (['-vf', ','.join(vf)] if vf else []) + ['-c:v', 'libwebp_anim', '-lossless', '0', '-q:v', '82', '-loop', '0']
    else:
        raise ValueError(ext)
    r = subprocess.run(['ffmpeg', '-y', '-hide_banner', '-loglevel', 'error'] + cmd + [str(out)], capture_output=True, text=True)
    if r.returncode:
        raise RuntimeError(r.stderr[-800:])
    return str(out)

def extract(video, out_dir, every=1, pattern='f_%04d.png'):
    """Video -> frames, for looking at something that was not rendered here."""
    out = Path(out_dir); out.mkdir(parents=True, exist_ok=True)
    subprocess.run(['ffmpeg', '-y', '-hide_banner', '-loglevel', 'error', '-i', str(video), '-vf', f'select=not(mod(n\\,{every}))', '-vsync', 'vfr', str(out / pattern)], check=True)
    return str(out / pattern)
