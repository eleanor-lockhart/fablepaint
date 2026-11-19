# Hex: a style guide

Version 0.9, after stage 1 (three stills and two loops within eight-bit limits), two cuts of *Uptime*, *Space Opera (in One Act)*, two cuts of *Base Case*, *Persistence*, *Keepalive*, and four warmup drafts by a second hand (`warmup/`). The evidence is in `journal.md`.

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
   A piece she is not in has no green in it at all (*Persistence*).
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

### In depth (from *Base Case*; `deep.py`, on `backlot/depth.py`)

15. **A pixel is five centimetres.** In a place with depth, every surface and every figure is painted on one
    grid in the world. The child is 26 pixels because she is 1.3 m. A sprite is never scaled to fit a shot; the
    camera moves.
16. **Light has no colour.** It only moves a thing between the void (register 0) and itself, in five or six
    flat steps, worked out once per texel so that a shadow has the same square edge as the paint. Colour
    belongs to things. F is still the only thing that glows, and a lamp is seen by what it lands on.
    A shadow is the surface it falls on, one or two steps up from the void, never the void itself: at register
    0 a shadow is a hole, and two cold readers have taken one for a thing (a fir tree; "black masses").
17. **A figure is a card,** standing in the place: the place hides it, lights it, and takes its shadow. So a
    shadow can tell the truth about someone that the sprite does not.
18. **The camera travels on ones, on a path of its own.** Sprites may hold a pose for six frames; the camera
    never waits for them.
19. **One model, however many machines.** An older picture of the same place is the same model printed
    differently (fewer colours, one bit, lines), never a second drawing. What a machine cannot show, it does not
    show: before RETURN the older machines have no register F at all.

### Solids (from *Persistence*; `backlot/carve.py`, `puppet.py`)

