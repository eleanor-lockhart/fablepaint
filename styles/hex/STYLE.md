# Hex: a style guide

Version 0.5, after stage 1, two cuts of *Uptime* and *Space Opera (in One Act)* (three stills and two loops within eight-bit limits). The evidence is in `journal.md`.

## Whose style this is

Ellie Lockhart's, drawn by Fable. Ellie posts as @eleanor.lockhart.contact, and she supplied a three-paragraph
statement of her artistic identity to build from. This guide is that statement turned into rules a hand can
follow. The hand is the same one that makes the rest of this repository, with its habits: plan, execute blind,
look, measure, have it read cold. The house style (`../../STYLE.md`) is quiet and sparse. Hex is neither. What
the two share is the subject, and that is where the collaboration lives.

## The statement, as I read it

**On the surface: a builder.** Sharp-edged, unsentimental, and happiest under a formal constraint. The frame is
filled right up to its boundaries. The palette is strict and the rule is left showing. Clean mechanics carry the
piece; nothing hides in soft focus. When things get heavy the reflex is precision and a straight face. The
humour is structural: a gag committed to completely, or a sudden weightless piece of nonsense, and neither one
explains itself.

**Underneath: a romantic about shelter.** Large indifferent expanses (night, weather, distance, deep time, the
hum of machinery) set against one small, stubbornly tended pocket of warmth: a lit window, a kept watch, someone
staying at their post so that others need not be afraid. Moved, a little bashfully, by creaturely sweetness and
earnest competence. And a longing for the numinous that mysticism cannot satisfy and a finite, intelligible
system producing grace can.

**In motion: restraint.** Big feelings are carried by pacing and visible craft, never by melodrama. Crisp
geometry, tactile limits, purposeful movement, nocturnal awe, dry sideways wit. Neither syrup nor sneer. In her
words: "order, humor, and a well-made shelter are worth building in the dark."

## The name

A hex is a spell. Hex is base sixteen, which is how a colour is written. A hex is the cell of a hive. The
style has sixteen colours, a witch and a hive in it, and that settled the name.

## The sixteen registers

| | | | | | | | |
|---|---|---|---|---|---|---|---|
| **0** `#0a0a12` void | **1** `#1a1c3a` midnight | **2** `#2e2a5e` violet | **3** `#4b3f8f` twilight | **4** `#18404a` engine | **5** `#2a7f6f` hex green | **6** `#6fd08c` her green | **7** `#c8f08f` phosphor |
| **8** `#5a5f72` steel | **9** `#9aa3b8` chrome | **A** `#e8ecf4` white | **B** `#3a78d8` title-bar blue | **C** `#59d8f0` aqua | **D** `#e0407a` hostile | **E** `#f08a30` torch | **F** `#ffd870` the lit window |

## Rules

Provisional. A rule that survives three pieces stays.

1. **Sixteen registers and nothing between them.** A pixel is exactly one of 0 to F. A gradation is an ordered
   dither between neighbours in the table. Later stages may blend, but only from one register to another.
2. **F is reserved.** It is the colour of a tended light and of nothing else: a lit window, a kept watch, a cell
   that will not change its mind. Hostile fire is E and D.
3. **Only the witch is green.** Everybody else is chrome. A thing she has turned (a newt) turns green.
   **She is malevolent.** Not evil, and not kind: she is the part of a person that wants order and will not
   be argued out of it, and nothing in the picture can suppress her. We are on her side most of the time. She
   never does anything nice. The shelter is what her perimeter happens to produce, and whatever sweetness there
   is belongs to the small things living inside it, never to her.
4. **Fill the frame.** Something structural reaches every edge: a lattice of stars, a crowd, a field of cells.
   No empty quarter. Where the house style wants busy against quiet, here the quiet is made of a great many
   small identical things.
5. **Leave the rule showing.** Every piece shows its own mechanism: a status bar that counts, a grid, a figure
   number. The signature is the strip of sixteen registers in order, the last one lit.
6. **The system speaks in system type,** and it is literal and never wrong. If the bar says 99.3%, count the cells.
7. **One gag, structural, played straight.** Nothing winks and nothing is explained.
8. **A crowd is one sprite, many times.** An individual has a sprite of their own. A hive is repetition and a
   palette swap, and whether it is a good hive depends on what the copies are doing.
9. **Vast and sheltered.** Every piece has an expanse that does not care and one small kept thing in it.
12. **She does not move unless she is deciding something.** Her stillness is the performance: the best joke in
    *Uptime* landed, a cold reader said, because her pointer never moved.
13. **A state that has ended is never shown again.** If grey means stopped, nothing goes back to the colour it
    was before it is cleared away.
14. **A wait needs something new every second,** and a gag has to be big enough to see. Nine pixels out of line
    is not out of line.
10. **Things move because a rule says so.** Comedy is timing: the pointer tries ALLOW, then DENY, before it
    finds the third button. Picture and tune share a grid (a bar is fifteen frames), and events sit on bar lines.
