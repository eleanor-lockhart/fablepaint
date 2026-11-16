"""backlot.ear: the listening room. An agent cannot hear, so this turns a recording into pictures and
numbers it can read: where the energy is, how loud, which notes, how regular, whether anything is broken.

    r = report('cue.wav', 'cue_report.jpg')       # one sheet: waveform, loudness, spectrogram, chroma, numbers
    print(r['lufs'], r['key'], r['bands'])

What this can tell: balance, loudness, clipping, pitch content, rhythm, silence, stereo. What it cannot tell:
whether it is beautiful. Treat the numbers as an instrument panel, not as taste.
"""
import math, subprocess, re
from pathlib import Path
import numpy as np
import cv2
from scipy import signal
from .sound import SR, read_wav, loudness, true_peak
from .score import NAMES

BANDS = [('sub', 20, 60), ('bass', 60, 250), ('low-mid', 250, 500), ('mid', 500, 2000), ('presence', 2000, 6000), ('air', 6000, 20000)]
_MAJ = np.array([6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88])      # Krumhansl-Kessler key profiles
_MIN = np.array([6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17])

def stft(x, n=4096, hop=1024):
    f, t, Z = signal.stft(x, SR, nperseg=n, noverlap=n - hop, window='hann', padded=False, boundary=None)
    return f, t, np.abs(Z)

