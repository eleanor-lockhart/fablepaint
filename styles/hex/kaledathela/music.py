"""Kaledathela concept film score: *Shuttered Lamp* (written before the picture).

32.0 seconds, 16 bars of 4/4 at 120 BPM (1 beat = 0.5 s = 12 frames; 1 bar = 2.0 s = 48 frames).
Synthesised strictly from `styles/hex/voices.py` + `backlot.sound` primitives:
  Bars 1–4   (0–8 s)    West Texas Waste: D Phrygian lonely plucked motif + wind sub + pumpjack clanks (2s, 6s) + Worm transit (4s)
  Bars 5–8   (8–16 s)   East Texas Bayou: Liturgical pipe organ cluster + 60 Hz refinery hum + Pastoral sonar pings (10s, 12s, 14s)
  Bars 9–12  (16–24 s)  Under the Worm-Rib: Warm F-major/D-Dorian harp & whistle (16s); proximity warning at 18s;
                        iron shutter CLACK at 20.0 s cuts all warmth to muffled overhead organ + quiet heartbeat!
  Bars 13–16 (24–32 s)  After He Passes: Patrol recedes (24s); shutter re-opens on warm F major at 26.0 s;
                        Celtic-metal twin leads + whistle/fiddle swell at 28.0 s & 30.0 s as the green ward lights.

    uv run python styles/hex/kaledathela/music.py
"""
import sys, json
from pathlib import Path
HERE = Path(__file__).resolve().parent; HEX = HERE.parent; ROOT = HERE.parents[2]
sys.path.insert(0, str(HEX)); sys.path.insert(1, str(ROOT))
import numpy as np
import voices as V
from backlot import sound as sd, ear

SECONDS = 32.0
BEAT = 0.5
BAR = 2.0
OUT = ROOT / 'out' / 'hex' / 'kaledathela'

POINTS = [
    (2.0,  'pumpjack stroke 1 + valve release'),
    (4.0,  'Worm-Border subspace transit'),
    (6.0,  'pumpjack stroke 2 + checkpoint'),
    (8.0,  'cut: East Bayou + Pastor overpass'),
    (10.0, 'Pastoral scan 01 (left drone)'),
    (12.0, 'Pastoral scan 02 (right drone)'),
    (14.0, 'Overpass cross lock -> West'),
    (16.0, 'cut: Sunken Worm-rib shelter (0xF lit)'),
    (18.0, 'proximity alert: searchlight overhead'),
    (20.0, 'Runner shutters the 0xF lamp (darkness)'),
    (24.0, 'cut: Exterior Worm-rib (patrol recedes)'),
    (26.0, 'shutter re-opens (0xF glow returns)'),
    (28.0, 'Signal keys green hex-ward on Worm-rib'),
    (30.0, 'final D5 Coven chord'),
]


def clank(dur=0.28):
    """Heavy cast-iron pumpjack / iron-shutter clank: inharmonic metallic partials + low body thud."""
    n = int(dur * V.SR); t = np.arange(n) / V.SR
    metal = (np.sin(2 * np.pi * 412 * t) * np.exp(-t * 28)
             + 0.7 * np.sin(2 * np.pi * 688 * t) * np.exp(-t * 36)
             + 0.5 * np.sin(2 * np.pi * 1190 * t) * np.exp(-t * 48)
             + 0.6 * V.bp(V.nz(n), 800, 3800) * np.exp(-t * 55))
    thud = np.sin(2 * np.pi * (92 * t + 60 / 30 * (1 - np.exp(-30 * t)))) * np.exp(-t * 18)
    return (0.65 * metal + 0.75 * thud) * V.env(n, .001, .02)


def desert_wind(dur):
    """Low West Texas alkali wind + distant pipeline hum (strictly continuous, no random clicks)."""
    n = int(dur * V.SR); t = np.arange(n) / V.SR
    swell = 0.55 + 0.45 * np.sin(2 * np.pi * 0.18 * t)
    return (V.bp(V.nz(n), 110, 460) * 0.45 * swell + 0.18 * np.sin(2 * np.pi * 55.0 * t)) * V.env(n, .25, .35)


def scan_ping(f0=1320.0, dur=0.55):
    """Cold technological Inquisition sonar/telemetry ping."""
    n = int(dur * V.SR); t = np.arange(n) / V.SR
    return (np.sin(2 * np.pi * f0 * t) * np.exp(-t * 7.5)
            + 0.45 * np.sin(2 * np.pi * (f0 * 1.5) * t) * np.exp(-t * 12.0)
            + 0.25 * V.hp(V.nz(n), 4500) * np.exp(-t * 60.0)) * V.env(n, .001, .04)


