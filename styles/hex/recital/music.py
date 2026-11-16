"""SPACE OPERA (IN ONE ACT): the song. Ninety-six seconds in 4/4 at 120 to the minute; a bar is two seconds.

    uv run python styles/hex/recital/music.py     writes out/hex/recital.wav, recital.mp3, the listening-room sheet and events.json

The song is the piece; the picture is hung on events.json, the list of every note that was played and by whom.
So whoever is seen playing is playing.

  bar 0        the baton, four times
  1-4          the spider, on its web: a harp. The rats in the pit hold a fifth on their strings
  5-12         verse: the druid's whistle; a drum; from bar 9 the cowboy commits (fiddle, a third below) and the newt comes in on bass
  13-16        the faculty at the organ, the drones as a choir, the snare closing up
  17-24        chorus in D minor: the bloc's guitars, a kick on every sixteenth, everybody on the hook, which peaks in its last bar
  25-28        the organ alone, in sequences, with the band hitting the first beat of each bar
  29-32        a short verse, held back, and a bar that turns the corner
  33-40        the chorus again, a tone higher, because that is what is done
  41-44        three chords and a major one; she cuts it off on the third beat
  45-47        nothing; a click; one harmonic from the spider
"""
import sys, json
from pathlib import Path
HERE = Path(__file__).resolve().parent; sys.path.insert(0, str(HERE.parent))
import numpy as np
import voices as V
from voices import put, midi, third, MINOR
from backlot import sound as sd, ear
BAR, E, S = 2.0, .25, .125; BARS = 48
V.new_mix(BARS * BAR)
T = lambda bar, eighth=0.0: bar * BAR + eighth * E
CH = dict(Dm=(38, [50, 57, 62, 65]), C=(36, [48, 55, 60, 64]), Bb=(34, [46, 53, 58, 62]), A=(33, [45, 52, 57, 61]), F=(41, [53, 57, 60, 65]), B=(35, [47, 54, 59, 63]), Emaj=(40, [52, 59, 64, 68]))      # name -> (bass, voicing)

def line(bars, start, voice, name, gain, pan=0.0, wet=.3, shift=0, harm=None, cuts=False):
    """Eight tokens a bar (eighth notes): a note, '.' a rest, '-' holds the note before."""
    for b, s_ in enumerate(bars):
        tok = s_.split(); k = 0
        while k < 8:
            if tok[k] in '.-': k += 1; continue
            L = 1
            while k + L < 8 and tok[k + L] == '-': L += 1
            m = midi(tok[k]) + shift
            if harm: m = third(m, harm, False)
            x = voice(m, E * L * .95, cut=m + 2) if (cuts and k % 4 == 0) else voice(m, E * L * .95)
            put(x, T(start + b, k), gain * (1.1 if k % 4 == 0 else 1.0), pan, wet, ev=(name, m)); k += L

VERSE = ['D5 F5 A5 F5 G5 F5 E5 D5', 'C5 E5 G5 E5 F5 E5 D5 C5', 'A#4 D5 F5 D5 E5 D5 C5 A#4', 'A4 C#5 E5 A5 G5 E5 C#5 A4']
VERSE_END = 'A4 C#5 E5 G5 A5 - A5 -'
RISE = ['F5 - - - G5 - - -', 'G5 - - - C6 - - -', 'A5 - - - D6 - - -', 'E6 - - - C#6 - E6 -']
HOOK = ['A5 - - F5 D5 - F5 A5', 'A#5 - - A5 F5 - D5 F5', 'A5 - - C6 A5 - F5 A5', 'G5 - - E5 C5 - E5 G5', 'A5 - - F5 D5 - F5 A5', 'A#5 - - D6 A#5 - A5 A#5', 'C6 - - E6 C6 - D6 E6', 'E6 - - - C#6 - E6 -']
SEQ = [[62, 65, 69, 74], [67, 70, 74, 79], [60, 64, 67, 72], [65, 69, 72, 77], [70, 74, 77, 82], [64, 67, 70, 76], [69, 73, 76, 81], [62, 65, 69, 74]]      # the organ's sequence: D minor, G minor, C, F, B flat, E diminished, A, D minor

