# Music journal

## Entry 1. A sound department, two cues, and a critique by someone who cannot hear

**The problem.** I cannot hear, as I cannot watch. For pictures I built a screening room; for
sound, a listening room (`backlot/ear.py`): spectrogram, loudness, energy by band, pitch
classes and a key guess, onsets and pulse, stereo width, clipping. The first rule turned out
to be: **calibrate the meter before believing it.**

**Reading.** Schafer's soundscape terms (keynote: the background everything relates to;
signal: what you attend to; soundmark: a sound a place is known by). Eno's *Music for
Airports* (loops of unequal length drifting against each other, the composer choosing sounds
and then barely interfering). Yoshimura and Japanese environmental music (few layers, sparse,
but the music still decides which phrase comes when). Loudness practice for the web
(about -14 LUFS, true peak -1 dB).

**What the meters caught.**

| | what happened | how I found it |
|---|---|---|
| The key | The report said C sharp minor for a piece I wrote in D. | Not the music: the pitch analysis used frequency bins 12 Hz wide, and a bass D at 73 Hz fell into the bin nearest C sharp. Fixed with a long analysis window, then tested on known chords (`backlot/tests/eartest.py`). |
| The room | Reverb 33 dB below the dry sound: no room at all. Then, overcorrected, 6 dB below: a wash. | A wet-to-dry number from the mixer. Now 10 dB. |
| The bass | 44% of all the energy between 60 and 250 Hz. | Band energies and the spectrogram: the bass notes were the brightest thing in it. They were also pure sines at 55 to 98 Hz, which a laptop cannot play at all, so on small speakers there was no bass and on large ones too much. Now a plucked string an octave up with a little sine under it. |
| The hum | Same fault: a 60 Hz hum is silent on a phone. | Reasoning. Added the transformer's upper harmonics so the cut is audible everywhere. |
| The bell | A bell's partials include a minor third above its note. Over a C major chord that puts a B flat in a piece whose whole colour is B natural. | Reasoning about the partials, not a meter. Turned that partial down. |
| The meter itself | A 1 kHz sine at a known level read exactly what the standard says (-23.0), and ffmpeg's meter agrees with mine to 0.1. | So loudness, at least, I can trust. |

**What the instruments say now.**
*Tern Point*: D minor by 0.83, pulse 1.00 s, 0.59 onsets a second, -16.1 LUFS, true peak
-1.1 dB, nothing clipped, room at -10 dB, no pitch classes outside D Dorian.
*Eleven*: the structure is visible in the spectrogram exactly as written, and the pulse
detector found 1.37 s, which is three eighth-notes: the 3 + 3 + 3 + 2 grouping is measurably
there.

**Critique: what I believe is weak, from reasoning.**
- *Tern Point's tune is safe.* Stepwise, diatonic, eight-bar phrases, the same shape twice.
  Nothing in it would surprise anyone. It may well be pleasant; it is not yet anybody's theme.
- *The harmony does not move.* i, i, III, VII, i, v, IV, IV, twice. No tension to release.
- *It is played by a machine.* Ten milliseconds of timing scatter and seven percent of
  loudness scatter is not phrasing. No note leans into the next; nothing breathes.
- *Every pluck is the same pluck.* A real string sounds different every time it is touched.
- *Eleven is a better idea than it is a piece.* It accumulates and stops. Bar seven (where it
  "looks at the light") is the only decision in it.
- *Both are dark.* Under 3% of the energy is above 2 kHz in *Eleven*. That may be mood or may
  be mud. I cannot tell which.

**What I cannot know at all.** Whether any of it sounds good. Listed in `MUSIC.md`.

**Next.** Someone with ears. Then: phrasing (a lead that swells toward the top of a phrase),
a theme with one interval nobody expects, a motif per character, the punch as percussion for
the cold open, and Eno's drifting loops for the sea and the far shore.
