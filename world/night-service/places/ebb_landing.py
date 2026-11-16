"""Ebb Landing, Slip 3: the place, in metres. Everything drawn of it comes from this one model.

    uv run python world/night-service/places/ebb_landing.py drawings    plans, elevations, a section, the size sheet
    uv run python world/night-service/places/ebb_landing.py check       the same cameras through Blender, compared
    uv run python world/night-service/places/ebb_landing.py score       my guesses (studies/space/JOURNAL.md, entry 0) against the model

x is east, y is north, z is up from tonight's water. The Sound is to the west, the hills to the east, and the
shoreline is the line x = 0. The night is a real one: the small hours of Friday 20 November 2026 at 47.6 N,
122.5 W. The boat sails at 01:35 with a moon three-quarters lit standing 8.5 degrees above due west, and that
moon sets at 02:32.

The parts of a ferry slip (trestle, bridge seat, transfer span hung from towers, wingwalls, dolphins) follow the
Washington State Ferries Terminal Design Manual, chapters 600 to 650; the sizes are my estimates for a small old
cable-operated slip and are not taken from a drawing.
"""
import sys, math
from pathlib import Path
from datetime import datetime, timedelta
HERE = Path(__file__).resolve().parent; NS = HERE.parent
sys.path.insert(0, str(NS))
import numpy as np
from backlot import space as sp
import things

LAT, LON = 47.6, -122.5
SAILING = datetime(2026, 11, 20, 9, 35)          # 01:35 Pacific Standard Time, as UTC
def pst(h, m=0): return datetime(2026, 11, 20, h + 8, m)
DECK, RAIL = 5.0, 5.55                           # the trestle's deck and the railhead, above the water
NO4_AT, NO4_FACING = (-420.0, 260.0, 0.0), 218.0 # it stands in the Sound and looks down it, toward Tern Point
STATURE = 1.80                                   # metres for a figure of stature 1.0 on the rig
RED = '#b23b28'