def arps(bar, name, gain=.2):
    root, vo = CH[name]
    for k, j in enumerate((0, 1, 2, 3, 2, 1, 3, 2)): put(V.harp(vo[j] + 12, 1.2), T(bar, k), gain * (1.15 if k % 4 == 0 else .9), -.45 + .12 * j, .45, ev=('harp', vo[j] + 12))

def chorus(start, tr, last=False):
    names = ['Dm', 'Bb', 'F', 'C', 'Dm', 'Bb', 'C', 'A']
    for j, nm in enumerate(names):
        b = start + j; root, vo = CH[nm]; root += tr; vo = [m + tr for m in vo]
        for k in range(8):
            acc = k in (0, 3, 6)                                                    # three, three, two
            put(V.guitar(root, E * (.95 if acc else .8), palm=not acc), T(b, k), .44 if acc else .36, ev=('guitar', root))
            put(V.bass(root, E * .9), T(b, k), .4, ev=('bass', root))
        for k in range(16): put(V.kick(), T(b) + k * S, .62 if k % 4 == 0 else .42, ev=('kick', 36) if k % 2 == 0 else None)
        for k in (2, 6): put(V.snare(), T(b, k), .62, 0, .15, ev=('snare', 38))
        if j % 2 == 0 or (last and j >= 4): put(V.crash(), T(b), .32, 0, .4, ev=('crash', 49))
        put(V.pad([m + 12 for m in vo[1:]] + ([m + 24 for m in vo[1:3]] if (last and j >= 4) else []), BAR * 1.01, 'choir', .05, .1), T(b), .27, 0, .5, ev=('choir', vo[3] + 12))
        put(V.pad(vo, BAR * 1.01, 'organ', .03, .08), T(b), .09, 0, .4, ev=('organ', vo[0]))
        put(V.pad([vo[0], vo[2], vo[3] + 12], BAR * 1.01, 'strings', .04, .1, trem=.6), T(b), .15, 0, .4, ev=('rats', vo[0]))
    line(HOOK, start, V.lead, 'lead', .32, -.3, .3, shift=tr - 12)
    line(HOOK, start, V.whistle, 'whistle', .38, .1, .4, shift=tr, cuts=True)
    line(HOOK, start, V.fiddle, 'fiddle', .26, .4, .3, shift=tr, harm=[(p + tr) % 12 for p in MINOR])

# bar 0: the baton
for k in range(4): put(V.tick(), T(0, 2 * k), .5, 0, .2, ev=('baton', 0))
# 1-4: the spider; the rats
put(V.pad([38, 45], 24.2, 'strings', 1.5, 2.0), T(1), .17, 0, .4, ev=('rats', 38))      # the pit: rats, bowing together
for b, nm in zip(range(1, 5), ('Dm', 'Bb', 'C', 'Dm')): arps(b, nm, .26)
# 5-12: the verse
line(VERSE + VERSE[:3] + [VERSE_END], 5, V.whistle, 'whistle', .42, -.1, .45, cuts=True)
line(VERSE[:3] + [VERSE_END], 9, V.fiddle, 'fiddle', .26, .35, .35, harm=MINOR)
for j, b in enumerate(range(5, 13)):
    nm = ('Dm', 'C', 'Bb', 'A')[j % 4]; arps(b, nm, .17)
    for k in range(8): put(V.bodhran(k % 4 == 0), T(b, k), .5 if k % 4 == 0 else .2, 0, .15, ev=('drum', 40))
    put(V.bodhran(False), T(b, 7.5), .18, 0, .15)
    if j >= 4:
        for k in range(0, 8, 2): put(V.bass(CH[nm][0], E * 1.8), T(b, k), .4, ev=('bass', CH[nm][0]))
