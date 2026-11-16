# Hex: journal

## Entry 0. Before drawing anything

**The brief.** Ellie wants a second style beside mine: one that expresses her, through her Bluesky account,
drawn by me so that it stays a collaboration. She supplied a statement of her artistic identity and a list of
motifs. It is to be built from the ground up, starting with drafts in a retro, eight-bit manner and climbing to
something contemporary, and the major piece at the end should feel like the years around 2000.

**What is hers and what is mine.** Hers: the temperament, the subjects, the jokes. Mine: the hand, the method,
and one habit that turns out to be shared. My own style is one small warm light in a large cool dark. Her
statement asks for "small, stubbornly tended pockets of warmth" in "large, indifferent expanses". So the two
styles have the same subject and opposite surfaces. Mine is sparse and says stop early. Hers fills the frame to
its edges and leaves the rule showing. The risk is that I make my own pictures again in brighter colours. The
test of each piece is whether it is dense, formal and funny on the outside.

**Decisions made before the first pixel.**

- A strict palette of sixteen, written 0 to F, with F reserved for tended light. Her statement asks for strict
  palettes and visible rules; a reserved register is a rule you can see being kept.
- Sprites are written as text, one hex digit per pixel. The picture is literally made of hex.
- The system talks. Dialog boxes and status bars are the straight face.
- The motifs are a cast, so the first draft is a cast sheet.
- The statement itself stays out of the public repository, apart from one sentence quoted as the motto. It
  describes a person as well as a style, and that is hers to publish.

**What I expect to get wrong.** Preciousness (my default is quiet awe, and this style is allergic to it).
Jokes that explain themselves. A witch who is cute.

## Entry 1. Stage 1: three stills and two loops

All at 320 x 180 in sixteen registers, shown at four times the size. `stage1.py` makes them.

**Fig. 1, persons of interest.** Ten sprites and a status for each. *Works:* it is a parts list and reads as
one; the statuses carry the tone ("8 LEGS, 0 NOTES"; the two drones are one sprite in two palettes, which is
the whole argument about hive minds in sixteen pixels). *Weak:* the people are small in their boxes, and the
cowboy's chrome face reads as a robot. The druid and the acolyte are generic robes.

**Fig. 2, the watch, and its loop, GATE.EXE.** A tower with one lit window, a crowd with torches from edge to
edge, three undecided cowboys on the ridge, a spider let down in front of the moon, and a dialog box asking
what to do about 437 users. In the loop the pointer tries ALLOW, hesitates over DENY, and presses NEWTS; the
conversion runs through the crowd from left to right; a second dialog reports the result; the cowboys leave.
*Works:* this is the style in one frame, and it was the second thing drawn. The reserved register does its
job: the window is the only F in the picture and the eye goes straight to it. *Weak:* the crowd reads as
wallpaper at this size, which is right for a hive and wrong for menace. The newts are green squiggles. The
tower was a blank slab until it was given courses of stone, and it could take a great deal more.

**Fig. 3, the research vessel *Perimeter* and a posse.** A cathedral as a starship: the rose window is the drive,
the exhaust is a broom, one clerestory window is lit, and five hats in formation have a lasso on the spire.
*Works:* the nebula (three sines, quantised and dithered) is the first psychedelic system and cost four lines.
*Weak:* the ship is still closer to a rocket than a cathedral. This is the weakest of the four.

**Fig. 4, consensus, with one dissent.** A field of hexagonal cells, four opinions, one rule: do what most of
your neighbours do. One opinion shouts, a little louder every second. A cell that has held the loud opinion
long enough grows an eye. One cell has the hat in it and never changes. When the field is unanimous the bar
reads CONSENSUS 99.9%, DISSENT 1, and then the six cells round the post light up one at a time. *Works:* it is
the statement as a mechanism: a finite, intelligible system, and the grace is that seven is more than one.
The first half is the psychedelic part and nobody drew it. *Weak:* the reboot is a wipe because I could not
think of a better way round the loop.