def build_score():
    OUT.mkdir(parents=True, exist_ok=True)
    V.new_mix(SECONDS)

    # ==================================================================
    # SHOT 1 (0.0 - 8.0 s, Bars 1-4): WEST TEXAS WASTE & WORM BORDER
    # ==================================================================
    V.put(desert_wind(7.95), 0.0, gain=.24, wet=.35)
    V.put(V.bass(V.midi('D1'), 1.9), 0.0, gain=.26)
    # Sparse Texas-gothic acoustic plucked motif (D Phrygian: D - A - Bb - Eb - D)
    west_notes = [
        (0.0, 'D3', 1.2), (0.5, 'A3', 0.9), (1.0, 'D4', 0.9), (1.5, 'D#4', 0.8),
        (2.5, 'D4', 0.9), (3.0, 'A3', 0.9), (3.5, 'F3', 0.8),
        (4.5, 'A#3', 0.9), (5.0, 'A3', 0.9), (5.5, 'D#3', 0.8),
        (6.5, 'F3', 0.9), (7.0, 'E3', 0.7), (7.5, 'D3', 0.6),
    ]
    for ts, nt, dur in west_notes:
        V.put(V.harp(V.midi(nt), dur), ts, gain=.24, pan=-.18, wet=.45, ev=('west_pluck', V.midi(nt)))

    # Sync 2.0 s: Pumpjack bottom-stroke 1 + valve hiss
    V.put(clank(0.32), 2.0, gain=.48, pan=-.30, wet=.25, ev=('pumpjack_1', 38))
    V.put(V.timp(V.midi('D2'), 0.65), 2.0, gain=.34, pan=-.25)

    # Sync 4.0 s: Worm-Border subspace transit spark overhead! Crystalline glass + high harmonic
    V.put(V.glass(V.midi('C6'), 1.8), 4.0, gain=.42, pan=.20, wet=.60, ev=('worm_transit', V.midi('C6')))
    V.put(V.glass(V.midi('G6'), 1.4), 4.0, gain=.28, pan=.30, wet=.60)
    V.put(V.bass(V.midi('C2'), 1.4), 4.0, gain=.32)
    V.put(V.click(), 4.0, gain=.26)

    # Sync 6.0 s: Pumpjack bottom-stroke 2 + convoy checkpoint beacon
    V.put(clank(0.32), 6.0, gain=.48, pan=-.30, wet=.25, ev=('pumpjack_2', 38))
    V.put(V.timp(V.midi('A1'), 0.75), 6.0, gain=.36)
    V.put(scan_ping(988.0, 0.45), 6.0, gain=.22, pan=.15)

    # ==================================================================
    # SHOT 2 (8.0 - 16.0 s, Bars 5-8): EAST TEXAS BAYOU & THE PASTOR
    # ==================================================================
    # Sync 8.0 s: Hard cut to East Bayou — heavy liturgical pipe organ + 60 Hz refinery drone!
    V.put(V.timp(V.midi('D2'), 1.1), 8.0, gain=.46, ev=('cut_bayou', V.midi('D2')))
    V.put(V.crash(1.3), 8.0, gain=.22, wet=.40)
    pastor_chords = [
        (8.0,  ['D2', 'A2', 'D3', 'F3', 'G#3']),                               # D diminished/minor liturgical tension
        (12.0, ['A1', 'E2', 'A2', 'C#3', 'F3']),                               # Augmented inquisitorial dominant
    ]
    for t0, ch in pastor_chords:
        V.put(V.pad([V.midi(n) for n in ch], 3.92, kind='organ', a=.02, r=.25), t0, gain=.28, wet=.50)
        V.put(V.pad([V.midi(n) + 12 for n in ch[2:]], 3.85, kind='choir', a=.12, r=.30), t0, gain=.18, wet=.55)
    # Slow relentless march pulse on bars
    for b_t in (8.0, 9.0, 11.0, 13.0, 15.0):
        V.put(V.bass(V.midi('D2' if b_t < 12.0 else 'A1'), 0.75), b_t, gain=.28)

    # Sync 10.0 s: Drone 1 wide Pastoral scan
    V.put(scan_ping(1480.0, 0.60), 10.0, gain=.42, pan=-.35, wet=.35, ev=('scan_1', 90))
    V.put(V.timp(V.midi('G#2'), 0.65), 10.0, gain=.32)

    # Sync 12.0 s: Drone 2 wide Pastoral scan + chord change
    V.put(scan_ping(1661.0, 0.60), 12.0, gain=.44, pan=.25, wet=.35, ev=('scan_2', 92))
    V.put(V.timp(V.midi('A2'), 0.75), 12.0, gain=.36)

    # Sync 14.0 s: Overpass cross telemetry lock -> moving West
    V.put(V.ding('sys'), 14.0, gain=.42, wet=.30, ev=('lock_west', 93))
    V.put(V.click(), 14.0, gain=.32)
    V.put(V.modem(404), 14.0, gain=.22, pan=.15)

    # ==================================================================
    # SHOT 3 (16.0 - 24.0 s, Bars 9-12): SUNKEN SHELTER — SHUTTERING THE LAMP
    # ==================================================================
    # Sync 16.0 s: Cut inside the Coven's warm 0xF shelter! Intimate Celtic harp + tender whistle
    V.put(V.bass(V.midi('F2'), 1.92), 16.0, gain=.32, ev=('cut_shelter', V.midi('F2')))
    V.put(V.pad([V.midi('F3'), V.midi('A3'), V.midi('C4'), V.midi('F4')], 1.92, kind='strings', a=.03, r=.18), 16.0, gain=.22, wet=.45)
    V.put(V.glass(V.midi('F5'), 1.6), 16.0, gain=.32, wet=.45)
    shelter_mel = [(16.0, 'A4', .5), (16.5, 'C5', .5), (17.0, 'D5', .5), (17.5, 'F5', .45)]
    for ts, nt, dur in shelter_mel:
        V.put(V.whistle(V.midi(nt), dur * .92, cut=V.midi(nt) + 2), ts, gain=.26, pan=-.12, wet=.35, ev=('shelter_whistle', V.midi(nt)))
        V.put(V.harp(V.midi(nt) - 12, dur * 1.1), ts, gain=.24, pan=.18, wet=.40)

    # Sync 18.0 s: PROXIMITY ALERT! White 0xA searchlight slices overhead! Sharp warning chime + tremolo strings
    V.put(scan_ping(1975.5, 0.55), 18.0, gain=.44, wet=.25, ev=('proximity_alert', 95))
    V.put(V.timp(V.midi('G#2'), 0.7), 18.0, gain=.38)
    V.put(V.pad([V.midi('G#3'), V.midi('D4'), V.midi('F4')], 1.94, kind='strings', a=.02, r=.08, trem=0.75), 18.0, gain=.24, wet=.30)
    for k in range(3):
        V.put(V.tick(), 18.5 + k * 0.5, gain=.24)

    # Sync 20.0 s: RUNNER SHUTTERS THE 0xF LAMP! Crisp iron clack + sudden hush!
    # Only muffled low Pastor pipe-organ passing outside + quiet low heartbeat bodhran in the dark (20.0 - 23.9 s)
    V.put(clank(0.22), 20.0, gain=.54, wet=.10, ev=('lamp_shuttered', 36))
    V.put(V.click(), 20.0, gain=.38)
    muffled_organ = V.lp(V.pad([V.midi('D2'), V.midi('A2'), V.midi('D#3')], 3.85, kind='organ', a=.18, r=.40)[:, 0], 420)
    V.put(muffled_organ, 20.08, gain=.26, wet=.20)
    for hb in (20.8, 21.05, 22.0, 22.25, 23.2, 23.45):
        V.put(V.bodhran(True), hb, gain=.16 if (hb * 10) % 5 == 0 else .11)

    # ==================================================================
    # SHOT 4 (24.0 - 32.0 s, Bars 13-16): AFTER HE PASSES — RE-LIGHTING & WARD
    # ==================================================================
    # Sync 24.0 s: Cut to Exterior Worm-rib night as patrol recedes into the distance
    V.put(V.timp(V.midi('D2'), 0.95), 24.0, gain=.40, ev=('cut_exterior', V.midi('D2')))
    V.put(V.harp(V.midi('D3'), 1.5), 24.0, gain=.30, wet=.45)
    V.put(V.harp(V.midi('A3'), 1.4), 24.5, gain=.24, wet=.45)
    V.put(desert_wind(1.95), 24.0, gain=.20, wet=.35)

    # Sync 26.0 s: SHUTTER RE-OPENS (0xF GLOW RETURNS)! Warm F major chord + bright bell + rising harp!
    f_warm = ['F3', 'C4', 'F4', 'A4', 'C5']
    V.put(V.bass(V.midi('F2'), 1.95), 26.0, gain=.38, ev=('lamp_reopened', V.midi('F2')))
    V.put(V.pad([V.midi(n) for n in f_warm], 1.95, kind='organ', a=.02, r=.30), 26.0, gain=.30, wet=.55)
    V.put(V.glass(V.midi('F5'), 1.9), 26.0, gain=.40, wet=.55)
    for i, nt in enumerate(('F4', 'A4', 'C5', 'F5', 'G5', 'A5')):
        V.put(V.harp(V.midi(nt), 1.1), 26.0 + i * 0.25, gain=.25, wet=.45)

    # Sync 28.0 s: SIGNAL KEYS THE GREEN HEX-WARD (0x6)! Celtic-metal twin leads + whistle/fiddle over Bb -> C -> D!
    V.put(V.ding('hers'), 28.0, gain=.38, wet=.45, ev=('ward_lit', 50))
    V.put(V.crash(1.5), 28.0, gain=.26, wet=.40)
    V.put(V.guitar(V.midi('A#1'), 0.96, palm=False), 28.0, gain=.28, wet=.25)
    V.put(V.guitar(V.midi('C2'), 0.96, palm=False), 29.0, gain=.28, wet=.25)
    coven_rise = [
        (28.0, 'A#1', 'D5'), (28.5, 'A#1', 'F5'),
        (29.0, 'C2',  'E5'), (29.5, 'C2',  'G5'),
    ]
    for tq, bs, nt in coven_rise:
        m = V.midi(nt)
        V.put(V.bass(V.midi(bs), 0.46), tq, gain=.32)
        V.put(V.kick(), tq, gain=.30)
        if tq in (28.5, 29.5):
            V.put(V.snare(), tq, gain=.26, wet=.25)
        V.put(V.lead(m, 0.46), tq, gain=.24, pan=-.28, wet=.35, ev=('coven_lead', m))
        V.put(V.lead(V.third(m, V.MINOR, up=True), 0.46), tq, gain=.19, pan=.28, wet=.35)
        V.put(V.whistle(m + 12, 0.45), tq, gain=.20, pan=-.12, wet=.40)
        V.put(V.fiddle(m, 0.45), tq, gain=.18, pan=.18, wet=.40)

    # Sync 30.0 s: Final resolute D5 Coven chord held warm to 32.0 s
    V.put(V.crash(1.7), 30.0, gain=.26, wet=.45, ev=('final_chord', V.midi('D5')))
    V.put(V.guitar(V.midi('D2'), 1.85, palm=False), 30.0, gain=.30, wet=.35)
    V.put(V.bass(V.midi('D2'), 1.85), 30.0, gain=.36)
    V.put(V.kick(), 30.0, gain=.36); V.put(V.snare(), 30.0, gain=.26, wet=.30)
    V.put(V.lead(V.midi('D5'), 1.80), 30.0, gain=.26, pan=-.26, wet=.45)
    V.put(V.lead(V.midi('A5'), 1.80), 30.0, gain=.22, pan=.26, wet=.45)
    V.put(V.whistle(V.midi('D6'), 1.75, cut=V.midi('E6')), 30.0, gain=.22, wet=.45)
    V.put(V.pad([V.midi('D3'), V.midi('A3'), V.midi('D4'), V.midi('F4')], 1.90, kind='organ', a=.02, r=.50), 30.0, gain=.26, wet=.55)

    ride = [
        (0.0, -2.5), (2.0, -1.5), (7.8, -1.0),
        (8.0, +0.5), (15.8, +0.5),
        (16.0, -0.5), (18.0, +0.5),
        (20.0, -2.0), (20.3, -5.5), (23.9, -5.5),                               # true hush while lamp is shuttered!
        (24.0, -2.0), (26.0, +0.8), (28.0, +2.0), (30.0, +2.2), (32.0, -6.0),
    ]
    wav_path = OUT / 'kaledathela.wav'
    samples = V.finish(ride, str(wav_path), target=-14.0)

    m = ear.measure(samples)
    print('ear.measure:', {k: (round(v, 2) if isinstance(v, float) else v) for k, v in m.items() if not hasattr(v, '__len__')})
    ear.report(str(wav_path), str(HERE / 'kaledathela_score.jpg'),
               title='KALEDATHELA (SHUTTERED LAMP): 16 bars at 120 BPM — West waste, Bayou organ, 20s shutter hush, Coven ward')
    sd.encode(str(wav_path), str(HERE / 'kaledathela_concept.mp3'))
    (OUT / 'events.json').write_text(json.dumps(V.EVENTS, indent=2))
    print('wrote', HERE / 'kaledathela_concept.mp3', 'and', len(V.EVENTS), 'events')


if __name__ == '__main__':
    build_score()
