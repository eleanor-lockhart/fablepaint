"""Score for *Reliquary Drop* (`raid_concept.mp4`) — Soft-R gothic combat & aftermath test (written before picture).

32.0 seconds, 16 bars of 4/4 at 120 BPM (1 beat = 0.5 s = 12 frames; 1 bar = 2.0 s = 48 frames).
Synthesised strictly via `styles/hex/voices.py` + custom ballistic/blade Foley primitives:
  Bars 1–4   (0–8 s)    Dropship Descent & Hard Breach: VTOL turbine roar, hydraulic slam (2s), charge arm (4s), breach boom (6s)
  Bars 5–8   (8–16 s)   The Colonnade Volley (*The Matrix*): D-Phrygian palm-muted chugs + gunfire bursts (8s),
                        Thorn struck (10s), Bullet-Time vacuum hush & tritone glass lattice (12s), Reversal kill (14s)
  Bars 9–12  (16–24 s)  Corridor of Knives (*The Raid*): Syncopated industrial/bodhran breakbeat (16s),
                        pillar-vault blade shing + hit-stop (18s), point-blank graze & wire-snare takedown (20s), broken retreat (22s)
  Bars 13–16 (24–32 s)  Rain & Kept Warmth: Percussion drops out; battered dropship lifts off in rain (24s);
                        warm 0xF sanctum opens over fallen sister (26s); mournful Celtic whistle memorial coda (30s).

    uv run python styles/hex/kaledathela/raid_music.py
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
OUT = ROOT / 'out' / 'hex' / 'raid'

RAID_POINTS = [
    (2.0,  'Dropship slams down + ramp opens'),
    (4.0,  'Breacher arms shaped charge on arch'),
    (6.0,  'Breach detonation! Squad enters'),
    (8.0,  'cut: Colonnade automatic volley + stone chips'),
    (10.0, 'Thorn struck! 0xD blood arc + 0x4 dim'),
    (12.0, 'Signal raises 0x6 Hex-Lattice (bullet-stop)'),
    (14.0, 'Lattice reversal! Point-Hunter downed'),
    (16.0, 'cut: Dark corridor — Bayou drops from rib'),
    (18.0, 'Pillar vault + 0x7 blade strike (Hunter 2)'),
    (20.0, 'Point-blank graze + wire-snare (Hunter 3)'),
    (22.0, 'Wounded Hunter 4 retreats through breach'),
    (24.0, 'cut: Rain courtyard — battered dropship lifts'),
    (26.0, '0xF sanctum opens over fallen sister'),
    (30.0, 'Bayou plants 0x7 memorial blade in rain'),
]


def gunshot(dur=0.14):
    """Sharp ballistic flechette/dish-rifle report: supersonic crack + chest punch + brass tick."""
    n = int(dur * V.SR); t = np.arange(n) / V.SR
    crack = V.bp(V.nz(n), 1100, 5200) * np.exp(-t * 48)
    punch = np.sin(2 * np.pi * (62 * t + 110 / 40 * (1 - np.exp(-40 * t)))) * np.exp(-t * 26)
    brass = np.sin(2 * np.pi * 6400 * t) * np.exp(-t * 95) * 0.25
    return (0.75 * crack + 0.85 * punch + brass) * V.env(n, .0006, .015)


def breach_boom(dur=1.15):
    """Shaped breaching charge detonation: white-hot transient + stone-shattering low sub rumble."""
    n = int(dur * V.SR); t = np.arange(n) / V.SR
    sub = np.sin(2 * np.pi * (38 * t + 85 / 18 * (1 - np.exp(-18 * t)))) * np.exp(-t * 3.8)
    debris = V.lp(V.nz(n), 1400) * np.exp(-t * 5.2) + 0.5 * V.bp(V.nz(n), 1800, 6000) * np.exp(-t * 14.0)
    return np.tanh((1.2 * sub + 0.9 * debris) * 1.6) * V.env(n, .001, .08)


def blade_shing(dur=0.38):
    """Calligraphic green-hex blade / wire-snare ring + flesh/armor impact thud."""
    n = int(dur * V.SR); t = np.arange(n) / V.SR
    ring = (np.sin(2 * np.pi * 2480 * t) * np.exp(-t * 9.0)
            + 0.6 * np.sin(2 * np.pi * 3710 * t) * np.exp(-t * 13.0)
            + 0.5 * V.hp(V.nz(n), 4200) * np.exp(-t * 42.0))
    impact = np.sin(2 * np.pi * (78 * t + 90 / 35 * (1 - np.exp(-35 * t)))) * np.exp(-t * 22.0)
    return (0.55 * ring + 0.85 * impact) * V.env(n, .0008, .03)


def vtol_rain(dur, turbine=1.0):
    """Continuous toxic rain + low VTOL turbine throb (smooth envelope, zero random pops)."""
    n = int(dur * V.SR); t = np.arange(n) / V.SR
    rain = V.bp(V.nz(n), 900, 4200) * 0.16
    turb = (0.35 * np.sin(2 * np.pi * 65.4 * t) + 0.22 * V.lp(V.saw(65.4, n), 240)) * (0.65 + 0.35 * np.sin(2 * np.pi * 7.5 * t))
    return (rain + turbine * turb) * V.env(n, .15, .25)


def clank_heavy(dur=0.30):
    n = int(dur * V.SR); t = np.arange(n) / V.SR
    m = (np.sin(2 * np.pi * 380 * t) * np.exp(-t * 24) + 0.7 * np.sin(2 * np.pi * 820 * t) * np.exp(-t * 34)
         + 0.6 * V.bp(V.nz(n), 700, 3400) * np.exp(-t * 45))
    th = np.sin(2 * np.pi * (52 * t + 70 / 28 * (1 - np.exp(-28 * t)))) * np.exp(-t * 16)
    return (0.6 * m + 0.85 * th) * V.env(n, .001, .02)


def build_score():
    OUT.mkdir(parents=True, exist_ok=True)
    V.new_mix(SECONDS)

    # ==================================================================
    # SHOT 1 (0–8 s): RELIQUARY DROPSHIP DESCENT & HARD BREACH
    # ==================================================================
    V.put(vtol_rain(7.95, turbine=0.9), 0.0, gain=.26, wet=.30)
    V.put(V.pad([V.midi('D2'), V.midi('A2'), V.midi('D#3')], 5.9, kind='organ', a=.15, r=.20), 0.0, gain=.20, wet=.45)

    # Sync 2.0 s: Dropship landing struts slam onto flooded stone + hydraulic ramp drops!
    V.put(clank_heavy(0.36), 2.0, gain=.54, wet=.25, ev=('dropship_land', 38))
    V.put(V.timp(V.midi('D2'), 0.85), 2.0, gain=.44)
    for step_t in (2.5, 2.75, 3.0, 3.25):
        V.put(V.bodhran(True), step_t, gain=.22)

    # Sync 4.0 s: Shaped thermite charge planted & armed on stone arch (rapid countdown ticks 4.5..5.75s)
    V.put(V.ding('sys'), 4.0, gain=.42, wet=.20, ev=('charge_armed', 93))
    V.put(V.click(), 4.0, gain=.35)
    for kt, dt_c in enumerate((4.5, 5.0, 5.25, 5.5, 5.625, 5.75, 5.875)):
        V.put(V.tick(), dt_c, gain=.22 + .02 * kt)

    # Sync 6.0 s: BREACH DETONATION! + Driving palm-muted D-Phrygian assault riff!
    V.put(breach_boom(1.2), 6.0, gain=.56, wet=.35, ev=('breach_boom', 26))
    V.put(V.crash(1.4), 6.0, gain=.28, wet=.40)
    for q in range(4):
        tq = 6.0 + q * BEAT
        V.put(V.guitar(V.midi('D2' if q < 3 else 'D#2'), 0.44, palm=True), tq, gain=.32)
        V.put(V.bass(V.midi('D2' if q < 3 else 'D#2'), 0.44), tq, gain=.34)
        V.put(V.kick(), tq, gain=.34)

    # ==================================================================
    # SHOT 2 (8–16 s): COLONNADE VOLLEY, CASUALTY & THE HEX-LATTICE
    # ==================================================================
    # Sync 8.0 s: Hard cut inside colonnade — automatic dish-rifle volley + D-Phrygian chugs!
    V.put(gunshot(), 8.0, gain=.52, pan=-.35, wet=.20, ev=('volley_start', 50))
    for gt in (8.16, 8.33, 8.50, 8.75, 9.0, 9.25, 9.50):
        V.put(gunshot(), gt, gain=.38, pan=-.30 if int(gt * 4) % 2 == 0 else -.15, wet=.20)
    for q in range(8):
        tq = 8.0 + q * BEAT
        nt_b = 'D2' if q % 4 < 2 else ('D#2' if q % 4 == 2 else 'C2')
        V.put(V.guitar(V.midi(nt_b), 0.45, palm=(q % 2 == 1)), tq, gain=.30, wet=.20)
        V.put(V.bass(V.midi(nt_b), 0.44), tq, gain=.34)
        V.put(V.kick(), tq, gain=.32)
        if q % 2 == 1:
            V.put(V.snare(), tq, gain=.28, wet=.25)

    # Sync 10.0 s: WITCH_THORN STRUCK! Heavy triple impact + tragic minor-ninth glass cry!
    V.put(gunshot(), 10.0, gain=.54, pan=-.20, ev=('thorn_hit', 62))
    V.put(blade_shing(0.28), 10.0, gain=.42, pan=.20)
    V.put(V.glass(V.midi('D#6'), 1.6), 10.0, gain=.38, pan=.25, wet=.55)
    V.put(V.timp(V.midi('G#1'), 0.9), 10.0, gain=.44)
    for gt in (10.75, 11.0, 11.25, 11.5):
        V.put(gunshot(), gt, gain=.36, pan=-.25, wet=.20)

    # Sync 12.0 s: BULLET-TIME HEX-LATTICE CATCH! Drums & guitars DROP OUT into eerie tritone shimmer!
    V.put(V.ding('hers'), 12.0, gain=.48, wet=.55, ev=('hex_lattice', 50))
    V.put(V.click(), 12.0, gain=.36)
    V.put(V.pad([V.midi('D4'), V.midi('G#4'), V.midi('A4'), V.midi('F5')], 1.92, kind='choir', a=.02, r=.15), 12.0, gain=.26, wet=.60)
    for sl_t in (12.12, 12.24, 12.36):
        V.put(V.glass(V.midi('A6'), 0.45), sl_t, gain=.20, wet=.50)

    # Sync 14.0 s: LATTICE REVERSAL! Slugs snap back -> Point-Hunter downed + lights shatter!
    V.put(blade_shing(0.42), 14.0, gain=.54, wet=.30, ev=('lattice_reversal', 62))
    V.put(V.crash(1.3), 14.0, gain=.30, wet=.40)
    V.put(V.guitar(V.midi('D2'), 1.90, palm=False), 14.0, gain=.32, wet=.30)
    V.put(V.bass(V.midi('D2'), 1.90), 14.0, gain=.38)
    V.put(V.kick(), 14.0, gain=.40); V.put(V.snare(), 14.5, gain=.30); V.put(V.kick(), 15.0, gain=.34); V.put(V.snare(), 15.5, gain=.32)

    # ==================================================================
    # SHOT 3 (16–24 s): CORRIDOR OF KNIVES (*THE RAID* CLOSE-QUARTERS)
    # ==================================================================
    # Sync 16.0 s: Cut to pitch-dark corridor — Bayou drops from Worm-rib! Fast syncopated breakbeat!
    V.put(clank_heavy(0.24), 16.0, gain=.48, ev=('cut_corridor', 38))
    V.put(V.timp(V.midi('D2'), 0.7), 16.0, gain=.42)
    for bar_k in range(3):                                                      # Bars 9..11 (16..22 s)
        bt0 = 16.0 + bar_k * BAR
        V.put(V.bass(V.midi('D2' if bar_k != 1 else 'F2'), 0.92), bt0, gain=.34)
        V.put(V.bass(V.midi('C2' if bar_k == 2 else 'D#2'), 0.92), bt0 + 1.0, gain=.32)
        for sub_b, acc in ((0.0, True), (0.375, False), (0.75, True), (1.0, False), (1.25, True), (1.5, True), (1.75, False)):
            V.put(V.bodhran(acc), bt0 + sub_b, gain=.28 if acc else .16)
        V.put(V.kick(), bt0, gain=.34); V.put(V.snare(), bt0 + 0.5, gain=.30)
        V.put(V.kick(), bt0 + 0.75, gain=.28); V.put(V.snare(), bt0 + 1.5, gain=.30)
        V.put(V.hat(), bt0 + 0.25, gain=.14); V.put(V.hat(), bt0 + 1.25, gain=.14)

    # Sync 18.0 s: Blind muzzle strobe + Bayou pillar-vault 0x7 blade sever!
    V.put(gunshot(), 17.85, gain=.26, pan=-.15)
    V.put(blade_shing(0.40), 18.0, gain=.56, pan=.15, wet=.25, ev=('bayou_slash', 74))
    V.put(V.lead(V.midi('F5'), 0.45), 18.0, gain=.26, pan=.20, wet=.30)
    V.put(V.lead(V.midi('D5'), 0.45), 18.5, gain=.24, pan=-.20, wet=.30)

    # Sync 20.0 s: Point-blank shot grazes Runner + green wire-snare & Signal lance finish Hunter #3!
    V.put(gunshot(), 20.0, gain=.50, pan=.20, ev=('wire_takedown', 69))
    V.put(blade_shing(0.42), 20.02, gain=.50, pan=-.20, wet=.30)
    V.put(V.lead(V.midi('A5'), 0.48), 20.0, gain=.28, pan=-.25, wet=.35)
    V.put(V.lead(V.midi('G#5'), 0.48), 20.5, gain=.25, pan=.25, wet=.35)

    # Sync 22.0 s: Wounded Hunter #4 stumbles out in retreat! Urgent retreat alarm + falling whine!
    V.put(V.ding('sys'), 22.0, gain=.46, wet=.25, ev=('hunter_retreat', 93))
    V.put(V.click(), 22.0, gain=.36)
    V.put(V.whine(), 22.05, gain=.26, pan=-.25)
    V.put(V.pad([V.midi('D2'), V.midi('A2')], 1.90, kind='organ', a=.05, r=.30), 22.0, gain=.24, wet=.40)

    # ==================================================================
    # SHOT 4 (24–32 s): POETIC AFTERMATH — RAIN, RETREAT & PIETÀ
    # ==================================================================
    # Sync 24.0 s: Cut to rain courtyard — percussion gone; smoking Reliquary Dropship lifts into toxic sky!
    V.put(V.timp(V.midi('D2'), 1.2), 24.0, gain=.44, ev=('cut_aftermath', V.midi('D2')))
    V.put(clank_heavy(0.26), 24.0, gain=.34, pan=-.30)
    V.put(vtol_rain(4.2, turbine=0.75), 24.0, gain=.24, pan=-.25, wet=.35)
    V.put(vtol_rain(4.0, turbine=0.0), 28.0, gain=.20, wet=.40)                 # pure quiet rain at the end

    # Sync 26.0 s: Inner sanctum 0xF shutter opens over fallen sister Thorn — warm F-major / D-minor elegy!
    elegy_ch = ['D3', 'A3', 'F4', 'A4', 'C5']
    V.put(V.bass(V.midi('D2'), 3.85), 26.0, gain=.34, ev=('sanctum_pieta', V.midi('D2')))
    V.put(V.pad([V.midi(n) for n in elegy_ch], 3.85, kind='strings', a=.04, r=.45), 26.0, gain=.26, wet=.60)
    V.put(V.glass(V.midi('F5'), 2.2), 26.0, gain=.38, wet=.55)
    for i, nt in enumerate(('D4', 'F4', 'A4', 'C5', 'F5')):
        V.put(V.harp(V.midi(nt), 1.5), 26.0 + i * 0.25, gain=.24, wet=.50)

    # Mournful Celtic whistle lament (27.5 .. 32.0 s)
    lament = [(27.5, 'A5', .75), (28.25, 'G5', .75), (29.0, 'F5', .5), (29.5, 'E5', .5)]
    for ts, nt, dur in lament:
        V.put(V.whistle(V.midi(nt), dur * .95, cut=V.midi(nt) + 2), ts, gain=.26, pan=.08, wet=.50, ev=('lament', V.midi(nt)))
        V.put(V.fiddle(V.midi(nt) - 12, dur * .94), ts, gain=.18, pan=-.18, wet=.50)

    # Sync 30.0 s: Bayou plants Thorn's 0x7 blade upright in the cracked stone — resonant bell + final D minor fifth!
    V.put(blade_shing(0.35), 30.0, gain=.42, wet=.45, ev=('memorial_blade', V.midi('D5')))
    V.put(V.glass(V.midi('D5'), 1.9), 30.0, gain=.36, wet=.60)
    V.put(V.whistle(V.midi('D5'), 1.85, cut=V.midi('F5')), 30.0, gain=.28, wet=.55)
    V.put(V.pad([V.midi('D2'), V.midi('A2'), V.midi('D3'), V.midi('F3'), V.midi('A3')], 1.92, kind='organ', a=.02, r=.60), 30.0, gain=.28, wet=.60)

    ride = [
        (0.0, -2.0), (2.0, -0.5), (5.9, -0.5),
        (6.0, +1.8), (11.9, +1.8),
        (12.0, -2.5), (13.9, -2.5),                                             # Bullet-time hush at 12..14s!
        (14.0, +2.0), (21.9, +1.8),
        (22.0, -0.5), (24.0, -2.0), (26.0, +0.2), (30.0, +0.5), (32.0, -6.5),
    ]
    wav_path = OUT / 'raid.wav'
    samples = V.finish(ride, str(wav_path), target=-14.0)

    m = ear.measure(samples)
    print('ear.measure:', {k: (round(v, 2) if isinstance(v, float) else v) for k, v in m.items() if not hasattr(v, '__len__')})
    ear.report(str(wav_path), str(HERE / 'raid_score.jpg'),
               title='RELIQUARY DROP: 16 bars at 120 BPM — VTOL breach, Matrix bullet-stop hush (12s), Raid breakbeat, whistle pieta')
    sd.encode(str(wav_path), str(HERE / 'raid_concept.mp3'))
    (OUT / 'events.json').write_text(json.dumps(V.EVENTS, indent=2))
    print('wrote', HERE / 'raid_concept.mp3', 'and', len(V.EVENTS), 'events')


if __name__ == '__main__':
    build_score()
