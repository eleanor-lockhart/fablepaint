"""GATE.EXE: the tune. Ten seconds, eight bars of 6/8, four voices and nothing sampled.

    uv run python styles/hex/gate_exe_tune.py      (after stage1.py) writes the wav, a listening-room sheet, and puts the sound on the loop

A bar is fifteen frames of the picture, so every event in the loop sits on a bar line: the dialog on bar 2, the
button on bar 4, the report on bar 7, OK on bar 8. Bars 1 to 3 are a jig in D Dorian over a drone (a whistle and
a drum). On the downbeat of bar 4 the button goes down. Bars 5 to 7 are the same key as symphonic metal has it:
two leads a third apart, a galloping bass, a kick on every eighth, chords as fast arpeggios, down through D minor,
C and B flat. Bar 8 is the dominant with its raised third, and it leads back to the top.

The voices are the ones an eight-bit machine had: two pulse waves, a triangle with sixteen steps, and noise.
"""
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
import numpy as np
from backlot import sound as sd, score, ear
SR = sd.SR; E = 10.0 / 48                                   # one eighth note, in seconds
N = int(10 * SR)

def env(n, decay, attack=.002, release=.006):
    t = np.arange(n) / SR; e = np.exp(-decay * t) * np.minimum(1, t / attack); r = int(release * SR)
    if n > r: e[-r:] *= np.linspace(1, 0, r)
    return e
def pulse(note, dur, duty=.25, decay=4.0, vib=0.0):
    n = int(dur * SR); t = np.arange(n) / SR; f = score.hz(note) * (1 + vib * .006 * np.sin(2 * np.pi * 5.5 * t))
    ph = np.cumsum(f) / SR; return np.where(ph % 1 < duty, 1.0, -1.0) * env(n, decay)
def tri(note, dur, decay=1.5):
    n = int(dur * SR); ph = score.hz(note) * np.arange(n) / SR
    w = 2 * np.abs(2 * (ph % 1) - 1) - 1; return np.round(w * 7.5) / 7.5 * env(n, decay)       # sixteen levels, as the old chip had
