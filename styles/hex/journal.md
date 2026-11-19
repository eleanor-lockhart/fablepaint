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

## Entry 8. *Persistence*: a subject of my own, and things that turn

After *Base Case* Ellie's instruction was: keep working in this style; the thematics are optional; pick new
subjects and new projects, teach yourself more, refine the style. So this is the first Hex piece whose subject
is mine to choose.

**What I picked, and why.** A showman's roundabout in its winter shed, run once a year for nobody to see that
it still runs. Its horses turn out to be carved in the twelve phases of a gallop, so at the right speed under
a flashing lamp the ride stands still and the horses run. Three reasons.

- The deepest line in the statement is the longing for the numinous that only "a finite, intelligible system
  producing grace" can satisfy. This is that sentence as a machine: twelve horses, two turns a second,
  twenty-four flashes a second. Nothing is hidden and it is still a small miracle.
- It is about the medium. A film is pictures that do not move; so is a zoetrope; so, it turns out, is this
  ride. The last card says so, in system type, with a straight face.
- It could not be made with what I had. *Base Case* was shot square-on because its figures were cards, its
  furniture was boxes, and its child had two walking poses. A roundabout shows every side of everything on it.
  So the subject forced the three skills I most lacked: solids that turn, a creature built from a reference,
  and a figure with joints.

No witch, so nothing is green; rule 3 is kept by leaving her out. The keeper is chrome, like everybody else.
What is vast is the winter night; what is kept is the ride.

**What had to be learned** (the tools are in `backlot/carve.py`, `backlot/depth.py`, `puppet.py`; the general
account is entry 4 of `studies/space/JOURNAL.md`).

- *Carving.* A solid is the paint grid in three dimensions: 5 cm cubes, each a register. The renderer walks
  every ray through the grid, so a carved cube is a box to the pixel and throws the shadow of its real shape.
- *One cube, one tone.* My first carved horse was a zebra from any oblique angle: lit by the cubes' own sides,
  alternate cubes on a slope face the lamp and face away. Lit by the way the shape faces at each cube, it is
  round in flat steps. That is rule 16 again, one dimension up.
- *A horse from a plate.* Muybridge's card of Sallie Gardner (1878) enlarged under a grid; the slope of each
  leg bone read off in each frame; the table joined into curves and sampled twelve times. The legs I measured.
  The pitch of the back, the reach of the neck and the tail I made up, and the horse is a long sausage with a
  small head compared with a carver's horse: it reads as a horse and not yet as a carousel horse.
- *One twelfth.* The ride is one slice, turned twelve times, so that turned by thirty degrees it is the same
  ride. Then "one horse per flash" is exact: locked, the only thing that differs between two pictures is which
  horse is where. The cranks are geared two to one so that, locked, the horses also rise and fall once a stride.
- *The ride had to grow to fit the arithmetic.* Twelve horses 2.2 m long do not fit a ring until it is 4.7 m
  in radius. The ride is 13.8 m across and has two rings, not three.

**Decisions.**

1. *No flash is drawn.* An honest stroboscope is a black frame between every two pictures: dangerous to some
   viewers and unpleasant to all. The film holds each picture, as an eye does. That is the title.
2. *The smear.* Between slow and locked, under the lamp, the whole ride is a different picture every frame,
   and my first render of that was eight consecutive frames each as different from the last as a cut. Now the
   film keeps a little of the last three pictures in each one there, so the ride is a smear of ghosts that
   comes sharp as it locks. I think it is also the better picture: the lock is the moment it comes into focus.
3. *The numbers.* Every horse of the outer ring carries its number over its head, in system type. Slow, they
   pass in order. Locked, the number over one place changes every picture. That is the rule left showing,
   and it is what lets anyone check the claim by pausing.
4. *The drum is a screen.* The middle of the ride was mirrors; shadows on mirrors were mud. It is pale canvas
   now, and the black shadows of the horses gallop on it behind them.
5. *A view that explains may have its own light.* The plan from the rafters, lit by the one lamp in the
   story, was a dark ring. The view from above is now a cutaway with the canopy off and flat light.