def measure(x):
    """The numbers. x is stereo."""
    mono = x.mean(1); out = {}
    out['seconds'] = len(x) / SR
    out['lufs'] = loudness(x); out['true_peak_db'] = true_peak(x)
    rms = float(np.sqrt((mono ** 2).mean())); out['rms_db'] = 20 * math.log10(max(rms, 1e-9))
    out['crest_db'] = 20 * math.log10(max(np.abs(mono).max(), 1e-9)) - out['rms_db']
    out['clipped_samples'] = int((np.abs(x) >= .999).sum()); out['dc'] = float(mono.mean())
    L, R = x[:, 0], x[:, 1]
    out['stereo_correlation'] = float(np.corrcoef(L, R)[0, 1]) if L.std() > 0 and R.std() > 0 else 1.0
    out['side_to_mid_db'] = 20 * math.log10(max(np.sqrt(((L - R) ** 2).mean()), 1e-9) / max(np.sqrt(((L + R) ** 2).mean()), 1e-9))
    f, t, S = stft(mono); P = (S ** 2).mean(1); tot = P.sum()
    out['bands'] = {nme: float(10 * math.log10(max(P[(f >= lo) & (f < hi)].sum() / tot, 1e-12))) for nme, lo, hi in BANDS}
    out['centroid_hz'] = float((f * P).sum() / tot)
    # short-term loudness (3 s windows, 1 s hop) and how much it moves
    st = np.array([loudness(x[i:i + 3 * SR]) for i in range(0, max(len(x) - 3 * SR, 1), SR)])
    out['short_term'] = st.round(1).tolist(); live = st[st > -60]
    out['loudness_range'] = float(np.percentile(live, 95) - np.percentile(live, 10)) if len(live) > 2 else 0.0
    blk = np.sqrt(np.array([(mono[i:i + SR // 4] ** 2).mean() for i in range(0, len(mono) - SR // 4, SR // 4)]))
    out['silent_fraction'] = float((20 * np.log10(np.maximum(blk, 1e-9)) < -60).mean())
    # pitch classes -> key
    C = chroma(x=mono); prof = C.mean(1); prof = prof / max(prof.sum(), 1e-12)
    out['chroma'] = {NAMES[i]: round(float(prof[i]), 3) for i in range(12)}
    keys = []
    for i in range(12):
        keys.append((float(np.corrcoef(np.roll(_MAJ, i), prof)[0, 1]), NAMES[i] + ' major')); keys.append((float(np.corrcoef(np.roll(_MIN, i), prof)[0, 1]), NAMES[i] + ' minor'))
    keys.sort(reverse=True); out['key'] = keys[0][1]; out['key_candidates'] = [(k, round(c, 2)) for c, k in keys[:3]]
    # onsets -> how busy, and a tempo guess
    flux = np.maximum(np.diff(np.log1p(S * 50), axis=1), 0).sum(0); flux = flux - signal.medfilt(flux, 31)
    pk, _ = signal.find_peaks(flux, height=flux.std() * 1.5, distance=3)
    out['onsets_per_second'] = float(len(pk) / out['seconds'])
    ac = np.correlate(flux - flux.mean(), flux - flux.mean(), 'full')[len(flux) - 1:]; hop_s = 1024 / SR
    lo, hi = int(.3 / hop_s), int(2.2 / hop_s)
    if hi < len(ac):
        lag = lo + int(np.argmax(ac[lo:hi])); out['pulse_seconds'] = float(lag * hop_s); out['pulse_bpm'] = float(60.0 / (lag * hop_s))
    return out

def chroma(f=None, S=None, x=None):
    """Energy by pitch class (12 rows, C..B) over time, 100 Hz to 2 kHz. Needs fine frequency resolution: with
    coarse bins a bass D lands on C sharp. Pass the mono signal as x= for a dedicated long-window analysis."""
    if x is not None:
        f, _, Z = signal.stft(x, SR, nperseg=16384, noverlap=16384 - 4096, window='hann', padded=False, boundary=None); S = np.abs(Z)
    C = np.zeros((12, S.shape[1])); m = (f >= 100) & (f <= 2000)
    semis = 12 * np.log2(f[m] / 440.0); near = np.round(semis)
    wgt = np.clip(1 - np.abs(semis - near) / .4, 0, 1)             # ignore energy that is not close to any note
    pc = (near.astype(int) + 9) % 12
    for i in range(12):
        C[i] = ((S[m][pc == i] ** 2) * wgt[pc == i][:, None]).sum(0)
    return C

def _spec_image(x, w=1400, h=360, lo=30.0, hi=16000.0, floor=-85.0):
    f, t, S = stft(x.mean(1))
    dbs = 20 * np.log10(np.maximum(S / max(S.max(), 1e-9), 1e-9))
    rows = np.geomspace(hi, lo, h)
    img = np.stack([np.interp(rows, f, dbs[:, j]) for j in range(dbs.shape[1])], 1)
    img = cv2.resize(((np.clip(img, floor, 0) - floor) / -floor * 255).astype(np.uint8), (w, h), interpolation=cv2.INTER_AREA)
    img = cv2.applyColorMap(img, cv2.COLORMAP_MAGMA)
    for fr in (50, 100, 200, 500, 1000, 2000, 5000, 10000):
        y = int(np.interp(math.log(fr), np.log(rows[::-1]), np.arange(h)[::-1]))
        cv2.line(img, (0, y), (w, y), (70, 70, 70), 1); cv2.putText(img, f'{fr if fr < 1000 else str(fr // 1000) + "k"}', (4, y - 3), cv2.FONT_HERSHEY_SIMPLEX, .38, (220, 220, 210), 1, cv2.LINE_AA)
    return img

def report(wav, out, title=None):
    """One sheet for one recording: waveform, short-term loudness, spectrogram, chromagram, and the numbers. Returns the numbers."""
    x, sr = read_wav(wav) if isinstance(wav, (str, Path)) else (wav, SR)
    m = measure(x); W = 1400; dur = m['seconds']
    def axis(img):
        step = 5 if dur < 80 else 10
        for s in range(0, int(dur) + 1, step):
            xx = int(W * s / dur); cv2.line(img, (xx, img.shape[0] - 8), (xx, img.shape[0]), (200, 200, 190), 1)
            cv2.putText(img, f'{s}s', (xx + 3, img.shape[0] - 3), cv2.FONT_HERSHEY_SIMPLEX, .34, (200, 200, 190), 1, cv2.LINE_AA)
        return img
    # waveform (peak envelope per column)
    wf = np.full((120, W, 3), 22, np.uint8); mono = x.mean(1); n = len(mono) // W
    env = np.abs(mono[:n * W]).reshape(W, n).max(1)
    for i, v in enumerate(env):
        cv2.line(wf, (i, 60 - int(v * 56)), (i, 60 + int(v * 56)), (150, 220, 255), 1)
    # short-term loudness
    ll = np.full((90, W, 3), 22, np.uint8); st = np.array(m['short_term'])
    for ref in (-14, -23, -40):
        y = int(np.interp(ref, [-60, -5], [88, 2])); cv2.line(ll, (0, y), (W, y), (60, 60, 60), 1); cv2.putText(ll, f'{ref} LUFS', (4, y - 2), cv2.FONT_HERSHEY_SIMPLEX, .34, (170, 170, 160), 1, cv2.LINE_AA)
    pts = np.array([[int(W * (i + 1.5) / dur), int(np.interp(max(v, -60), [-60, -5], [88, 2]))] for i, v in enumerate(st)], np.int32)
    if len(pts) > 1: cv2.polylines(ll, [pts], False, (120, 255, 170), 2, cv2.LINE_AA)
    sp = _spec_image(x, W)
    C = chroma(x=x.mean(1)); C = C / max(C.max(), 1e-12)
    ch = cv2.applyColorMap(cv2.resize((np.sqrt(C[::-1]) * 255).astype(np.uint8), (W, 12 * 13), interpolation=cv2.INTER_NEAREST), cv2.COLORMAP_VIRIDIS)
    for i in range(12):
        cv2.putText(ch, NAMES[11 - i], (4, i * 13 + 11), cv2.FONT_HERSHEY_SIMPLEX, .36, (255, 255, 255), 1, cv2.LINE_AA)
    txt = np.full((112, W, 3), 22, np.uint8)
    lines = [f'{title or Path(str(wav)).name}   {dur:.1f} s   {m["lufs"]:.1f} LUFS integrated   true peak {m["true_peak_db"]:.1f} dB   loudness range {m["loudness_range"]:.1f}   crest {m["crest_db"]:.1f} dB   clipped {m["clipped_samples"]}',
             'bands (dB of total):  ' + '   '.join(f'{k} {v:.1f}' for k, v in m['bands'].items()) + f'   centroid {m["centroid_hz"]:.0f} Hz',
             f'key guess: {", ".join(f"{k} ({c})" for k, c in m["key_candidates"])}   strongest pitch classes: ' + ' '.join(k for k, v in sorted(m['chroma'].items(), key=lambda kv: -kv[1])[:5]),
             f'onsets {m["onsets_per_second"]:.2f}/s   pulse {m.get("pulse_seconds", 0):.2f} s ({m.get("pulse_bpm", 0):.0f} bpm)   stereo correlation {m["stereo_correlation"]:.2f}   side/mid {m["side_to_mid_db"]:.1f} dB   silent {m["silent_fraction"] * 100:.0f}%']
    for i, s in enumerate(lines):
        cv2.putText(txt, s, (8, 22 + i * 25), cv2.FONT_HERSHEY_SIMPLEX, .46, (225, 225, 215), 1, cv2.LINE_AA)
    sheet = np.vstack([txt, axis(wf), ll, axis(sp), ch])
    Path(out).parent.mkdir(parents=True, exist_ok=True); cv2.imwrite(str(out), sheet, [cv2.IMWRITE_JPEG_QUALITY, 88])
    return m

def ffmpeg_loudness(path):
    """Second opinion from ffmpeg's EBU R128 meter: (integrated LUFS, loudness range, true peak dBFS)."""
    r = subprocess.run(['ffmpeg', '-hide_banner', '-nostats', '-i', str(path), '-af', 'ebur128=peak=true', '-f', 'null', '-'], capture_output=True, text=True).stderr
    tail = r[r.rfind('Summary:'):]
    g = lambda pat: float(re.search(pat, tail).group(1)) if re.search(pat, tail) else None
    return g(r'I:\s+(-?[\d.]+) LUFS'), g(r'LRA:\s+(-?[\d.]+) LU'), g(r'Peak:\s+(-?[\d.]+) dBFS')