def build(boat=True, no4=True, cable=True, eye=True):
    S = sp.Set('Ebb Landing', LAT, LON)
    S.face('water', [(-6000, -4000, 0), (400, -4000, 0), (400, 4000, 0), (-6000, 4000, 0)], kind='water')
    # ---- the land: a bench behind a sea wall, a hill in steps, and Ebb Creek cutting through it to the north
    for nm, y in (('south', (-700, 185)), ('north', (260, 800))):
        for k, (x, top) in enumerate((((0, 70), DECK), ((70, 150), 9), ((150, 260), 18), ((260, 380), 30))):
            S.box(f'land.{nm}{k}', x, y, (-3, top), kind='land')
    S.box('land.head', (380, 620), (-700, 800), (-3, 45), kind='land')
    S.face('tideflat', [(110, 185, .3), (380, 185, .3), (380, 260, .3), (110, 260, .3)], kind='land', colour='#0d131a')
    for k, (x, y, z, lit) in enumerate(((92, -46, 9, 1), (104, 28, 9, 1), (118, 112, 9, 0), (176, -92, 18, 1), (196, 52, 18, 1), (214, 140, 18, 1), (300, -30, 30, 1), (318, 96, 30, 0), (96, 300, 9, 1), (190, 330, 18, 1))):
        S.box(f'house{k}', (x, x + 9), (y, y + 7), (z, z + 3.2)); S.gable(f'house{k}.roof', (x, x + 9), (y, y + 7), z + 3.2, z + 5.2, along='x')
        S.face(f'house{k}.window', [(x - .02, y + 2.2, z + 1.3), (x - .02, y + 3.6, z + 1.3), (x - .02, y + 3.6, z + 2.4), (x - .02, y + 2.2, z + 2.4)], kind='light' if lit else 'wall', colour='#ffc070' if lit else '#05070a', emit=2.0 if lit else 0)
    # ---- the Shore Line: ballast, rails, the Board, and a timber trestle over the creek mouth
    for nm, y in (('south', (-700, 185)), ('north', (260, 800))): S.box(f'ballast.{nm}', (32, 38), y, (DECK, DECK + .4), kind='track')
    for k, x in enumerate((34.28, 35.72)): S.box(f'rail{k}', (x - .04, x + .04), (-700, 800), (DECK + .4, RAIL), kind='rail')
    S.box('creektrestle.deck', (32.6, 37.4), (185, 260), (DECK - .1, DECK + .4), kind='deck')
    for k in range(15):
        y = 187.5 + 5 * k
        for j, x in enumerate((33.2, 35.0, 36.8)): S.cylinder(f'creektrestle.pile{k}_{j}', (x, y), .18, -2, DECK - .1, n=6, kind='pile')
        S.tube(f'creektrestle.brace{k}', [(33.2, y, .8), (36.8, y, DECK - .5)], .09, n=4, kind='pile')
    S.tube('board.mast', [(39.5, -60, DECK), (39.5, -60, 10.6)], .09, kind='rail')
    S.box('board.head', (39.15, 39.85), (-60.2, -59.8), (9.2, 10.6), kind='wall')
    for side, y in (('s', -60.22), ('n', -59.78)):
        S.face(f'board.red.{side}', [(39.3, y, 10.0), (39.7, y, 10.0), (39.7, y, 10.4), (39.3, y, 10.4)], kind='light', colour='#ff3b28', emit=4.0)
    # ---- on the bench: the ticket office (the union's drawer is in it)
    S.box('office', (8, 16), (10, 18), (DECK, 8.2)); S.gable('office.roof', (8, 16), (10, 18), 8.2, 9.9, along='x')
    S.face('office.window.s', [(10.5, 9.98, 6.2), (12.2, 9.98, 6.2), (12.2, 9.98, 7.4), (10.5, 9.98, 7.4)], kind='light', colour='#ffb347', emit=2.5)
    S.face('office.window.w', [(7.98, 12.6, 6.2), (7.98, 15.4, 6.2), (7.98, 15.4, 7.4), (7.98, 12.6, 7.4)], kind='light', colour='#ffb347', emit=2.5)
    # ---- the trestle: ninety metres out, twelve wide, on bents of four piles every seven and a half metres
    S.box('trestle.deck', (-90, 0), (-6, 6), (DECK - .6, DECK), kind='deck')
    for k in range(1, 13):
        x = -7.5 * k + 3.0
        S.box(f'trestle.cap{k}', (x - .25, x + .25), (-6, 6), (DECK - 1.0, DECK - .6), kind='pile')
        for j, y in enumerate((-5.2, -1.75, 1.75, 5.2)): S.cylinder(f'trestle.pile{k}_{j}', (x, y), .2, -6, DECK - 1.0, n=8, kind='pile')
    for side, y in (('s', -5.9), ('n', 5.9)):
        gaps = [(-90, -70.3), (-59.7, 0)] if side == 's' else [(-90, 0)]          # the shed stands in the south rail
        for a, b in gaps:
            S.tube(f'trestle.rail.{side}{a}', [(a, y, DECK + 1.05), (b, y, DECK + 1.05)], .05, n=4, kind='rail')
            S.tube(f'trestle.midrail.{side}{a}', [(a, y, DECK + .55), (b, y, DECK + .55)], .035, n=4, kind='rail')
            for x in np.arange(a, b + .01, 3.75): S.box(f'trestle.post.{side}{x:.1f}', (x - .05, x + .05), (y - .05, y + .05), (DECK, DECK + 1.05), kind='rail')
    for x in (-15, -30, -45, -75):                                               # lamps nobody minds: dark
        S.tube(f'lamp{-x}', [(x, 5.6, DECK), (x, 5.6, 10.2), (x, 4.7, 10.5)], .07, n=5, kind='rail'); S.box(f'lamp{-x}.head', (x - .25, x + .25), (4.3, 4.9), (10.3, 10.55), kind='rail')
    S.box('shed', (-70, -60), (-6, -2.5), (DECK, 7.8)); S.gable('shed.roof', (-70, -60), (-6, -2.5), 7.8, 8.9, along='x')
    S.face('shed.window', [(-67.2, -2.48, 6.1), (-65.6, -2.48, 6.1), (-65.6, -2.48, 7.2), (-67.2, -2.48, 7.2)], kind='light', colour='#ffd08a', emit=3.0)
    S.face('shed.door', [(-63, -2.48, DECK), (-61.9, -2.48, DECK), (-61.9, -2.48, 7.1), (-63, -2.48, 7.1)], kind='wall', colour='#06080c')
    for y in (-5.6, 5.6): S.tube(f'chain.post{y}', [(-88, y, DECK), (-88, y, 6.1)], .08, n=5, kind='rail')
    S.tube('chain', [(-88, -5.6, 5.95), (-88, -2.8, 5.8), (-88, 0, 5.75), (-88, 2.8, 5.8), (-88, 5.6, 5.95)], .03, n=4, kind='rail')
    # ---- the transfer span, hung from two towers; the wingwalls; the dolphins
    S.hexa('span', [(-90, -3.5, 4.4), (-117, -3.5, 2.4), (-117, 3.5, 2.4), (-90, 3.5, 4.4)], [(-90, -3.5, DECK), (-117, -3.5, 3.0), (-117, 3.5, 3.0), (-90, 3.5, DECK)], kind='deck')
    for y in (-5.2, 5.2):
        S.box(f'tower{y}', (-115.5, -114.5), (y - .5, y + .5), (-6, 19), kind='pile')
        S.box(f'counterweight{y}', (-114.3, -113.3), (y - .7, y + .7), (9.5, 12.5), kind='pile')
        S.tube(f'spancable{y}', [(-115, y * .66, 18), (-116, y * .66, 3.0)], .05, n=4, kind='rail')
    S.box('headframe', (-115.6, -114.4), (-5.9, 5.9), (17.8, 19), kind='pile')
    for sgn in (-1, 1):
        w = S.box(f'wingwall{sgn}', (-136, -118), (7.5, 8.7) if sgn > 0 else (-8.7, -7.5), (-6, 4.5), kind='pile'); w.turn(-12 * sgn, about=(-118, 8.1 * sgn))
        for x, y in ((-150, 15.5), (-178, 16.5)):
            S.cylinder(f'dolphin{sgn}_{-x}', (x, y * sgn), 1.5, -6, 6.0, r1=1.25, n=10, kind='pile')
    # ---- slips 1 and 2: only their piles are left
    for row, y in enumerate((32, 44, 62, 74)):
        for k in range(11):
            x = -14 - 9 * k - (row % 2) * 3; top = 1.2 + 3.4 * (((k * 7919 + row * 104729) % 97) / 97)
            S.cylinder(f'oldpile{row}_{k}', (x, y + ((k * 31 + row * 17) % 7 - 3) * .25), .2, -6, top, n=6, kind='pile')
    # ---- Substation 9, where the Cable comes ashore. Continuity's light is a strip, never a window.
    S.box('substation', (26, 46), (292, 308), (DECK, 11.0))
    S.face('substation.strip.w', [(25.98, 294, 9.7), (25.98, 306, 9.7), (25.98, 306, 10.15), (25.98, 294, 10.15)], kind='cold', emit=4.0)
    S.face('substation.strip.s', [(28, 291.98, 9.7), (44, 291.98, 9.7), (44, 291.98, 10.15), (28, 291.98, 10.15)], kind='cold', emit=4.0)
    # ---- Tern Point, two and a half kilometres down the Sound
    S.prism('ternpoint', [(-1120, -2600), (-700, -2620), (-640, -2360), (-880, -2250), (-1130, -2380)], -3, 6, kind='far')
    S.cylinder('ternpoint.tower', (-900, -2400), 3.0, 6, 24, r1=2.2, n=10, kind='wall'); S.cylinder('ternpoint.lantern', (-900, -2400), 1.8, 24, 27, n=10, kind='light', emit=6.0)
    if boat: kittiwake(S)
    if no4: lineman(S, cable, eye)
    annotate(S)
    return S