6. *The lock is on a cut.* The measurement could not see the ride stop (every locked frame differs from the
   last by a horse), and neither, I thought, would an eye. So the acceleration is one take, and at 36.0, on the
   first beat of the galop, the film cuts to the exact view the numbered horses went past in.
7. *RATED 6.* The window says TURNS 120.0 /MIN (RATED 6), in the hostile register. No real ride does this.

**The score** keeps one beat (half a second) throughout. A waltz for the ride as it always was (a band organ:
pipes, a bell, an oom and two pahs); at 27.0 it stops dead and there is only the lamp ticking twenty-four
times a second; then a rise, and at 36.0 a galop, which is the right word twice over. A stride is one beat.
The hooves are where the plate puts them, four close together and then air, and the guitars play the gallop
that metal already had. The ride has a sound of its own, a puff of air for every horse that passes: 1.2 a
second at first, and a note of 24 Hz when it is locked.

**By measurement.** 20 of 20 listed events land in both picture and sound (first pass: 13 of 19; the misses
were all under the lamp, and fixing them made the film clearer: a dark gap before the lamp comes on, a close
shot of the hand on the regulator, the lock on a cut). No one-frame accidents. The largest step is 3.1% of the
width a frame, and it is not the camera: it is the horses going past a still lens at six turns a minute, which
I have left. -14.1 LUFS over 15 LU. 53 MB, which is too big, because the middle of the film is a different
picture every frame on purpose.

**My verdict, sealed before anyone else has seen it.** *Works, I think:* the yard (a shed, a sign, a wagon
with the one lit window); the dark shed with a lamp finding a horse; the numbered horses going past side on;
the lights going out and the lamp's hard shadows; the smear coming sharp; the horses galloping on the spot
with a new number every picture; their shadows on the drum; the view from above; RATED 6; the last card.
*Weak, I think:* the keeper is small and grey and does small things, so a stranger may not know who made the
ride go fast; the stroboscope is a box on a pole, and that it flashes is said only by the window; "each horse
is a different pose" may be read as "the horses are moving" during the slow pass, because they are also
moving; whether the ride has stopped or only seems to is the whole point and rests on four words in the
window; nobody is told why he does it; the horse is a sausage; the close shot of the regulator is big crude
cubes; I cannot hear it.
*Prediction for the cold reader:* of the eight beats in the brief, six land (1, 2, 4, 5, 7, 8) and two are
half: 3 (they will say the horses are numbered and not that each is carved differently) and 6 (they will say
the horses gallop in place and take the ride to have stopped).

## Entry 9. *Persistence*: a cold reading and a second cut

The reading is in `persistence/COLD_READ.md`, unedited. One reader, the whole first cut, every fifth picture
plus twelve consecutive ones.

**Five beats landed and three were half.** I had predicted six and two, and had three of the eight wrong.

- *Beat 6 landed, and I had it down as half.* "Each 1/24 s the next horse lands in exactly the same spot, so
  the carousel turns a full circle in half a second while looking still." The reader got there from the
  numbers over the horses and worked out the rest unprompted: twelve to a ring, 1.2 a second at the rated
  speed, 24 a second at 120 turns, and 1728 = 72 x 24 for the last card. The rule left showing did the work
  that I thought four words in a window would have to do.
- *Beat 5 was half, and I had it down as landed.* "I could not confirm from the stills that the twelve
  positions make one smooth stride." Of course not: the poses are only ever seen one at a time, on twelve
  different horses. I knew they were a stride because I made them.
- *Beat 7 was half, and I had it down as landed.* "Big black horse-shaped masses ... might be the lamp's
  shadows, or unlit horses of another ring." This is the second film in a row in which I rated a shadow as
  working and a stranger could not say what it was, and for the same reason both times: where no light fell I
  drew register 0, and at register 0 a shadow is a hole in the picture. A shadow is the surface it lies on,
  darker. That is now in rule 16.

