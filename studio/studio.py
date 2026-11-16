#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "pillow", "opencv-python-headless"]
# ///
"""
FABLE STUDIO -- a present-day painting program with no window, driven by Python scripts.

Everything is 32-bit float, linear light, premultiplied RGBA; the picture is only
squeezed to 8 bits (with dither) when it is looked at or exported.

  studio.py new <session> --size 2560x1440 [--bg '#101014']
  studio.py run <session> script.py        run a painting script (atomic: an error changes nothing)
  studio.py undo <session> [n]
  studio.py view <session> [--crop X Y W H] [--layer NAME] [--max 1500] [-o file]
  studio.py layers <session>
  studio.py export <session> -o out.png [--bits 16] [--scale 0.5]
  studio.py timelapse <session> -o out.mp4
  studio.py api                            every script function, with signatures

Inside a script (all coordinates in canvas pixels, colours '#rrggbb', (r,g,b) or hsv(h,s,v)):

 layers    layer(name, blend, opacity, above/below, clip)  use(name)  props(name, opacity=, blend=,
           visible=, clip=, lock=)  delete  duplicate  rename  move  merge_down  stamp_visible(new, names)
           mask(source)  mask_mode(on)  apply_mask()  drop_mask()  lock(on)  clear()
           adjust(name, kind, **args)   non-destructive: levels curves hue_sat exposure balance
                                        brightness_contrast desaturate colorize gradient_map
 blends    normal add multiply screen overlay soft_light hard_light darken lighten dodge burn
           difference color luminosity hue saturation  (+ erase, behind for brushes)
 brushes   brush(tip=, size=, hardness=, opacity=, flow=, spacing=, angle=, roundness=, follow=,
                 scatter=, count=, size_jitter=, angle_jitter=, flow_jitter=, hue_jitter=, sat_jitter=,
                 val_jitter=, psize=, pflow=, taper=(in,out), blend=, mix=, grain=, smooth=)
           tips: round chalk charcoal sponge cloud bristle flat splatter stipple leaf blade needle
                 star spruce square        preset(name)  stroke(points[,color,pressure])  dabs(points)
           scatter(n, area|density=)  erase(points)  smudge  blur_stroke  dodge  burn  liquify
 shapes    fill()  fill_poly(points, color, opacity, feather, smooth)  fill_ellipse  fill_rect
           gradient(kind, p0, p1, stops)  bucket(x, y, color, tol)  text(x, y, s, size)
 select    select_all/none/invert  select_rect  select_ellipse  select_poly  select_alpha(layer)
           select_luma(lo, hi)  select_color(color, tol)  select_array(a)  feather(r)  grow(px)
 filters   gaussian_blur  motion_blur  smear  zoom_blur  sharpen  noise  clouds  glow  turbulence
           wave  emboss  median  high_pass  vignette  modulate(array)  levels  curves  hue_sat
           balance  brightness_contrast  exposure  invert  desaturate  posterize  threshold
           colorize  gradient_map
 transform transform(scale, rotate, translate, center)  flip(axis)  perspective(src, dst)
 misc      sample(x, y)  noise_field(...)  path(points, closed)  px(name)  W  H  rng  np  math
"""
import sys, os, json, math, time, glob, shutil, argparse, traceback, subprocess, colorsys
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
SESS = os.path.join(HERE, 'sessions')
F32 = np.float32
EPS = 1e-6


# ============================================================ colour
def s2l(c):
    c = np.asarray(c, F32)
    return np.where(c <= 0.04045, c / 12.92, ((np.maximum(c, 0) + 0.055) / 1.055) ** 2.4).astype(F32)


def l2s(c):
    c = np.clip(np.asarray(c, F32), 0, None)
    return np.where(c <= 0.0031308, c * 12.92, 1.055 * np.power(c, 1 / 2.4) - 0.055).astype(F32)


class Lin(np.ndarray):
    """A colour already in linear light."""


def col(c):
    if isinstance(c, Lin):
        return c
    if isinstance(c, str):
        h = c.lstrip('#')
        if len(h) == 3:
            h = ''.join(ch * 2 for ch in h)
        v = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    else:
        v = [float(x) for x in c[:3]]
        if max(v) > 1.0:
            v = [x / 255 for x in v]
    return s2l(v).view(Lin)


def hsv(h, s, v):
    return s2l(colorsys.hsv_to_rgb((h % 360) / 360, s, v)).view(Lin)


def mix(a, b, t):
    return (col(a) * (1 - t) + col(b) * t).view(Lin)


def lum(rgb):
    return rgb[..., 0] * 0.2126 + rgb[..., 1] * 0.7152 + rgb[..., 2] * 0.0722


def _g(x):
    return np.power(np.clip(x, 0, 1), 1 / 2.2)


def _l(x):
    return np.power(np.clip(x, 0, 1), 2.2)


def _setlum(c, l):
    d = l - lum(c)
    c = c + d[..., None]
    L = lum(c)[..., None]
    n = c.min(-1, keepdims=True)
    x = c.max(-1, keepdims=True)
    c = np.where(n < 0, L + (c - L) * L / np.maximum(L - n, EPS), c)
    return np.where(x > 1, L + (c - L) * (1 - L) / np.maximum(x - L, EPS), c)


def _setsat(c, s):
    n = c.min(-1, keepdims=True)
    x = c.max(-1, keepdims=True)
    return (c - n) / np.maximum(x - n, EPS) * s[..., None]


def _sat(c):
    return c.max(-1) - c.min(-1)


def _overlay(b, s):
    return np.where(b <= 0.5, 2 * b * s, 1 - 2 * (1 - b) * (1 - s))


def _soft(b, s):
    d = np.where(b <= 0.25, ((16 * b - 12) * b + 4) * b, np.sqrt(np.clip(b, 0, 1)))
    return np.where(s <= 0.5, b - (1 - 2 * s) * b * (1 - b), b + (2 * s - 1) * (d - b))


BLEND = {
    'multiply': lambda b, s: b * s,
    'screen': lambda b, s: 1 - (1 - np.clip(b, 0, 1)) * (1 - np.clip(s, 0, 1)),
    'overlay': lambda b, s: _l(_overlay(_g(b), _g(s))),
    'hard_light': lambda b, s: _l(_overlay(_g(s), _g(b))),
    'soft_light': lambda b, s: _l(_soft(_g(b), _g(s))),
    'darken': np.minimum,
    'lighten': np.maximum,
    'dodge': lambda b, s: np.clip(b / np.maximum(1 - s, 1e-3), 0, 8),
    'burn': lambda b, s: 1 - np.clip((1 - np.clip(b, 0, 1)) / np.maximum(s, 1e-3), 0, 1),
    'difference': lambda b, s: np.abs(b - s),
    'color': lambda b, s: _l(_setlum(_g(s), lum(_g(b)))),
    'luminosity': lambda b, s: _l(_setlum(_g(b), lum(_g(s)))),
    'hue': lambda b, s: _l(_setlum(_setsat(_g(s), _sat(_g(b))), lum(_g(b)))),
    'saturation': lambda b, s: _l(_setlum(_setsat(_g(b), _sat(_g(s))), lum(_g(b)))),
}


def composite(dst, src, mode='normal'):
    """Premultiplied RGBA: put src onto dst."""
    sa = src[..., 3:4]
    if mode == 'normal':
        return src + dst * (1 - sa)
    da = dst[..., 3:4]
    if mode == 'erase':
        return dst * (1 - sa)
    if mode == 'behind':
        return dst + src * (1 - da)
    out = np.empty_like(dst)
    out[..., 3:4] = sa + da - sa * da
    if mode == 'add':
        out[..., :3] = dst[..., :3] + src[..., :3]
        return out
    cs = src[..., :3] / np.maximum(sa, EPS)
    cb = dst[..., :3] / np.maximum(da, EPS)
    out[..., :3] = (1 - da) * src[..., :3] + (1 - sa) * dst[..., :3] + sa * da * BLEND[mode](cb, cs)
    return out


# ============================================================ noise and brush tips
def fbm(h, w, scale=6.0, octaves=5, seed=0, gain=0.5, lac=2.0, stretch=(1.0, 1.0), ridged=False, norm=True):
    rng = np.random.default_rng(seed)
    out = np.zeros((h, w), F32)
    amp, tot, f = 1.0, 0.0, float(scale)
    for _ in range(octaves):
        gx = min(w, max(2, int(round(f * stretch[0])) + 1))
        gy = min(h, max(2, int(round(f * stretch[1] * h / w)) + 1))
        n = cv2.resize(rng.random((gy, gx), dtype=F32), (w, h), interpolation=cv2.INTER_CUBIC)
        if ridged:
            n = 1 - np.abs(2 * n - 1)
        out += amp * n
        tot += amp
        amp *= gain
        f *= lac
    out /= tot
    if norm:
        lo, hi = np.percentile(out[::4, ::4], [0.5, 99.5])
        out = (out - lo) / max(hi - lo, 1e-6)
    return np.clip(out, 0, 1)


_BASE, _TIPS = {}, {}