def kittiwake(S, bow=-118.5):
    """The M/V Kittiwake in the slip, bow to the span. Fifty-two metres, fourteen in the beam, double-ended."""
    hb = [(0, 4.0), (3, 5.8), (8, 6.8), (14, 7.0), (38, 7.0), (44, 6.8), (49, 5.8), (52, 4.0)]
    S.prism('kittiwake.hull', [(bow - t, b) for t, b in hb] + [(bow - t, -b) for t, b in hb[::-1]], -1.2, 2.8, kind='hull')
    for sgn in (-1, 1): S.box(f'kittiwake.sidehouse{sgn}', (bow - 46, bow - 6), (5.0 * sgn, 7.0 * sgn) if sgn > 0 else (-7.0, -5.0), (2.8, 6.0), kind='hull')
    S.box('kittiwake.cabin', (bow - 47, bow - 5), (-7, 7), (6.0, 8.6), kind='cabin')
    for sgn in (-1, 1):
        for k in range(11):
            x = bow - 8.5 - k * 3.4
            S.face(f'kittiwake.window{sgn}_{k}', [(x, 7.02 * sgn, 6.9), (x - 1.7, 7.02 * sgn, 6.9), (x - 1.7, 7.02 * sgn, 7.8), (x, 7.02 * sgn, 7.8)], kind='light', colour='#f4cf80', emit=2.0)
    for k, (a, b) in enumerate(((-5.2, -2.2), (-1.5, 1.5), (2.2, 5.2))):
        S.face(f'kittiwake.endwindow{k}', [(bow - 4.98, a, 6.9), (bow - 4.98, b, 6.9), (bow - 4.98, b, 7.8), (bow - 4.98, a, 7.8)], kind='light', colour='#f4cf80', emit=2.0)
    for nm, x in (('fore', bow - 7.5), ('aft', bow - 41)):
        S.box(f'kittiwake.wheelhouse.{nm}', (x - 3.5, x), (-2.2, 2.2), (8.6, 11.2), kind='cabin')
        S.tube(f'kittiwake.mast.{nm}', [(x - 1.75, 0, 11.2), (x - 1.75, 0, 15.2)], .07, n=5, kind='rail')
    S.face('kittiwake.wheelhouse.glass', [(bow - 7.48, -1.9, 9.9), (bow - 7.48, 1.9, 9.9), (bow - 7.48, 1.9, 10.8), (bow - 7.48, -1.9, 10.8)], kind='light', colour='#ffd9a0', emit=.8)
    S.cylinder('kittiwake.funnel', (bow - 26, 0), 1.1, 8.6, 14.0, n=12, kind='hull')
    S.cylinder('kittiwake.funnel.band', (bow - 26, 0), 1.13, 12.3, 13.1, n=12, kind='hull', colour=RED)
    # tonight she leaves westward, so the west end is the bow: red to port (south), green to starboard (north), white astern
    S.box('kittiwake.light.port', (bow - 41.3, bow - 40.9), (-7.25, -7.05), (9.0, 9.3), kind='light', colour='#ff4030', emit=5.0)
    S.box('kittiwake.light.starboard', (bow - 41.3, bow - 40.9), (7.05, 7.25), (9.0, 9.3), kind='light', colour='#40ff90', emit=5.0)
    S.box('kittiwake.light.stern', (bow - 5.0, bow - 4.8), (-.15, .15), (8.75, 9.0), kind='light', colour='#fff0d0', emit=5.0)

