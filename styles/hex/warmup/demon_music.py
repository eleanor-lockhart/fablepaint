"""Warmup 4: Demon.exe — the score (written before the picture).

28.0 seconds, 14 bars of 4/4 at 120 BPM (1 beat = 0.5 s = 12 frames; 1 bar = 2.0 s = 48 frames).
Synthesised through `styles/hex/voices.py`:
  Bar 1       (0–2 s)    Equilibrium: cold machine drone + chaotic molecular ticks
  Bars 2–5    (2–10 s)   Phrase A (D Dorian, whistle + harp + bodhran): slots 0..7 sorted on beats 2 & 4
  Bars 6–9    (10–18 s)  Phrase B (fiddle in thirds + bass): slots 8..F sorted on beats 2 & 4
  Bar 10      (18–20 s)   +20 C reached: F major chord & bell as the shelter window lights in register F
  Bar 11      (20–22 s)  SECOND_LAW.SYS interrupts: system alert ding + bare machine hum; cursor clicks
  Bars 12–14  (22–28 s)  WITCH.EXE ("I DO NOT FORGET THINGS."): twin symphonic-metal leads over D - Bb - C - D

    uv run python styles/hex/warmup/demon_music.py
"""
import sys, json
from pathlib import Path
HERE = Path(__file__).resolve().parent; HEX = HERE.parent; ROOT = HERE.parents[2]
sys.path.insert(0, str(HEX)); sys.path.insert(1, str(ROOT))
import numpy as np
import voices as V
from backlot import sound as sd, ear

SECONDS = 28.0
BEAT = 0.5
BAR = 2.0
OUT = ROOT / 'out' / 'hex' / 'demon'

# 16 gate sorts (slots 0..F) on beats 2 and 4 of Bars 2..9, plus 3 post-decree sorts in Bars 12..13
SORT_TIMES = [2.0 + b * BAR + off for b in range(8) for off in (0.5, 1.5)]     # 2.5, 3.5, ..., 17.5 (16 sorts)
EXTRA_SORTS = [23.0, 24.0, 25.0]


