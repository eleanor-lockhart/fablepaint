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

**Fig. 3, the research vessel *Tenure* and a posse.** A cathedral as a starship: the rose window is the drive,
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