def lineman(S, cable=True, eye=True):
    """No. 4: a paper card forty metres tall standing in the Sound, and the Cable, as thick as a ferry's funnel."""
    S.card('no4', things.NO4, NO4_AT, NO4_FACING, metres=things.NO4_M, kind='machine')
    if eye:                                                                      # cold while the Cable is in; dark once it is cut
        S.card('no4.eye', [things.NO4_EYE], NO4_AT, NO4_FACING, metres=things.NO4_M, layer=-1, kind='cold', emit=5.0)
        S.card('no4.eye.near', [things.NO4_EYE], NO4_AT, NO4_FACING, metres=things.NO4_M, layer=1, kind='cold', emit=5.0)
    S.box('no4.footprint', (NO4_AT[0] - 6, NO4_AT[0] + 6), (NO4_AT[1] - 3, NO4_AT[1] + 3), (0, 1), kind='machine', on='drawing').turn(90 - NO4_FACING, about=NO4_AT[:2])
    if cable:
        o = np.array(NO4_AT); back = o + sp.direction(NO4_FACING) * things.NO4_BACK[0] * things.NO4_M + (0, 0, things.NO4_BACK[1] * things.NO4_M)
        S.tube('cable', [back, back + (14, 10, -9), (-380, 284, 3), (-340, 292, -1.2), (-200, 300, -1.5), (-30, 300, -1.5), (-4, 300, 1.5), (12, 300, 6.0), (27, 300, 6.6)], 1.1, n=8, kind='machine')
        S.tube('cable.route', [(-350, 290, .2), (-200, 300, .2), (-6, 300, .2)], .45, n=4, kind='machine', on='drawing')       # where it lies under the water, for the plan

