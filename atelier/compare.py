#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = ["pillow"]
# ///
"""Build the side-by-side comparison sheets in compare/."""
from PIL import Image, ImageDraw, ImageFont
BG, FG = '#1e1e1e', '#e8e4d8'
def font(sz):
    for p in ('/usr/share/fonts/liberation/LiberationSans-Regular.ttf', '/usr/share/fonts/TTF/DejaVuSans.ttf'):
        try: return ImageFont.truetype(p, sz)
        except Exception: pass
    return ImageFont.load_default()
def fit(im, h=None, w=None):
    if h: return im.resize((int(im.width * h / im.height), h), Image.LANCZOS)
    return im.resize((w, int(im.height * w / im.width)), Image.LANCZOS)
def row(items, h, pad=24, title=None):
    """items: list of (image, caption). Returns one strip."""
    ims = [(fit(im, h=h), cap) for im, cap in items]
    W = sum(i.width for i, _ in ims) + pad * (len(ims) + 1)
    top = 64 if title else 16
    out = Image.new('RGB', (W, h + top + 52), BG); d = ImageDraw.Draw(out)
    if title: d.text((pad, 18), title, fill=FG, font=font(28))
    x = pad
    for im, cap in ims:
        out.paste(im, (x, top)); d.text((x, top + h + 12), cap, fill='#b8b4a8', font=font(20)); x += im.width + pad
    return out
def stack(rows, pad=0):
    W = max(r.width for r in rows)
    out = Image.new('RGB', (W, sum(r.height for r in rows) + pad * (len(rows) - 1)), BG)
    y = 0
    for r in rows: out.paste(r, (0, y)); y += r.height + pad
    return out
O = Image.open
s1 = O('studies/s01_materials.png'); a = O('studies/s02a_memory_subjects.png'); b = O('studies/s02b_reference_subjects.png')
# 1. memory against reference, subject by subject
heron = row([(a.crop((20, 20, 653, 620)), 'heron, from memory'), (b.crop((20, 20, 653, 620)), 'heron, after two photographs and a grid')], 520, title='1. What a reference does: the same subject from memory, then after looking')
ferry = row([(a.crop((673, 20, 1306, 620)), 'ferry, from memory'), (b.crop((673, 20, 1306, 620)), 'ferry, after four photographs (box model in metres)')], 520)
fir = row([(s1.crop((886, 460, 1306, 880)), 'firs, from memory'), (b.crop((20, 640, 1306, 1060)), 'firs, after a photograph and a Yoshida print')], 420)
stack([heron, ferry, fir]).save('compare/1_memory_vs_reference.png')
# 2. the same picture before any research and after
row([(O('studies/s00_memory.png'), 'Study 0: from memory, before any research'), (O('refs/prints/h_ushibori_evening.jpg'), 'what a real one looks like (Hasui, 1930)'),
     (O('prints/p1_last_boat_v1.png'), 'Print 1, first pass with the notes'), (O('prints/p1_last_boat_v2.png'), 'Print 1 after its own critique')], 900,
    title='2. The same subject (night ferry) before research, and after research plus notes').save('compare/2_before_and_after_notes.png')
# 3. the assigned subject, without and with the method
old = O('../gallery/studio/orca_vs_mech.png')
row([(old, 'before: painted as a realistic scene, no method'), (O('prints/p3_full_moon_v2.png'), 'after: same brief through the method')], 900,
    title='3. The assigned subject (orca, machine, full moon, battle)').save('compare/3_assigned_subject.png')
# 4. the three prints
row([(O('prints/p1_last_boat_v2.png'), 'Last boat, rain'), (O('prints/p2_lookout_v2.png'), 'Lookout, first snow'), (O('prints/p3_full_moon_v2.png'), 'Full moon over the Sound')], 1100).save('compare/4_three_prints.png')
for f in ('1_memory_vs_reference', '2_before_and_after_notes', '3_assigned_subject', '4_three_prints'):
    print(f, O(f'compare/{f}.png').size)