def _base_tip(name):
    if name in _BASE:
        return _BASE[name]
    N = 256
    rng = np.random.default_rng(sum(map(ord, name)))
    yy, xx = np.mgrid[:N, :N].astype(F32)
    u = (xx - N / 2 + .5) / (N / 2)
    v = (yy - N / 2 + .5) / (N / 2)
    r = np.hypot(u, v)
    soft = np.clip(1 - r, 0, 1)
    soft = soft * soft * (3 - 2 * soft)

    def blobs(n, sx, sy, r0, r1, hard, normal=False):
        a = np.zeros((N, N), F32)
        for _ in range(n):
            cx = (rng.normal(0, sx) if normal else rng.uniform(-sx, sx)) * N / 2 + N / 2
            cy = (rng.normal(0, sy) if normal else rng.uniform(-sy, sy)) * N / 2 + N / 2
            rad = rng.uniform(r0, r1)
            d = np.hypot(xx - cx, yy - cy)
            a = np.maximum(a, (np.clip(rad - d + .5, 0, 1) if hard else np.exp(-(d / rad) ** 2)) * rng.uniform(.5, 1))
        return a

    if name == 'chalk':
        a = np.sqrt(soft) * np.clip((fbm(N, N, 10, 4, 11) - .42) * 4, 0, 1)
    elif name == 'charcoal':
        a = np.clip(1 - r, 0, 1) ** .3 * np.clip((fbm(N, N, 28, 3, 12) - .35) * 3, 0, 1)
    elif name == 'sponge':
        a = soft ** .4 * (fbm(N, N, 40, 2, 13) > .55)
    elif name == 'cloud':
        a = soft * np.clip((fbm(N, N, 5, 5, 14) - .25) * 2, 0, 1)
    elif name == 'bristle':
        a = blobs(46, .22, .92, 2.5, 5, False)
    elif name == 'flat':
        streak = cv2.resize(rng.random((32, 1), dtype=F32), (N, N), interpolation=cv2.INTER_CUBIC)
        a = np.clip((.28 - np.abs(u)) * 14, 0, 1) * np.clip((.92 - np.abs(v)) * 14, 0, 1) * (.55 + .45 * streak)
    elif name == 'splatter':
        a = blobs(26, .62, .62, 2, 13, True) * (r < .95)
    elif name == 'stipple':
        a = blobs(260, .4, .4, 1, 2.4, True, normal=True)
    elif name == 'leaf':
        a = np.clip((.34 * (1 - u * u) - np.abs(v)) * 10, 0, 1) * (np.abs(u) < 1)
    elif name == 'blade':
        t = (u + 1) / 2
        a = np.clip((.09 * (1 - t) + .006 - np.abs(v - .15 * t * t)) * 40, 0, 1)
    elif name == 'needle':
        a = np.zeros((N, N), F32)
        for th in np.radians(np.linspace(-34, 34, 9)):
            al = (u + .9) * math.cos(th) + v * math.sin(th)
            pe = -(u + .9) * math.sin(th) + v * math.cos(th)
            Lr = 1.7 * (1 - abs(th) * .5)
            a = np.maximum(a, np.clip((.03 * (1 - al / Lr) + .006 - np.abs(pe)) * 60, 0, 1) * (al > 0) * (al < Lr))
    elif name == 'star':
        a = np.maximum(np.exp(-np.abs(u) * 5 - (v * 36) ** 2), np.exp(-np.abs(v) * 5 - (u * 36) ** 2))
        a = np.maximum(a, np.exp(-(r * 7) ** 2))
    elif name == 'spruce':
        t = (v + 1) / 2
        edge = cv2.resize(rng.random((24, 1), dtype=F32), (N, N), interpolation=cv2.INTER_LINEAR)
        hw = .44 * t ** .9 * (.62 + .38 * ((t * 9) % 1)) * (.8 + .4 * edge) + .012
        a = np.clip((hw - np.abs(u)) * 30, 0, 1) * (t < .93) + (np.abs(u) < .035) * (t >= .9)
    elif name == 'square':
        a = np.ones((N, N), F32)
    else:
        raise ValueError(f'no brush tip {name!r}')
    _BASE[name] = np.clip(a, 0, 1).astype(F32)
    return _BASE[name]


def _round_tip(n, d, hard, cx, cy):
    yy, xx = np.ogrid[:n, :n]
    dist = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2)
    r = d / 2
    if hard >= .995:
        return np.clip(r - dist + .5, 0, 1).astype(F32)
    inner = r * hard
    t = np.clip((dist - inner) / max(r - inner, .7), 0, 1)
    return (1 - t * t * (3 - 2 * t)).astype(F32)


def get_tip(name, size, angle=0.0, roundness=1.0, hardness=.5):
    if name == 'round' and roundness > .98:
        key = ('r', int(round(size)), round(hardness, 2))
        if key not in _TIPS:
            n = int(round(size)) + 3
            _TIPS[key] = _round_tip(n, round(size), hardness, (n - 1) / 2, (n - 1) / 2)
        return _TIPS[key]
    key = (name, int(round(size)), int(round(angle / 4)) % 90, round(roundness, 2), round(hardness, 2))
    if key in _TIPS:
        return _TIPS[key]
    base = _round_tip(256, 252, hardness, 127.5, 127.5) if name == 'round' else _base_tip(name)
    n0 = 256
    while n0 // 2 >= max(16, 2 * size):            # crude mip chain so small tips don't alias
        n0 //= 2
    if n0 != 256:
        base = cv2.resize(base, (n0, n0), interpolation=cv2.INTER_AREA)
    n = int(math.ceil(size)) + 2
    s = size / n0
    th = math.radians(angle)
    c, sn = math.cos(th), math.sin(th)
    A = np.array([[c * s, -sn * s * roundness], [sn * s, c * s * roundness]])
    t = np.array([(n - 1) / 2, (n - 1) / 2]) - A @ np.array([(n0 - 1) / 2, (n0 - 1) / 2])
    tip = cv2.warpAffine(base, np.hstack([A, t[:, None]]).astype(np.float64), (n, n), flags=cv2.INTER_LINEAR)
    if len(_TIPS) > 6000:
        _TIPS.clear()
    _TIPS[key] = tip
    return tip


def _smooth(pts, closed=False):
    P = np.asarray(pts, float)
    if len(P) < 3:
        return P
    Q = np.vstack([P[-1], P, P[0], P[1]]) if closed else np.vstack([P[0], P, P[-1]])
    out = []
    for i in range(1, len(Q) - 2):
        p0, p1, p2, p3 = Q[i - 1], Q[i], Q[i + 1], Q[i + 2]
        n = max(2, int(np.hypot(*(p2[:2] - p1[:2])) / 4))
        t = np.linspace(0, 1, n, endpoint=False)[:, None]
        out.append(.5 * (2 * p1 + (p2 - p0) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t * t + (3 * p1 - p0 - 3 * p2 + p3) * t ** 3))
    out.append(Q[-2][None])
    return np.vstack(out)


def _resample(P, step):
    d = np.hypot(np.diff(P[:, 0]), np.diff(P[:, 1]))
    s = np.concatenate([[0], np.cumsum(d)])
    if s[-1] < 1e-6:
        return P[:1], np.zeros(1), np.zeros(1)
    t = np.clip(np.arange(0, s[-1] + step * .5, step), 0, s[-1])
    Q = np.stack([np.interp(t, s, P[:, k]) for k in range(P.shape[1])], 1)
    if len(Q) > 1:
        ang = np.degrees(np.arctan2(np.gradient(Q[:, 1]), np.gradient(Q[:, 0])))
    else:
        ang = np.zeros(1)
    return Q, ang, t / s[-1]


BRUSH0 = dict(tip='round', size=20.0, hardness=.8, opacity=1.0, flow=1.0, spacing=.1, angle=0.0, roundness=1.0,
              follow=False, scatter=0.0, count=1, size_jitter=0.0, angle_jitter=0.0, flow_jitter=0.0,
              hue_jitter=0.0, sat_jitter=0.0, val_jitter=0.0, psize=True, pflow=False, taper=(0.0, 0.0),
              blend='normal', mix=0.0, grain=0.0, smooth=True)
PRESETS = {
    'pencil': dict(tip='round', size=3, hardness=.7, flow=.7, spacing=.15, grain=.5, pflow=True),
    'ink': dict(tip='round', size=6, hardness=.95, flow=1, spacing=.06, taper=(.15, .25)),
    'marker': dict(tip='flat', size=28, flow=.6, spacing=.06, follow=True, psize=False),
    'airbrush': dict(tip='round', size=120, hardness=0, flow=.07, spacing=.05, psize=False),
    'oil': dict(tip='bristle', size=44, flow=.75, spacing=.05, follow=True, mix=.35, val_jitter=.03),
    'acrylic': dict(tip='flat', size=40, flow=.9, spacing=.05, follow=True),
    'watercolor': dict(tip='cloud', size=90, flow=.12, spacing=.12, angle_jitter=1, grain=.5, psize=False),
    'chalk': dict(tip='chalk', size=30, flow=.7, spacing=.12, angle_jitter=1, grain=.4),
    'charcoal': dict(tip='charcoal', size=22, flow=.5, spacing=.1, angle_jitter=1, grain=.6, pflow=True),
    'sponge': dict(tip='sponge', size=60, flow=.5, spacing=.3, angle_jitter=1, scatter=.2),
    'splatter': dict(tip='splatter', size=70, flow=.9, spacing=.6, angle_jitter=1, scatter=.5, size_jitter=.5),
    'foliage': dict(tip='leaf', size=16, flow=.9, spacing=.5, angle_jitter=1, scatter=.9, count=3,
                    size_jitter=.4, val_jitter=.12, hue_jitter=6),
    'grass': dict(tip='blade', size=40, flow=.9, spacing=.3, angle=-90, angle_jitter=.08, scatter=.3, size_jitter=.4),
    'glow': dict(tip='round', size=80, hardness=0, flow=.25, spacing=.08, blend='add', psize=False),
    'eraser': dict(tip='round', size=40, hardness=.5, flow=1, blend='erase'),
}