def noise(dur, rate, decay, seed):
    n = int(dur * SR); r = np.random.default_rng(seed); hold = max(1, int(SR / rate))
    return np.repeat(r.uniform(-1, 1, n // hold + 1), hold)[:n] * env(n, decay, attack=.0005)

L = np.zeros(N + SR); R = np.zeros(N + SR)
def put(x, eighth, gain=1.0, pan=0.0):
    i = int(round(eighth * E * SR)); L[i:i + len(x)] += x * gain * (1 - max(pan, 0)); R[i:i + len(x)] += x * gain * (1 + min(pan, 0))

JIG = ['A4 D5 D5 F5 D5 D5', 'A4 D5 D5 G5 F5 E5', 'A4 D5 D5 F5 D5 F5']
for b, bar in enumerate(JIG):                               # bars 1-3: the whistle, the drone, the drum
    for k, nt in enumerate(bar.split()):
        put(pulse(nt, E * .92, .25, 5.0, vib=1.0), b * 6 + k, .30 if k in (0, 3) else .24)
    put(tri('D2', E * 3, .8), b * 6, .36); put(tri('A2', E * 3, .8), b * 6 + 3, .30)
    for k in range(6): put(noise(.06, 900 if k in (0, 3) else 2600, 60 if k in (0, 3) else 110, b * 6 + k), b * 6 + k, .30 if k in (0, 3) else .10)
put(pulse('A6', .05, .5, 30), 6, .16); put(pulse('D7', .09, .5, 22), 6.25, .16)                  # bar 2: the dialog arrives
for nt, g in (('D4', .26), ('A4', .22), ('D5', .22), ('A5', .26)): put(pulse(nt, E * 2.6, .25, 2.2), 18, g, 0.0)      # bar 4: the button
put(tri('D2', E * 2.6, 1.2), 18, .6); put(noise(.9, 9000, 5.5, 99), 18, .26); put(noise(.03, 3000, 150, 98), 18, .3)
for k, nt in enumerate(('D4', 'F4', 'A4')): put(pulse(nt, E * .9, .125, 6.0), 21 + k, .16 + .05 * k)                  # ...and a run up into it
METAL = [('D5 F5 A5 D6 A5 F5', 'F5 A5 D6 F6 D6 A5', 'D2', 'D4 F4 A4'), ('C5 E5 G5 C6 G5 E5', 'E5 G5 C6 E6 C6 G5', 'C2', 'C4 E4 G4'), ('A#4 D5 F5 A#5 F5 D5', 'D5 F5 A#5 D6 A#5 F5', 'A#1', 'A#3 D4 F4')]
for b, (lead, harm, bass, chord) in enumerate(METAL, start=4):                                   # bars 5-7: the conversion
    for k, (a, h) in enumerate(zip(lead.split(), harm.split())):
        put(pulse(a, E * .95, .25, 3.0, vib=1.0), b * 6 + k, .26, -.25); put(pulse(h, E * .95, .125, 3.0, vib=1.0), b * 6 + k, .19, .35)
        put(tri(bass, E * .9, 3.0), b * 6 + k, .38)
        put(noise(.05, 700, 70, b * 6 + k), b * 6 + k, .22)                                       # a kick on every eighth
        if k == 3: put(noise(.12, 5000, 28, 50 + b), b * 6 + k, .30)                              # and the snare where a jig leans
    ch = chord.split()
    for j in range(24): put(pulse(ch[j % 3], E / 4 * .95, .5, 8.0), b * 6 + j / 4, .075, -.5 if j % 2 else .5)        # a choir, the way a chip sings one
put(pulse('A6', .05, .5, 30), 36, .16); put(pulse('D7', .09, .5, 22), 36.25, .16)                # bar 7: the report arrives
for nt, g in (('A3', .24), ('C#4', .2), ('E4', .2), ('A4', .24), ('C#5', .18)): put(pulse(nt, E * 2.7, .25, 2.4), 42, g)   # bar 8: OK. The dominant, third raised
put(tri('A1', E * 2.7, 1.2), 42, .6); put(noise(.7, 9000, 6.5, 97), 42, .22); put(pulse('E7', .07, .5, 25), 42, .14)
for k, nt in enumerate(('E5', 'C#5', 'A4')):                                                     # and back round
    put(pulse(nt, E * .9, .25, 6.0), 45 + k, .24); put(noise(.07, 4000, 45, 60 + k), 45 + k, .2 + .04 * k)
put(tri('A2', E * 3, 1.0), 45, .45)

x = np.c_[L[:N], R[:N]]; x[:200] *= np.linspace(0, 1, 200)[:, None]; x[-400:] *= np.linspace(1, 0, 400)[:, None]
x = sd.master(x, target_lufs=-14.0, ceiling=-1.0)
out = HERE / 'stage1'; wav = Path('out/hex'); wav.mkdir(parents=True, exist_ok=True)
sd.write_wav(wav / 'gate_exe.wav', x); m = ear.measure(x)
print({k: (round(v, 2) if isinstance(v, float) else v) for k, v in m.items() if not hasattr(v, '__len__')})
ear.report(str(wav / 'gate_exe.wav'), str(out / 'fig2_gate_exe_tune.jpg'), title='GATE.EXE: eight bars of 6/8, two pulses, a triangle and noise')
sd.encode(str(wav / 'gate_exe.wav'), str(out / 'fig2_gate_exe.mp3'))
if (out / 'fig2_gate_exe_silent.mp4').exists():
    sd.mux(str(out / 'fig2_gate_exe_silent.mp4'), str(wav / 'gate_exe.wav'), str(out / 'fig2_gate_exe.mp4'), loop_video=False, crf=14)
    print('sound is on', out / 'fig2_gate_exe.mp4')
