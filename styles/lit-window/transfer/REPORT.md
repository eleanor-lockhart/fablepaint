# Cold-start test: can the notes alone teach the style?

A fresh agent that had never seen the style being developed was given only the files on disk
(`STYLE.md` v3, the kit, the three prints, the references) and asked to make one print of a
subject of its own choosing, then to report on the notes without being polite.

**Result:** `t1_v2.png`, *Red board, rain*: a block signal holding red over empty track on a
shore line, its light lying on the wet rails, a coyote stopped to look. It chose its notan by
measurement (variant B, 43 / 38 / 19, over the "obvious, dramatic" one), built the track and
signal through one camera in metres, measured ferns, signal and coyote from photographs, and
kept the light as a hard shape whose effect shows only on the rails.
Measured: dark 45, mid 39, light 16; chroma 6.8; warm 0.4%; detail 7.0%.

## What transferred from the text alone (its words)

Choosing the notan by rule and not by drama; no glow on the light; no tangents; line kept
rare; hiding what cannot be drawn; small true things (the signal on the correct side of the
track it governs); the measure step, "which caught a colour fault I had looked straight past".

## What it had to learn from the example pictures and scripts instead

How to build a notan sheet; what counts as dark / mid / light (thresholds are only in
`analyze.py`: L* 35 and 65); the actual palette (hex values exist only in `prints/*/common.py`;
told only "one hue family, greyed" it greyed everything and v1 came out at chroma 4.8); what a
"pigment" is for the nine-pigment rule; the lit-plane and knife-not-spline rules; pixel caps for
marks; the camera-plus-subject-file workflow; how much rain is "a quarter"; reflections on
anything that is not water; layer mechanics and the finish, seal and title code.

"The faults list did not stop me making evenly spaced marks or too much rain, even though I
read it before printing."

## Its complaints, condensed (to fix in a v4)

Guide: rule 1's "none under 15%" is broken by the guide's own prints; value thresholds and
pass/fail ranges are not in the guide; the detail range is not reachable by any print so far;
no palette table; no lower bound for the warm accent; "pigment" undefined; rule 8 assumes a
yellow lamp; the seal is an unruled second red and its placement is inconsistent; reflection
vocabulary covers water only; no counts for weather; three different numbers for wood grain;
no pixel caps stated; rule 15 does not explain how a gridded photo becomes a subject file,
whether `conifer()` counts as measured, or what to do when photo and camera viewpoints differ;
`fetch.py` unmentioned; no notan sheet size; `finish()` comes before any v2 pass, so new blocks
land above the margin; `hz` undefined in the quick reference; title conventions only in
scripts; unclear whether a visitor writes in the journal.

Kit: `rain()` says sheaves but scatters evenly, angle and length undocumented; `conifer()`
makes blots under about 25 px and see-through stands at distance; superseded `fir()` and
`snowload()` are still there unmarked; `ramp()` misorders mixed plain and positioned stops;
`extrude()` does not say which wall is which; no helper for placing a camera; `window()` must
be re-called in every script; many short global names can be clobbered.

Tools: `fetch.py` writes `SOURCES.md` into the current directory and returns titles only;
`analyze.py --crop` is not matched to the image window; `sheet` and `stats` split values
differently. Manual: `new --force`, `view --max`, `view -o` undocumented.