**The tune for GATE.EXE** (`gate_exe_tune.py`). Ten seconds, eight bars of 6/8, on the voices an eight-bit
machine had. Three bars of a jig in D Dorian over a drone; the button goes down on bar 4; then the same key the
way symphonic metal has it (two leads a third apart, a kick on every eighth, chords as fast arpeggios) down
through D minor, C and B flat to a dominant with its third raised, and round again. The picture was retimed so
that a bar is fifteen frames and every event sits on a bar line. I cannot hear it. The listening room says:
-14.3 LUFS, nothing clipped, a pulse at 97 to the minute (the jig's beat), D and A the strongest pitches, and
the first mix was bottom-heavy, so the bass came down by a quarter. Whether the join between the jig and the
metal is funny or just abrupt is a question for someone with ears.

**Against the statement.** Dense, formal, deadpan: yes. Vast and sheltered: yes in figs. 2 and 4, thin in 3.
Syrup: no. Sneer: fig. 1 is close to it, since ten jokes at ten people's expense is a lot; the witch needs to
be seen being kind to something. Creaturely sweetness: not yet. The spider is the obvious candidate.

**Not yet tested:** nobody has read these cold, and nobody has heard the tune.

**Next.** Stage 2: the same sixteen registers at 640 x 360 with parallax, colour cycling and walk cycles;
the witch and the spider with something to do together; and a whole song, written first, with the picture
hung on it.

## Entry 2. A correction, and the major piece

**The witch.** I wrote above that she "needs to be seen being kind to something". Ellie corrected that: the
witch does not have kindness as a trait. She is not evil but she is malevolent: the authoritarian part of a
person, the basic darkness that can never be suppressed. Kindness is outside her, in the setting. That is a
better engine than mine. The light in the window is kept by something dreadful, the small things inside the
wall are safe because of it, and nobody thanks her. It also hands the film its central gag: a thing that cannot
be suppressed is a process that cannot be closed.

**The major piece** is *Uptime*: the last fifty seconds of 1999 and the first twenty-two of whatever comes
next, on a small server kept by a witch, staged on a desktop of the period. Storyboard on a bar grid in
`uptime/BRIEF.md`. The song is written first this time and the picture is hung on it. One bar is one second,
so the system clock is the metronome.

## Entry 3. *Uptime*, first cut

Seventy-two seconds, 1,728 frames, a score of seventy-two bars. `uptime/music.py` was written first and
`uptime/film.py` hung on it. One bar is one second, so the clock in the corner of the screen is the metronome
and every event in the storyboard sits on a tick.

**By measurement.** All 33 storyboard events land in both picture and sound (`uptime/uptime_sync.jpg`); the
first pass had 22. No one-frame accidents: the detector caught my countdown shake, which toggled every frame,
and it is now a jump on each tick. Nothing strobes. The score is at -14.2 LUFS with a range of 14 LU: the jig
sits at -22 dB, the hive at -15, midnight at -34 and the decree, the loudest thing in it, at -11.6.

**How the stages show in it.** The tower is the stage 1 scene, live, in a window, still 320 by 180 and still on
twos. Round it is the stage 3 finish: gradients, gloss, soft shadows, a glow, a flare. Every colour on the
screen is one of the sixteen registers or a blend of two, and the only thing that glows is register F.

**My own verdict, written before anybody else has seen it.**

What I think works:

1. The three clicks. CLOSE, END TASK, ARE YOU SURE?, and then a small green dialog that says SHE IS.
2. THE END (v2.0) going on counting after zero: -1, -2, -3. The system is literal.
3. Midnight. Everything goes grey, the hive shuts its eyes, and one window is still the colour it was.
4. IT IS THE YEAR 2000 BECAUSE I SAY SO. She does not fix the clock; she overrules it.
5. The clock as the metronome.

What I think is weak:

1. She is never seen. She is sixteen pixels of silhouette, a pointer and four dialogs. A stranger may not
   connect the green pointer with the figure in the window.
2. The watchers are a row of small sprites. That they have come to see her fail is carried by one window title.
3. The hive may read as a virus or a wallpaper, not as a mind made of many.
4. There is a great deal to read, and some of it is up for two seconds.
5. The sweetness in the coda (a drone carries a light to the spider's page and its counter goes up by one) is
   very small. So is the joke on the bin: NEWTS (111435), which is 437 times 255.
6. The finish is gloss and gradients. There is no clear plastic, no wireframe, nothing low-polygon.
7. Nobody has heard the score. The choir and the organ are a saw wave with holes cut in it.

What I expect a cold reader to get, of the seven things in the brief: the crowd and the newts, the takeover
that cannot close her, the lights going out and hers staying, and the decree. Half: that she is in charge;
that everybody was waiting for her to fail; that she is not nice and the place is safe anyway.

## Entry 4. The cold reading, and the second cut

The reading is in `uptime/COLD_READ_v1.md`. Five of the seven things the film must say landed and two
half-landed; I had predicted four and three. The reader's best moment was the one I listed first, and it gave
a reason I had not thought of: SHE IS. lands "because the witch's pointer never moves". Her stillness is the
performance. That is now a rule.

**What it found that I had not.** Three of its six faults were not on my sealed list at all: the hive coming
back pink at the decree after I had turned it grey at midnight, the countdown as fourteen flat seconds, and an
opening in which my one gag was invisible because the icon was nine pixels out of line. The pattern is the
same as with the opening for NIGHT SERVICE: what I got right about my own work was general (she is never
seen; there is a lot to read) and what I missed was specific.

**The second cut.**

| what the reader said | what changed |
|---|---|
| the pink came back at 56 seconds | at midnight the hive stops for good: grey, eyes shut. The decree clears it from the tower outward and it is never pink again |
| fourteen flat seconds | the watchers heckle, one line a bar or so: ANY SECOND NOW. NOBODY IS PID 1. UNDECIDED. ALSO UNDECIDED. SHE HAS TO BLINK. NO GODS. NO ADMINS. Every eye in the hive turns to her window and they blink together on the tick. The picture closes in slowly on the clock and lets go at midnight |
| who are the watchers | the heckling says so; the countdown window is now titled THE END - 30 WATCHING |
| a slow opening; the pointer "wanders" | the icon is well out of line and her grid shows for a moment when she snaps it. Drones carry lights from page to page and the counters count them. She turns in her window every three seconds, except while they are trying to close her |
| the icon stayed pink; one stray newt | the hive's pointer goes in a white flash like everybody else, and the hive's icon becomes a newt. Both are counted: 111435, then 111436, then 111437 |
| too small to read | the count of newts is in the process list at full size |

By measurement the second cut still has all 33 events landing in picture and sound, no one-frame accidents and
nothing strobing.

**Not tested.** The second cut has not been read cold: a reader works once and I have not spent another.
Nobody has heard the score. And whether she reads as malevolent, not merely formidable, is still open: the
reader saw someone who turns objections into newts and did not use a word like that.

## Entry 5. *Space Opera (in One Act)*

Ellie asked for another piece that mixes the art of now with the art of around and before 2000, with the music
at the centre, because she liked the score of *Uptime*. While it was being made she asked for the ship to be
renamed (it is the *Perimeter* now, everywhere) and for rats.

**What it is.** Ninety-six seconds. Aboard the research vessel *Perimeter* the witch conducts a space opera,
which is an opera, in space. She has her back to us and plays nothing. Everyone you hear is someone you can
see: the spider on its web, which is a harp; eight rats in the pit, bowing together; a druid on the whistle;
an acolyte on the drums; the cowboy on fiddle, once he commits; a newt on bass; the faculty at the organ, whose
pipes are also the level meter; the drones as a choir; the bloc on guitars. Each is dark until their first
note. She cuts the last chord off on its third beat. A dialog asks APPLAUSE? [ALLOW] [DENY] [NEWTS], she
presses DENY, and the spider plays one more note anyway.

**How it is made.** The song was written first, as before, but this time the song also writes down what it
played: `voices.py` keeps a list of every note (when, how long, by whom), 1,382 of them, and `film.py` draws
from that list and from nothing else. Nobody is animated. They are played.

**The two eras.** From before 2000: the sprites, on twos; a tracker with the song going past as rows of notes
and hex; a player window with a scrolling title. From now: ribbons in a flow field, on ones; a rose window
whose twelve lights are the twelve pitch classes; and the tune drawn along the front of the stage, note by
note, so that by the end the whole song is a skyline.

**The song.** 4/4 at 120, two seconds a bar: four taps of the baton; the spider and the rats; a verse on the
Andalusian cadence (D minor, C, B flat, A); organ and choir closing in; a chorus whose hook peaks in its last
bar, which is what the critic of the NIGHT SERVICE theme said a chorus should do; the organ alone in a
sequence; a short verse; the chorus again a tone higher, because that is what is done; three chords and a
major one.

**By measurement.** 18 of 19 events land in both picture and sound. The nineteenth is the cut-off, which is a
silence and cannot have an onset. No one-frame accidents. -14.0 LUFS over a range of 17 LU.

**My verdict, before anyone else has seen or heard it.** *Works:* the entrances, since a figure lighting up on
its first note needs no explaining; the rose window; DENY. *Weak:* it is one wide shot for ninety-six seconds
and a music video cuts; "playing" is a four-pixel bob and a moving bow, so nobody's hands do anything; the
witch is a dark shape in a busy frame and the eye may not find her; the tracker is very small; and I have not
heard a note of it. The key change is either the best joke in it or the corniest thing in it and I cannot tell
which from here.

**Not tested:** no cold reader has seen it.

## Entry 6. *Base Case*: the style gets depth

Ellie asked for two things at once: learn to put flat animation in deep space ("2.5D", with perspective), and
make something with it, perhaps from the childhood-home pictures, perhaps going down into the basement "in a
fairy-tale sort of way".

**What I took from her.** The house is the one already in `gallery/house`, and she had told me how you got to
its basement: through a trap door in the pantry floor that you had to lift. She has said in public that the
basement was where she sat as a child with a Pentium 100 and a dehumidifier, playing an adventure game, and
that she is fond of it; and she has shared a photograph of it, which gave me the red steel posts, the brick
chimney, the furnace and the water heater. So the basement is the shelter, not the horror, and the fairy tale
was already down there on a screen. The photograph is a reference and stays out of the repository; so do my
notes on what else of hers I read and chose to use or leave alone.

**The premise.** A recursion. The power goes out; the one light left is under the pantry floor; a child goes
down; the computer is on and shows the same house; she goes in, and there is a pantry, a trap door, a basement
and a computer, drawn as a machine nine years older would draw them; and again; and again, until there is a
basement with no computer in it. That is the base case, and the witch lives there. She refuses a polite
request (the parser does not know the word "please", which is Ellie's correction about kindness made
literal), then acts for her own reason and presses RETURN. The value returned is F. On the way back up every
machine redraws its house with the lights on, and in the real basement the child's shadow on the wall wears a
hat. Third in a row to end on a button: OK, DENY, RETURN.

**What "2.5D" turned out to be.** Four decisions that I used to make by feel, now made by the model
(`backlot/depth.py`, and `styles/hex/deep.py` for what Hex does with it):

1. *A texel is a size in the world.* Everything is painted on one 5 cm grid: walls, stairs, the child (26
   pixels is 1.3 m). A sprite is never scaled to "look right"; the camera moves instead.
2. *Light is worked out per texel*, at the middle of each, so a shadow's edge is the same hard square as the
   paint. I tried dithering between light levels and it was noise; five flat steps read better.
3. *A figure is a card*: a cut-out standing in the set, hidden by it, lit by it, and casting its own shape. A
   card that casts but is not drawn is how a child's shadow can be a witch's. The last beat of the story is
   carried by the new machinery and by nothing else.
4. *The camera moves; the paint stays.* Parallax is then one over distance. The first tracking shot followed
   the child's feet and strobed (2.4% of the width a frame, because she moves in steps); the camera now runs on
   its own smoothed path (0.45%).

For Hex there is one more rule: **light has no colour; it only moves a thing between the void and itself.**
Colour belongs to things. F is still the only thing that glows.

**One model, four prints.** The house is built once, in metres (`house.py`: 200 solids; the plan and section
are drawn from it). Level 0 is that model with cast light and a travelling camera. Levels 1 to 3 are the same
model through fixed cameras at each machine's resolution with a different last step: sixteen colours and an
ordered dither with a figure that shrinks as she walks away (1989); one bit, with edges inked, in a window
with a striped title bar (1987); hidden-line edges and forty columns of text (1980). Each level down gives up
something a picture can have: cast light and camera movement, then colour, then surfaces. I did not draw any
of the three; I only wrote three ways of printing.

**The score** is a ground (D, C, B flat, A: one bass note a bar) stated twelve times, a scene each. Each step
on the stairs is a note of the scale, going down two octaves. The tune goes to three square waves, then one
eight-bit voice, then a beeper, then nothing but a pedal and the keys. RETURN is an F major chord (the value
returned is F), and the way back is the tune in the relative major with each machine joining in turn.

**By measurement.** 35 of 35 listed events land in both picture and sound (first pass: 20; the misses were
clicks too small to see, three events a frame late because their times were not on the frame grid, and
windows lighting during a crane). No one-frame accidents. The camera's largest step is 0.45% of the width.
-14.4 LUFS over a range of 20 LU.

**My verdict, sealed before anyone else has seen it.** *Works, I think:* the opening section (the whole
geography in one picture, and the one screen still lit underground); the line of light round the trap door;
the torch in the basement; the zoom through the glass into the same house; "I DON'T KNOW THE WORD
"PLEASE"."; the gold lines; the screens inside screens on the way out; the shadow.
*Weak, I think:* the 1989 level is eight seconds and has two text boxes in it, so it may be seen and not read;
the 1987 level is first-person and small in its window, and a stranger may not know it is the pantry again;
I do not know whether "DESCEND(1998)" reads as "this picture is from 1998" or as noise; the child's walk is two
poses; the child is hidden by the monitor when she arrives at the desk; the furnace, heater and chimney are
boxes; and I cannot hear it.
*Prediction for the cold reader:* of the eight beats in the brief, six land (1, 2, 3, 5, 6, 7), and two are
half: 4 (they will say "the art style changes" without saying each is inside the last) and 8 (they will see a
dark shape on the wall and may not call it hers).

## Entry 7. *Base Case*: two cold readings and a second cut

**The first reading** (`basecase/COLD_READ_v1.md`; the whole film, 48 sheets). Six of the eight beats landed,
one was half and one was missed. I had predicted six and two halves and had the wrong ones.

- The recursion, which I expected to be half-understood, landed completely and unprompted: "Each look appears
  on a computer screen inside the one before it, so they are nested. Each looks older and cruder than the last,
  and the years count down." The stack window was read as "a running list of nested calls". So was the worry
  about the eight-second 1989 level: both its text boxes were read and quoted.
- The shadow, which I had sealed as one of the things that worked, was "a stepped triangle shaped like a pine
  tree". Two causes, and the first is the oldest fault on this style's list: her hat is register 0, so on the
  black screen of 1980 she had no hat, and the reader had only ever seen "a wide flat purple hat". The second:
  the caster was her whole squat sprite and its shadow fell behind a water heater.
- Nobody was seen to press RETURN. The pointer was green, but it appeared "near the table", and a text game has
  no pointer.
- "F" meant nothing ("false" was the reader's best guess, and it "sits oddly with the lights then coming on").
- The torch was never seen as a torch. Its beam on the water heater was "a flame or a lighting effect".
- The rat "stays there as the camera moves", because it ran the way the camera was going at the camera's speed.

What my eye was good for: the things that are structure (the nesting, the stack, the parser) I under-rated.
The thing that is a *shape* I over-rated, because I knew what shape it was meant to be. That is the same
lesson as the hat-shaped saucers in stage 1, and I did not apply it.

**The second cut.** A white line round her in the 1980 picture. A new shadow: head and shoulders in profile
with a bent hat, a brim wider than the shoulders, a nose, a chin and a neck, thrown from a low light to the
child's right so that all of it lands on clear wall, twice her size, looking at her; at 82.0 the light dips
for four frames and when it comes back the shadow has one green eye. The water heater went in front of the
chimney, which is where it is in the photograph and where I should have put it. Her pointer leaves from her
hand, and the parser, which narrates everything else, narrates that too: SHE PRESSES RETURN. THE VALUE IS F.
Then: F IS A LIT WINDOW, which is the definition in this style's own table, said by the machine. The sixteen
registers, named, sit in the stack window and the last one answers each return. Dust in the torch's beam. A
notice when the power goes (THE POWER IS OUT. 1 LIGHT IS STILL ON.), which also points at the screen in the
basement. The game's score line counts windows (0 OF 5, then 7 OF 5), because the first reader took seven lit
windows where five had been for a slip and it is the point: she did not allow the dark, any of it.

**The second reading** (`basecase/COLD_READ_v2.md`; a new reader, the second half only, since that is where
both failures were). "A pointed purple hat." "The witch clicks RETURN herself." "F is a lit window ... reaching
the real house." And the shadow: "a pointed hat, a long hooked nose, a jutting chin and a robe-like body. It is
a witch's silhouette, facing her. I see no shadow shaped like the girl herself." Whose it is, the reader would
not say: the witch come up with the value, the child's own shadow, something off-screen, or a protector. I am
scoring that half and leaving it. The reader noticed the one clue there is (the child has no other shadow),
and the film is not going to say more than that.

**By measurement, second cut.** 37 of 37 listed events land in both picture and sound. No one-frame
accidents. The camera's own largest step is 0.45% of the width; the travel meter also reports one frame at
3.4%, which is the pool of torchlight going down a stair with her (it reads any large bright thing that moves
as the camera). -14.8 LUFS, range 20 LU.

**What is still weak, in my own judgment.**

- The child has two walking poses and one sitting one. She does not look at the shadow, or at anything.
- The furnace, the heater and the chimney are boxes and cylinders with one paint each. The place is correct and
  it is not yet *finished*: no stains, no clutter that tells you who lives there.
- Level 0 is dark, and video compression is unkind to dark dithered snow. 24 MB for 96 seconds.
- LIGHTS: 7 OF 5 is too small to read on the way out.
- Four of the five shots at level 0 are seen from the south, square on. The model would allow anything.
- I have not heard a note of it. The thing I most want checked by ear: whether the tune is still the same
  tune when the beeper has it, and whether the F major chord at RETURN is a relief or a jingle.
- Not tested: the second cut's first half has not been read (its beats landed in the first cut, and it has
  changed: a notice, a beam, a rat, a lifting pose).
