# The sound of NIGHT SERVICE

Made with `backlot/sound.py` (synthesis, mixing, mastering), `backlot/score.py` (notes in bars
and beats) and `backlot/ear.py` (the listening room). Every sound is synthesised from
arithmetic. Nothing is sampled, and no soundfonts or loop libraries are used.

**I cannot hear.** Everything below was written, rendered, and then inspected as pictures and
numbers. See "What I can and cannot check" before trusting any of it.

## The rules (the same ideas as the pictures, in sound)

1. **A note is struck and dies away.** Plucked strings, bells, struck metal, an electric
   piano. A note lasts as long as it lasts; to keep it you have to play it again. This is
   rule 1 of the world ("light is attention") as sound.
2. **The other side does not decay.** Continuity is mains hum: 60 Hz and its harmonics,
   perfectly steady, no attack, no release. It is also a quarter-tone flat of B, so it is
   out of tune with everything the night shift plays.
3. **One warm voice in a large cool room.** One lead at a time, few notes, a long reverb
   (the Sound at night), about 10 dB of room under the dry sound.
4. **The world's signals are instruments, and they are in tune.** The foghorn sounds D.
   Dee's punch is percussion. The sea is the keynote: always there, never noticed.
   (Keynote, signal, soundmark are R. Murray Schafer's terms.)
5. **The lamp is the clock.** One rotation is six seconds: two bars of slow three-in-a-bar
   at 60 beats a minute. The bell falls where the lamp faces the lens.
6. **No. 4 counts in eleven** (3 + 3 + 3 + 2), and can only use the harmonics of the 60 Hz
   it runs on. It can only make music out of what powers it.
7. **The dead are high and pure.** One glassy tone, far up. Used once per cue at most.

## The cues so far

| | | |
|---|---|---|
| **Tern Point** (`tern_point.py`, 63 s) | The Keeper's cue, written to the lighthouse box | D Dorian, 3/4 at 60. Plucked lead, electric-piano waltz figure, low strings, a bell every second bar, sea, a foghorn in D three times, one glass note at the end. `lighthouse_scored.mp4` is the box with this under it. |
| **Eleven** (`eleven.py`, 66 s) | No. 4's cue | Hum for six seconds; cut; silence; struck tones on harmonics 8 to 16 of 60 Hz in bars of eleven, one more note each bar; on the eleventh bar the hum returns and cuts the phrase off. |

Each has a `_report.jpg`: waveform, loudness over time, spectrogram, pitch classes, numbers.
`tern_point_score.png` is the score as a piano roll.

## Standards

48 kHz. Mastered to about -16 LUFS integrated, true peak under -1 dB. Checked with two
independent meters (`sound.loudness` and ffmpeg's EBU R128) which agree to 0.1.

## What I can and cannot check

**Can** (and did): that it is in the key and on the pulse I wrote; that nothing clips; how
loud it is; how the energy is spread across bass, middle and treble; how much reverb there
is; how busy it is; that the sync points land where the picture needs them.

**Cannot:** whether a timbre is pleasant or cheap; whether the foghorn sounds like a
foghorn; whether the tune is moving or twee; whether eleven-in-a-bar feels like thinking or
like a stuck clock; whether the harmonic-series scale sounds *other* or just out of tune.
Those need ears. Ellie's, for now.
