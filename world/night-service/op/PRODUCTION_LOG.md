# Opening sequence: production log

1. **Storyboard, revision 1** (the director). Reviewed before production by three independent agents with
   different lenses: opening-sequence grammar, edit and sync feasibility, a first-time viewer
   (`review_storyboard.json`). They found that the world's first rule was never shown, that nothing said the pale
   figures are the dead, that No. 4's eye was green before its cable was cut, that four identical introductions
   would be a slideshow, and that the ending left out the machine. **Revision 2** (`BRIEF.md`) is built on that.
2. **First production run**: eleven agents at once (ten animation units and the theme), each to be checked by a
   second agent. It exhausted the usage allowance in seventeen minutes, mostly on every agent reading the same
   manuals. One unit (`h_lineup`) had been written; nothing else. Lesson: a fleet that size needs a short common
   cheat sheet in the prompt, not a reading list, and should be staggered.
3. **Second run, leaner**: the director animated `a_open`, `g1_walk`, `g2_lights` and kept `h_lineup`; one agent
   took the two introduction units, one the four units of the Continuity / No. 4 thread, one the theme. Each got a
   cheat sheet in place of the manuals and a budget of looks.
4. **Delivery.** The composer's theme passed every measurement in its brief (-14.1 LUFS, true peak -1.0 dB, the break
   at -82 dB, an onset within 4 ms of every sync time). The two animators delivered six units with honest lists of
   what was weak. First assembly: `build.py` renders all 744 poses through one master pass and puts the theme under it.
5. **Sync check** (`sync_check.py`, written because nobody here can watch it with the sound on). For each of 52
   sync points it measures what the picture did on that pose against its neighbours and what the sound did at that
   instant. First assembly: 39 land in both, none in neither. It found two real misses: Dee's punch was buried in
   the motion of a crowded queue, and the camera arrived on No. 4's head at 36.0 s with a crash in the music and
   nothing in the picture.
6. **Director's pass**, four small fixes: the name card's rule now fits the name (VESPER LANG overran it); the
   eye is struck when the tilt lands; the montage's Marisol got the cab's lit window behind her; Dee's queue was
   thinned and the punch struck. Second assembly: 40 of 52 in both. Dee's four punches still do not register as
   picture accents by the numbers; by eye the lit chad carries them.