def annotate(S):
    L = S.label
    L('THE TRESTLE', (-45, 1.2, 12.5)); L('waiting shed', (-65, -9.5, 10.2), True); L('the chain', (-88, 9.5, 7.6), True); L('transfer span', (-103, -7, 0.2), True)
    L('towers', (-115, 11.5, 20.6), True); L('SLIP 3', (-128, 1.2, -4.5)); L('M/V KITTIWAKE', (-144.5, -10.5, 16.2)); L('wingwalls', (-127, 14.5, 6.0), True)
    L("the heron's dolphin", (-178, 22.5, 8.2), True); L('slips 1 and 2: piles only', (-62, 53.5, 6.5), True); L('ticket office', (12, 22, 11.2), True)
    L('THE SHORE LINE', (35, -100, 7.5)); L('Signal 114.2, the Board', (64, -60, 12.0), True); L('level crossing', (52, -2.5, 7.0), True); L('EBB CREEK', (215, 224, 2.0))
    L('railway trestle', (58, 222, 7.4), True); L('SUBSTATION 9', (36, 316, 12.6)); L('No. 4', (-420, 247, 44.0)); L('the Cable', (-190, 307, 3.0), True)
    L('the hill; the houses', (205, 100, 24.0), True); L('TERN POINT LIGHT', (-900, -2330, 30.0)); L('the tide flat', (300, 240, 2.0), True)
    D = S.dim
    D((-90, -6, DECK), (0, -6, DECK), '90 m', 3.5); D((-117, -6, 3), (-90, -6, 3), '27 m', 6.5); D((-170.5, -7, 2.8), (-118.5, -7, 2.8), '52 m', 3.0); D((-30, -6, DECK), (-30, 6, DECK), '12 m', -6.0)
    D((6, 0, 0), (6, 0, DECK), '+5.0', -1.2); D((-112, 0, 0), (-112, 0, 19), '19 m', -1.0); D((-141, 0, 0), (-141, 0, 14), '14 m', -1.0); D((-405, 260, 0), (-405, 260, 40), '40 m', -3.0)
    return S

# ------------------------------------------------------------------ people: the cast as cards standing in the set
_CAST = None
def stand(S, who, at, heading, pose=None, flip=False, tag=None):
    """Stand a member of the cast (world/night-service/cast.py) in the set as a paper puppet, feet at `at`."""
    global _CAST
    import cast as _cast
    if _CAST is None: _CAST = _cast.cast()
    c = _CAST[who]; fig = c['fig']; m = STATURE * c['height']; nm = tag or who
    far, body, near = c.get('colours', ('#080b11', '#0e131c', '#0e131c'))
    for part in fig.parts(c['pose'] if pose is None else pose):
        name, P, layer = part[:3]
        S.card(f'{nm}.{name}', [P], at, heading, metres=m, flip=flip, layer=layer, kind='wall', colour=part[3] if len(part) > 3 else (far if layer < 0 else body if layer == 0 else near))
    J = fig.joints(c['pose'] if pose is None else pose)
    win = fig.on_trunk(J, [(.250, -.002), (.250, .030), (.205, .030), (.205, -.002)])
    for layer in (4, -2): S.card(f'{nm}.window{layer}', [win], at, heading, metres=m, flip=flip, layer=layer, kind='light', colour=c['window'], emit=5.0)
    return m

def perch(S, at, heading, tag='heron'):
    S.card(tag, things.heron(), at, heading, metres=things.HERON_M, kind='wall', colour='#10161f')

# ------------------------------------------------------------------ the night, and the cameras
def night(when=SAILING): return sp.moon(when, LAT, LON)

def cameras():
    c = {}
    c['1'] = sp.Camera(eye=(-30, 0, DECK + 1.6), az=270, lens=28, name='1')                       # wide, standing on the trestle
    c['2'] = sp.Camera(eye=(-62.4, 3.0, DECK + 1.5), look=(-88, 0.0, DECK + .9), lens=85, name='2')    # long, from a few steps out of the shed door, on the chain. (In the doorway itself, as entry 0 had it, the shed's own wall hides Dee.)
    c['3'] = sp.Camera(eye=(40, -60, 30), look=(-90, 0, DECK), lens=35, name='3')                 # high, over the shore
    return c

BASELINE_MOON = (255.0, 9.0)                     # what entry 0 assumed before the almanac was asked: "15 degrees left of west, 9 up"
DEE_AT = (-88.0, -4.6, DECK)                     # at the south post of the chain, facing north across the deck

def stage(people=True):
    S = build()
    if people:
        stand(S, 'dee', DEE_AT, 0.0)
        perch(S, (-178, 16.5, 6.0), 200.0)
    return S