# ============================================================ colour adjustments (on linear RGB)
def a_levels(rgb, black=0.0, white=1.0, gamma=1.0, out_black=0.0, out_white=1.0):
    g = np.clip((l2s(rgb) - black) / max(white - black, 1e-4), 0, 1) ** (1 / gamma)
    return s2l(out_black + g * (out_white - out_black))


def a_curves(rgb, points=((0, 0), (1, 1)), channel='rgb'):
    P = _smooth(sorted(points)) if len(points) > 2 else np.asarray(sorted(points), float)
    g = l2s(np.clip(rgb, 0, 1))
    ch = {'rgb': (0, 1, 2), 'r': (0,), 'g': (1,), 'b': (2,)}[channel]
    for k in ch:
        g[..., k] = np.interp(g[..., k], P[:, 0], np.clip(P[:, 1], 0, 1))
    return s2l(g)


def a_hue_sat(rgb, hue=0.0, sat=1.0, light=1.0):
    h = cv2.cvtColor(np.clip(l2s(rgb), 0, 1), cv2.COLOR_RGB2HSV)
    h[..., 0] = (h[..., 0] + hue) % 360
    h[..., 1] = np.clip(h[..., 1] * sat, 0, 1)
    h[..., 2] = np.clip(h[..., 2] * light, 0, 1)
    return s2l(cv2.cvtColor(h, cv2.COLOR_HSV2RGB))


def a_exposure(rgb, stops=0.0):
    return rgb * F32(2.0 ** stops)


def a_balance(rgb, shadows=(0, 0, 0), mids=(0, 0, 0), highs=(0, 0, 0)):
    g = l2s(rgb)
    l = np.clip(lum(g), 0, 1)[..., None]
    ws, wh = (1 - l) ** 2, l ** 2
    g = g + ws * np.asarray(shadows, F32) + (1 - ws - wh) * np.asarray(mids, F32) + wh * np.asarray(highs, F32)
    return s2l(np.clip(g, 0, 1))


def a_brightness_contrast(rgb, brightness=0.0, contrast=0.0):
    return s2l(np.clip((l2s(rgb) - .5) * (1 + contrast) + .5 + brightness, 0, 1))


def a_desaturate(rgb, amount=1.0):
    return rgb + (lum(rgb)[..., None] - rgb) * amount


def a_invert(rgb):
    return s2l(1 - np.clip(l2s(rgb), 0, 1))


def a_posterize(rgb, levels=4):
    return s2l(np.round(l2s(np.clip(rgb, 0, 1)) * (levels - 1)) / (levels - 1))


def a_threshold(rgb, level=.5):
    return np.repeat((l2s(lum(rgb)) > level).astype(F32)[..., None], 3, -1)


def a_colorize(rgb, color='#888888', amount=1.0):
    c = col(color)
    return rgb + (lum(rgb)[..., None] * c / max(float(lum(c)), 1e-3) - rgb) * amount


def a_gradient_map(rgb, stops=((0, '#000000'), (1, '#ffffff'))):
    t = l2s(np.clip(lum(rgb), 0, 1))
    pos = [s[0] for s in stops]
    cs = np.array([col(s[1]) for s in stops])
    return np.stack([np.interp(t, pos, cs[:, k]) for k in range(3)], -1).astype(F32)


ADJ = dict(levels=a_levels, curves=a_curves, hue_sat=a_hue_sat, exposure=a_exposure, balance=a_balance,
           brightness_contrast=a_brightness_contrast, desaturate=a_desaturate, invert=a_invert,
           posterize=a_posterize, threshold=a_threshold, colorize=a_colorize, gradient_map=a_gradient_map)


# ============================================================ document
class Layer:
    def __init__(s, name, kind='pixel'):
        s.name, s.kind, s.px, s.mask = name, kind, None, None
        s.opacity, s.blend, s.visible, s.clip, s.lock = 1.0, 'normal', True, False, False
        s.params, s.id, s.ver, s.mver, s.dirty, s.mdirty = {}, 0, 0, 0, True, False

    def meta(s):
        return dict(name=s.name, kind=s.kind, opacity=s.opacity, blend=s.blend, visible=s.visible, clip=s.clip,
                    lock=s.lock, params=s.params, id=s.id, ver=s.ver, mver=s.mver, has_mask=s.mask is not None)


def sdir(name, *more):
    return os.path.join(SESS, name, *more)


