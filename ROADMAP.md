# Roadmap

What is queued, in the order Ellie asked for it. Each study has goals and a test that can fail. Tick things
off here; the detail lives in each folder's journal. The style all of it serves is in `STYLE.md`.

## Done

1. **The opening sequence** (`world/night-service/op/`), as a prototype: storyboard reviewed cold by three
   agents; ten units and a theme; sync measured; v1 published (tag `op-v1`); reviewed by an independent critic
   (5/10); v1.1 from the review; cold reading (4 of 6 story beats land, was 2); retrospective.
2. **Stock-take after the opening:** the house style written down for the first time (`STYLE.md`), a screen
   style guide for the film (`world/night-service/STYLE.md`), and the instruments that earned their keep moved
   into the library (`lab.bloom(protect=)`, strict `draw.font`, `backlot.sync`, `backlot.reader`).

## Now: study 2, space (`studies/space/`)

Everything so far is seen square-on from the side, at sizes and positions chosen by feel. The study is to think
a physical place out first, model it once in real units, draw it as plan, elevation and section, build it as a
3D set, and derive every picture and camera move from that model.

| goal | the test |
|---|---|
| **Think it out.** Before computing anything, say where the horizon falls, how tall a figure stands and what hides what, from a camera described in words | guess-against-projection sheets: my written predictions scored against the computed frame. Baseline in journal entry 0; by the end, horizon within 3% of frame height and sizes within 20% |
| **One model per place.** Plan, elevations, section and the 3D set all come from the same data, in metres | the drawings regenerate from the model; my projection agrees with Blender's camera to a pixel |
| **One sky.** The moon and stars have a direction for the night and a size for the lens | the moon's bearing and height are the same numbers in every shot; its disc is half a degree in all of them |
| **Lenses on purpose.** A shot is a camera position, an eye height and a focal length, marked on the plan | a lens sheet (one subject held the same size at five focal lengths) and a camera plot for every scene |
| **Motion in depth.** A camera moving on ones through a set; a figure walking toward the lens with planted feet | `sync.travel` under 1% of the width per frame; foot slide under a pixel; size goes as one over distance |
| **It reads.** A stranger can tell where things are | a cold reader, given three shots of a place, lists what is where; at least 80% of its left-of, nearer-than and taller-than relations match the plan |

First place: **Ebb Landing**, because the opening's three spatial questions live there (where is the moon, how
big is No. 4 beside a person, what does a camera see moving along the pier). Then Tern Point, the tower on
Mount Vesper and the *Kittiwake*'s car deck.

## Next: study 3, bones

Research how rigs are built and driven (hierarchies, FK and IK, constraints, skinning and deformation, curves,
secondary motion) and take `backlot.figure` beyond rigid paper parts.

| goal | the test |
|---|---|
| Things hang, lag and swing: a lantern, a coat, a cable | a pendulum prop driven by the arm; overlap measured on an arc sheet |
| Bodies that differ: age, build, carriage. Hands | the six of the cast told apart in silhouette *without hats* by a cold reader |
| Acting, starting with the hardest two seconds in the opening | "a man falls asleep on his feet and catches himself", read as that by a cold reader from frames alone |
| Turnaround: a figure that is not only in profile | three-quarter and front views off one rig, placed in a set from study 2 |

## Then: study 4, finish

How to paint a figure that moves: flats and shadow shapes, line, texture that stays put on the body, costume
detail, faces.

| goal | the test |
|---|---|
| A face that survives being forty pixels tall | expression sheets read cold: which of six is tired, afraid, amused |
| Texture and costume that travel with the body | no swimming, measured on a tracked patch |
| Close-ups that hold | a cut-in from wide to close on the same figure without a change of manner |

## After that: version 2 of the opening, as the exam

Known and waiting, from the review: Orrin's doze (stage him lit, facing us; `sync.pops` also finds a one-pose
flicker in it); the light code as now written (the dead warm, Continuity a strip); 24 frames a second with the
camera on ones; bodies, hands, follow-through; No. 4's insulator horn and lattice shoulders; one model per
prop and per place; a verse tune and a chorus that peaks at its end; uneven cuts. Targets: six of six beats
read cold; `sync.pops` empty; no strobing frames; an outside critic at 7 or better. And what somebody with
ears says about the theme (five questions in `world/night-service/music/JOURNAL.md`).

## Standing rules

Every asset is made in code. References are for looking and measuring. OpenArt only as reference, never in a
finished piece. The Muybridge plates stay out of the public repository.