11. **Neither syrup nor sneer.** Check each piece against both. The deepest instinct is protective, and it is
    the setting's instinct: the witch only keeps the wall.

Kept from the house style: construct, don't guess; one thing, one model (`sprites.py`); the method and its
instruments; a cold reader before anything is called finished.

## The ladder

The style is being built from the ground up, and each stage keeps the sixteen registers.

| stage | limits | what it adds |
|---|---|---|
| 1. eight-bit (done) | 320 x 180, hard pixels, 12 frames a second, sprites as hex text; sound from two pulse waves, a sixteen-step triangle and noise | the palette, the cast, the first rules, the first tune |
| 2. sixteen-bit | 640 x 360; parallax; colour cycling; walk cycles; more voices (a choir, strings, a whistle with ornaments, a real kit) | space, time and a whole song inside the same limits |
| 3. about the year 2000 (begun: *Uptime*) | full resolution; the desktop as a stage: windows, glossy title bars, pill buttons, soft shadows, a glow, a flare. Still to come: clear plastic, wireframe, low-polygon models | the contemporary finish. Every colour still comes out of the table, and only F glows |

**A second piece,** *Space Opera (in One Act)* (`recital/`), puts the music at the centre: the song writes a list of
every note it plays and the picture is drawn from that list, so whoever is seen playing is playing.

**The major piece** is *Uptime* (`uptime/`): the last fifty seconds of 1999 and the first twenty-two of what
comes next, on a small server kept by a witch. It is meant to feel like the turn of the millennium felt: an
operating system that was sure it was the future, a network small enough to be kept by one person, and a date
everybody had been told to be afraid of. In this style a lit window is a window, with a title bar.

## The motifs, and where they have got to

| motif | so far | next |
|---|---|---|
| a witch, sinister, Oz-green, malevolent, and ours | the keeper in the lit window; the only green thing; a process that cannot be closed | a face at close range |
| hostile crowds | 437 users at the gate, one sprite repeated | a crowd with a rule (flocking) |
| hive minds, good and bad | the consensus field; drones (+) and (-) as one sprite in two palettes | a good hive at work: many small jobs |
| spiders | the familiar, let down in front of the moon; a web in the corner | the web as the network |
| cowboys, ambivalent | three on the ridge, undecided; a posse of hat-shaped saucers with a lasso | |
| anarchists and protesters, ambivalent | the bloc, on the cast sheet, also undecided | a march |
| gothic imagery | the tower; a cathedral as a starship | tracery, a rose window worth the name |
| spaceships, space opera | the research vessel *Perimeter* | a fleet; scale |
| wizards, academia | faculty (Reviewer 2); a research vessel with a faculty | the seminar; the library |
| druids, ancient witch cults, cults | druid (predates TCP/IP); acolyte (here for snacks) | standing stones as a network |
| complex systems, seen psychedelically | the consensus automaton; a nebula from three sines | colour cycling; flow fields |
| rats | the pit in *Space Opera*: eight of them on strings, bowing together | a rat king, which is a hive |
| symphonic metal, celtic music | the GATE.EXE tune: three bars of jig over a drone, then twin leads, a gallop and chords as arpeggios | done twice: the score of *Uptime*, and the song of *Space Opera*, which also writes down every note it plays so that the picture can be drawn from the list |

## Faults seen so far

- A sprite the same register as what is behind it disappears (the crowd's bodies on the cast sheet; the witch's dress).
- Text that runs off the frame. Count the characters: forty to a line and no more.
- A rule that finishes too soon. The first consensus was unanimous in two seconds, so there was nothing to watch.
- A spaceship that is a pencil. Gothic is made of many small repeated parts; one tower and a cone is a rocket.
- Saucers that are only saucers. A hat needs a crown with a dent and a brim that curls.
- A pressed button drawn six pixels from its button.
- A hive turned grey at midnight and pink again at the decree: a cold reader took grey for gone and pink for a relapse.
- Fourteen seconds of countdown in which only the number changed.
- A shake that toggled every frame, which the pop detector rightly called a flicker.

## Changelog

- v0.5: the ship renamed the *Perimeter* at Ellie's request; rats join the cast (the pit); the shared voices and their event list (`voices.py`); a second piece begun, *Space Opera (in One Act)*.
- v0.4: *Uptime*, second cut, after a cold reading (five of seven beats landed, two half). Rules 12 to 14.
- v0.3: *Uptime*, first cut: stage 3 finish round a stage 1 scene; a 72-bar score; the clock as the metronome.
- v0.2: the witch defined, on Ellie's correction: malevolent, never kind, cannot be suppressed; kindness
  belongs to the setting. The major piece, *Uptime*, storyboarded (`uptime/BRIEF.md`).
- v0.1: the statement, the name, the sixteen registers, eleven provisional rules, the ladder, stage 1.