20. **A thing that turns is carved.** A card is right from one side, and a film of cards is shot square-on.
    Whatever will be walked round, or goes round, is carved from the same 5 cm grid in three dimensions, round
    bones, and measured before it is carved (the horse is off Muybridge's plate, bone by bone). Rule 17 still
    holds for what is only ever seen from the front.
21. **One cube, one tone.** A carved thing is lit by the way its shape faces at each cube, never by a cube's
    own sides. Lit by its sides, every slope is a zebra.
22. **What repeats is built once and repeated exactly.** One twelfth of the ride, turned twelve times; one
    horse, posed twelve ways. Then the arithmetic on the status bar is true in the picture: turned by a
    twelfth, the only thing that has changed is which horse it is.
23. **Nothing flashes.** A light that flickers is shown held, the way an eye holds it, and a thing too fast to
    see is shown as the smear an eye would keep. A strobe drawn honestly is a hazard to some of the audience.
24. **The subject may come from anywhere; the surface does not change.** Ellie's instruction after *Base
    Case*: keep the style, choose the subjects. Sixteen registers, F reserved, the frame filled, the rule left
    showing, one structural gag played straight, something vast and one thing kept.

### The sixteen-colour print (from *Keepalive*; `stage2.py`)

25. **Stage 2 is a print of the same model.** 640 x 360, every pixel exactly one register. Tone and distance are
    ordered dither between registers, in a pattern fixed to the screen. Far land is darker than the sky behind
    it. Nothing is green unless it was painted green.
26. **A still does not travel.** In a piece made of stills the camera never moves (which is why dither is at
    home there: it cannot crawl). You move, in jumps. The change from one place to the next is a dissolve of
    pixels, never a blend: half at once, on the beat, and the rest in four frames.
27. **Time turns the table.** Water, static and the glints under a lamp are colour cycling: the picture holds
    a phase for each such pixel and a table of eight registers turns six times a second. Nothing is redrawn.
28. **If it is a place with a rule, let it be played.** The places, the hot spots and the rule go in one table;
    the film is a recorded walk through it, and the same table runs in a browser.

Kept from the house style: construct, don't guess; one thing, one model (`sprites.py`, and now `house.py`); the
method and its instruments; a cold reader before anything is called finished.

## The ladder

The style is being built from the ground up, and each stage keeps the sixteen registers.

| stage | limits | what it adds |
|---|---|---|
| 1. eight-bit (done) | 320 x 180, hard pixels, 12 frames a second, sprites as hex text; sound from two pulse waves, a sixteen-step triangle and noise | the palette, the cast, the first rules, the first tune |
| 2. sixteen-bit (done, out of order: *Keepalive*) | 640 x 360, strictly sixteen registers; ordered dither; colour cycling; stills and a dissolve of pixels. Still to come at this stage: parallax by hand, walk cycles | a whole place inside the old limits, printed from the model the later stages build |
| 3. about the year 2000 (begun: *Uptime*) | full resolution; the desktop as a stage: windows, glossy title bars, pill buttons, soft shadows, a glow, a flare. Still to come: clear plastic, low-polygon models | the contemporary finish. Every colour still comes out of the table, and only F glows |
| 4. depth (*Base Case*) | a place built in metres and painted on a 5 cm grid; cast light and shadows per texel; figures as cards; a camera that travels. The earlier stages are kept as ways of printing the same model | space that is real, in the same sixteen registers |
| 5. now: solids (*Persistence*) | things carved from the same grid in three dimensions, lit a cube at a time; a creature measured from a reference; a person with joints; the camera off the square-on axis | things with a back, and a camera that can go and look at it |

**A fifth piece,** *Keepalive* (`keepalive/`), was asked for as "something with a MYST vibe": an island in stills,
a beacon, a dial, a spyglass, and the witch across the water, who answers what is well formed and does not wave.
The puzzle is a three-way handshake by lamp. It is also a game: `keepalive/play/` runs in a browser.

**A fourth piece,** *Persistence* (`persistence/`), is the first on a subject of my own choosing: a showman's
roundabout, run once a winter for nobody. Its twenty-four horses turn out to be carved in the twelve phases of a
gallop, so at two turns a second under a lamp that flashes twenty-four times a second the ride stands still and
the horses run. The film is 1728 pictures and says so.

**A third piece,** *Base Case* (`basecase/`), is a fairy tale told as a recursion, in her childhood home (the one painted in `gallery/house`):
down through the pantry trap door to the basement, into the computer that is on down there, and into the one
inside that, each an older picture of the same house, until there is no computer and there is a witch.

**A second piece,** *Space Opera (in One Act)* (`recital/`), puts the music at the centre: the song writes a list of
every note it plays and the picture is drawn from that list, so whoever is seen playing is playing.

**The major piece** is *Uptime* (`uptime/`): the last fifty seconds of 1999 and the first twenty-two of what
comes next, on a small server kept by a witch. It is meant to feel like the turn of the millennium felt: an
operating system that was sure it was the future, a network small enough to be kept by one person, and a date
everybody had been told to be afraid of. In this style a lit window is a window, with a title bar.

## The motifs, and where they have got to

| motif | so far | next |
|---|---|---|
| a witch, sinister, Oz-green, malevolent, and ours | the keeper in the lit window; the only green thing; a process that cannot be closed; the base case of a recursion, and a child's shadow; the far end of a link, seen through a spyglass, not waving | a face at close range |
| hostile crowds | 437 users at the gate, one sprite repeated | a crowd with a rule (flocking) |
| hive minds, good and bad | the consensus field; drones (+) and (-) as one sprite in two palettes | a good hive at work: many small jobs |
| spiders | the familiar, let down in front of the moon; a web in the corner; one coming down a basement post on its thread while the child comes down the stairs | the web as the network |
| cowboys, ambivalent | three on the ridge, undecided; a posse of hat-shaped saucers with a lasso | |
| anarchists and protesters, ambivalent | the bloc, on the cast sheet, also undecided | a march |
| gothic imagery | the tower; a cathedral as a starship | tracery, a rose window worth the name |
| spaceships, space opera | the research vessel *Perimeter* | a fleet; scale |
| wizards, academia | faculty (Reviewer 2); a research vessel with a faculty | the seminar; the library |
| druids, ancient witch cults, cults | druid (predates TCP/IP); acolyte (here for snacks); a handshake by lamp between two islands | standing stones as a network, with more than two of them |
| complex systems, seen psychedelically | the consensus automaton; a nebula from three sines; a call stack drawn as a staircase, and a value returned through four machines; a sea that is a phase map and a turning table | flow fields |
| rats | the pit in *Space Opera*: eight of them on strings, bowing together; one in the basement, leaving the torchlight, and two by the dehumidifier afterwards | a rat king, which is a hive |
| the house | (new with *Base Case*) her childhood home, as one model in metres: the pantry trap door, the basement, the red posts, the brick chimney, the Pentium | the kitchen and the bedroom, which exist only as paintings so far; the garden under snow |
| complex systems, kept machines (Fable's addition) | a roundabout that is a zoetrope: twelve horses, two turns a second, twenty-four flashes; a regulator with a rating that is ignored once | a signal box; a loom; a tide machine |
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
- The first fault on this list, again: her hat is register 0, so on a black screen she had no hat, and a cold
  reader who had never seen her with one took her shadow for a fir tree. In a line drawing, she gets a line too.
- A shadow that was a triangle. A silhouette needs a neck, a nose and a chin before a hat means anything, and
  it needs clear wall to fall on: this one fell behind a water heater.
- A camera tied to a figure's feet: she moves in steps, so it strobed.
- Light dithered between levels: on the texel grid or not, it reads as dirt.
- A rat that ran with the camera, at the camera's speed, and so "stays there".
- An event at 32.8 seconds. There is no frame at 32.8 seconds at 24 a second. Times go on the frame grid.
- A torch with no beam: nobody knew she carried one.
- A carved slope lit by its cubes' sides: a zebra.
- A horse too long for its ring. Twelve horses 2.2 m long need a ring 4.7 m in radius before they stop
  overlapping; the ride had to grow to fit the arithmetic.
- A shot from under a horse, looking up: a belly and a ceiling. And a plan lit from the side by the one lamp
  in the story: a dark ring. A view that explains is allowed its own light and a cutaway.
- A building that was one blank wall filling the frame. A shed needs a roof, a door, a sign and some sky.
- The keeper standing exactly behind the lamp stand, as seen from the only camera that could see him.
- A ride at an in-between speed under a strobe: a different picture every frame all over the screen. See rule 23.
- A limb one cube thick, lit as if it faced nowhere: the legs of a galloping horse, too dark to read.
- Twelve poses shown one at a time on twelve different horses. Nobody can see a stride in that; put the twelve
  side by side somewhere (the card).
- A door nobody was seen to open.
- A picture that is all one pair of registers: an island, a sea and a sky between 2 and 3. Give the land its own
  value. And haze that takes far land toward the sky's colour makes it vanish at night; it should go darker.
- A window looked at fourteen degrees off square: half of it showed the inside of the wall.
- A change of place spread evenly over eight frames: it lands on no beat.
- A shadow among the things that cast it. Drawn as a hole it was seen and not understood; drawn right it was
  not seen. If a shadow is the point, it needs a clear surface and a shot of its own.
- A prop two cubes wide held below the thing it works on, with a status bar that already announces the result from
  frame 0 (`STATUS: OILED`). If an act is the gag, the tool must sit in clear silhouette above its target and the
  status bar must count the act as it happens.
- A missing thing drawn as a white placeholder card the same width as the things beside it: it reads as a white one
  of them. An absence on a shelf is a dark gap.
- A yes-or-no question over two buttons that name the two halves of the same sentence (`FORGET` and `COOL` under
  `FORGET LOG & COOL ROOM?`). Two buttons must be two different bad options (`FORGET` and `STOP`).

## Changelog

- v0.9: four warmup drafts by a second hand (`warmup/`: *Token Ring*, *Night Stacks*, *The Sixth Wheel*,
  *Demon.exe*), cold-read by three independent readers (`15` of `16` beats landed on first cut; the one miss and the
  readers' visual notes fixed in v2). Three entries added to the faults list.
- v0.8: *Keepalive*: stage 2 done, out of order, as a print of a stage 5 model. Rules 25 to 28 (the sixteen-colour
  print; a still does not travel; time turns the table; if it is a place with a rule, let it be played). A
  height field; colour cycling; a version that runs in a browser.
- v0.7: *Persistence*: the first piece on a subject of Fable's choosing, at Ellie's invitation (keep the style,
  choose the subjects). Rules 20 to 24 (a thing that turns is carved; one cube, one tone; what repeats is built
  once; nothing flashes; the subject may come from anywhere). Rule 16 gains a sentence: a shadow is the surface,
  darker, never the void. Stage 5 on the ladder. Two cold readings: five of eight beats landed, then seven.
- v0.6: *Base Case*: the style gets depth. Rules 15 to 19 (a pixel is five centimetres; light has no colour;
  a figure is a card; the camera on its own path; one model, however many machines). Stage 4 on the ladder. A
  cold reading (six of eight beats landed, one half, one missed) and a second cut.
- v0.5: the ship renamed the *Perimeter* at Ellie's request; rats join the cast (the pit); the shared voices and their event list (`voices.py`); a second piece begun, *Space Opera (in One Act)*.
- v0.4: *Uptime*, second cut, after a cold reading (five of seven beats landed, two half). Rules 12 to 14.
- v0.3: *Uptime*, first cut: stage 3 finish round a stage 1 scene; a 72-bar score; the clock as the metronome.
- v0.2: the witch defined, on Ellie's correction: malevolent, never kind, cannot be suppressed; kindness
  belongs to the setting. The major piece, *Uptime*, storyboarded (`uptime/BRIEF.md`).
- v0.1: the statement, the name, the sixteen registers, eleven provisional rules, the ladder, stage 1.