def lights(boat=True):
    """The lights that land on things: (position, colour, strength, reach in metres). Only minded lights."""
    L = [((-66.4, -1.2, 6.9), '#ffd08a', 1.0, 3.0), ((11.3, 9.4, 6.8), '#ffb347', 1.2, 3.5), ((7.4, 14, 6.8), '#ffb347', 1.2, 3.5), ((39.5, -60.8, 10.2), '#ff3b28', 1.2, 4.0), ((39.5, -59.2, 10.2), '#ff3b28', 1.2, 4.0),
         ((25.0, 300, 9.9), '#dbeeff', 1.2, 6.0), ((36, 291, 9.9), '#dbeeff', 1.2, 6.0)]      # kept short: at full strength Continuity's strip lit a wall a hundred metres away across the creek
    if boat:
        b = -118.5
        L += [((b - 2.6, y, 6.6), '#f4cf80', .5, 4.0) for y in (-3.7, 0, 3.7)]
        L += [((b - 9.4 - k * 6.8, 9.2 * sgn, 6.4), '#f4cf80', .35, 3.5) for k in range(6) for sgn in (-1, 1)]
    return L

# ------------------------------------------------------------------ commands
OUT = HERE / 'ebb-landing'

def drawings():
    S = build(); C = list(cameras().values()); m = night(); OUT.mkdir(exist_ok=True)
    moon_note = [(m['az'], f'moon 01:35, {m["alt"]:.0f} deg up')]
    sp.drawing(S, 'plan', OUT / 'plan_site.svg', bounds=((-470, 420), (-130, 345), (-6, 60)), scale=2.0, cameras=C, grid=10, title='site plan', sky=moon_note, notes=['x east, y north'], reach=110)
    sp.drawing(S, 'plan', OUT / 'plan_slip.svg', bounds=((-192, 62), (-34, 92), (-6, 60)), scale=6.0, cameras=C, grid=5, title='Slip 3, plan', sky=moon_note, reach=40)
    sp.drawing(S, 'from_south', OUT / 'elevation_slip.svg', bounds=((-192, 62), (-34, 92), (-8, 24)), scale=6.0, grid=5, title='Slip 3, from the south')
    sp.drawing(S, 'from_south', OUT / 'elevation_site.svg', bounds=((-470, 420), (-130, 345), (-10, 52)), scale=2.0, grid=10, title='the whole place, from the south')
    sp.drawing(S, 'from_west', OUT / 'section_trestle.svg', bounds=((-90, 0), (-14, 14), (-8, 13)), scale=22.0, grid=1, cut=45.0, title='section through the trestle at 45 m, looking east')
    sp.drawing(S, 'plan', OUT / 'plan_world.svg', bounds=((-1500, 700), (-2750, 700), (-6, 60)), scale=.3, grid=100, title='the Sound', notes=['far shore 4.5 km west, never shown'])
    sizes()
    print('drawings in', OUT)

def sizes():
    """How big things are beside a person: one elevation, one scale."""
    S = sp.Set('How big'); x = 0.0
    S.face('water', [(-10, -5, 0), (140, -5, 0), (140, 5, 0), (-10, 5, 0)], kind='water')
    perch(S, (x, 0, 0), 90.0); S.label('the heron, 1.15', (x, 0, 3.4), True); x += 5
    m = stand(S, 'dee', (x, 0, 0), 90.0); S.label(f'Dee, {m:.2f}', (x, 0, 3.4), True); x += 5
    m = stand(S, 'lang', (x, 0, 0), 90.0); S.label(f'Lang, {m:.2f}', (x, 0, 3.4), True); x += 9
    S.box('shed', (x - 5, x + 5), (-1.7, 1.7), (0, 2.8)); S.gable('shed.roof', (x - 5, x + 5), (-1.7, 1.7), 2.8, 3.9); S.label('the shed, 3.9', (x, 0, 5.4), True); x += 12
    S.cylinder('cable', (x, 0), 1.1, 0, 2.2, kind='machine'); S.label('the Cable, 2.2 across', (x, 0, 3.8), True); x += 9
    S.cylinder('funnel', (x, 0), 1.1, 0, 5.4, kind='hull'); S.label('her funnel, 2.2 across', (x, 0, 7.0), True); x += 12
    for y in (-1, 1): S.box(f'tower{y}', (x - .5, x + .5), (y * 5.2 - .5, y * 5.2 + .5), (-5, 14))
    S.label('a span tower, 14 above the deck', (x, 0, 15.6), True); x += 34
    S.card('no4', things.NO4, (x, 0, 0), 90.0, metres=things.NO4_M, kind='machine'); S.card('no4.eye', [things.NO4_EYE], (x, 0, 0), 90.0, metres=things.NO4_M, layer=1, kind='cold')
    S.label('No. 4, 40', (x, 0, 44.5)); x += 30
    S.dim((x - 14, 0, 0), (x - 14, 0, 40), '40 m', -1.0)
    sp.drawing(S, 'from_south', OUT / 'sizes.svg', bounds=((-6, x - 6), (-6, 6), (-3, 48)), scale=12.0, grid=5, title='how big things are', notes=['a person is the unit'])

