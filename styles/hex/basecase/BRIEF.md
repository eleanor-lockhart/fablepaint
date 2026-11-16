# Base Case: the brief, written before the picture

Ninety-six seconds, 24 frames a second, forty-eight bars of 4/4 at 120: a bar is two seconds, a beat is half a
second, and every cut and every click is on a beat. The music is a ground (four bars, one bass note a bar,
stepping down) stated twelve times; each statement is eight seconds and one scene.

## What it is

A fairy tale of the going-down-and-coming-back kind, told as a recursion.

A small house in the country, in snow, at night. The power goes out. One light is left: it is under the pantry
floor. A child with a torch lifts the trap door (you had to lift it), goes down to the basement, and finds the
computer on. On its screen is the same house. She goes in. There is a pantry, a trap door, a basement and a
computer, drawn the way a machine nine years older would draw them; and in that one, the same again, older;
and in that one, lines and a parser, and no computer. That is the base case. A witch lives there.

The child asks for light. The witch does not take requests, and the parser does not know the word "please".
Then the witch decides, for her own reason (it is dark in *her* house and she did not allow that), and presses
RETURN. The value returned is F. It comes back up through every frame of the stack, and each machine redraws its
house with the lights on. In the real basement the screen throws the child's shadow on the wall behind her, and
the shadow wears a hat.

The structural gag, played straight: **a recursion needs a base case, a house has a basement, and what is at the
bottom of both is her.** Each level down loses something a picture can have: first cast light and a moving
camera, then colour, then surfaces, until there are only lines and words. Coming back, it gets them all again.

The house is the one in `gallery/house` (the pantry trap door is drawn there in one bit). The basement is from
a photograph Ellie shared (the red steel post, the brick chimney, the furnace and its ducts, the water heater);
the photograph itself stays out of the repository.

## What it must say (the test for the cold reader)

1. A house at night in snow; its lights go out.
2. A child with a torch opens a trap door and goes down into a basement.
3. A computer is on down there, and its screen shows the same house.
4. She goes into the screen, and the same thing happens again in an older-looking picture; and again; each
   time further down, each time older.
5. At the bottom there is no computer, only a witch, who refuses a polite request.
6. The witch then acts for her own reason and presses RETURN.
7. Light comes back up through every level, and the house is lit again.
8. The child's shadow is the witch's.

## The grid

| bars | seconds | picture | sound |
|---|---|---|---|
| 0-3 | 0-8 | the house in section, snow; at 5.0 every window goes dark; one screen is still lit, underground, and the house says so (5.5) | wind; a music box with the tune, which stops dead at 5.0 |
| 4-7 | 8-16 | the pantry from the kitchen; a line of light round the trap door; she lifts it (11.6 to 12.8); from 13.0 a step every beat | the ground, plucked; a clock; the hinge; each step a note of the scale, going down |
| 8-11 | 16-24 | the basement in section, the camera travelling with her: stairs to 20.5, then the floor | the scale goes on down two octaves; a whistle has the tune; footfalls on the beat |
| 12-15 | 24-32 | she reaches the desk (25.5); from behind her (26); over her shoulder and into the glass (32.0) | the tune answered on the music box, harp, strings; a rise |
| 16-19 | 32-40 | **1989**: sixteen colours, a parser, a figure that shrinks with distance. LIFT TRAPDOOR (34.0), down (35.2), the basement (36.0), into its screen (38.6) | three square waves |
| 20-23 | 40-48 | **1987**: one bit, a window, four cards; clicks at 41, 43, 45, 46; into its screen (46.0) | one eight-bit voice, and the mouse |
| 24-27 | 48-56 | **1980**: lines and forty columns. DOWN (50.6). THERE IS NO COMPUTER HERE. At 54.0, THERE IS A WITCH HERE | a beeper; the keys; at 54.0 her chord, from outside the machine |
| 28-31 | 56-64 | ASK WITCH FOR LIGHT / SHE DOES NOT TAKE REQUESTS. SAY PLEASE / I DON'T KNOW THE WORD "PLEASE". | keys, beeps, an error; a pedal note growing |
| 32-35 | 64-72 | LOOK AT WITCH / SHE WAS ALREADY LOOKING AT YOU. Her dialog (66.0); her pointer leaves her hand (67 to 69.4); RETURN (70.0): SHE PRESSES RETURN. THE VALUE IS F. Every line turns to register F. F IS A LIT WINDOW (71.0) | a heartbeat; silence at 69.5; at 70.0 the chord turns to F major |
| 36-39 | 72-80 | out through each screen (72, 74, 76), each with its lights on and the one below still showing on its glass | the tune in the major, each machine's voice joining in turn |
| 40-43 | 80-88 | the real basement, lit by the screen: her shadow on the wall is the witch, in profile, looking at her; at 82.0 it opens a green eye. The shop light catches (83.0 to 84.0) and the shadow is still there | everyone: guitars, drums, choir, whistle |
| 44-47 | 88-96 | out and up through the ground to the house in the snow; the windows come back in a run (90.0 to 91.5), all seven where five were lit before; title at 92.0 | the answer; a note for each window; the music box, alone, last |

## Rules for this piece

- One model (`house.py`), metres, texel 5 cm, for every level. No level is drawn separately.
- Light has no colour here: it moves a thing between the void and itself. F is the screen, the torch's lens,
  the windows, the crack round the trap door, and, after 70.0, whatever was returned.
- No green anywhere but her (and her dialog, her pointer, and her line in the stack).
- She does not move. Her pointer moves once.
- Level 0: drawings (the child) on twos, camera on ones. Level 1 on threes. Level 2 does not animate, it changes
  cards. Level 3 draws itself.

(The grid above is as it stands after the second cut. What changed after the cold reading, and why, is in
`COLD_READ_v1.md`.)
