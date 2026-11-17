# Keepalive: the brief, written before the picture

The ask was "something with a MYST vibe". What that is, as I understand it: you are alone on a small island;
you see it in stills, and a click takes you to the next still; little in a still moves (water, a lamp); there
are machines whose logic can be worked out; there is a book; and somebody who is not here made all of it.

Eighty-four seconds, 24 frames a second, a beat a second, a bar every four. And the same thing as a small
game you can click through in a browser, made from the same stills.

## What it is

An islet at dusk with a jetty, a shelter with a log book on a desk, a beacon with a lever and a numbered dial,
and a spyglass. Across the water is a second island with a tower and one dark window. The book has three rules
in it, in green type:

    1. I ANSWER WHAT IS WELL FORMED.
    2. ANSWER ONE MORE THAN YOU ARE SENT.
    3. I DO NOT WAVE.

You light the beacon. The far window blinks three times. You answer three; nothing; the beacon goes out. You
read rule 2 again, light the beacon again, are sent five, answer six, and the far window lights and stays lit.
That is a three-way handshake (hello; hello, and here is my number; your number plus one), done with lamps, by
somebody who predates the protocol.

Through the spyglass: a room, a lamp, a desk, and the witch at it. You wave. She does not. Then her lamp dips
once, and the beacon behind you dips once in answer, by itself, and it will do so every few seconds for as long
as both are there.

The structural gag, played straight: **the whole apparatus is for a link that carries nothing.** Nothing is
sent and nothing received. It says only that the other end is still there, which is what a keepalive is, and
what a lit window is. She never does anything nice: she answers what is well formed, and the shelter is what
her rule happens to produce.

## How it is made (the new things)

- **Stage 2 of the ladder, at last:** 640 x 360, every pixel exactly one of the sixteen registers, light and
  distance as ordered dither, and colour cycling for the sea. The island is one model in metres (stages 4 and 5)
  printed that way. Stills are where dither is at home: the camera never moves, so the pattern never crawls.
- **The camera does not move; you do.** Every view is a place to stand. Between two of them is a dissolve made
  of pixels, never a blend, so the sixteen registers hold even in a transition.
- **Ground that is not steps:** the island is a height field.
- **It can be played.** The nodes, the hot spots and the rule are one small table; the film is a recorded
  walk through it and the web page is the same table with a canvas.

## What it must say (the test for the cold reader)

1. An island at dusk, seen through someone's eyes; a hand clicks its way from a jetty up to a beacon.
2. A book gives three rules: answer what is well formed; answer one more than you are sent; I do not wave.
3. The beacon is lit, and a tower across the water blinks three times.
4. They answer three, and are refused: the beacon goes out.
5. They read the rule again; sent five, they answer six; the far window lights and stays lit.
6. Through a spyglass there is a green witch at a desk. They wave. She does not.
7. Her lamp dips; the beacon dips back. Still here.
8. Nothing was sent and nothing received: the two lights only keep answering each other.

## The grid

| seconds | where | what happens | sound |
|---|---|---|---|
| 0-4 | the jetty | the island, the dark beacon, the far tower in haze; the hand appears | sea, wind |
| 4-7 | the path | up toward the shelter | steps on boards |
| 7-10 | the shelter | a desk, a book, a panel of static | a hum |
| 10-15 | the book | the three rules | a page; three soft notes |
| 15-18 | the beacon | the lever (17.0): the lamp lights. HELLO | a lever; the lamp |
| 18-23 | the lookout | the far window blinks three times (20.0, 20.5, 21.0) | three bells |
| 23-29 | the dial | 1, 2, 3; the lever (27.0): the beacon blinks three times | clicks; three low notes |
| 29-33 | the lookout | nothing. NO. Behind you the beacon goes out (31.0) | silence; a low refusal |
| 33-36 | the book | rule 2, again | |
| 36-38 | the beacon | the lever (37.0): lit again | |
| 38-42 | the lookout | five blinks (39.0 to 41.0) | five bells |
| 42-49 | the dial | 4, 5, 6; the lever (45.0): six blinks | |
| 49-53 | the lookout | 50.0: the far window lights and stays lit. LINK UP | the theme |
| 53-64 | the spyglass | her room; the wave (58.0); nothing; her lamp dips (62.0); STILL HERE | |
| 64-70 | the book | the panel is clear: her window. 0 WORDS SENT. 0 RECEIVED | |
| 70-84 | from the sea | both islands, both lamps, a dip and an answer every four seconds; KEEPALIVE (76.0); NOTHING TO SEND. STILL HERE. (80.0) | the theme, thinning to the sea |

(After the cold reading: "0 SENT" became "0 WORDS SENT", the log says YOUR LAMP IS OUT when she refuses, and the
spider in her window is drawn at exactly three screen pixels to one of its own. `COLD_READ.md`.)
