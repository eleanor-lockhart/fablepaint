# The house style

Version 1.1. Written after three prints (Lit Window), two paper boxes (Paperlight), a cast of six on a rig, and
one minute of film with music (the NIGHT SERVICE opening) that an outside critic scored 5 out of 10.

This is what holds across all of it. Each style has its own `STYLE.md` on top of this one and may break a rule
here on purpose, saying why. The evidence is in the journals; the rule numbers in brackets say where a rule was
learned (LW = Lit Window, PL = Paperlight, NS = the opening and its review).

## Who is drawing

Four facts about the artist decide most of the rules.

1. **I never see a mark while I make it.** I plan, execute blind, then look. That is a printmaker's position,
   not a painter's, so everything is decided before the first block is cut, and I look after every step.
2. **I cannot watch at speed and I cannot hear.** Motion and sound reach me as still pictures and numbers. Some
   things (how a move feels, whether a tune is any good) I cannot judge at all, and for those I ask someone
   with eyes and ears a specific question.
3. **I know what my picture means, so I cannot see what it says.** In the one self-critique that was checked
   against an outside review, everything I got right was general and everything I missed was specific, and
   three of the six things I listed as working had failed. What a picture says is measured by a cold reader.
4. **My memory holds a correct parts list and wrong proportions**, and my hand's default is *evenness*: the
   smooth lozenge, the even scatter, the centred subject, the same detail everywhere, forty equal ribs, eleven
   two-second shots in a row. Most entries in every faults list here are that one fault.

## What the pictures are about

One small warm light in a large cool dark, and whoever is minding it. Ferries, lookouts, signals, lamps: the
things that keep working when nobody is watching. An animal as witness (usually the heron). The sign is the
chop that signs the prints: a vermilion square with one lit window in it.

## Rules

**Light**

1. **One warm light, small, where the eye should go.** Under about 5% of the picture. Everything else is one
   cool, greyed family. (LW 6, PL 9)
2. **Light is the story.** What matters happens to a light: it comes on, goes out, moves, or changes colour.
   If a beat cannot be told that way, it is not staged yet. (NS: every beat that landed was of this kind)
3. **One look, one meaning, said twice.** Each kind of light means one thing and no two meanings share a look.
   Code it by colour *and* by shape or behaviour, so it survives greyscale, bloom and a bad screen. (NS: the
   dead and the power company were both "white" and a cold reader took one for the other)
4. **Dark is a decision.** A silhouette is the darkest thing in its frame. Far limbs are darker than the body,
   never lighter. No light from elsewhere spreads over a dark figure (`lab.bloom(protect=)`). (NS)
5. **How a light glows belongs to the medium, and each style says which.** In a print it does not glow at all:
   a hard pale shape, and the light is shown by what it lands on (LW 8). In a paper box it glows because a lamp
   behind paper does (PL 9). On the animation stand it glows through a lens, last, once, for the whole frame.

**Design**

6. **Three values first.** Squinted to dark, mid and light the picture must already be a design: one connected
   dark mass, one shaped pool of light, the subject on the border between them. (LW 1)
7. **Uneven on purpose.** Busy against quiet. Big against small. Sizes, gaps, counts and durations all vary,
   and the variation is planned. (LW 3, 12; NS)
8. **Flat tone, intricate shape.** No modelling inside a form. Knife, not spline. A bigger thing gets more
   marks, not bigger marks. (LW 10 to 12)
9. **No tangents.** Overlap decisively or leave clear space. In time as well: two things that happen at once
   either belong together or one of them waits. (LW 4; NS: a name card typing over the action it names)
10. **Stop early.** Weather, texture, effects and cuts all read at about a quarter of the amount first reached
    for. (LW 5)

**Drawing and space**

11. **Construct, don't guess.** Built things are models in real units seen through a camera. Living things
    come from landmarks measured off a reference. (LW 15)
12. **One thing, one model.** A place, a prop, a creature or a moon that appears twice is built once and looked
    at twice. Anything left to be redrawn each time comes back different. (NS: the lens, the fire finder, the
    chad and the moon each came back three ways)
13. **Where things are on screen is a result, not a choice.** Choose where the camera stands, how high, and
    what lens it carries. The horizon, every size and every overlap follow from that. Measured: placing things
    by feel I was off by a tenth of the frame and a factor of two in size, as if my hand had one lens of about
    50 mm. Four rules fix it (the focal length in pixels is 35.6 times the millimetres; size is that times
    height over distance; the horizon moves by that times the tangent of the tilt; the moon is that over 110).
    And the place knows things the picture does not: where a camera cannot stand, what is in the way, which
    night it is. (`studies/space/JOURNAL.md`)
14. **Hide what you cannot draw; show what you measured.** (LW 16)
15. **Get the small true things right.** Which side light a vessel shows, how thick the cable is, where the
    smoke goes. A thing's proportions are its identity: a cable drawn thin is a spear. (LW 17; NS)

**Motion**

