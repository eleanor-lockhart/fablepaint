"""Is the picture on the music?   uv run python world/night-service/op/sync_check.py     (after build.py)

Nobody here can watch the film with the sound on, so this measures it. For every sync point in the brief it
reports what the picture did on that pose (how much of the frame changed against the pose before, compared with
the poses around it) and what the sound did at that instant (the strongest onset within 60 ms, and how far off
it is). It also draws both on one timeline: op/review/sync.jpg.

A picture accent "lands" if the change on its pose is clearly bigger than its neighbours'. A sound accent
"lands" if there is an onset above the detector's threshold within 40 ms.

The measuring itself began in this file and now lives in the library (backlot.sync) so that every later film
gets it; what stays here is this film's list of moments.

    uv run python world/night-service/op/sync_check.py            table, op/review/sync.jpg, sync.json
    uv run python world/night-service/op/sync_check.py events     a sheet of 12 consecutive poses round every moment
    uv run python world/night-service/op/sync_check.py pops       large changes that are not on the list
    uv run python world/night-service/op/sync_check.py travel     the camera's speed, pose by pose"""
import sys, json
from pathlib import Path
HERE = Path(__file__).resolve().parent
from backlot import sync

FPS = 12
SYNC = [(2.0, 'punch: window 1'), (2.5, 'punch: window 2'), (3.0, 'punch: window 3'), (3.5, 'punch: window 4'), (4.0, 'TITLE HIT'),
        (6.0, 'tagline'), (10.0, 'lamp starts to sink'), (11.0, 'lamp flares'), (12.5, 'Dee punch'), (13.5, 'Dee punch'), (14.5, 'Dee punch'), (15.5, 'Dee punch'),
        (17.0, 'light leaves the house'), (18.0, 'cut: Marisol close'), (21.5, 'mast drops to green'), (22.0, 'cut: Red close'), (24.0, 'pre-chorus: the crossing'),
        (26.0, 'cut: heron'), (27.0, 'heron blinks'), (28.0, 'cut: Lang'), (28.5, 'Lang tap 1'), (29.0, 'Lang tap 2'), (29.5, 'Lang tap 3'), (30.0, 'Lang tap 4'),
        (30.5, 'Lang tap 5'), (31.0, 'Lang tap 6'), (32.0, 'BREAK: black'), (33.0, 'cold eye opens'), (34.0, 'CHORUS: No. 4'), (36.0, 'tilt lands'),
        (38.0, 'cut: the pod'), (41.5, 'CABLE SNAPS'), (42.0, 'cut: the eye stutters'), (42.5, 'the cold eye goes out'), (43.0, 'cut: the walk'), (46.0, 'cut 1'), (46.5, 'cut 2'), (47.0, 'cut 3'), (47.5, 'cut 4'),
        (48.0, 'cut 5'), (48.5, 'cut 6'), (49.0, 'cut 7'), (49.5, 'cut 8'), (50.0, 'cut: No. 4 head'), (50.5, 'eye turns green'), (52.0, 'WINDOW OPENS'),
        (54.0, 'lineup: Orrin'), (54.5, 'Red'), (55.0, 'Dee'), (55.5, 'Marisol'), (56.0, 'Passenger'), (56.5, 'Lang'), (57.0, 'No. 4, far off'), (58.0, 'END CARD')]

FRAMES, WAV = 'out/op/full/frames', 'out/op/music/night_service_op.wav'
FLASHES = [506, 508]       # deliberate one-pose flashes: the cold eye stuttering out. Pose 128 is NOT allowed: the lamp recovering for one pose in Orrin's doze was meant as him catching himself and reads as a fault (found by sync.pops after v1.1 shipped; for version 2)

def main(frames_dir=FRAMES, wav=WAV):
    return sync.check(SYNC, frames_dir, wav, FPS, HERE / 'review' / 'sync.jpg', HERE / 'review' / 'sync.json')

def events(frames_dir=FRAMES, out_dir='out/op/events'):
    made = sync.events(SYNC, frames_dir, out_dir, FPS); print(len(made), 'event sheets in', out_dir); return made

if __name__ == '__main__':
    a = sys.argv[1:]
    if a and a[0] == 'events': events(*a[1:])
    elif a and a[0] == 'pops': print(json.dumps(sync.pops(SYNC, *(a[1:] or [FRAMES]), fps=FPS, allow=FLASHES), indent=1))
    elif a and a[0] == 'travel':
        steps, st = sync.travel(*(a[1:] or [FRAMES])); print(json.dumps(st))
    else: main(*a)
