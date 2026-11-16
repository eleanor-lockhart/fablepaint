"""f15_eye_out: the cable is cut, and No. 4's cold eye goes out (the first second of bar 22).

Added in v1.1 after the outside review: in v1 the cable snapped at 41.5 s and the eye turned green at 50.5, with
four seconds of walking and four of montage in between, so the film's central change had its cause and its effect
nine seconds apart. Now the effect begins half a second after the cause: the same head against the same moon that
the tilt landed on, the cold eye stuttering and dying on the beat at 42.5. f2_window later finds it still dark."""
import numpy as np
import common as C
import f2_window as F2                      # its pose 0 is this framing with the eye dark and the cable stub sparking
import e_no4 as E                           # for the eye's matte at the FINAL placement

N = 12
FLICKER = [9.0, 0.0, 6.0, 1.2, 4.0, .6]     # poses 0-5: the supply failing. From pose 6 (42.5 s, on the beat): out.

def frame(i):
    img = F2.frame(i % 6)                   # poses 0-5 of f2_window: eye dark, sparks at the stub
    k = FLICKER[i] if i < 6 else 0.0
    return C.light(img, E.EYE_M, C.COLD, k) if k > 0 else img