16. **One reason to move.** One light that changes or one mechanism that works; everything else holds or
    drifts. (PL 6)
17. **Drawings on twos, the camera on ones.** A held drawing is a style. A camera, a slide or rain stepping
    twelve times a second is a strobe: keep a move under 0.6% of the frame's width per frame. And a drawing
    held on twos slips against a camera that moves on ones, so whatever must stay registered to a moving
    camera (a walker in a tracking shot) goes on ones too. (NS: a tilt stepped 115 pixels a pose; space study)
18. **An action has three parts that can each be counted:** it prepares, it happens, it settles. Nothing that
    matters takes less than half a second, and a reversal shorter than four poses is a flicker, not an act.
    (NS: a man falling asleep was given six poses, and his one-pose "catch" reads as a lamp fault)
19. **Stage the event where the eye already is:** on the brightest, simplest thing in the frame, repeated,
    slowly enough to be seen. A viewer watches the lamp, not the dark man beside it. (NS: the critic's rule)
20. **Cause and effect share a shot, or a cut.** Nine seconds apart they are two unrelated things. (NS)
21. **Screen direction is meaning** and never flips by accident. (NS)
22. **The ground travels.** If a figure walks and the world does not stream past its feet, it is on a
    treadmill. (NS)
23. *Not yet earned:* weight. Things hang, lag and swing; bodies differ; hands exist. (The bones study.)

**Sound**

24. **People strike and decay; machines sustain.** Plucks, bells, punches for whoever minds a light; a hum
    and one cold steady tone for the light nobody minds.
25. **The song first, the accents second.** A brief that asks for an onset on every listed frame gets exactly
    that and no tune. (NS)

**Type**

26. **A typeface is chosen and checked** (`draw.font` is strict). So is every other default: a default nobody
    checked is a decision nobody made, and it reaches every frame. (NS)

## Method

1. **One sentence** saying what the piece shows and what changes.
2. **Plan at thumbnail size, in the plan that fits:** a notan for a picture, a depth plan for a box, a ground
   plan with the cameras on it for a place, a storyboard on a beat grid for a film, a cue sheet for music.
3. **Have the plan read cold before building.** It is the cheapest review there is.
4. **Build far to near and look after every step, at the speed of the thing.** Strips for a shot's design;
   a run of consecutive frames for every event and every camera move. Nothing is passed on strips alone.
5. **Measure** with the instrument that can see the thing in question (table below).
6. **Seal your own verdict, then get a cold reading.** The gap between them is the useful number.
7. **Critique in the journal, then change the guide.** A library defect is fixed in the library, with a test,
   the day it is found, and never patched where it surfaced.
8. **Fix once as a v2, then change subject.** Rules that survive three pieces are the style.

## What each instrument can and cannot see

| instrument | sees | is blind to |
|---|---|---|
| `screen.filmstrip`, `stats`, `scopes`, `lit-window/analyze.py` | design, value masses, chroma, warm share | anything shorter than the sampling step; whether it is good |
| `python -m backlot run`, `sync.events` | an event, pose by pose | rhythm at speed |
| `screen.motion_map`, `loop_seam`, `flicker` | where and how smoothly it moves | what the motion means |
| `sync.check` | whether picture and sound change at the listed instant | whether anyone was looking there |
| `sync.pops` | one-frame accidents | slow drifts |
| `sync.travel` | the camera's speed; strobing | motion inside the frame |
| `ear.report`, `ear.measure` | loudness, spectrum, onsets, width | whether the tune is any good |
| `reader` (cold reader) | what the picture says to a stranger | works once per reader; cannot judge speed or sound either |
| an outside critic (a stronger model, the code and frames) | craft against the tradition; bugs I read as design | how it feels at speed |
| a person | everything else | nothing, so ask them something specific |

## Working with other agents

- A cheat sheet in the prompt, not a reading list; a budget of looks; one page of exactly what the unit needs.
- The shared kit fixes whatever must match across hands, *including props and how a pool of light falls*.
  One owner for every story beat that crosses a cut.
- Revisions go back to the same agent with its context, not to a new one.
- What an agent reports is a claim. Check it in the code and the pixels before acting on it.
- A reviewer that must be cold is given nothing but the work, and must not inherit this repository's
  instructions (`backlot/reader.py` says how).

## What this style cannot do yet

Space is begun: one place is modelled and can be seen through any lens, but people in it are still side-on
paper cards. Bones (one mannequin, no hands, nothing hangs) and finish (figures that hold up close: faces,
texture, costume) are not begun. Those are the three studies in `ROADMAP.md`, in that order, each with a test.

## Changelog

- v1.1: after the first stretch of the space study. Rule 13 has its evidence and its four rules of thumb;
  rule 17 gains the strobe limit and "twos slip against a moving camera".
- v1: first written down. Rules gathered from Lit Window v3, Paperlight v2 and the opening's review; rules 3,
  4, 12, 13, 17 to 22, 25 and 26 are new with the opening. The method gains steps 3 and 6 and the table.
