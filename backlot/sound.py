"""backlot.sound: the sound department. Instruments made from arithmetic, a mixer with a reverb send,
mastering to a loudness target, and file output. Nothing is sampled: every sound here is synthesised.

Sound is float arrays at SR samples a second: mono (n,) from instruments, stereo (n, 2) from the mixer.

    m = Mix(60)                                   # a 60-second stereo mix with a reverb bus
    m.add(pluck(293.66, 4), at=1.0, gain=-12, pan=-.2, send=-10)
    out = master(m.render(), target_lufs=-16)
    write_wav('cue.wav', out); encode('cue.wav', 'cue.mp3')
"""
import math, wave, subprocess
from pathlib import Path
import numpy as np
from scipy import signal

SR = 48000

def _n(dur): return max(1, int(round(dur * SR)))
def tt(dur): return np.arange(_n(dur)) / SR
def db(x): return 10.0 ** (x / 20.0)

def fade(x, fin=.004, fout=.03):
    """Short fades so nothing starts or stops with a click."""
    x = np.array(x, float); a, b = min(_n(fin), len(x) // 2), min(_n(fout), len(x) // 2)
    x[:a] *= np.linspace(0, 1, a); x[-b:] *= np.linspace(1, 0, b)
    return x

def adsr(dur, a=.01, d=.1, s=.7, r=.2):
    n = _n(dur); t = np.arange(n) / SR; e = np.full(n, s)
    e = np.where(t < a, t / max(a, 1e-6), np.where(t < a + d, 1 - (1 - s) * (t - a) / max(d, 1e-6), e))
    rel = np.clip((dur - t) / max(r, 1e-6), 0, 1)
    return e * rel

# ------------------------------------------------------------------ filters
def lowpass(x, fc, order=2):
    return signal.sosfilt(signal.butter(order, min(fc, SR * .45), 'low', fs=SR, output='sos'), x, axis=0)
def highpass(x, fc, order=2):
    return signal.sosfilt(signal.butter(order, fc, 'high', fs=SR, output='sos'), x, axis=0)
def bandpass(x, lo, hi, order=2):
    return signal.sosfilt(signal.butter(order, [lo, min(hi, SR * .45)], 'band', fs=SR, output='sos'), x, axis=0)

# ------------------------------------------------------------------ instruments (mono)
def sine(f, dur, phase=0.0):
    return np.sin(2 * math.pi * f * tt(dur) + phase)

def partials(f, dur, amps, ratios=None, t60=None, phases=None):
    """Additive synthesis: a sum of sine partials, each with its own level, tuning ratio and decay time."""
    t = tt(dur); out = np.zeros(len(t))
    for k, a in enumerate(amps):
        r = ratios[k] if ratios is not None else k + 1
        if f * r > SR * .45 or a == 0: continue
        e = np.exp(-6.91 * t / t60[k]) if t60 is not None else 1.0
        out += a * e * np.sin(2 * math.pi * f * r * t + (phases[k] if phases is not None else 0.0))
    return out

def pluck(f, dur=4.0, bright=.55, pos=.19, t60=3.2, seed=0):
    """A plucked string (harp, koto, music-box end of things). Every partial dies away, the high ones first:
    the note lasts only as long as it lasts. `pos` is where along the string it is plucked."""
    K = int(min(40, SR * .45 / f)); k = np.arange(1, K + 1)
    amps = np.abs(np.sin(k * math.pi * pos)) / k ** (1.35 - .6 * bright)
    ratios = k * np.sqrt(1 + .00035 * k * k)
    t6 = t60 / (1 + (k * f / 1400.0) ** 1.15)
    r = np.random.default_rng(seed)
    x = partials(f, dur, amps, ratios, t6, r.uniform(0, .3, K))
    thump = bandpass(r.normal(0, 1, _n(.012)), 800, 5000) * np.linspace(1, 0, _n(.012)) ** 2      # the finger leaving the string
    x[:len(thump)] += thump * .25 * bright
    return fade(x / max(np.abs(x).max(), 1e-9), .0015, .05)

def bell(f, dur=7.0, t60=6.0, bright=.5, third=.85):
    """A struck bell: partials that are not harmonics of each other, a low hum that outlasts the strike."""
    ratios = [.5, 1.0, 1.19, 1.5, 2.0, 2.51, 2.66, 3.01, 4.17, 5.43]
    amps = np.array([.55, 1.0, third, .55, .75, .45, .35, .4, .28, .18]) * np.array([1, 1, 1, 1, 1] + [bright * 1.6] * 5)    # `third`: the minor-third partial; turn it down over major chords
    t6 = [t60 * 1.3, t60, t60 * .8, t60 * .6, t60 * .5, t60 * .32, t60 * .28, t60 * .22, t60 * .14, t60 * .1]
    x = partials(f, dur, amps, ratios, t6)
    return fade(x / max(np.abs(x).max(), 1e-9), .001, .08)

def glass(f, dur=5.0, t60=4.0):
    """A pure, slightly breathy high tone with a soft start: the passengers' windows."""
    t = tt(dur)
    x = (np.sin(2 * math.pi * f * t) + .12 * np.sin(2 * math.pi * 2.0 * f * t) + .05 * np.sin(2 * math.pi * 3.01 * f * t)) * np.exp(-6.91 * t / t60)
    return fade(x * np.clip(t / .04, 0, 1), .002, .1)

def epiano(f, dur=3.5, vel=.7, t60=2.6):
    """An electric piano by frequency modulation: bright when struck hard, round when not."""
    t = tt(dur)
    idx = 2.2 * vel * np.exp(-t / .5) + .35 * vel
    x = np.sin(2 * math.pi * f * t + idx * np.sin(2 * math.pi * f * t)) * np.exp(-6.91 * t / t60)
    x += .18 * vel * np.sin(2 * math.pi * 14 * f * t if 14 * f < SR * .45 else 0) * np.exp(-t / .06)      # the tine
    return fade(x / max(np.abs(x).max(), 1e-9), .002, .06)

def pad(freqs, dur, attack=2.5, release=3.5, cutoff=900.0, detune=7.0, seed=0):
    """A soft held chord: detuned sawtooths through a low-pass, slow in, slow out. Use sparingly: a held
    sound that does not die away is the other side's kind of sound."""
    r = np.random.default_rng(seed); t = tt(dur); x = np.zeros(len(t))
    for f in freqs:
        for c in (-detune, 0, detune):
            ff = f * 2 ** (c / 1200.0); K = int(min(24, cutoff * 3 / ff)) or 1
            x += partials(ff, dur, [1.0 / k for k in range(1, K + 1)], phases=r.uniform(0, 6.28, K))
    x = lowpass(x, cutoff, 2) * adsr(dur, attack, .1, 1.0, release)
    return x / max(np.abs(x).max(), 1e-9)

def sub(f, dur=1.5, t60=1.6):
    t = tt(dur)
    return fade((np.sin(2 * math.pi * f * t) + .22 * np.sin(4 * math.pi * f * t)) * np.exp(-6.91 * t / t60), .012, .08)

def noise(dur, color='pink', seed=0):
    """white, pink (1/f) or brown (1/f^2) noise, peak-normalised."""
    n = _n(dur); r = np.random.default_rng(seed)
    X = np.fft.rfft(r.normal(0, 1, n)); f = np.fft.rfftfreq(n, 1 / SR); f[0] = f[1]
    X *= {'white': 1.0, 'pink': 1 / np.sqrt(f), 'brown': 1 / f}[color]
    x = np.fft.irfft(X, n)
    return x / max(np.abs(x).max(), 1e-9)

def sea(dur, period=6.0, phase=0.0, seed=0):
    """Water on a shore: a low wash that swells and a hiss of foam that follows it, once every `period` seconds."""
    t = tt(dur)
    swell = (.5 - .5 * np.cos(2 * math.pi * (t / period + phase))) ** 1.6
    foam = (.5 - .5 * np.cos(2 * math.pi * (t / period + phase - .16))) ** 3.0
    body = lowpass(noise(dur, 'brown', seed), 500) * (.35 + .65 * swell)
    hiss = bandpass(noise(dur, 'white', seed + 1), 1800, 7000) * foam * .22
    x = body / max(np.abs(body).max(), 1e-9) + hiss
    return fade(x / max(np.abs(x).max(), 1e-9), .5, 1.0)

def rain(dur, density=1.0, seed=0):
    """Steady rain: a bright hiss with thousands of small separate drops in it."""
    r = np.random.default_rng(seed); n = _n(dur)
    hiss = bandpass(r.normal(0, 1, n), 2500, 11000) * .25
    drops = np.zeros(n); k = int(dur * 220 * density)
    drops[r.integers(0, n, k)] = r.uniform(.3, 1, k)
    drops = signal.fftconvolve(drops, bandpass(r.normal(0, 1, _n(.004)), 1500, 9000) * np.linspace(1, 0, _n(.004)) ** 2, 'same')
    x = hiss + drops * 1.2
    return fade(x / max(np.abs(x).max(), 1e-9), .5, 1.0)

def foghorn(dur=3.4, f=146.83, grunt=.5):
    """A diaphone, far off: a long reedy note that ends by dropping to a lower one (the 'grunt')."""
    n = _n(dur); t = np.arange(n) / SR
    tg = dur - grunt
    freq = np.where(t < tg, f, f * (1 - .42 * np.clip((t - tg) / .12, 0, 1)))
    ph = 2 * math.pi * np.cumsum(freq) / SR
    x = sum(np.sin(k * ph) / k ** 1.05 for k in range(1, 15))
    x = lowpass(x, 1100, 2) * np.clip(t / .3, 0, 1) * np.clip((dur - t) / .25, 0, 1) * (1 + .03 * np.sin(2 * math.pi * 4.5 * t))
    return x / max(np.abs(x).max(), 1e-9)

def hum(dur, f=60.0, buzz=.5):
    """Mains hum. Perfectly steady, no beginning and no end: the sound of light nobody is watching.
    `buzz` adds the transformer's upper odd harmonics, which is the part small speakers can actually play."""
    t = tt(dur)
    x = sum(a * np.sin(2 * math.pi * f * k * t) for k, a in ((1, 1.0), (2, .5), (3, .7), (5, .34), (7, .2), (9, .1), (11, .05)))
    x = x + buzz * sum(np.sin(2 * math.pi * f * k * t + k) * 6.0 / k ** 2 for k in range(13, 41, 2))
    return x / np.abs(x).max()

def punch():
    """Dee's ticket punch: chk."""
    r = np.random.default_rng(3)
    click = bandpass(r.normal(0, 1, _n(.006)), 2200, 7500) * np.linspace(1, 0, _n(.006)) ** 2
    thunk = np.sin(2 * math.pi * 95 * tt(.05)) * np.exp(-tt(.05) / .012)
    ring = np.sin(2 * math.pi * 2350 * tt(.09)) * np.exp(-tt(.09) / .02) * .3
    x = np.zeros(_n(.1)); x[:len(click)] += click; x[:len(thunk)] += thunk * .7; x[:len(ring)] += ring
    return x / np.abs(x).max()

# ------------------------------------------------------------------ space
def pan(x, p=0.0):
    """Mono -> stereo, equal power. p from -1 (left) to 1 (right)."""
    a = (p + 1) * math.pi / 4
    return np.c_[x * math.cos(a), x * math.sin(a)]

def reverb_ir(t60=4.0, damp=.55, predelay=.025, seed=0):
    """A synthetic room: noise that dies away, the treble faster than the bass, a few early echoes first."""
    r = np.random.default_rng(seed); n = _n(t60 * 1.15); t = np.arange(n) / SR
    ir = np.zeros((n, 2))
    for ch in (0, 1):
        w = r.normal(0, 1, n)
        lo, mid, hi = lowpass(w, 500), bandpass(w, 500, 3000), highpass(w, 3000)
        x = lo * np.exp(-6.91 * t / (t60 * 1.15)) + mid * np.exp(-6.91 * t / t60) + hi * np.exp(-6.91 * t / (t60 * (1 - damp) + .05))
        for d, g in zip(r.uniform(.006, .07, 6), r.uniform(.25, .6, 6)):
            x[_n(d)] += g * 6
        ir[:, ch] = np.r_[np.zeros(_n(predelay)), x][:n]
    return ir / np.sqrt((ir ** 2).sum(0).mean())

def delay(x, time=.5, feedback=.35, mix=.3, lp=3500):
    out = np.array(x, float); echo = np.array(x, float)
    for _ in range(6):
        echo = np.r_[np.zeros((_n(time),) + x.shape[1:]), lowpass(echo, lp) * feedback][:len(x)]
        out += echo * mix
    return out

class Mix:
    """A stereo mix with one reverb bus. Levels are in decibels. `send` is how much of a sound also goes to the reverb."""
    def __init__(self, dur, t60=4.0, damp=.55, seed=0):
        self.n = _n(dur); self.dry = np.zeros((self.n, 2)); self.bus = np.zeros((self.n, 2)); self.ir = reverb_ir(t60, damp, seed=seed)
    def add(self, x, at=0.0, gain=0.0, pan_=0.0, send=None):
        x = pan(x, pan_) if x.ndim == 1 else x
        i = _n(at) if at > 0 else 0
        if i >= self.n: return
        x = x[:self.n - i] * db(gain)
        self.dry[i:i + len(x)] += x
        if send is not None:
            self.bus[i:i + len(x)] += x * db(send)
    def render(self, wet=0.0):
        rev = np.c_[signal.fftconvolve(self.bus[:, 0], self.ir[:, 0])[:self.n], signal.fftconvolve(self.bus[:, 1], self.ir[:, 1])[:self.n]] * db(wet)
        rms = lambda a: math.sqrt(float((a ** 2).mean()) + 1e-20)
        self.wet_to_dry_db = 20 * math.log10(rms(rev) / rms(self.dry))        # how much room there is, as a number
        return self.dry + rev

# ------------------------------------------------------------------ mastering and files
def loudness(x):
    """Integrated loudness in LUFS (ITU-R BS.1770: K-weighting, 400 ms blocks, absolute and relative gates)."""
    x = pan(x) if x.ndim == 1 else x
    y = signal.lfilter([1.53512485958697, -2.69169618940638, 1.19839281085285], [1.0, -1.69065929318241, 0.73248077421585], x, axis=0)
    y = signal.lfilter([1.0, -2.0, 1.0], [1.0, -1.99004745483398, 0.99007225036621], y, axis=0)
    b, h = _n(.4), _n(.1)
    ms = np.array([(y[i:i + b] ** 2).mean(0).sum() for i in range(0, len(y) - b + 1, h)])
    if not len(ms): return -70.0
    L = -.691 + 10 * np.log10(np.maximum(ms, 1e-12))
    g = ms[L > -70]
    if not len(g): return -70.0
    rel = -.691 + 10 * np.log10(g.mean()) - 10
    g = ms[(L > -70) & (L > rel)]
    return float(-.691 + 10 * np.log10(g.mean()))

def true_peak(x):
    return float(20 * np.log10(max(np.abs(signal.resample_poly(x, 4, 1, axis=0)).max(), 1e-9)))

def master(x, target_lufs=-16.0, ceiling=-1.0, hp=28.0):
    """High-pass the rumble, bring the whole thing to a target loudness, and hold the peaks under a ceiling
    (a look-ahead limiter: it turns down just before a peak and lets go slowly)."""
    from scipy.ndimage import maximum_filter1d
    x = highpass(x, hp, 2)
    x = x * db(target_lufs - loudness(x))
    env = maximum_filter1d(np.abs(x).max(1), size=2 * _n(.004) + 1)
    g = np.minimum(1.0, db(ceiling - .5) / np.maximum(env, 1e-9))
    g = np.minimum(g, signal.filtfilt(*signal.butter(1, 30, 'low', fs=SR), g))
    x = x * g[:, None]
    return x * db(min(0.0, ceiling - true_peak(x)))

def write_wav(path, x, bits=16):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    x = pan(x) if x.ndim == 1 else x
    d = (np.random.default_rng(1).random(x.shape) - np.random.default_rng(2).random(x.shape)) / 32768.0
    y = np.clip(np.round((x + d) * 32767), -32768, 32767).astype('<i2')
    with wave.open(str(path), 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(y.tobytes())
    return str(path)

def read_wav(path):
    with wave.open(str(path), 'rb') as w:
        ch, sw, sr, n = w.getnchannels(), w.getsampwidth(), w.getframerate(), w.getnframes()
        a = np.frombuffer(w.readframes(n), dtype='<i2' if sw == 2 else '<i4').astype(float) / (32768.0 if sw == 2 else 2147483648.0)
    a = a.reshape(-1, ch)
    return (a if ch == 2 else np.c_[a[:, 0], a[:, 0]]), sr

def encode(wav, out, bitrate='192k'):
    """wav -> .mp3, .m4a (AAC), .ogg or .opus, by extension."""
    codec = {'.mp3': ['-c:a', 'libmp3lame'], '.m4a': ['-c:a', 'aac'], '.ogg': ['-c:a', 'libvorbis'], '.opus': ['-c:a', 'libopus']}[Path(out).suffix.lower()]
    subprocess.run(['ffmpeg', '-y', '-hide_banner', '-loglevel', 'error', '-i', str(wav)] + codec + ['-b:a', bitrate, str(out)], check=True)
    return str(out)

def mux(video, audio, out, loop_video=True, crf=26, width=None):
    """Put a soundtrack under a picture. With loop_video the picture repeats for as long as the sound lasts.
    A long loop of grainy video is large: raise crf or give a smaller width for the web."""
    vf = ['-vf', f'scale={width}:-2:flags=lanczos'] if width else []
    cmd = ['ffmpeg', '-y', '-hide_banner', '-loglevel', 'error'] + (['-stream_loop', '-1'] if loop_video else []) + ['-i', str(video), '-i', str(audio),
           '-map', '0:v', '-map', '1:a'] + vf + ['-c:v', 'libx264', '-crf', str(crf), '-preset', 'slow', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '160k', '-shortest', '-movflags', '+faststart', str(out)]
    subprocess.run(cmd, check=True)
    return str(out)