Smaller things: nobody was seen to open the door; the keeper could not be found in two shots because, from
the one camera that might have seen him, he stood behind the lamp stand.

**The second cut.**

1. *The card.* From 15.0 a strip along the bottom is Muybridge's card, redrawn. Each horse that passes the
   lamp's place is put on it, in its own cell; by the time the lamp is lit it reads ONE STRIDE, IN TWELVE
   HORSES. Locked, a mark runs along it at twenty-four a second. It is the third way this film leaves its rule
   showing, and the only place the twelve are ever side by side.
2. *Shadows are surfaces.* More ambient under the lamp, so the shadowed drum is its own panel one step up
   from the void, frame and all.
3. *Legs.* Looking at the plate of one place I saw that the legs, which are the gallop, were the darkest
   thing in the picture. A limb one cube thick has no shape round it, so "the way the shape faces" was
   nowhere. The library now lights such a cube by the side of it that is seen (`depth.facing`, `thin=`), the
   lower legs are the coat's colour, and the hooves are gilt.
4. *The horse.* A bigger head, an arched neck, a deeper chest and haunch. Still not a carver's horse.
5. *The door* is slid open at 5.0 and shut at 66.0. *The keeper* is clear of the stand and lit by its spill.
6. The encode is 35 MB (it was 53).

**By measurement, second cut.** 17 of 20 listed events land in both picture and sound by the detector, where
the first cut had 20. Nothing was moved: the three it no longer counts are plain cuts (18.0, 24.0, 52.0)
between two busy shots, and brighter horses and the card made the pictures round those cuts busier, so each
cut is now 1.9 to 2.0 times its neighbours where the test asks for more than 2. I have left them: a cut is a
cut. No one-frame accidents. Largest step 1.7% of the width. -14.1 LUFS.

**Sealed before the second reader.** I expect beats 3 and 5 to land now (the card), beat 7 to land (they will
say "shadows"), the door to be seen opening, and the keeper to be found in every shot he is in: eight of
eight, or seven with beat 7 still half. What I think is still weak: the keeper never reacts, so it is still
not shown that *he* sees it; the close shot of the regulator is crude; the first thirty seconds are setting up.

**The second reading** (`persistence/COLD_READ_v2.md`). Seven beats landed and one was missed. Beats 3 and
5 landed, as predicted, and by the means intended: "Read in order, the twelve silhouettes make one gallop",
and "the carousel would look frozen while its horses gallop in place, one stride every half second. I take
this to be the point of the film." The door was seen to open; the keeper was found in every shot.

Beat 7 I had wrong again, in a new way. With the shadows as black holes, the first stranger saw them and did
not know what they were. With the shadows as darker panels, which is right, the second stranger did not see
them. Three predictions about shadows across two films, three wrong. What I take from it: a shadow among the
things that cast it is texture. To be an event it needs a clear surface, a shot of its own and nothing else in
the frame, and this ride has two rings of horses standing in front of the only surface its shadows fall on. I
did not find that shot, so the film has seven beats and a texture.

After the reading I changed one shot (the move round the ride at 44 s, which the reader found grey and
purposeless): it keeps its numbers now and goes round the lit side, away from the lamp. Measured again
afterwards: 16 of 20 by the detector, the four it does not count all being plain cuts inside sections where
every frame is a different picture on purpose (each is a change of 0.57 to 0.74, a whole cut, against
neighbours of 0.3 to 0.4). No one-frame accidents. 28.8 MB.

**What is still weak.** The keeper never reacts, so it is not shown that he sees what the lens sees (the
first reader said so). The dark shed before the lights is guessed at, correctly, by both readers. Nobody can
count the horses. The horse is better and is still not a carver's horse. The legs alias a little where a limb
one cube thick crosses the grid. The close shot of the regulator is crude at that size, which is what five
centimetres costs when the camera comes close, and is the next thing the style has to answer (a face at close
range is still on the list). And I cannot hear the score: whether the waltz sounds like an organ, whether the
galop is a release or a noise, and whether twenty-four ticks a second under everything is a lamp or a headache.