def check():
    S = stage(); res = {}
    for k, c in cameras().items():
        Path('out/space').mkdir(parents=True, exist_ok=True); r = sp.blender_check(S, c, f'out/space/check_{k}_blender.png'); res[k] = r
        print(f'camera {k}: my render and Blender agree on {r["agree"] * 100:.3f}% of pixels; least-agreeing solids {r["worst"][:3]}')
    return res

def score():
    """The guesses of journal entry 0 against the model."""
    C = cameras(); S = stage(); rows = []
    def row(shot, what, guess, real, unit='px', frame=720.0):
        err = abs(guess - real); rows.append((shot, what, guess, real, unit, err, err / frame * 100 if unit in ('px', 'y', 'x') else abs(guess / real - 1) * 100 if real else 0))
    c = C['1']; dee = c.place(DEE_AT, STATURE * .92); P = lambda cam, x, y, z: cam.project([(x, y, z)])[0]
    row(1, 'horizon y', 360, c.horizon(), 'y'); row(1, 'Dee, height', 70, dee['px'], 'size')
    row(1, 'trestle width at Dee', 300, abs(P(c, -88, 6, DECK)[0] - P(c, -88, -6, DECK)[0]), 'size')
    row(1, 'top of the towers y', 150, P(c, -115, 5.2, 19)[1], 'y'); row(1, 'top of the funnel y', 250, P(c, -144.5, 0, 14)[1], 'y')
    n4 = c.place(NO4_AT, things.NO4_M); row(1, 'No. 4 x', 1000, n4['x'], 'x', 1280.0); row(1, 'No. 4 height', 200, n4['px'], 'size')
    mx, my, mr = c.sky(*BASELINE_MOON, .52); row(1, 'moon x', 360, mx, 'x', 1280.0); row(1, 'moon y', 200, my, 'y'); row(1, 'moon width', 40, 2 * mr, 'size')
    c = C['2']; dee = c.place(DEE_AT, STATURE * .92)
    row(2, 'Dee, height', 240, dee['px'], 'size'); row(2, 'frame width at Dee (m)', 8, 1280 / c.scale(dee['depth']), 'size')
    print('   2  top of the towers: guessed "off the top of the frame"; model y = %.0f: right' % P(c, -115, 5.2, 19)[1]); row(2, 'near wheelhouse roof y', 150, P(c, -126, 0, 11.2)[1], 'y')
    h = c.place((-178, 16.5, 6.0), things.HERON_M); row(2, 'heron height', 12, h['px'], 'size'); row(2, 'heron x', 900, h['x'], 'x', 1280.0)
    c = C['3']
    row(3, 'horizon y', 120, c.horizon(), 'y'); a, b = P(c, 0, 0, DECK), P(c, -90, 0, DECK); row(3, 'trestle length on screen', 500, float(np.hypot(*(a - b)[:2])), 'size')
    a, b = P(c, -118.5, 0, 2.8), P(c, -170.5, 0, 2.8); row(3, 'Kittiwake length on screen', 220, float(np.hypot(*(a - b)[:2])), 'size')
    row(3, "No. 4's head above the horizon", 30, c.horizon() - c.place(NO4_AT, things.NO4_M)['top'], 'size')
    o = P(c, 12, 14, 8); row(3, 'ticket office x', 1050, o[0], 'x', 1280.0); row(3, 'ticket office y', 600, o[1], 'y')
    print(f'{"shot":>4}  {"what":<42} {"guess":>8} {"model":>8}   error')
    for s, what, g, r, unit, err, pct in rows:
        print(f'{s:>4}  {what:<42} {g:>8.0f} {r:>8.1f}   ' + (f'{pct:5.0f}% of the frame' if unit in ('x', 'y') else f'{g / r:5.2f} x the true size' if r else ''))
    pos = [p for *_, u, e, p in rows if u in ('x', 'y')]; siz = [g / r for _, _, g, r, u, *_ in rows if u == 'size' and r > 0]
    print(f'positions: mean error {np.mean(pos):.1f}% of the frame, worst {np.max(pos):.0f}%   sizes: geometric mean ratio {np.exp(np.mean(np.log(siz))):.2f}, mean |log2| {np.mean(np.abs(np.log2(siz))):.2f} (1.0 = a factor of two)')
    return rows