put(V.bodhran(True), T(5), 1.0, 0, .2); put(V.click(), T(5), .4); put(V.kick(), T(9), .8); put(V.click(), T(9), .4)      # each entrance gets a downbeat you can hear
# 13-16: organ, choir, the snare closing up
line(RISE, 13, lambda m, d, **kw: V.pad([m, m - 5], d, 'choir', .06, .12), 'choir', .3, 0, .5); line(RISE, 13, V.whistle, 'whistle', .3, -.1, .45)
for j, b in enumerate(range(13, 17)):
    nm = ('Bb', 'C', 'Bb', 'A')[j]; root, vo = CH[nm]
    for k in range(8): put(V.pad([vo[0] + 12, vo[2] + 12], .16, 'organ', .01, .05), T(b, k), .2 + .03 * j, 0, .3, ev=('organ', vo[0] + 12)); put(V.bass(root, E * .9), T(b, k), .36 + .02 * j, ev=('bass', root))
    for k in range(0, 8, 2): put(V.kick(), T(b, k), .7, ev=('kick', 36))
    hits = [0, 2, 4, 6] if j < 2 else list(range(8)) if j == 2 else [x / 2 for x in range(16)]
    for q, k in enumerate(hits): put(V.snare(), T(b, k), (.22 + .09 * j) * (.7 + .3 * q / max(len(hits) - 1, 1)), 0, .15, ev=('snare', 38) if k == int(k) else None)
    if j >= 2: put(V.guitar(root, BAR * .98), T(b), .3 + .12 * (j - 2), 0, .2, ev=('guitar', root))
# 17-24: the chorus
chorus(17, 0)
# 25-28: the organ alone; the band on the first beat of each bar
for h, tri in enumerate(SEQ):
    t0 = T(25) + h * 1.0
    for k, j in enumerate((0, 1, 2, 3, 2, 1, 2, 3)): put(V.pad([tri[j]], .14, 'organ', .005, .04), t0 + k * S, .5, .2 * (-1) ** k, .45, ev=('organ', tri[j]))
    put(V.pad([tri[0] - 24], .95, 'organ', .01, .08), t0, .42, 0, .4)
for j, nm in enumerate(('Dm', 'C', 'Bb', 'A')):
    root = CH[nm][0]; b = 25 + j
    put(V.guitar(root, .45), T(b), .5, 0, .25, ev=('guitar', root)); put(V.bass(root, .45), T(b), .45, ev=('bass', root)); put(V.kick(), T(b), .9, ev=('kick', 36)); put(V.crash(.7), T(b), .26, 0, .4, ev=('crash', 49))
for k in range(8): put(V.snare(), T(28, 4) + k * S, .3 + .05 * k, 0, .15, ev=('snare', 38) if k % 2 == 0 else None)
# 29-32: a short verse, held back
line(VERSE[:3], 29, V.whistle, 'whistle', .4, -.1, .45, cuts=True); line(VERSE[:3], 29, V.fiddle, 'fiddle', .26, .35, .35, harm=MINOR)
line(['A4 C#5 E5 A5 . . . .'], 32, V.whistle, 'whistle', .4, -.1, .45); line(['. . . . B4 C#5 D#5 F#5'], 32, V.lead, 'lead', .34, -.2, .3)
for j, b in enumerate(range(29, 33)):
    nm = ('Dm', 'C', 'Bb', 'A')[j]; root = CH[nm][0]; arps(b, nm, .15)
    half = (j == 3)
    for k in range(4 if half else 8):
        put(V.guitar(root, E * .8, palm=True), T(b, k), .34, ev=('guitar', root)); put(V.bass(root, E * .9), T(b, k), .38, ev=('bass', root)); put(V.hat(), T(b, k), .2, .3)
    put(V.kick(), T(b, 0), .8, ev=('kick', 36)); put(V.kick(), T(b, 3), .6, ev=('kick', 36))
    if not half: put(V.snare(), T(b, 4), .55, 0, .15, ev=('snare', 38))
