# Persistence: the brief, written before the picture

Seventy-two seconds, 24 frames a second, 1728 pictures. One beat is half a second (twelve frames) from
beginning to end. The first thirty-six seconds and the last twelve are a waltz (three beats, a bar is 1.5 s);
the twenty-four seconds in the middle are a galop (four beats, a bar is 2 s). Every cut is on a bar line.

## What it is

A showman's winter quarters, at night, in snow. In the shed is a big set of gallopers: a roundabout with
twenty-four wooden horses in two rings of twelve. Once a winter somebody runs it, for nobody, to see that it
still runs. The keeper puts the lights on, the organ plays its waltz, and the ride goes round at six turns a
minute as it always has. Going past him one at a time the horses turn out to be carved differently, each a
little further through a stride than the one in front, and they are numbered 01 to 12.

He wheels a stroboscope up to it (a lamp that flashes twenty-four times a second, which a mechanic uses to
look at a machine while it runs), puts the lights out, and opens the regulator. The ride goes faster than it
was ever meant to. Under the lamp it seems to slow, to drift backward, and to stop. It has not stopped. Two
turns a second is twenty-four horses a second past any one place, one horse per flash, and each is the next
drawing: so the roundabout stands still and the horses gallop. Their shadows gallop on the wall. Whoever
carved them a hundred years ago did it on purpose, and it could not be seen until tonight.

He closes the regulator. They are wood again. He goes out, and the shed has a lit window in the snow.

The structural gag, played straight: **this film is the same machine.** It is 1728 pictures and none of them
moves. The last card says so. And the flying gallop, all four legs flung out, which is how every carousel
horse was carved, is the pose Muybridge's photographs showed no horse ever takes; these twelve are carved from
his photographs instead.

No witch in this one, so nothing is green. Rule 3 is kept by leaving her out.

## The arithmetic, which the picture must keep exactly

- 12 horses to a ring, 30 degrees apart. Behind each horse is the one a twelfth of a stride later.
- Locked: the ride turns exactly 30 degrees a frame. That is 2 turns a second, 120 a minute; the beat is 120
  a minute; a stride is twelve frames, one beat.
- Everything on the ride is built as one twelfth and repeated twelve times, so that at 30 degrees a frame the
  only thing that differs from one picture to the next is which horse it is.
- The horses rise and fall on cranks geared two to one, so locked they rise and fall once a stride.
- No flash is drawn. A stroboscope drawn honestly is a black frame between every two pictures, which is a
  hazard to some viewers and bad to look at. The film holds each picture the way an eye does; that is what
  the word in the title means.
- Between slow and locked, under the lamp, the ride would be a different picture every frame all over the
  screen. There the film keeps a little of the last three pictures in each (never across a cut), so the ride
  is a smear of ghosts that comes sharp as it locks. Slow, or locked, every picture is clean.

## What it must say (the test for the cold reader)

1. A shed in snow at night; somebody goes in with a lamp.
2. Inside is a carousel. They switch it on: lights, and it turns slowly.
3. The horses are numbered, and each is carved in a different pose of a gallop.
4. They bring up a flashing lamp, put the lights out and make the carousel go much faster.
5. The carousel appears to stop turning, and the horses gallop on the spot.
6. It has not stopped: a different numbered horse is in the same place in every picture.
7. Their shadows gallop behind them.
8. It is slowed, the horses are wood again, the keeper leaves; the film says it is itself pictures that do not move.

## The grid

| seconds | bars | picture | sound |
|---|---|---|---|
| 0-6 | waltz 1-4 | outside: snow, the shed dark, a wagon with one lit window; the keeper walks to the shed door with a lamp, reaches it at 5.0 and slides it open. A line of system type says what the place is | wind; his steps on the beat; the door; the waltz tune once, far off, on a music box |
| 6-12 | 5-8 | inside, dark: his lamp finds horses, still, on their poles. He reaches the switch (10.5) and throws it (12.0) | steps; the lamp's hum; a knife switch |
| 12-18 | 9-12 | the lights chase round the rounding boards; the ride starts and turns (6 a minute); wide. From 15.0 the numbers over the horses, and the card along the bottom: each horse that passes the lamp's place is put on it | the organ: the waltz, complete |
| 18-24 | 13-16 | close, at the rim: the horses go by one at a time, numbered 01, 02, 03..., each in the next pose | the waltz, second strain; a bell as each number passes |
| 24-30 | 17-20 | he has wheeled up the stroboscope (the window grows: HORSES PASSING 1.2 /S, LAMP FLASHES 24 /S). 27.0: lights out; only the lamp. 28.5 to 30: close on the regulator, his hand opening it a notch at a time | the organ thins to one pipe; the switch; the lamp ticking; six notches |
| 30-36 | 21-24 | one take: the ride accelerates, the count climbs, it smears, runs backward, slows, comes sharp, and at 36.0 has stopped: LOCKED | a rise; a drum that cannot keep up; at 36.0, the galop |
| 36-44 | galop 1-4 | 36.0, cut to the view the numbered horses went by in: the ride standing still and the horses galloping, a new number over each in every picture. 40.0: three quarters, with the keeper and the lamp | hooves (the footfalls measured off the plate), guitars at a gallop, the tune in two |
| 44-52 | 5-8 | the camera goes round it: it is solid. Then close (48.0): their shadows galloping on the drum behind them | the full band; the choir |
| 52-60 | 9-12 | over the keeper's shoulder; then from above with the canopy cut away (56.0): the whole wheel, two rings of twelve, a phenakistoscope disc | the last strain; a held chord |
| 60-66 | waltz 25-28 | he closes the regulator: forward drift, a blur, slow turning, lights on (63.0), stopped (66.0). Wood | the galop winds down into the waltz, one pipe, then the organ stops |
| 66-72 | 29-32 | outside: he slides the door shut and walks back; the shed window lit. 69.0: PERSISTENCE. 70.5: 1728 PICTURES. NONE OF THEM MOVED. | the door; wind; the music box, alone, last |

## Rules for this piece

- One model (`ride.py`), metres, 5 cm cubes. The horse is carved once (`horse.py`) and posed twelve ways.
- Things that turn are carved (`backlot.carve`, `depth.block`); nothing here is a card except the trees.
- Light has no colour. F is the wagon window, the bulbs, the lamp, the shed window at the end.
- No green.
- The camera moves on ones. The horses do not move at all: they are twelve different horses.
- The rule left showing, three ways: the window (turns a minute, horses passing a second, flashes a second,
  LOCKED); a number over every horse of the outer ring; and the card, which is Muybridge's card redrawn, filled
  in as the horses pass and, locked, read off at twenty-four a second.

(The grid is as it stands after the second cut. What changed on the way is in entries 8 and 9 of `../journal.md`,
and what a cold reader made of the first cut is in `COLD_READ.md`.)
