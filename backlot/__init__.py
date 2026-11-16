"""backlot: a production pipeline for an agent artist. See backlot/MANUAL.md.

    core    the image convention, file in/out            draw    mattes, fills, gradients, noise, tracing
    shapes  a vocabulary of carved shapes                comp    over, blend, matte algebra, multiplane, depth
    lab     colour, lens, film, print, screen finishes   anim    easing, tracks, loops, parallel render, encode
    screen  filmstrips, onion skins, scopes, statistics  model   the bridge to Blender (the model shop)
"""
from . import core, draw, shapes, comp, lab, anim, screen, model
from .core import load, save, canvas, col, lum, resize, flat, read_exr