put(V.guitar(CH['B'][0], 1.0), T(32, 4), .5, 0, .25, ev=('guitar', CH['B'][0])); put(V.bass(CH['B'][0], 1.0), T(32, 4), .45, ev=('bass', CH['B'][0]))      # the corner: the dominant of the new key
for k in range(8): put(V.snare(), T(32, 4) + k * S, .3 + .06 * k, 0, .15, ev=('snare', 38) if k % 2 == 0 else None)
# 33-40: again, a tone higher
chorus(33, 2, last=True)
# 41-44: three chords and a major one
for j, nm in enumerate(('Dm', 'Bb', 'C', 'Emaj')):
    b = 41 + j; root, vo = CH[nm]; tr = 0 if nm == 'Emaj' else 2; root += tr; vo = [m + tr for m in vo]; d = 1.0 if j == 3 else 1.9
    put(V.guitar(root, d), T(b), .52, 0, .25, ev=('guitar', root)); put(V.bass(root, d), T(b), .45, ev=('bass', root)); put(V.kick(), T(b), .95, ev=('kick', 36)); put(V.crash(.95 if j == 3 else 1.4), T(b), .36, 0, .4, ev=('crash', 49))
    put(V.pad([m + 12 for m in vo] + ([m + 24 for m in vo[1:]] if j == 3 else []), d, 'choir', .03, .06), T(b), .3, 0, .5, ev=('choir', vo[3] + 12)); put(V.pad(vo, d, 'organ', .02, .05), T(b), .14, 0, .4, ev=('organ', vo[0]))
    put(V.timp(root if root > 36 else root + 12, min(d, .9)), T(b), .6, 0, .3)
    if j == 2:
        for k in range(16): put(V.snare(), T(b) + k * S, .2 + .03 * k, 0, .15, ev=('snare', 38) if k % 2 == 0 else None)
    if j == 3: put(V.whistle(88, .95), T(b), .4, -.1, .45, ev=('whistle', 88)); put(V.lead(76, .95), T(b), .32, -.3, .3, ev=('lead', 76)); put(V.fiddle(83, .95), T(b), .28, .4, .3, ev=('fiddle', 83))
# 45-47: nothing; a dialog; a click; and the spider, once
put(V.ding('sys'), T(45), .4, 0, .4, ev=('ui', 0)); put(V.click(), T(45), .5); put(V.click(), T(46), .6, ev=('ui', 1))
put(V.harp(76, 2.4), T(46, 4), .4, -.3, .6); put(V.glass(88, 2.4), T(46, 4), .34, -.3, .6, ev=('harp', 88)); put(V.glass(83, 2.4), T(46, 4) + .03, .16, -.3, .6)

ride = [(0, -2), (2, -4), (10, -6), (18, -5), (26, -4), (32, -2), (34, .5), (50, .5), (50.05, 0), (58, 0), (58.05, -5), (65, -3), (66, 1.5), (82, 2), (89, 2), (89.6, -3), (96, -3)]
out = Path('out/hex'); out.mkdir(parents=True, exist_ok=True)
x = V.finish(ride, out / 'recital.wav')
json.dump(dict(bar=BAR, bars=BARS, events=sorted(V.EVENTS)), open(HERE / 'events.json', 'w'), separators=(',', ':'))
m = ear.measure(x); print({k: round(v, 2) for k, v in m.items() if isinstance(v, float)}); print(len(V.EVENTS), 'events;', sorted({e[2] for e in V.EVENTS}))
for name, a, b in (('count-in', 0, 1), ('spider', 1, 5), ('verse', 5, 13), ('rise', 13, 17), ('chorus', 17, 25), ('organ', 25, 29), ('verse 2', 29, 33), ('chorus 2', 33, 41), ('ending', 41, 45), ('after', 45, 48)):
    seg = x[int(a * BAR * V.SR):int(b * BAR * V.SR)]; print(f'  {name:<10} rms {20 * np.log10(np.sqrt(np.mean(seg ** 2)) + 1e-9):6.1f} dB')
ear.report(str(out / 'recital.wav'), str(HERE / 'recital_score.jpg'), title='SPACE OPERA (IN ONE ACT): 48 bars of 4/4, two seconds a bar')
sd.encode(str(out / 'recital.wav'), str(HERE / 'recital.mp3'))