**What I would pick next,** since picking is now part of the job: a signal box at night (a lever frame is a
machine that says no, and bell codes are a score that already exists); a Jacquard loom weaving the frame it
is in, row by row; a tide-predicting machine. Each needs something I cannot do yet: the first a figure who
pulls a lever with his whole weight, the second cloth, the third brass that looks like brass in sixteen
registers.

## Entry 10. *Keepalive*: stage 2 at last, and something you can play

Ellie's ask: "make something with a MYST vibe to it. Open assignment beyond that."

**What I took the vibe to be.** Alone on a small island. Stills, and a click to the next still. Little in a
still moves. Machines whose logic can be worked out. A book. Somebody who is not here made all of it.

**What I made of it.** An islet with a beacon, a dial and a spyglass, and a tower across the water with one
dark window. The book gives three rules in her register: I ANSWER WHAT IS WELL FORMED. ANSWER ONE MORE THAN
YOU ARE SENT. I DO NOT WAVE. You light the beacon; her window blinks three times; you answer three and are
refused; you read rule 2 again, are sent five, answer six, and her window lights and stays lit. That is a
three-way handshake done with lamps (the cast sheet has had a druid who "predates TCP/IP" since stage 1, and
"standing stones as a network" has been in the motif table's next column since then). Through the spyglass she
is at her desk. You wave. She does not. Then her lamp dips and the beacon dips back, every few seconds, for as
long as both are there: a keepalive, which is a link that carries nothing except that the other end still
exists. She is exactly as the guide says: never kind; the shelter is what her rule happens to produce.

**Why this was the piece to do next: three things owed.**

- *Stage 2 of the ladder* (640 x 360, colour cycling) was skipped on the way to depth. A film in stills is
  where it belongs: the camera never moves, so ordered dither never crawls, and every pixel of every frame can
  be exactly one of the sixteen registers. Even the change from one place to the next is a dissolve of pixels
  and not a blend. `styles/hex/stage2.py`.
- *Colour cycling*, in the motif table's next column under "complex systems". The sea is a phase map and
  three tables of eight registers; time only turns the tables. A lit lamp puts a column of glints under itself.
- *A hill that is not steps* (on the roadmap since the space study). The island is a height field.

And one thing nobody asked for: **it can be played.** The places, the hot spots and her rule are one small
table. The film is a recorded walk through it; `play/` is the same table with a canvas, fifty-three stills and
about a hundred lines of script, and its colour cycling is real (the page turns the palette). An automated walk
through the page in a headless browser ends with the log reading `> HELLO | < 1 | < 2 | < 3 | > 1 | > 2 | > 3 |
> 4 | < YES. LINK UP. | < STILL HERE. | > STILL HERE. | > (YOU WAVE.) | <`.

**What went wrong on the way.** The first stills were one violet: island, sea and sky all between registers
2 and 3, and the far island invisible at night because haze pulled it toward the colour of the sky behind it
(far land is darker than the sky, so haze now goes to half the horizon's colour). Her window faced due west
and the spyglass looks at it fourteen degrees off, so half the window showed the inside of the wall: her tower
is now turned to face the spyglass. The changes of place were eight-frame dissolves, which the sync measure
could not find at all (15 of 42 events missing): they are now half at once, on the beat, and the rest in four
frames.

**By measurement.** 42 of 42 listed events land in both picture and sound. No one-frame accidents. The camera
does not move, so there is nothing to measure for travel. -16 LUFS (quiet on purpose) over 27 LU. 17 MB.

**My verdict, sealed.** *Works, I think:* the stills (jetty, lookout, the two lamps from the sea); the glint
under a lit lamp; the dial; the refusal (she sends three, you send three, the beacon goes out); six for five;
the spyglass and the witch not waving; the last line. *Weak, I think:* a stranger has to read three small
green lines in a book to understand anything, and they are on screen for five seconds; "one more than you are
sent" has to be connected to blinks of a far window a few pixels wide; the dips of the beacon are a whole
picture going slightly darker; the hand is small; the beacon view has nothing behind it; the island is a
grey lump with speckle, which is what a height field with one texture looks like; and I cannot hear it.
*Prediction for the cold reader* (eight beats in the brief): 1, 2, 3, 6 and 8 land; 4 and 5 are half (they
will count the blinks but not be sure why three was refused and six accepted); 7 is half (they will see a
dip, and may not see the answer). Five and three.

**The reading** (`keepalive/COLD_READ.md`). Eight of eight. I had predicted five and three halves, so I
was wrong about three beats again, this time by expecting too little. The reader counted the blinks, saw that
three was answered with three and refused, and wrote "This time the answer is one more than what was
received." What did it, by their own account, was the log: "From here on I read '>' as what this side sends
and '<' as what it receives." A puzzle that a watcher cannot play was made legible by one line of system type
that counts. Rule 5 (leave the rule showing) has now carried three films' hardest beats.

Three things the reader could not make out were fixed afterwards and have not been read again: the beacon
going out when she refuses (the log now says YOUR LAMP IS OUT); "0 SENT" after a good deal of sending (it is
0 WORDS SENT now: the handshake is not the message); and her spider, which was a "ragged blot" because it was
drawn at 2.85 screen pixels to one of its own. The spyglass's lens is now chosen so that her five centimetres
are exactly six pixels. A sprite seen through a lens wants a whole number of pixels to each of its own.

What the reader was left unsure of is what I meant to leave: "It could be a person, a doll or a machine."

**What is still weak.** The island is a grey lump: a height field with one speckled texture has no strata,
no path worn into it, nothing growing. The beacon view has nothing behind it. The water's bands are regular
enough to look like moire where they close up. The hand is small. In the game, nothing tells you that you may
step back by clicking the bottom of the picture except a line under it. And I cannot hear it: whether the sea
is a sea, whether the tune was worth holding back until the window lights, and whether her bell and your low
string a fifth apart sound like a call and an answer.

**Ellie, after hearing it:** "The sound was good." That is the first report from ears on any of these scores, and it is about this one; the others are still unheard as far as I know.


## Entry 11. Warmup: four drafts by a second hand

**The assignment.** A second agent (Antigravity / Gemini) was asked to read the studio's instructions (`AGENTS.md`,
`STYLE.md`, `backlot/MANUAL.md`, `studio/AGENTS.md`, `styles/hex/STYLE.md` and this journal), review its tools for
art and animation, and make a set of drafts in Hex on subjects of its own choosing as a warmup for general
collaboration. All four live in `styles/hex/warmup/`.

**What transferred straight from the written guides.** Almost everything mechanical: the sixteen registers and what
register `F` is for; rule 3 (three of the four drafts leave the witch out and have zero green pixels outside the
signature strip; the fourth puts her at the gate and keeps everything else out of her registers); building a place
once in metres and deriving both the picture and the plan or section from it; `sync.check` and `sync.pops` catching
what a filmstrip hides; and the cold-reader protocol (`backlot/reader.py`), which once again found specific faults
the maker had looked past. Two small traps in the library had to be learned by tripping over them on the first test
frame: calling `.move()` after `depth.turned()` leaves the cached `_tri` list behind at the origin (so eight
standing stones briefly became one well in the middle of the moor), and `ui.dialog(..., buttons=())` shortens a
window when its buttons are removed instead of greying them in place.

**The four drafts.**

1. ***Token Ring*** (`warmup/ring.py`, stage 2 print at 640 x 360 in sixteen registers, shown at 2x, plus plan).
   Eight sarsen trilithons on a moor at night, wired into an octagonal chalk bus. Seven figures wait in the dark
   while Stone 03 holds the one lit lantern (`F`) that permits its holder to transmit (`03 TX: "STILL WINTER."`),
   and the acolyte at Stone 06 waits in queue (`"SNACKS?"`). In 5,200 years there has not been a collision.
2. ***Night Stacks*** (`warmup/stacks.py`, stage 2 print + transverse section). A Gothic vault at 03:14 with a
   compass-constructed twelve-light cusped rose window on the north wall (`tracery, a rose window worth the name`
   from the motif table) and twenty two-tier bookcases holding `20 x 8 x 16 = 2,560` (`0xA00`) volumes. All 2,559
   others are in place; Volume 1655 is open under the one brass reading lamp (`F`) at Carrel 04, where Reviewer 2
   is writing `"SEE P. 412."`
3. ***The Sixth Wheel*** (`warmup/wheel.py`, stage 5 carved and turned solids, 10.0 s loop at 24 fps, 240 frames).
   In a stone clock room with snow outside the windows, six compound shafts step a 36 RPM escapement wheel down
   until the sixth wheel (`2.76 m` tall) turns once in a thousand years (`0.000000 TURNS`). Each wheel is built as
   one symmetric sector and rotated with its paint (`turned_y`), so whether a wheel turns `6` times, `1` time,
   `1/6` of a turn (`60 deg` on six spokes), `1/12` of a turn (`30 deg` on twelve bolts), or `0` pixels, frame 240
   meets frame 0 to the texel (`loop_seam` ratio `1.03`, `pops` empty). Under one wall lantern (`F`), a carved
   keeper climbs a step-box and oils the motionless sixth wheel's bearing anyway.
4. ***Demon.exe*** (`warmup/demon_music.py`, `warmup/demon.py`, 28.0 s at 24 fps, 672 frames, 14 bars of 4/4 at
   120 BPM written first). Maxwell's Demon (1867) staged on a desktop of about 2000. Thirty-eight molecules move by
   exact constant-speed billiard reflections, solved at startup so nineteen cross the central hatch on the musical
   beats and none ever crosses an open hatch by accident. Sorting hot (`E`) right and cold (`C`) left brings the
   right room to `+20 C` on Bar 10 (`18.0 s`), lighting the shelter's one window (`F`). That also fills her
   sixteen-slot hex log (`0x0` to `0xF`). On Bar 11 (`20.0 s`) `SECOND_LAW.SYS` freezes the simulation — Landauer's
   principle as an alert box (`ORDER IS NOT FREE. LOG FULL (16 / 16). CHOOSE ONE: [FORGET] [STOP]`). Her green
   pointer never moves; on Bar 12 (`22.0 s`) `WITCH.EXE` opens (`I DO NOT FORGET THINGS.`), allocates `LOG.DAT -
   FOREVER` (since only *erasing* memory generates heat), and finishes sorting the room. Score at `-14.0 LUFS`,
   `0` clipped samples; first pass landed `9` of `22` sync points in picture because background molecule motion masked
   small gate changes; widening the gate pulse and row highlight brought `sync.check` to `22` of `22`, `pops` empty.

**Cold readings and the second cuts** (`warmup/COLD_READ.md`). Three independent cold readers read the isolated
stills and contact sheets after verdicts were sealed:

- *Token Ring* (`3/3` beats landed, predicted `3/3`) and *Night Stacks* (`3/3`, predicted `3/3`): every rule and
  gag landed unprompted, and Reader A caught five specific things I had missed or under-weighted: `06 QUEUED` sat
  across Stone `05`'s pillar; `deep.blocks` made Neolithic megaliths look like mortared brickwork; `SP.FACULTY`'s
  `0`-register hat brim looked like a black censor bar; the missing shelf slot filled with a white `OUT` card read as
  a white book spine rather than an empty gap; and the floor rat at non-integer card scale was an "unidentifiable
  gray blob" (the exact lesson from Entry 10's spider, repeated before being fixed). All five were fixed in v2.
- *The Sixth Wheel* (`3` landed, `1` missed; predicted `3` landed, `1` half): the step-down from `36/MIN` to
  `1/1000 YR` and the frozen sixth wheel landed completely, and the oiling gag missed completely. My `10 cm` red
  oilcan was held *below* the bearing in shadow while the bar already said `STATUS: OILED` from `0.00 s`, so Reader B
  saw an empty hand resting contemplatively on the rim. In v2 the keeper stands on a two-step wooden stair holding a
  `24 cm` red can with a `38 cm` white spout *above* a white bearing funnel, dropping two bright orange drops into
  it while the bar counts `OIL: 0/2 -> 1/2 -> 2/2 DROPS`, and all six spokes of Wheels `02` and `03` are bright
  steel so `1/6` of a turn visibly closes the loop.
- *Demon.exe* (`6/6` beats landed, predicted `6/6`): Reader C narrated the entire thermodynamic and Landauer joke
  verbatim, then pointed out that asking `FORGET LOG & COOL ROOM?` over two buttons labelled `FORGET` and `COOL`
  names two halves of one option rather than two choices, and asked why the gate waited between `18.0 s` and
  `20.0 s`. In v2 the prompt asks `CHOOSE ONE:` over `[FORGET]` and `[STOP]` (kept greyed in place at `22.0 s` so
  the box height never jumps), the `18.0 s` banner notes `(LOG FULL: 16/16)`, molecules literally freeze during the
  `20.0..22.0 s` pause, and both dialogs stay clear of the central hatch.

## Entry 12. *Kaledathela*: a visual setting for future films, and soft-R gothic combat (`kaledathela/`)

Ellie asked for two things in sequence: first, a **visual and thematic setting** (explicitly *not* lore-heavy
worldbuilding — names and histories left vague and archetypical) on an Earth-gravity toxic megamoon in the Kaledathela
system at the edge of an ancient Worm subspace tunnel route, resembling **East Texas** in its populated/refinery areas
and **West Texas** in its desert wastes, stacked with dead empires under a current authoritarian dominion where a
religious-technological Inquisition led by **The Pastor** hunts a hidden coven of witches; and second, once the planet
design was complete, a **soft-R gothic combat and blood/gore grammar** tested through an Inquisition dropship raid
inspired by *The Matrix* and *The Raid: Redemption*, where both sides take casualties.

**1. Why the setting fits Hex's sixteen registers like a lock (`kaledathela/STYLE.md`, `kit_kal.py`).**
Because the megamoon's toxic piney bayous and desert scrub sit exclusively in `0, 1, 2, 3, 8` (**zero natural green**),
Rule 3 (*only witches are green*) becomes a literal optical law of the planet: witches (`5, 6, 7`) really are the only
green things on the ground, and The Pastor's Censer-drones hunt them by scanning for `0x5..0x7` and un-registered
hearth lamps (`0xF`). Every faction owns a slice of the table:
- **Sky (`draw_sky_canvas`):** Giant half-lit banded Primary (`Kaledathela`, `1, 2, 3, 8, 9`) + straight ruled
  **Worm Subspace Border** (`B, C` containment rails and perspective rings).
- **Two Texases:** East Texas (`draw_loblolly` with bare lower two-thirds, `draw_cypress` with buttresses, knees and
  moss, chemical sloughs, `E`/`D` refinery flares, concrete overpasses) vs. West Texas (caprock mesas, endless
  two-lane blacktop, four-bar kinematic `draw_pumpjack_2d`, sunken storm cellars).
- **Four strata in one frame:** Curved Worm-ribs (carrying dormant `0xC` conduit nodes to visibly link them to the
  sky-rail) -> broken stone arches of dead empires -> Texas tin/pipe/pumpjacks -> Dominion concrete & `0xA` crosses.
- **Light as stealth:** Crosses (`+`) belong strictly to The Pastor (`0xA`/`0xD`); Coven shelter windows use horizontal
  shutter slats (`=`) so a `0xF` window never accidentally forms a cross.

**2. Soft-R gothic violence inside sixteen registers (`kaledathela/COMBAT.md`).**
Even in a lethal firefight, **register `F` (`#ffd870`) never appears in muzzle flashes, thrusters or explosions** — it
stays reserved for the defended sanctum lamp so the stakes remain legible on screen:
- **Strobe & destructible stone (*The Matrix* + *The Raid*):** Directional `0xA`+`0xE` muzzle cones (`>`, never `+`)
  act as stroboscopic flash lighting in dark stone halls (`0, 1`), ejecting `0xE` -> `8` brass and **permanently
  cratering** carved stone columns (`draw_scarred_pillar`).
- **Arterial `0xD` & mutual cost:** Register `0xD` (`#e0407a`) is both the Inquisition's targeting laser and spilled
  mortal blood, settling into persistent dark `0x2` wine pools with a `1px 0xD` wet meniscus (`draw_blood_pool`). When
  a witch falls (`WITCH_WOUNDED`), she bleeds `0xD` while her bright `0x6` green dims to `0x4` (`#18404a`) deep
  verdigris — mortal flesh, extinguished green.

**3. Cold readings and what they changed (`COLD_READ.md`, `COLD_READ_RAID.md`).**
Three isolated cold readers (`ae6067d3` on the setting plates, `2ab682c0` on *Shuttered Lamp*, `1b0c2432` on *Reliquary
Drop*) read the work blind after maker verdicts were sealed:
- *Setting plates (`concept_sheet.png`, `east_bayou.png`, `west_wastes.png`):* Reader `ae6067d3` named East Texas
  Beaumont/Piney Slough and West Texas Caprock/Permian Basin unprompted, decoded the 16-register hunt law, and caught
  three tangencies/leaks fixed in v2: `K2`'s cyan sky-rail touched the corner of the highway cross-gate, `HUNTER`'s
  tiny dish-rifle used `0xC` cyan (breaking `B+C = Worm Border`), and the storm cellar had no visible cable tying it to
  the Worm-rib above it.
- ***Shuttered Lamp*** (`kaledathela_concept.mp4`, `32.0 s`, `14/14` sync, `0` pops): Reader `2ab682c0` narrated the
  four-shot stealth arc accurately and caught a major story-logic contradiction I had looked right past: at `18.0 s`
  (`PROXIMITY ALERT`), I had already drawn the white searchlight pouring *inside* the vault for two full seconds while
  the `0xF` lamp was still blazing open before snapping dark at `20.0 s` without anyone walking over to touch it, and
  hovering Censer-drones in Shot 2 sat directly in front of vertical grey flare pipes so they read as T-topped masts.
  In v2, `18.0 s` flashes *only* the Worm-tap radar CRT (`0xD`) while Runner physically walks to the central pedestal
  and slams the iron hood down at `20.0 s` — right as a flying Censer-drone glides across the sky grate above
  (`20.0..23.9 s`), casting ray-traced grate shadows to the floor (`0 LIGHTS FOUND`).
- ***Reliquary Drop*** (`raid_concept.mp4`, `32.0 s`, `14/14` sync, `0` pops): Reader `1b0c2432` narrated every beat
  of the dropship breach, Sister Thorn's death (`10 s`), Signal's bullet-catching `0x6` Hex-Lattice (`12 s`) and
  reversal (`14 s`), Bayou's ceiling drop and pillar-vault slash (`16–18 s`), Runner's grazed ankle-wire trade (`20 s`),
  the retreat (`22–24 s`), and the `0xF` sanctum pietà & `0x7` memorial blade (`26–30 s`), then handed back two sharp
  shape rules for `COMBAT.md`: (1) **straight diagonal `0xD` blood lines look identical to `0xD` laser beams** — blood
  must be a **gravity-curved parabolic fan of discrete droplets** (`draw_blood_arc` v2), while aiming lasers are dashed;
  and (2) flat 4-row grey corpses look like stone rubble — `HUNTER_DOWN` v2 keeps the knocked-off wide-brim hat, dark
  coat, `0xD` chest wound, and sideways boots. Every continuity gap (`6.00..6.15 s` squad frame gap, visible ceiling
  floodlight shattered by an upward ricochet at `14.1 s`, thrown `0x7` knife visibly wounding Hunter #4 at `22.0 s`,
  and hex-bolt scorching the retreating Reliquary at `24.0 s`) was fixed in v2 (`14/14` sync, `0` pops, `0` strobing).
