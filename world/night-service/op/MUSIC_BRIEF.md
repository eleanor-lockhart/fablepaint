# NIGHT SERVICE opening theme: brief for the composer

Sixty-two seconds of music for the opening in `BRIEF.md` (the last four ring out under a held end card). Picture and music share a grid
and never see each other's files: land your accents on the times below and they will be in sync.

**You cannot hear, and neither can anyone else working on this.** You will write the piece, render it, and
judge it by what the listening room shows: `backlot/ear.py` (spectrogram, loudness, energy by band, pitch
classes, onsets). Calibrate your trust in it with `backlot/tests/eartest.py`. Read `world/night-service/music/
MUSIC.md` (the rules of this world's sound) and `music/JOURNAL.md` (what went wrong last time), and
`music/tern_point.py` and `music/eleven.py` as working examples of `backlot/sound.py` and `backlot/score.py`.

## Grid

120 beats a minute, 4/4. One beat 0.5 s, one bar 2 s, thirty bars. Bar *b* starts at 2(*b* - 1) seconds.

## What happens when

The picture is 62 seconds; the last four are a held end card with the sound ringing out under it.

| seconds | bars | picture | music |
|---|---|---|---|
| 0-4 | 1-2 | black; a far light; then four lit windows snap on | almost nothing: sea. Ticket punches (`sound.punch`) at **2.0, 2.5, 3.0, 3.5**. A foghorn swelling into 4.0. |
| 4-8 | 3-4 | the title; the tagline at 6.0 | **the hit at 4.0**: everything enters. State the hook plainly: the three-note figure A, D, E ("the three lights") from *Tern Point*. |
| 8-12 | 5-6 | Orrin walks to his lamp (steps on the beats 8.0-9.5); he nods off and the lamp sinks (10.0-10.9); he wakes and it flares at 11.0 | verse. Thin out and sink with the lamp from 10.0; **a bell on 11.0** when it flares. |
| 12-16 | 7-8 | Dee punches the passengers' cards | the punch as percussion on **12.5, 13.5, 14.5, 15.5**. |
| 16-20 | 9-10 | Marisol; at 16.5 a house's light goes out and walks away in a pale figure's chest | one high pure tone (`sound.glass`) on **16.5**; high bright plucked notes for Marisol. |
| 20-24 | 11-12 | Red; the signal drops to green by itself at 21.5; she raises her lantern, up by 22.5 | a low single-note ostinato, steady, unimpressed; a small accent on **22.5**. |
| 24-26 | 13 | the ferry crossing in rain | pre-chorus: thin out. Glass tones for the passengers. |
| 26-28 | 14 | the heron, perfectly still; it blinks at 27.0 | nearly nothing. One small sound on **27.0**. |
| 28-32 | 15-16 | Vesper Lang taps six lit windows cold, one a beat: 28.5, 29.0, 29.5, 30.0, 30.5, 31.0 | mains hum (`sound.hum`, 60 Hz) and one cold steady tone, rising from 28 to 32; a dry tick on each tap. The only sustained sounds in the piece. |
| 32-34 | 17 | **the break**: black; at 33.0 a cold eye opens | at **32.0 everything stops dead**. Real silence. One low struck tone on **33.0**. |
| 34-38 | 18-19 | No. 4 revealed, the camera tilting up it and landing at 36.0; a cold pulse runs down its cable on every beat | **chorus, the hit at 34.0**. The theme at full strength, drums. An accent on **36.0**. |
| 38-42 | 20-21 | the pod goes in; an orca takes the cable; it snaps at 41.5 | chorus continues. The biggest accent of the piece on **41.5**, and whatever stood for the cable (the hum, if you kept it under the chorus) stops there for good. |
| 42-46 | 22-23 | the four of them walking across the moon, a foot down on every beat | a kick on every beat. The tune at its most open. |
| 46-50 | 24-25 | minder, light, minder, light: a cut on every beat | an accent on every beat: 46.0, 46.5 ... 49.5, each struck and dying. |
| 50-54 | 26-27 | No. 4's eye turns green at 50.5; a window opens in its chest at 52.0 | half-time, space. A small sound on 50.5. **A bell and one glass tone on 52.0.** |
| 54-58 | 28-29 | the lineup; windows light at 54.0, 54.5, 55.0, 55.5, 56.0, 56.5; No. 4's, far off, at 57.0 | six struck notes climbing on those six times; a seventh, lower and bigger, on **57.0**. |
| 58-62 | 30-31 | the end card, held | **the last chord on 58.0** with a bell and the foghorn. Let it ring to 62. Nothing after. |

## The rules of this world's sound (from MUSIC.md)

- The night shift's notes are **struck and die away**. Energy comes from striking again: repeated notes,
  arpeggios, drums. Do not hold a pad under the heroes.
- **Sustained sound belongs to the other side**: the hum, a cold steady tone. Use it only at 30-32, and, if you
  want a threat under the chorus, very quietly.
- One lead at a time. A long room (about 10 dB of reverb under the dry sound; `Mix.wet_to_dry_db` tells you).
- The foghorn sounds D. The punch is percussion. The sea is always there and never noticed.
- Everything is synthesised with numpy and scipy. No samples, no soundfonts. You may define new instruments
  (kick, snare, hats, a lead) in your own file; do not edit `backlot/`.

## Musical requirements

- D is home. Verse in D Dorian (B natural). For the chorus you may lift into the relative major and use the
  progression every anime opening knows, IV-V-iii-vi (B flat, C, A minor, D minor), or stay in Dorian: your
  choice, but the chorus must be clearly bigger than the verse.
- The hook (A, D, E rising) must be recognisable in the title, come back in the chorus, and end the piece.
- It should make someone want to hear it again. Last time the tune was "safe: stepwise, the same shape twice".
  Give this one an interval nobody expects, and a rhythm that is not all quarter notes.
- Humanise: nobody plays exactly on the grid or equally loud twice. But keep the listed sync times exact.

## What to deliver

- `world/night-service/op/music.py`: runs from the repository root with `uv run python world/night-service/op/music.py`,
  writes `out/op/music/night_service_op.wav` (48 kHz stereo, 62 s), `world/night-service/op/night_service_op.mp3`,
  `world/night-service/op/music_report.jpg` (from `ear.report`) and `world/night-service/op/music_score.png` (`score.piano_roll`).
- Mastered to **-14 LUFS** (within 0.5), true peak at or under -1.0 dB, nothing clipped.

## How to judge it (you must do all of this and report the numbers)

1. `ear.report`: key guess in the D minor / F major family; pulse near 0.5 s; loudness; clipping.
2. Loudness by section from the samples: the chorus (34-50) at least 2 LU above the verse (8-24).
3. The break: RMS between 32.05 and 32.95 s below -50 dB (reverb tails count: cut the room too).
4. Sync: for every time in bold above, an onset within 40 ms (use the spectral-flux onset envelope, or the
   sample envelope).
5. Balance: no band above -2.5 dB of the total; bass (60-250 Hz) between -12 and -4; presence (2-6 kHz)
   between -22 and -8. Last time the bass was pure low sines that small speakers cannot play: give low notes harmonics.
6. Look at the spectrogram in the report (Read the jpg). Can you see the sections? The break? The hits?
7. Then say, honestly, what you cannot tell from any of this.