class Doc:
    def __init__(s, name, w, h):
        s.name, s.w, s.h = name, w, h
        s.layers, s.ai, s.sel, s.selver, s.seldirty = [], 0, None, 0, False
        s.fg, s.brushd, s.mmode = col('#000000'), dict(BRUSH0), False
        s.batch, s.nextid, s.frames, s._last, s._grainarr = 0, 1, 0, 0.0, None
        s.rng = np.random.default_rng(1)
        s.W, s.H = w, h

    # ---------------------------------------------------- storage
    def _save(s):
        d = sdir(s.name)
        for L in s.layers:
            if L.kind == 'pixel' and L.dirty:
                L.ver += 1
                np.save(os.path.join(d, f'px_{L.id}_{L.ver}.npy'), L.px)
            if L.mask is not None and (L.mdirty or L.mver == 0):
                L.mver += 1
                np.save(os.path.join(d, f'mk_{L.id}_{L.mver}.npy'), L.mask)
            L.dirty = L.mdirty = False
        if s.sel is not None and s.seldirty:
            s.selver += 1
            np.save(os.path.join(d, f'sel_{s.selver}.npy'), s.sel)
        s.seldirty = False
        meta = dict(w=s.w, h=s.h, batch=s.batch, ai=s.ai, nextid=s.nextid, frames=s.frames,
                    fg=[float(v) for v in s.fg], brush={k: (list(v) if isinstance(v, tuple) else v) for k, v in s.brushd.items()},
                    mask_mode=s.mmode, sel=s.selver if s.sel is not None else 0, selver=s.selver,
                    layers=[L.meta() for L in s.layers])
        with open(os.path.join(d, f'state_{s.batch:04d}.json'), 'w') as f:
            json.dump(meta, f)
        with open(os.path.join(d, 'head.json'), 'w') as f:
            json.dump({'batch': s.batch}, f)
        keep = set()
        for st in sorted(glob.glob(os.path.join(d, 'state_*.json')))[-4:]:
            m = json.load(open(st))
            for L in m['layers']:
                keep.add(f"px_{L['id']}_{L['ver']}.npy")
                keep.add(f"mk_{L['id']}_{L['mver']}.npy")
            keep.add(f"sel_{m['sel']}.npy")
        for f in glob.glob(os.path.join(d, '*.npy')):
            if os.path.basename(f) not in keep:
                os.remove(f)

    @staticmethod
    def _load(name):
        d = sdir(name)
        if not os.path.exists(os.path.join(d, 'head.json')):
            sys.exit(f'no session {name!r}')
        b = json.load(open(os.path.join(d, 'head.json')))['batch']
        m = json.load(open(os.path.join(d, f'state_{b:04d}.json')))
        s = Doc(name, m['w'], m['h'])
        s.batch, s.ai, s.nextid, s.frames, s.selver, s.mmode = m['batch'], m['ai'], m['nextid'], m['frames'], m['selver'], m['mask_mode']
        s.fg = np.asarray(m['fg'], F32).view(Lin)
        s.brushd = dict(BRUSH0, **{k: (tuple(v) if isinstance(v, list) else v) for k, v in m['brush'].items()})
        if m['sel']:
            s.sel = np.load(os.path.join(d, f"sel_{m['sel']}.npy"))
        for lm in m['layers']:
            L = Layer(lm['name'], lm['kind'])
            for k in ('opacity', 'blend', 'visible', 'clip', 'lock', 'params', 'id', 'ver', 'mver'):
                setattr(L, k, lm[k])
            if L.kind == 'pixel':
                L.px = np.load(os.path.join(d, f'px_{L.id}_{L.ver}.npy'))
            if lm['has_mask']:
                L.mask = np.load(os.path.join(d, f'mk_{L.id}_{L.mver}.npy'))
            L.dirty = False
            s.layers.append(L)
        s.rng = np.random.default_rng(1000 + s.batch)
        return s

    # ---------------------------------------------------- internals
    @property
    def _A(s):
        return s.layers[s.ai]

    def _find(s, name):
        for i, L in enumerate(s.layers):
            if L.name == name:
                return i
        raise KeyError(f'no layer {name!r}; have {[L.name for L in s.layers]}')

    def _L(s, name=None):
        return s._A if name is None else s.layers[s._find(name)]

    def _flat(s, region=None, step=1, names=None):
        y0, y1, x0, x1 = region or (0, s.h, 0, s.w)
        sl = (slice(y0, y1, step), slice(x0, x1, step))
        acc, base = None, None
        for L in s.layers:
            if not L.visible or (names is not None and L.name not in names):
                if not L.clip:
                    base = None
                continue
            f = L.opacity
            if L.mask is not None:
                f = L.mask[sl] * f
            if L.clip and base is not None:
                f = base * f
            if L.kind == 'pixel':
                src = L.px[sl]
                if not (isinstance(f, float) and f == 1.0):
                    src = src * (f[..., None] if isinstance(f, np.ndarray) else F32(f))
                if not L.clip:
                    base = src[..., 3]
                acc = src.copy() if acc is None else composite(acc, src, L.blend)
            elif acc is not None:
                a = acc[..., 3:4]
                rgb = acc[..., :3] / np.maximum(a, EPS)
                new = ADJ[L.params['kind']](rgb, **L.params['args'])
                acc[..., :3] = (rgb + (new - rgb) * (f[..., None] if isinstance(f, np.ndarray) else F32(f))) * a
        if acc is None:
            acc = np.zeros(((y1 - y0 + step - 1) // step, (x1 - x0 + step - 1) // step, 4), F32)
        return acc

    def _to8(s, acc, dither=True):
        g = l2s(np.clip(acc[..., :3], 0, 1)) * 255
        if dither:
            r = np.random.default_rng(7)
            g = g + r.random(g.shape, dtype=F32) - r.random(g.shape, dtype=F32)
        return np.clip(np.round(g), 0, 255).astype(np.uint8)

    def _op(s, major=False):
        now = time.time()
        if not (major or now - s._last > .3):
            return
        step = max(1, int(math.ceil(s.w / 960)))
        img = s._to8(s._flat(step=step), dither=False)
        os.makedirs(sdir(s.name, 'frames'), exist_ok=True)
        cv2.imwrite(sdir(s.name, 'frames', f'{s.frames:06d}.jpg'), img[..., ::-1], [cv2.IMWRITE_JPEG_QUALITY, 88])
        s.frames += 1
        s._last = time.time()

    def _grain(s):
        if s._grainarr is None:
            s._grainarr = fbm(s.h, s.w, 420, 2, 99)
        return s._grainarr

    def _commit(s, rgba, x0, y0, blend='normal'):
        L = s._A
        h, w = rgba.shape[:2]
        X0, Y0, X1, Y1 = max(x0, 0), max(y0, 0), min(x0 + w, s.w), min(y0 + h, s.h)
        if X1 <= X0 or Y1 <= Y0:
            return
        src = rgba[Y0 - y0:Y1 - y0, X0 - x0:X1 - x0]
        if s.sel is not None:
            src = src * s.sel[Y0:Y1, X0:X1, None]
        if s.mmode:
            if L.mask is None:
                L.mask = np.ones((s.h, s.w), F32)
            a = src[..., 3]
            if blend == 'erase':
                L.mask[Y0:Y1, X0:X1] *= 1 - a
            else:
                L.mask[Y0:Y1, X0:X1] = L.mask[Y0:Y1, X0:X1] * (1 - a) + lum(src[..., :3])
            L.mdirty = True
            return
        if L.kind != 'pixel':
            raise ValueError(f'{L.name!r} is an adjustment layer; paint on its mask (mask_mode(True)) or pick another layer')
        dst = L.px[Y0:Y1, X0:X1]
        out = composite(dst, src, blend)
        if L.lock:
            da = dst[..., 3:4]
            out[..., :3] *= da / np.maximum(out[..., 3:4], EPS)
            out[..., 3:4] = da
        L.px[Y0:Y1, X0:X1] = out
        L.dirty = True

    def _mask_of(s, points, feather=0.0, smooth=False):
        P = np.asarray(_smooth(points, closed=True) if smooth else points, float)[:, :2]
        pad = int(feather * 3) + 2
        x0, y0 = max(int(P[:, 0].min()) - pad, 0), max(int(P[:, 1].min()) - pad, 0)
        x1, y1 = min(int(P[:, 0].max()) + pad + 1, s.w), min(int(P[:, 1].max()) + pad + 1, s.h)
        if x1 <= x0 or y1 <= y0:
            return None, 0, 0
        m = np.zeros((y1 - y0, x1 - x0), np.uint8)
        cv2.fillPoly(m, [np.round((P - [x0, y0]) * 16).astype(np.int32)], 255, lineType=cv2.LINE_AA, shift=4)
        m = m.astype(F32) / 255
        if feather > 0:
            m = cv2.GaussianBlur(m, (0, 0), feather)
        return m, x0, y0

    def _setsel(s, m, mode):
        if mode == 'replace' or s.sel is None:
            if mode in ('sub', 'intersect') and s.sel is None:
                s.sel = np.ones((s.h, s.w), F32)
            else:
                s.sel = m.astype(F32)
                s.seldirty = True
                return
        s.sel = {'add': np.maximum(s.sel, m), 'sub': s.sel * (1 - m), 'intersect': s.sel * m, 'replace': m}[mode].astype(F32)
        s.seldirty = True

    def _filter(s, fn):
        L = s._A
        if L.kind != 'pixel':
            raise ValueError('filters need a pixel layer')
        new = fn(L.px)
        if s.sel is not None:
            new = L.px + (new - L.px) * s.sel[..., None]
        L.px = np.ascontiguousarray(new, F32)
        L.dirty = True
        s._op(True)

    def _cfilter(s, f):
        def fn(px):
            a = px[..., 3:4]
            out = np.empty_like(px)
            out[..., :3] = f(px[..., :3] / np.maximum(a, EPS)) * a
            out[..., 3:4] = a
            return out
        s._filter(fn)

    # ==================================================== layers
    def layer(s, name, blend='normal', opacity=1.0, above=None, below=None, clip=False):
        """Make (or switch to) a layer."""
        try:
            s.ai = s._find(name)
            return
        except KeyError:
            pass
        L = Layer(name)
        L.px = np.zeros((s.h, s.w, 4), F32)
        L.blend, L.opacity, L.clip, L.id = blend, float(opacity), clip, s.nextid
        s.nextid += 1
        i = s._find(above) + 1 if above else s._find(below) if below else (s.ai + 1 if s.layers else 0)
        s.layers.insert(i, L)
        s.ai = i

    def use(s, name):
        s.ai = s._find(name)

    def props(s, name=None, **kw):
        L = s._L(name)
        for k, v in kw.items():
            if k not in ('opacity', 'blend', 'visible', 'clip', 'lock'):
                raise ValueError(f'no layer property {k!r}')
            setattr(L, k, v)

    def lock(s, on=True):
        s._A.lock = on

    def delete(s, name):
        i = s._find(name)
        del s.layers[i]
        s.ai = min(max(s.ai - (i <= s.ai), 0), len(s.layers) - 1)

    def duplicate(s, name, new):
        i = s._find(name)
        src = s.layers[i]
        L = Layer(new, src.kind)
        L.px = None if src.px is None else src.px.copy()
        L.mask = None if src.mask is None else src.mask.copy()
        L.opacity, L.blend, L.visible, L.clip, L.lock, L.params = src.opacity, src.blend, src.visible, src.clip, src.lock, dict(src.params)
        L.id, L.mdirty = s.nextid, L.mask is not None
        s.nextid += 1
        s.layers.insert(i + 1, L)
        s.ai = i + 1

    def rename(s, name, new):
        s._L(name).name = new

    def move(s, name, above=None, below=None):
        L = s.layers.pop(s._find(name))
        i = s._find(above) + 1 if above else s._find(below) if below else len(s.layers)
        s.layers.insert(i, L)
        s.ai = i

    def merge_down(s, name=None):
        i = s.ai if name is None else s._find(name)
        if i == 0 or s.layers[i - 1].kind != 'pixel' or s.layers[i].kind != 'pixel':
            raise ValueError('nothing paintable to merge down into')
        T, Bt = s.layers[i], s.layers[i - 1]
        src = T.px * (T.opacity * (T.mask[..., None] if T.mask is not None else 1.0))
        Bt.px = composite(Bt.px, src.astype(F32), T.blend)
        Bt.dirty = True
        del s.layers[i]
        s.ai = i - 1

    def stamp_visible(s, new, names=None):
        """Flatten what is visible (or just the named layers) into a new layer on top."""
        acc = s._flat(names=names)
        s.layer(new, above=s.layers[-1].name)
        s._A.px = acc
        s._A.dirty = True

    def clear(s):
        s._A.px[:] = 0
        s._A.dirty = True

    def mask(s, source='selection', name=None):
        L = s._L(name)
        if isinstance(source, np.ndarray):
            L.mask = np.clip(source, 0, 1).astype(F32)
        elif source == 'selection':
            L.mask = (s.sel if s.sel is not None else np.ones((s.h, s.w), F32)).copy()
        else:
            L.mask = np.full((s.h, s.w), 1.0 if source == 'white' else 0.0, F32)
        L.mdirty = True

    def mask_mode(s, on=True):
        s.mmode = on

    def apply_mask(s, name=None):
        L = s._L(name)
        if L.mask is not None:
            L.px *= L.mask[..., None]
            L.mask, L.dirty = None, True

    def drop_mask(s, name=None):
        s._L(name).mask = None

    def adjust(s, name, kind, **args):
        if kind not in ADJ:
            raise ValueError(f'no adjustment {kind!r}')
        L = Layer(name, 'adjust')
        L.params, L.id = dict(kind=kind, args=args), s.nextid
        s.nextid += 1
        s.layers.insert(s.ai + 1, L)
        s.ai += 1

    def px(s, name=None):
        L = s._L(name)
        L.dirty = True
        return L.px

    # ==================================================== brushes
    def color(s, c):
        s.fg = col(c)
        return s.fg

    def brush(s, tip=None, **kw):
        if tip is not None:
            kw['tip'] = tip
        for k in kw:
            if k not in BRUSH0:
                raise ValueError(f'no brush setting {k!r}')
        s.brushd.update(kw)

    def preset(s, name, **kw):
        s.brushd = dict(BRUSH0, **PRESETS[name])
        s.brush(**kw)

    def _jit(s, c, B):
        h, sa, v = colorsys.rgb_to_hsv(*[float(x) for x in np.clip(l2s(c), 0, 1)])
        r = s.rng
        h = (h + B['hue_jitter'] / 360 * r.uniform(-1, 1)) % 1
        sa = min(max(sa * (1 + B['sat_jitter'] * r.uniform(-1, 1)), 0), 1)
        v = min(max(v * (1 + B['val_jitter'] * r.uniform(-1, 1)), 0), 1)
        return s2l(colorsys.hsv_to_rgb(h, sa, v))

    def _stamp(s, buf, bx, by, B, d, ang, x, y, c, a):
        if B['tip'] == 'round' and B['roundness'] > .98 and d < 28:
            n = int(math.ceil(d)) + 3
            ix, iy = int(math.floor(x)) - n // 2, int(math.floor(y)) - n // 2
            tip = _round_tip(n, d, B['hardness'], x - ix, y - iy)
        else:
            tip = get_tip(B['tip'], d, ang, B['roundness'], B['hardness'])
            n = tip.shape[0]
            ix, iy = int(round(x - (n - 1) / 2)), int(round(y - (n - 1) / 2))
        X0, Y0 = max(ix, bx), max(iy, by)
        X1, Y1 = min(ix + n, bx + buf.shape[1]), min(iy + n, by + buf.shape[0])
        if X1 <= X0 or Y1 <= Y0:
            return
        t = tip[Y0 - iy:Y1 - iy, X0 - ix:X1 - ix] * F32(a)
        reg = buf[Y0 - by:Y1 - by, X0 - bx:X1 - bx]
        k = 1 - t
        reg[..., 0] = reg[..., 0] * k + c[0] * t
        reg[..., 1] = reg[..., 1] * k + c[1] * t
        reg[..., 2] = reg[..., 2] * k + c[2] * t
        reg[..., 3] = reg[..., 3] * k + t

    def _paint(s, Q, ang, pr, c0, B):
        size = float(B['size'])
        pad = int(size * (1 + B['size_jitter']) * .8 + B['scatter'] * size * 3.2 + 6)
        x0, y0 = max(int(Q[:, 0].min()) - pad, 0), max(int(Q[:, 1].min()) - pad, 0)
        x1, y1 = min(int(Q[:, 0].max()) + pad, s.w), min(int(Q[:, 1].max()) + pad, s.h)
        if x1 <= x0 or y1 <= y0:
            return
        buf = np.zeros((y1 - y0, x1 - x0, 4), F32)
        r = s.rng
        jit = B['hue_jitter'] or B['sat_jitter'] or B['val_jitter']
        L = s._A
        for i in range(len(Q)):
            for _ in range(int(B['count'])):
                p = float(pr[i])
                d = size * (p if B['psize'] else 1.0)
                if B['size_jitter']:
                    d *= 1 + B['size_jitter'] * r.uniform(-1, 1)
                if d < .3:
                    continue
                x, y = Q[i, 0], Q[i, 1]
                if B['scatter']:
                    x += r.normal(0, B['scatter'] * size)
                    y += r.normal(0, B['scatter'] * size)
                a = B['flow'] * (p if B['pflow'] else 1.0)
                if B['flow_jitter']:
                    a *= 1 - B['flow_jitter'] * r.random()
                th = B['angle'] + (ang[i] if B['follow'] else 0.0)
                if B['angle_jitter']:
                    th += B['angle_jitter'] * r.uniform(-180, 180)
                c = s._jit(c0, B) if jit else c0
                if B['mix'] > 0 and L.kind == 'pixel':
                    xi, yi = int(min(max(x, 0), s.w - 1)), int(min(max(y, 0), s.h - 1))
                    under = L.px[yi, xi]
                    if under[3] > .05:
                        c = c * (1 - B['mix']) + under[:3] / under[3] * B['mix']
                s._stamp(buf, x0, y0, B, d, th, x, y, c, a)
        if B['grain'] > 0:
            buf *= (1 - B['grain'] + B['grain'] * s._grain()[y0:y1, x0:x1])[..., None]
        if B['opacity'] != 1:
            buf *= F32(B['opacity'])
        s._commit(buf, x0, y0, B['blend'])

    def stroke(s, points, color=None, pressure=None, **kw):
        """One brush stroke through the points; each may carry a pressure 0..1 as a third value."""
        B = dict(s.brushd, **kw)
        P = np.array([[p[0], p[1], (p[2] if len(p) > 2 else 1.0)] for p in points], float)
        if pressure is not None:
            P[:, 2] = np.interp(np.linspace(0, 1, len(P)), np.linspace(0, 1, len(pressure)), pressure)
        if B['smooth'] and len(P) > 2:
            P = _smooth(P)
        Q, ang, u = _resample(P, max(.35, B['spacing'] * float(B['size'])))
        pr = Q[:, 2].copy()
        ta, tb = B['taper']
        if ta > 0:
            pr *= np.clip(u / ta, 0, 1)
        if tb > 0:
            pr *= np.clip((1 - u) / tb, 0, 1)
        s._paint(Q, ang, pr, col(color) if color is not None else s.fg, B)
        s._op()

    def dabs(s, points, color=None, **kw):
        """Single stamps at points (x, y[, size scale])."""
        B = dict(s.brushd, **kw)
        P = np.asarray([[p[0], p[1], (p[2] if len(p) > 2 else 1.0)] for p in points], float)
        if len(P):
            s._paint(P, np.zeros(len(P)), P[:, 2], col(color) if color is not None else s.fg, B)
            s._op()

    def scatter(s, n, area=None, density=None, color=None, **kw):
        """n stamps placed at random in a rect (x0,y0,x1,y1), a polygon, or by a density map."""
        r = s.rng
        if density is None and area is not None and not np.isscalar(area[0]):
            m, x0, y0 = s._mask_of(area)
            density = np.zeros((s.h, s.w), F32)
            density[y0:y0 + m.shape[0], x0:x0 + m.shape[1]] = m
        if density is not None:
            k = 4
            p = np.clip(cv2.resize(np.asarray(density, F32), (s.w // k, s.h // k), interpolation=cv2.INTER_AREA), 0, None).ravel().astype(np.float64)
            idx = r.choice(len(p), size=n, p=p / p.sum())
            ys, xs = np.divmod(idx, s.w // k)
            pts = np.stack([(xs + r.random(n)) * k, (ys + r.random(n)) * k], 1)
        else:
            x0, y0, x1, y1 = area if area is not None else (0, 0, s.w, s.h)
            pts = np.stack([r.uniform(x0, x1, n), r.uniform(y0, y1, n)], 1)
        s.dabs(pts, color, **kw)

    def erase(s, points, **kw):
        s.stroke(points, **dict(kw, blend='erase'))

    def _walk(s, points, size, spacing):
        P = np.array([[p[0], p[1]] for p in points], float)
        Q, ang, _ = _resample(_smooth(P) if len(P) > 2 else P, max(1.0, size * spacing))
        n = int(size) | 1
        for x, y in Q:
            x0, y0 = int(round(x)) - n // 2, int(round(y)) - n // 2
            if x0 < 0 or y0 < 0 or x0 + n > s.w or y0 + n > s.h:
                yield None
            else:
                yield x0, y0, n

    def smudge(s, points, size=40, strength=.7, hardness=.2, spacing=.1):
        """Drag paint along a path."""
        L, carried = s._A, None
        for w in s._walk(points, size, spacing):
            if w is None:
                carried = None
                continue
            x0, y0, n = w
            cur = L.px[y0:y0 + n, x0:x0 + n]
            if carried is not None:
                m = get_tip('round', n - 3, 0, 1, hardness)[:n, :n, None] * strength
                if m.shape[0] != n:
                    m = cv2.resize(m[..., 0], (n, n))[..., None]
                if s.sel is not None:
                    m = m * s.sel[y0:y0 + n, x0:x0 + n, None]
                new = cur * (1 - m) + carried * m
                L.px[y0:y0 + n, x0:x0 + n] = new
                carried = new.copy()
            else:
                carried = cur.copy()
        L.dirty = True
        s._op()

    def _local(s, points, size, spacing, hardness, fn):
        L = s._A
        for w in s._walk(points, size, spacing):
            if w is None:
                continue
            x0, y0, n = w
            m = cv2.resize(get_tip('round', max(n - 3, 4), 0, 1, hardness), (n, n))[..., None]
            if s.sel is not None:
                m = m * s.sel[y0:y0 + n, x0:x0 + n, None]
            cur = L.px[y0:y0 + n, x0:x0 + n]
            L.px[y0:y0 + n, x0:x0 + n] = cur + (fn(cur) - cur) * m
        L.dirty = True
        s._op()

    def blur_stroke(s, points, size=60, strength=1.0, radius=6.0, hardness=.2):
        s._local(points, size, .25, hardness, lambda c: c + (cv2.GaussianBlur(c, (0, 0), radius) - c) * strength)

    def dodge(s, points, size=60, exposure=.2, hardness=.1):
        """Lighten along a path."""
        def f(c):
            o = c.copy()
            o[..., :3] *= 1 + exposure
            return o
        s._local(points, size, .25, hardness, f)

    def burn(s, points, size=60, exposure=.2, hardness=.1):
        def f(c):
            o = c.copy()
            o[..., :3] *= 1 - exposure
            return o
        s._local(points, size, .25, hardness, f)

    def liquify(s, points, size=120, strength=.5):
        """Push pixels along a path."""
        L = s._A
        prev = None
        for w in s._walk(points, size, .2):
            if w is None:
                prev = None
                continue
            x0, y0, n = w
            if prev is not None:
                dx, dy = (x0 - prev[0]) * strength, (y0 - prev[1]) * strength
                m = cv2.resize(get_tip('round', max(n - 3, 4), 0, 1, 0.0), (n, n))
                yy, xx = np.mgrid[:n, :n].astype(F32)
                L.px[y0:y0 + n, x0:x0 + n] = cv2.remap(np.ascontiguousarray(L.px[y0:y0 + n, x0:x0 + n]), xx - dx * m, yy - dy * m,
                                                       cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
            prev = (x0, y0)
        L.dirty = True
        s._op()

    # ==================================================== shapes and fills
    def fill(s, color=None, opacity=1.0, blend='normal'):
        c = col(color) if color is not None else s.fg
        rgba = np.empty((s.h, s.w, 4), F32)
        rgba[..., :3] = c * opacity
        rgba[..., 3] = opacity
        s._commit(rgba, 0, 0, blend)
        s._op(True)

    def fill_poly(s, points, color=None, opacity=1.0, feather=0.0, blend='normal', smooth=False):
        m, x0, y0 = s._mask_of(points, feather, smooth)
        if m is None:
            return
        c = col(color) if color is not None else s.fg
        rgba = np.empty(m.shape + (4,), F32)
        m = m * opacity
        rgba[..., :3] = c * m[..., None]
        rgba[..., 3] = m
        s._commit(rgba, x0, y0, blend)
        s._op()

    def fill_ellipse(s, cx, cy, rx, ry, angle=0.0, **kw):
        t = np.linspace(0, 2 * math.pi, 96, endpoint=False)
        c, sn = math.cos(math.radians(angle)), math.sin(math.radians(angle))
        ex, ey = rx * np.cos(t), ry * np.sin(t)
        s.fill_poly(np.stack([cx + ex * c - ey * sn, cy + ex * sn + ey * c], 1), **kw)

    def fill_rect(s, x0, y0, x1, y1, **kw):
        s.fill_poly([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], **kw)

    def gradient(s, kind, p0, p1, stops, opacity=1.0, blend='normal', ease=None):
        """kind: linear radial reflect angle. stops: (position, colour[, alpha])."""
        yy, xx = np.mgrid[:s.h, :s.w].astype(F32)
        dx, dy = p1[0] - p0[0], p1[1] - p0[1]
        L2 = float(dx * dx + dy * dy) or 1.0
        if kind == 'radial':
            t = np.hypot(xx - p0[0], yy - p0[1]) / math.sqrt(L2)
        elif kind == 'angle':
            t = (np.arctan2(yy - p0[1], xx - p0[0]) - math.atan2(dy, dx)) / (2 * math.pi) % 1
        else:
            t = ((xx - p0[0]) * dx + (yy - p0[1]) * dy) / L2
            if kind == 'reflect':
                t = np.abs(t)
        t = np.clip(t, 0, 1)
        if ease == 'smooth':
            t = t * t * (3 - 2 * t)
        pos = [st[0] for st in stops]
        al = np.array([st[2] if len(st) > 2 else 1.0 for st in stops])
        cs = np.array([col(st[1]) for st in stops]) * al[:, None]
        rgba = np.empty((s.h, s.w, 4), F32)
        for k in range(3):
            rgba[..., k] = np.interp(t, pos, cs[:, k])
        rgba[..., 3] = np.interp(t, pos, al)
        rgba *= F32(opacity)
        s._commit(rgba, 0, 0, blend)
        s._op(True)

    def bucket(s, x, y, color=None, tol=12, opacity=1.0, feather=0.0):
        """Flood fill, judged on the visible picture."""
        img = np.ascontiguousarray(s._to8(s._flat(), dither=False))
        m = np.zeros((s.h + 2, s.w + 2), np.uint8)
        cv2.floodFill(img, m, (int(x), int(y)), (0, 0, 0), (tol,) * 3, (tol,) * 3, 4 | cv2.FLOODFILL_MASK_ONLY | (255 << 8))
        m = m[1:-1, 1:-1].astype(F32) / 255
        if feather > 0:
            m = cv2.GaussianBlur(m, (0, 0), feather)
        c = col(color) if color is not None else s.fg
        s._commit(np.dstack([c[0] * m, c[1] * m, c[2] * m, m]).astype(F32) * F32(opacity), 0, 0)
        s._op(True)

    def text(s, x, y, string, size=48, font=None, color=None, anchor='la', opacity=1.0, blend='normal'):
        path = font if font and os.path.exists(font) else subprocess.run(
            ['fc-match', '-f', '%{file}', font or 'sans'], capture_output=True, text=True).stdout.strip()
        f = ImageFont.truetype(path, int(size))
        l, t, r, b = f.getbbox(string, anchor=anchor)
        im = Image.new('L', (r - l + 4, b - t + 4), 0)
        ImageDraw.Draw(im).text((2 - l, 2 - t), string, fill=255, font=f, anchor=anchor)
        m = np.asarray(im, F32) / 255 * opacity
        c = col(color) if color is not None else s.fg
        s._commit(np.dstack([c[0] * m, c[1] * m, c[2] * m, m]).astype(F32), int(x + l - 2), int(y + t - 2), blend)
        s._op()

    # ==================================================== selections
    def select_all(s):
        s.sel, s.seldirty = None, False

    select_none = select_all

    def select_invert(s):
        s._setsel(1 - (s.sel if s.sel is not None else np.ones((s.h, s.w), F32)), 'replace')

    def select_poly(s, points, mode='replace', feather=0.0, smooth=False):
        m, x0, y0 = s._mask_of(points, feather, smooth)
        full = np.zeros((s.h, s.w), F32)
        if m is not None:
            full[y0:y0 + m.shape[0], x0:x0 + m.shape[1]] = m
        s._setsel(full, mode)

    def select_rect(s, x0, y0, x1, y1, **kw):
        s.select_poly([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], **kw)

    def select_ellipse(s, cx, cy, rx, ry, **kw):
        t = np.linspace(0, 2 * math.pi, 96, endpoint=False)
        s.select_poly(np.stack([cx + rx * np.cos(t), cy + ry * np.sin(t)], 1), **kw)

    def select_alpha(s, name=None, mode='replace'):
        s._setsel(np.clip(s._L(name).px[..., 3], 0, 1), mode)

    def select_luma(s, lo=.5, hi=1.0, soft=.05, mode='replace'):
        l = l2s(np.clip(lum(s._flat()[..., :3]), 0, 1))
        s._setsel(np.clip((l - lo) / soft + .5, 0, 1) * np.clip((hi - l) / soft + .5, 0, 1), mode)

    def select_color(s, color, tol=.12, soft=.05, mode='replace'):
        d = np.sqrt(((l2s(np.clip(s._flat()[..., :3], 0, 1)) - l2s(col(color))) ** 2).sum(-1))
        s._setsel(np.clip((tol - d) / soft + .5, 0, 1), mode)

    def select_array(s, a, mode='replace'):
        s._setsel(np.clip(np.asarray(a, F32), 0, 1), mode)

    def feather(s, r):
        if s.sel is not None:
            s._setsel(cv2.GaussianBlur(s.sel, (0, 0), r), 'replace')

    def grow(s, px):
        if s.sel is not None and px:
            k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * abs(int(px)) + 1,) * 2)
            s._setsel((cv2.dilate if px > 0 else cv2.erode)(s.sel, k), 'replace')

    # ==================================================== filters
    def gaussian_blur(s, r):
        if s.mmode and s._A.mask is not None:
            s._A.mask = cv2.GaussianBlur(s._A.mask, (0, 0), r)
            s._A.mdirty = True
            return
        s._filter(lambda p: cv2.GaussianBlur(p, (0, 0), r))

    def _ray_kernel(s, length, angle, decay, two_sided):
        k = int(length) * 2 + 1
        K = np.zeros((k, k), F32)
        c = k // 2
        dx, dy = math.cos(math.radians(angle)), -math.sin(math.radians(angle))
        for t in np.arange(0, length, .5):
            wgt = math.exp(-t / (decay * length)) if decay else 1.0
            for sg in ((1, -1) if two_sided else (1,)):
                x, y = c - sg * dx * t, c - sg * dy * t
                xi, yi = int(math.floor(x)), int(math.floor(y))
                fx, fy = x - xi, y - yi
                for ox, oy, ww in ((0, 0, (1 - fx) * (1 - fy)), (1, 0, fx * (1 - fy)), (0, 1, (1 - fx) * fy), (1, 1, fx * fy)):
                    if 0 <= xi + ox < k and 0 <= yi + oy < k:
                        K[yi + oy, xi + ox] += wgt * ww
        return K / K.sum()

    def motion_blur(s, length=40, angle=0.0):
        K = s._ray_kernel(length / 2, angle, 0, True)
        s._filter(lambda p: cv2.filter2D(p, -1, K, borderType=cv2.BORDER_REPLICATE))

    def smear(s, length=200, angle=90.0, decay=.4, gain=1.0):
        """One-sided streak: everything trails off in the given direction (90 = up)."""
        K = s._ray_kernel(length, angle, decay, False) * gain
        s._filter(lambda p: cv2.filter2D(p, -1, K, borderType=cv2.BORDER_CONSTANT))

    def zoom_blur(s, cx, cy, amount=.1, steps=16):
        def fn(p):
            acc = np.zeros_like(p)
            for i in range(steps):
                z = 1 + amount * i / (steps - 1)
                M = np.array([[z, 0, cx * (1 - z)], [0, z, cy * (1 - z)]])
                acc += cv2.warpAffine(p, M, (s.w, s.h), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
            return acc / steps
        s._filter(fn)

    def sharpen(s, amount=.6, radius=1.5):
        s._filter(lambda p: p + (p - cv2.GaussianBlur(p, (0, 0), radius)) * amount)

    def high_pass(s, radius=8.0):
        def fn(p):
            o = p.copy()
            o[..., :3] = (p[..., :3] - cv2.GaussianBlur(p, (0, 0), radius)[..., :3]) * .5 + .18 * p[..., 3:4]
            return o
        s._filter(fn)

    def median(s, k=5):
        s._filter(lambda p: np.dstack([cv2.medianBlur(np.ascontiguousarray(p[..., i]), k | 1 if k <= 5 else 5) for i in range(4)]))

    def emboss(s, angle=135.0, depth=1.0):
        dx, dy = math.cos(math.radians(angle)), -math.sin(math.radians(angle))
        def fn(p):
            l = lum(p[..., :3])
            g = (cv2.Sobel(l, cv2.CV_32F, 1, 0) * dx + cv2.Sobel(l, cv2.CV_32F, 0, 1) * dy) * depth
            o = p.copy()
            o[..., :3] = np.clip(.18 + g, 0, 1)[..., None] * p[..., 3:4]
            return o
        s._filter(fn)

    def noise(s, amount=.03, mono=True, scale=1.0, seed=None):
        """Grain, in perceptual units, added where the layer has paint."""
        r = np.random.default_rng(s.rng.integers(1 << 30) if seed is None else seed)
        h, w = int(s.h / scale), int(s.w / scale)
        n = r.normal(0, 1, (h, w, 1 if mono else 3)).astype(F32)
        if scale != 1:
            n = cv2.resize(n, (s.w, s.h), interpolation=cv2.INTER_CUBIC).reshape(s.h, s.w, -1)
        s._cfilter(lambda rgb: s2l(np.clip(l2s(rgb) + n * amount, 0, 1)))

    def clouds(s, c1='#000000', c2='#ffffff', scale=5.0, octaves=6, seed=0, stretch=(1, 1), ridged=False, contrast=1.0, opacity=1.0, blend='normal'):
        """Render fractal noise between two colours."""
        n = np.clip((fbm(s.h, s.w, scale, octaves, seed, stretch=stretch, ridged=ridged) - .5) * contrast + .5, 0, 1)[..., None]
        rgb = col(c1) * (1 - n) + col(c2) * n
        s._commit(np.dstack([rgb, np.ones((s.h, s.w), F32)]).astype(F32) * F32(opacity), 0, 0, blend)
        s._op(True)

    def noise_field(s, scale=5.0, octaves=5, seed=0, stretch=(1, 1), ridged=False):
        return fbm(s.h, s.w, scale, octaves, seed, stretch=stretch, ridged=ridged)

    def modulate(s, arr):
        """Multiply the layer (colour and alpha) by a 2-D array."""
        s._filter(lambda p: p * np.asarray(arr, F32)[..., None])

    def glow(s, radius=30.0, strength=.6, threshold=0.0):
        def fn(p):
            b = p.copy()
            b[..., :3] = np.maximum(b[..., :3] - threshold * b[..., 3:4], 0)
            g = cv2.GaussianBlur(b, (0, 0), radius) * strength
            o = p.copy()
            o[..., :3] += g[..., :3]
            o[..., 3] = np.clip(o[..., 3] + g[..., 3] * (1 - o[..., 3]), 0, 1)
            return o
        s._filter(fn)

    def _remap(s, dx, dy):
        yy, xx = np.mgrid[:s.h, :s.w].astype(F32)
        s._filter(lambda p: cv2.remap(p, xx + dx.astype(F32), yy + dy.astype(F32), cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE))

    def turbulence(s, amount=12.0, scale=8.0, seed=0, octaves=3):
        """Displace by fractal noise: roughens edges, breaks up straight lines."""
        s._remap((fbm(s.h, s.w, scale, octaves, seed) - .5) * 2 * amount, (fbm(s.h, s.w, scale, octaves, seed + 1) - .5) * 2 * amount)

    def wave(s, amp=6.0, wavelength=60.0, axis='x', phase=0.0):
        yy, xx = np.mgrid[:s.h, :s.w].astype(F32)
        if axis == 'x':
            s._remap(amp * np.sin(yy / wavelength * 2 * math.pi + phase), np.zeros_like(xx))
        else:
            s._remap(np.zeros_like(xx), amp * np.sin(xx / wavelength * 2 * math.pi + phase))

    def vignette(s, strength=.5, radius=.75, softness=.5, color='#000000'):
        yy, xx = np.mgrid[:s.h, :s.w].astype(F32)
        d = np.hypot((xx - s.w / 2) / (s.w / 2), (yy - s.h / 2) / (s.h / 2)) / math.sqrt(2)
        m = np.clip((d - radius * .7) / max(softness, 1e-3), 0, 1)
        m = (m * m * (3 - 2 * m) * strength)[..., None]
        c = col(color)
        s._cfilter(lambda rgb: rgb * (1 - m) + c * m)

    def levels(s, **kw): s._cfilter(lambda r: a_levels(r, **kw))
    def curves(s, points, channel='rgb'): s._cfilter(lambda r: a_curves(r, points, channel))
    def hue_sat(s, **kw): s._cfilter(lambda r: a_hue_sat(r, **kw))
    def balance(s, **kw): s._cfilter(lambda r: a_balance(r, **kw))
    def brightness_contrast(s, **kw): s._cfilter(lambda r: a_brightness_contrast(r, **kw))
    def exposure(s, stops): s._cfilter(lambda r: a_exposure(r, stops))
    def desaturate(s, amount=1.0): s._cfilter(lambda r: a_desaturate(r, amount))
    def posterize(s, levels=4): s._cfilter(lambda r: a_posterize(r, levels))
    def threshold(s, level=.5): s._cfilter(lambda r: a_threshold(r, level))
    def colorize(s, color, amount=1.0): s._cfilter(lambda r: a_colorize(r, color, amount))
    def gradient_map(s, stops): s._cfilter(lambda r: a_gradient_map(r, stops))

    def invert(s):
        if s.mmode and s._A.mask is not None:
            s._A.mask = 1 - s._A.mask
            s._A.mdirty = True
            return
        s._cfilter(a_invert)

    # ==================================================== transforms
    def _warp(s, M, persp=False):
        L = s._A
        f = cv2.warpPerspective if persp else cv2.warpAffine
        L.px = f(L.px, M, (s.w, s.h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_CONSTANT)
        if L.mask is not None:
            L.mask = np.clip(f(L.mask, M, (s.w, s.h), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT), 0, 1)
            L.mdirty = True
        L.dirty = True
        s._op(True)

    def transform(s, scale=1.0, rotate=0.0, translate=(0, 0), center=None):
        cx, cy = center or (s.w / 2, s.h / 2)
        sx, sy = (scale, scale) if np.isscalar(scale) else scale
        c, sn = math.cos(math.radians(rotate)), math.sin(math.radians(rotate))
        A = np.array([[c * sx, -sn * sy], [sn * sx, c * sy]])
        t = np.array([cx + translate[0], cy + translate[1]]) - A @ np.array([cx, cy])
        s._warp(np.hstack([A, t[:, None]]))

    def flip(s, axis='h'):
        L = s._A
        L.px = np.ascontiguousarray(L.px[:, ::-1] if axis == 'h' else L.px[::-1])
        if L.mask is not None:
            L.mask = np.ascontiguousarray(L.mask[:, ::-1] if axis == 'h' else L.mask[::-1])
            L.mdirty = True
        L.dirty = True
        s._op(True)

    def perspective(s, src, dst):
        s._warp(cv2.getPerspectiveTransform(np.asarray(src, F32), np.asarray(dst, F32)), True)

    # ==================================================== looking
    def sample(s, x, y, r=2):
        a = s._flat((max(int(y) - r, 0), int(y) + r + 1, max(int(x) - r, 0), int(x) + r + 1))
        c = l2s(np.clip(a[..., :3].mean((0, 1)), 0, 1))
        hx = '#%02x%02x%02x' % tuple(int(round(v * 255)) for v in c)
        print(f'sample({int(x)},{int(y)}) = {hx}')
        return hx

    def path(s, points, closed=False):
        return _smooth(points, closed)


def render_view(D, crop=None, maxdim=1500, layer=None):
    x, y, w, h = crop or (0, 0, D.w, D.h)
    x, y = max(0, x), max(0, y)
    w, h = min(w, D.w - x), min(h, D.h - y)
    img = D._to8(D._flat((y, y + h, x, x + w), names=[layer] if layer else None))
    sc = min(maxdim / w, maxdim / h, 6.0)
    img = cv2.resize(img, (int(w * sc), int(h * sc)), interpolation=cv2.INTER_AREA if sc < 1 else cv2.INTER_CUBIC)
    M = 26
    out = np.full((img.shape[0] + M, img.shape[1] + M, 3), 24, np.uint8)
    out[M:, M:] = img
    step = next(st for st in (10, 20, 50, 100, 200, 500, 1000) if st * sc >= 70)
    for v in range((x // step + 1) * step, x + w, step):
        X = int((v - x) * sc) + M
        out[M - 6:M, X] = 200
        cv2.putText(out, str(v), (X - 14, 13), cv2.FONT_HERSHEY_SIMPLEX, .38, (220, 220, 220), 1, cv2.LINE_AA)
    for v in range((y // step + 1) * step, y + h, step):
        Y = int((v - y) * sc) + M
        out[Y, M - 6:M] = 200
        cv2.putText(out, str(v), (0, Y + 4), cv2.FONT_HERSHEY_SIMPLEX, .32, (220, 220, 220), 1, cv2.LINE_AA)
    return out


# ============================================================ command line
def cmd_new(a):
    if os.path.exists(sdir(a.session)):
        if not a.force:
            sys.exit(f'session {a.session!r} exists (--force to start over)')
        shutil.rmtree(sdir(a.session))
    os.makedirs(sdir(a.session, 'scripts'))
    w, h = (int(v) for v in a.size.lower().split('x'))
    D = Doc(a.session, w, h)
    D.layer('Background')
    D.fill(a.bg)
    D.frames = 0
    D._save()
    print(f'{a.session}: {w}x{h}, float32 linear RGBA')


def cmd_run(a):
    D = Doc._load(a.session)
    D.batch += 1
    D.rng = np.random.default_rng(1000 + D.batch)
    ns = {k: getattr(D, k) for k in dir(D) if not k.startswith('_') and callable(getattr(D, k))}
    ns.update(W=D.w, H=D.h, rng=D.rng, np=np, math=math, cv2=cv2, col=col, hsv=hsv, mix=mix, fbm=fbm, s2l=s2l, l2s=l2s, lum=lum)
    src = open(a.script).read()
    t0 = time.time()
    try:
        exec(compile(src, a.script, 'exec'), ns)
    except Exception:
        traceback.print_exc()
        sys.exit('script failed -- nothing was saved')
    D._op(True)
    with open(sdir(a.session, 'scripts', f'{D.batch:03d}.py'), 'w') as f:
        f.write(src)
    D._save()
    cv2.imwrite(sdir(a.session, 'view.jpg'), render_view(D)[..., ::-1], [cv2.IMWRITE_JPEG_QUALITY, 90])
    print(f'batch {D.batch:03d} ok in {time.time() - t0:.1f}s; {len(D.layers)} layers; view -> {sdir(a.session, "view.jpg")}')


def cmd_undo(a):
    d = sdir(a.session)
    b = json.load(open(os.path.join(d, 'head.json')))['batch']
    nb = max(0, b - a.n)
    if not os.path.exists(os.path.join(d, f'state_{nb:04d}.json')):
        sys.exit('that far back is no longer kept (undo depth is 3)')
    with open(os.path.join(d, 'head.json'), 'w') as f:
        json.dump({'batch': nb}, f)
    fr = json.load(open(os.path.join(d, f'state_{nb:04d}.json')))['frames']
    for f in glob.glob(os.path.join(d, 'frames', '*.jpg')):
        if int(os.path.basename(f)[:6]) >= fr:
            os.remove(f)
    for k in range(nb + 1, b + 1):
        for f in (os.path.join(d, f'state_{k:04d}.json'), os.path.join(d, 'scripts', f'{k:03d}.py')):
            if os.path.exists(f):
                os.remove(f)
    print(f'back to batch {nb:03d}')


def cmd_view(a):
    D = Doc._load(a.session)
    out = a.out or sdir(a.session, 'crop.jpg' if a.crop else 'view.jpg')
    cv2.imwrite(out, render_view(D, a.crop, a.max, a.layer)[..., ::-1], [cv2.IMWRITE_JPEG_QUALITY, 92])
    print(out)


def cmd_layers(a):
    D = Doc._load(a.session)
    for i, L in reversed(list(enumerate(D.layers))):
        print(f"{'>' if i == D.ai else ' '} {i:2d} {L.name:<18} {L.kind:<6} {L.blend:<10} {L.opacity:4.2f}"
              f"{'' if L.visible else '  hidden'}{'  clip' if L.clip else ''}{'  lock' if L.lock else ''}{'  mask' if L.mask is not None else ''}"
              f"{'  ' + L.params['kind'] if L.kind == 'adjust' else ''}")


def cmd_export(a):
    D = Doc._load(a.session)
    acc = D._flat()
    if a.scale != 1:
        acc = cv2.resize(acc, None, fx=a.scale, fy=a.scale, interpolation=cv2.INTER_AREA if a.scale < 1 else cv2.INTER_LANCZOS4)
    if a.bits == 16:
        img = np.clip(np.round(l2s(np.clip(acc[..., :3], 0, 1)) * 65535), 0, 65535).astype(np.uint16)
    else:
        img = D._to8(acc)
    cv2.imwrite(a.out, img[..., ::-1], [cv2.IMWRITE_JPEG_QUALITY, 95] if a.out.lower().endswith(('.jpg', '.jpeg')) else [])
    print(a.out, img.shape[1], 'x', img.shape[0])


def cmd_plates(a):
    """Write every visible pixel layer as its own 16-bit PNG with alpha, plus plates.json (bottom to top):
    plates that an animation stand can move separately (see ../backlot, comp.multiplane)."""
    D = Doc._load(a.session)
    os.makedirs(a.out, exist_ok=True)
    man = []
    for i, L in enumerate(D.layers):
        if L.kind != 'pixel' or not L.visible or L.px is None:
            continue
        p = L.px if L.mask is None else L.px * L.mask[..., None]
        al = np.clip(p[..., 3:4], 0, 1)
        if float(al.max()) <= 0:
            continue
        rgb = l2s(np.clip(p[..., :3] / np.maximum(al, 1e-6), 0, 1))
        img = np.clip(np.round(np.concatenate([np.asarray(rgb)[..., ::-1], al], 2) * 65535), 0, 65535).astype(np.uint16)
        fn = f'{i:02d}_{L.name}.png'
        cv2.imwrite(os.path.join(a.out, fn), img)
        man.append(dict(file=fn, name=L.name, blend=L.blend, opacity=L.opacity, clip=L.clip))
    json.dump(dict(size=[D.w, D.h], plates=man), open(os.path.join(a.out, 'plates.json'), 'w'), indent=1)
    print(len(man), 'plates ->', a.out)


def cmd_timelapse(a):
    d = sdir(a.session, 'frames')
    files = sorted(glob.glob(os.path.join(d, '*.jpg')))
    if not files:
        sys.exit('no frames recorded')
    lst = os.path.join(d, 'list.txt')
    with open(lst, 'w') as f:
        for p in files:
            f.write(f"file '{p}'\nduration {1 / a.fps:.4f}\n")
        f.write(f"file '{files[-1]}'\nduration 4\nfile '{files[-1]}'\n")
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', lst, '-vf', 'scale=trunc(iw/2)*2:trunc(ih/2)*2',
                    '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '20', '-r', '30', a.out], check=True)
    print(a.out, len(files), 'frames')


TIP_NAMES = 'round chalk charcoal sponge cloud bristle flat splatter stipple leaf blade needle star spruce square'


def cmd_api(a):
    """Print every script function with its real signature, straight from the code."""
    import inspect
    for k in sorted(dir(Doc)):
        f = getattr(Doc, k)
        if k.startswith('_') or not callable(f):
            continue
        sig = str(inspect.signature(f)).replace('(s, ', '(').replace('(s)', '()')
        doc = ' '.join((f.__doc__ or '').split())
        print(f'{k}{sig}' + (f'   # {doc}' if doc else ''))
    print('\nalso in scope: W H rng np math cv2 col(c) hsv(h,s,v) mix(a,b,t) fbm(h,w,scale,octaves,seed,...) s2l l2s lum')
    print('\nbrush settings and defaults:')
    for k, v in BRUSH0.items():
        print(f'  {k} = {v!r}')
    print('\npresets: ' + ' '.join(PRESETS))
    print('tips: ' + TIP_NAMES)
    print('layer blends: normal add ' + ' '.join(BLEND) + '   (brush-only: erase behind)')
    print('adjustment kinds: ' + ' '.join(ADJ))


def main():
    ap = argparse.ArgumentParser(prog='studio.py', description='Fable Studio')
    sub = ap.add_subparsers(dest='cmd', required=True)
    p = sub.add_parser('new'); p.add_argument('session'); p.add_argument('--size', default='2560x1440'); p.add_argument('--bg', default='#ffffff'); p.add_argument('--force', action='store_true'); p.set_defaults(fn=cmd_new)
    p = sub.add_parser('run'); p.add_argument('session'); p.add_argument('script'); p.set_defaults(fn=cmd_run)
    p = sub.add_parser('undo'); p.add_argument('session'); p.add_argument('n', type=int, nargs='?', default=1); p.set_defaults(fn=cmd_undo)
    p = sub.add_parser('view'); p.add_argument('session'); p.add_argument('--crop', type=int, nargs=4); p.add_argument('--layer'); p.add_argument('--max', type=int, default=1500); p.add_argument('-o', '--out'); p.set_defaults(fn=cmd_view)
    p = sub.add_parser('layers'); p.add_argument('session'); p.set_defaults(fn=cmd_layers)
    p = sub.add_parser('export'); p.add_argument('session'); p.add_argument('-o', '--out', required=True); p.add_argument('--bits', type=int, default=8); p.add_argument('--scale', type=float, default=1.0); p.set_defaults(fn=cmd_export)
    p = sub.add_parser('timelapse'); p.add_argument('session'); p.add_argument('-o', '--out', required=True); p.add_argument('--fps', type=int, default=30); p.set_defaults(fn=cmd_timelapse)
    p = sub.add_parser('plates'); p.add_argument('session'); p.add_argument('-o', '--out', required=True); p.set_defaults(fn=cmd_plates)
    sub.add_parser('help').set_defaults(fn=lambda a: print(__doc__))
    sub.add_parser('api').set_defaults(fn=cmd_api)
    a = ap.parse_args()
    a.fn(a)


if __name__ == '__main__':
    main()
