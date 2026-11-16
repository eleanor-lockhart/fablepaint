"""backlot: a production pipeline for an agent artist. See backlot/MANUAL.md.

    core    the image convention, file in/out            draw    mattes, fills, gradients, noise, tracing
    shapes  a vocabulary of carved shapes                comp    over, blend, matte algebra, multiplane, depth
    lab     colour, lens, film, print, screen finishes   anim    easing, tracks, loops, parallel render, encode
    screen  filmstrips, onion skins, scopes, statistics  model   the bridge to Blender (the model shop)
    figure  a jointed human in profile                   sound   synthesis, mixing, mastering
    score   notes, chords, sequences                     ear     the listening room: sound as pictures and numbers
    sync    is the picture on the music; pops; camera speed  reader  the cold reader: what does the picture say
    space   places in metres: plan, elevation, a real lens, the real moon
"""
from . import core, draw, shapes, comp, lab, anim, screen, model, figure, sound, score, ear, sync, reader, space
from .core import load, save, canvas, col, lum, resize, flat, read_exr