def build_score():
    OUT.mkdir(parents=True, exist_ok=True)
    V.new_mix(SECONDS)

    # Bar 1 (0.0 - 2.0 s): Equilibrium — cold machine hum on D2/A2 + unpitched molecular wall bounces
    V.put(V.pad([V.midi('D2'), V.midi('A2')], 2.1, kind='organ', a=.08, r=.3), 0.0, gain=.22, wet=.3)
    rng = np.random.default_rng(1867)
    for k in range(11):
        V.put(V.click(), 0.12 + k * 0.17, gain=.18, pan=float(rng.uniform(-.6, .6)))

    # Bars 2–5 (2.0 - 10.0 s): Phrase A — D Dorian melody over Dm - C - G - A
    prog_a = [
        ('D2', ['D4', 'F4', 'A4'], [('D5', .5), ('E5', .5), ('F5', .5), ('A5', .5)]),
        ('C2', ['C4', 'E4', 'G4'], [('G5', .5), ('F5', .5), ('E5', .5), ('C5', .5)]),
        ('G2', ['G3', 'B3', 'D4'], [('D5', .5), ('E5', .5), ('F5', .5), ('G5', .5)]),
        ('A2', ['A3', 'C#4', 'E4'], [('E5', .75), ('D5', .25), ('C#5', .5), ('A4', .5)]),
    ]
    for b, (bs, ch, mel) in enumerate(prog_a):
        t0 = 2.0 + b * BAR
        V.put(V.bass(V.midi(bs), 0.95), t0, gain=.28)
        V.put(V.bass(V.midi(bs), 0.95), t0 + 1.0, gain=.24)
        V.put(V.pad([V.midi(n) for n in ch], 1.95, kind='strings', a=.10, r=.25), t0, gain=.14, wet=.45)
        for beat_i in range(4):
            V.put(V.bodhran(beat_i in (0, 2)), t0 + beat_i * BEAT, gain=.26 if beat_i in (0, 2) else .16)
        tc = t0
        for nt, dur in mel:
            V.put(V.whistle(V.midi(nt), dur * .94, cut=V.midi(nt) + 2), tc, gain=.26, pan=-.15, wet=.35, ev=('whistle', V.midi(nt)))
            tc += dur

    # Bars 6–9 (10.0 - 18.0 s): Phrase B — Fiddle joins a third up, climbing toward +20 C over Dm - Bb - C - C7
    prog_b = [
        ('D2', ['D4', 'F4', 'A4'], [('A5', .5), ('G5', .5), ('F5', .5), ('E5', .5)]),
        ('A#1', ['A#3', 'D4', 'F4'], [('F5', .5), ('G5', .5), ('A5', .5), ('A#5', .5)]),
        ('C2', ['C4', 'E4', 'G4'], [('G5', .5), ('A5', .5), ('A#5', .5), ('C6', .5)]),
        ('C2', ['C4', 'E4', 'G4', 'A#4'], [('A5', .5), ('A#5', .5), ('C6', .5), ('E6', .5)]),
    ]
    for b, (bs, ch, mel) in enumerate(prog_b):
        t0 = 10.0 + b * BAR
        for q in range(4):
            V.put(V.bass(V.midi(bs), 0.46), t0 + q * BEAT, gain=.30 if q % 2 == 0 else .22)
            V.put(V.bodhran(q in (0, 2)), t0 + q * BEAT, gain=.28 if q in (0, 2) else .18)
            V.put(V.hat(), t0 + q * BEAT + 0.25, gain=.10)
        V.put(V.pad([V.midi(n) for n in ch], 1.95, kind='strings', a=.08, r=.22), t0, gain=.17, wet=.45)
        tc = t0
        for nt, dur in mel:
            m = V.midi(nt)
            V.put(V.whistle(m, dur * .94), tc, gain=.25, pan=-.22, wet=.35, ev=('whistle', m))
            V.put(V.fiddle(V.third(m, V.MINOR, up=False), dur * .92), tc, gain=.20, pan=.25, wet=.35, ev=('fiddle', m))
            tc += dur

    # Distinct plucked harp accent on every one of the 16 gate openings (slots 0..F) so gate & music lock
    arp_pitches = ['D5', 'A5', 'E5', 'G5', 'D5', 'A5', 'E5', 'A5',
                   'F5', 'A5', 'F5', 'A#5', 'G5', 'C6', 'A5', 'E6']
    for k, (ts, nt) in enumerate(zip(SORT_TIMES, arp_pitches)):
        V.put(V.harp(V.midi(nt), 0.55), ts, gain=.30, pan=.15 if k % 2 == 0 else -.15, wet=.35, ev=('gate', V.midi(nt)))
        V.put(V.tick(), ts, gain=.16)

    # Bar 10 (18.0 - 20.0 s): +20 C — Register F window lights! Warm F major chord + bell + harp cascade
    f_chord = ['F3', 'C4', 'F4', 'A4', 'C5']
    V.put(V.bass(V.midi('F2'), 1.95), 18.0, gain=.36)
    V.put(V.pad([V.midi(n) for n in f_chord], 1.95, kind='organ', a=.03, r=.35), 18.0, gain=.30, wet=.55)
    V.put(V.pad([V.midi(n) for n in f_chord], 1.95, kind='choir', a=.06, r=.35), 18.0, gain=.24, wet=.60)
    V.put(V.glass(V.midi('F5'), 1.9), 18.0, gain=.36, wet=.5, ev=('window_lit', V.midi('F5')))
    for i, nt in enumerate(('F4', 'A4', 'C5', 'F5', 'A5')):
        V.put(V.harp(V.midi(nt), 1.2), 18.0 + i * 0.08, gain=.24, wet=.45)

    # Bar 11 (20.0 - 22.0 s): SECOND_LAW.SYS — system alert ding + cold bare machine drone + two cursor hovers
    V.put(V.ding('sys'), 20.0, gain=.42, wet=.20, ev=('sys_dialog', 93))
    V.put(V.timp(V.midi('A2'), .7), 20.0, gain=.34)
    V.put(V.pad([V.midi('A1'), V.midi('E2')], 1.98, kind='organ', a=.02, r=.15), 20.0, gain=.20, wet=.15)
    V.put(V.click(), 20.75, gain=.30); V.put(V.tick(), 20.75, gain=.22)        # cursor reaches [FORGET]
    V.put(V.click(), 21.50, gain=.30); V.put(V.tick(), 21.50, gain=.22)        # cursor reaches [EQUALIZE]

    # Bars 12–14 (22.0 - 28.0 s): WITCH.EXE ("I DO NOT FORGET THINGS.") — her chime + symphonic metal triumph!
    V.put(V.ding('hers'), 22.0, gain=.40, wet=.45, ev=('witch_dialog', 50))
    V.put(V.crash(1.6), 22.0, gain=.26, wet=.40)
    metal_bars = [
        ('D2', ['D5', 'E5', 'F5', 'A5'], 22.0),
        ('A#1', ['A#4', 'D5', 'F5', 'A5'], 24.0),
    ]
    for bs, notes, t0 in metal_bars:
        V.put(V.guitar(V.midi(bs), 1.95, palm=False), t0, gain=.28, wet=.25)
        V.put(V.pad([V.midi(bs) + 12, V.midi(bs) + 19, V.midi(bs) + 24], 1.95, kind='choir', a=.05, r=.25), t0, gain=.22, wet=.50)
        for q, nt in enumerate(notes):
            tq = t0 + q * BEAT
            m = V.midi(nt)
            V.put(V.lead(m, 0.46), tq, gain=.25, pan=-.28, wet=.30, ev=('lead', m))
            V.put(V.lead(V.third(m, V.MINOR, up=True), 0.46), tq, gain=.20, pan=.28, wet=.30)
            V.put(V.bass(V.midi(bs), 0.44), tq, gain=.30)
            V.put(V.kick(), tq, gain=.30)
            if q in (1, 3):
                V.put(V.snare(), tq, gain=.28, wet=.25)
            V.put(V.hat(), tq + 0.25, gain=.12)

    for ts, nt in zip(EXTRA_SORTS, ('A5', 'D6', 'F6')):
        V.put(V.harp(V.midi(nt), 0.55), ts, gain=.32, wet=.35, ev=('extra_sort', V.midi(nt)))

    # Bar 14 (26.0 - 28.0 s): Final cadence C5 -> D5 power chord & sustained warm F-lit organ fifth
    V.put(V.guitar(V.midi('C2'), 0.48), 26.0, gain=.28)
    V.put(V.bass(V.midi('C2'), 0.48), 26.0, gain=.32); V.put(V.kick(), 26.0, gain=.32); V.put(V.snare(), 26.0, gain=.26)
    V.put(V.lead(V.midi('C6'), 0.46), 26.0, gain=.26, pan=-.25); V.put(V.lead(V.midi('E6'), 0.46), 26.0, gain=.20, pan=.25)

    V.put(V.crash(1.5), 26.5, gain=.24, wet=.45)
    V.put(V.guitar(V.midi('D2'), 1.40), 26.5, gain=.30, wet=.30)
    V.put(V.bass(V.midi('D2'), 1.40), 26.5, gain=.36); V.put(V.kick(), 26.5, gain=.35)
    V.put(V.lead(V.midi('D6'), 1.35), 26.5, gain=.28, pan=-.25, wet=.40)
    V.put(V.lead(V.midi('F6'), 1.35), 26.5, gain=.22, pan=.25, wet=.40)
    V.put(V.pad([V.midi('D3'), V.midi('A3'), V.midi('D4'), V.midi('F4')], 1.45, kind='organ', a=.02, r=.45), 26.5, gain=.26, wet=.55)

    ride = [(0.0, -3.0), (2.0, -1.0), (10.0, 0.0), (18.0, +1.2), (20.0, -4.0), (21.9, -4.0), (22.0, +1.8), (27.2, +1.0), (28.0, -8.0)]
    wav_path = OUT / 'demon.wav'
    samples = V.finish(ride, str(wav_path), target=-14.0)

    m = ear.measure(samples)
    print('ear.measure:', {k: (round(v, 2) if isinstance(v, float) else v) for k, v in m.items() if not hasattr(v, '__len__')})
    ear.report(str(wav_path), str(HERE / 'demon_score.jpg'),
               title='DEMON.EXE: 14 bars of 4/4 (120 BPM) — D Dorian jig, F major lamp, symphonic metal reprise')
    sd.encode(str(wav_path), str(HERE / 'demon_exe.mp3'))
    (OUT / 'events.json').write_text(json.dumps(V.EVENTS, indent=2))
    print('wrote', HERE / 'demon_exe.mp3', 'and', len(V.EVENTS), 'events')


if __name__ == '__main__':
    build_score()