def cameras2():
    """Three new cameras for the second round of predictions (journal entry 2)."""
    return dict(A=sp.Camera(eye=(12, 9, 6.6), az=270, lens=50, name='A'),                                  # from the ticket office door, level
                B=sp.Camera(eye=(-185, 30, 1.0), look=(-115, 5.2, 19), lens=24, name='B'),                 # from a skiff by the heron's dolphin, up at the towers
                C=sp.Camera(eye=(36, 300, 12.5), look=(-420, 260, 34.3), lens=135, name='C'))              # from the roof of Substation 9, on No. 4's eye

def score2():
    """Round two: predictions made with the rules (focal length in pixels = 35.6 x mm; size = f x height / distance;
    horizon = centre + f x tan(tilt); moon = f / 110), worked in the head and written down before this was run."""
    C = cameras2(); m = night(); rows = []; P = lambda cam, x, y, z: cam.project([(x, y, z)])[0]
    def row(shot, what, guess, real, unit, frame=720.0): rows.append((shot, what, guess, real, unit, abs(guess - real) / frame * 100))
    c = C['A']; mx, my, mr = c.sky(m['az'], m['alt'], m['diameter'])
    row('A', 'horizon y', 360, c.horizon(), 'y'); row('A', 'shed ridge y', 307, P(c, -65, -4.25, 8.9)[1], 'y'); row('A', 'top of the towers y', 186, P(c, -115, 5.2, 19)[1], 'y')
    row('A', 'Dee, height', 30, c.place(DEE_AT, STATURE * .92)['px'], 'size'); row('A', 'moon x', 488, mx, 'x', 1280.0); row('A', 'moon y', 92, my, 'y'); row('A', 'moon width', 16, 2 * mr, 'size')
    c = C['B']; f = P(c, -144.5, 0, 14); h = c.place((-178, 16.5, 6.0), things.HERON_M)
    row('B', 'horizon y', 566, c.horizon(), 'y'); row('B', 'funnel top x', 891, f[0], 'x', 1280.0); row('B', 'funnel top y', 338, f[1], 'y'); row('B', 'heron height', 82, h['px'], 'size')
    print('   B  heron: predicted off the right of the frame (x about 1379); model x = %.0f: %s' % (h['x'], 'right' if h['x'] > 1280 else 'WRONG'))
    c = C['C']; n4 = c.place(NO4_AT, things.NO4_M); mx, my, mr = c.sky(m['az'], m['alt'], m['diameter'])
    row('C', 'horizon y', 589, c.horizon(), 'y'); row('C', 'No. 4 height', 419, n4['px'], 'size'); row('C', "No. 4's waterline y", 720, n4['foot'], 'y'); row('C', 'moon x', 648, mx, 'x', 1280.0); row('C', 'moon width', 44, 2 * mr, 'size')
    print('   C  moon: predicted off the top of the frame (y about -127); model y = %.0f: %s' % (my, 'right' if my < 0 else 'WRONG'))
    for sh_, what, g, r, unit, pct in rows:
        print(f'{sh_:>4}  {what:<28} {g:>8.0f} {r:>8.1f}   ' + (f'{pct:5.1f}% of the frame' if unit in ('x', 'y') else f'{g / r:5.2f} x the true size'))
    pos = [p_ for *_, u, p_ in rows if u in ('x', 'y')]; siz = [g / r for _, _, g, r, u, _ in rows if u == 'size']
    print(f'positions: mean error {np.mean(pos):.1f}% of the frame, worst {np.max(pos):.1f}%   sizes: mean |log2| {np.mean(np.abs(np.log2(siz))):.2f}, worst ratio {max(siz, key=lambda v: abs(np.log2(v))):.2f}')

if __name__ == '__main__':
    a = sys.argv[1:] or ['drawings']
    {'drawings': drawings, 'check': check, 'score': score, 'score2': score2}[a[0]]()
