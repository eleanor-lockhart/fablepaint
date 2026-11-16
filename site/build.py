#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = ["pillow"]
# ///
"""Build the GitHub Pages gallery: writes ../index.html and thumbnails in site/thumbs/.

Run from anywhere:  ./site/build.py     then commit and push.
To publish a new picture, add it to SECTIONS below (or just push the file: every file in the
repo is reachable at  https://eleanor-lockhart.github.io/fablepaint/<path in repo>).
Entries whose file does not exist yet are skipped, so it is safe to list work in progress.
"""
import html, os
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
REPO = 'https://github.com/eleanor-lockhart/fablepaint'
SITE = 'https://eleanor-lockhart.github.io/fablepaint/'
THUMB = 760

def blob(p): return f'{REPO}/blob/main/{p}'
def tree(p): return f'{REPO}/tree/main/{p}'

# (title, blurb, [(file, caption, [(label, file-or-url), ...]), ...])
SECTIONS = [
    ('Planned prints',
     'A style developed on purpose: the inter-war Japanese colour woodblock idiom, applied to the Pacific Northwest at night. '
     'Each print was chosen from three three-value thumbnails, built from measured references, then revised once after its own critique.',
     [('atelier/prints/p1_last_boat_v2.png', 'Last boat, rain', [('first pass', 'atelier/prints/p1_last_boat_v1.png'), ('thumbnails', 'atelier/prints/p1/00_notan.png'), ('time-lapse', 'atelier/prints/p1_timelapse.mp4'), ('scripts', tree('atelier/prints/p1'))]),
      ('atelier/prints/p2_lookout_v2.png', 'Lookout, first snow', [('first pass', 'atelier/prints/p2_lookout_v1.png'), ('thumbnails', 'atelier/prints/p2/00_notan.png'), ('time-lapse', 'atelier/prints/p2_timelapse.mp4'), ('scripts', tree('atelier/prints/p2'))]),
      ('atelier/prints/p3_full_moon_v2.png', 'Full moon over the Sound', [('first pass', 'atelier/prints/p3_full_moon_v1.png'), ('thumbnails', 'atelier/prints/p3/00_notan.png'), ('time-lapse', 'atelier/prints/p3_timelapse.mp4'), ('scripts', tree('atelier/prints/p3'))])]),
    ('How the style was arrived at',
     'Side-by-side evidence, and the studies behind it. The journal has the reasoning.',
     [('atelier/compare/1_memory_vs_reference.png', 'The same subjects from memory, then after looking at references', []),
      ('atelier/compare/2_before_and_after_notes.png', 'One subject before any research, and after research plus notes', []),
      ('atelier/compare/3_assigned_subject.png', 'The assigned subject without and with the method', []),
      ('atelier/compare/4_three_prints.png', 'The three prints together', []),
      ('atelier/studies/s00_memory.png', 'Study 0: a "woodblock print" from memory, before any research', []),
      ('atelier/studies/s01_materials.png', 'Study 1: six material problems', []),
      ('atelier/studies/s02a_memory_subjects.png', 'Study 2a: heron and ferry from memory', []),
      ('atelier/studies/s02b_reference_subjects.png', 'Study 2b: the same after photographs, plus firs', [])]),
    ('Cold-start test',
     'A fresh agent that never saw the style being developed, working only from the written guide.',
     [('atelier/transfer/t1_v2.png', 'Its print, revised', [('first pass', 'atelier/transfer/t1_v1.png'), ('thumbnails', 'atelier/transfer/t1_notan.png'), ('scripts', tree('atelier/transfer'))])]),
    ('Fable Studio',
     'Pictures from the full-featured headless paint program (studio/studio.py), painted before there was a method.',
     [('gallery/studio/aurora.png', 'Aurora', [('16-bit', 'gallery/studio/aurora_16bit.png'), ('time-lapse', 'gallery/studio/aurora_timelapse.mp4')]),
      ('gallery/studio/orca_vs_mech.png', 'Orca and machine, first version', [('time-lapse', 'gallery/studio/orca_vs_mech_timelapse.mp4')])]),
    ('The house, on the family computers',
     'A childhood home as someone living there in the 1990s might have drawn it: four in 256-colour VGA, two on a black-and-white Mac.',
     [('gallery/house/uphill.png', 'From the road', [('in the program', 'gallery/house/uphill_in_fpaint.png'), ('time-lapse', 'gallery/house/uphill_timelapse.gif')]),
      ('gallery/house/garden.png', 'The garden', [('in the program', 'gallery/house/garden_in_fpaint.png'), ('time-lapse', 'gallery/house/garden_timelapse.gif')]),
      ('gallery/house/kitchen.png', 'The kitchen', [('in the program', 'gallery/house/kitchen_in_fpaint.png'), ('time-lapse', 'gallery/house/kitchen_timelapse.gif')]),
      ('gallery/house/bedroom.png', 'The bedroom', [('in the program', 'gallery/house/bedroom_in_fpaint.png'), ('time-lapse', 'gallery/house/bedroom_timelapse.gif')]),
      ('gallery/house/mac_house.png', 'The house, on the Mac', [('time-lapse', 'gallery/house/mac_house_timelapse.gif')]),
      ('gallery/house/mac_trapdoor.png', 'The pantry trap door, on the Mac', [('time-lapse', 'gallery/house/mac_trapdoor_timelapse.gif')])]),
    ('A DOS paint program',
     'First experiments with fpaint.py, a period-limited paint program (VGA mode 13h, EGA, CGA, early Mac).',
     [('gallery/lighthouse.png', 'Lighthouse', [('in the program', 'gallery/lighthouse_in_fpaint.png'), ('time-lapse', 'gallery/lighthouse_timelapse.gif'), ('colour cycling', 'gallery/lighthouse_cycling.gif')]),
      ('gallery/desk.png', 'Desk at night', [('in the program', 'gallery/desk_in_fpaint.png'), ('time-lapse', 'gallery/desk_timelapse.gif')]),
      ('gallery/saturn.png', 'Saturn', [('in the program', 'gallery/saturn_in_fpaint.png'), ('time-lapse', 'gallery/saturn_timelapse.gif')])]),
]
DOCS = [('Style guide', blob('atelier/STYLE.md')), ('Journal', blob('atelier/journal.md')), ('Paint program manual', blob('studio/AGENTS.md')), ('Repository', REPO)]

def thumb(rel):
    src = ROOT / rel
    out = ROOT / 'site' / 'thumbs' / (rel.replace('/', '__').rsplit('.', 1)[0] + '.jpg')
    if not out.exists() or out.stat().st_mtime < src.stat().st_mtime:
        out.parent.mkdir(parents=True, exist_ok=True)
        im = Image.open(src); im.seek(0) if getattr(im, 'is_animated', False) else None
        im = im.convert('RGB'); im.thumbnail((THUMB, THUMB), Image.LANCZOS); im.save(out, quality=84)
    w, h = Image.open(out).size
    return out.relative_to(ROOT).as_posix(), w, h

def href(target): return target if target.startswith('http') else html.escape(target)

CSS = """
:root{--bg:#efe7d6;--ink:#26231d;--muted:#6d6759;--card:#f8f3e7;--line:#d9cfb9;--accent:#b23b28}
@media (prefers-color-scheme:dark){:root{--bg:#14161a;--ink:#e6e1d4;--muted:#9c978b;--card:#1d2025;--line:#2c3037;--accent:#d9634c}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.55 system-ui,-apple-system,"Segoe UI",sans-serif}
main{max-width:1180px;margin:0 auto;padding:40px 20px 80px}
h1,h2{font-family:"Iowan Old Style","Palatino Linotype",Palatino,Georgia,serif;font-weight:500;letter-spacing:.01em}
h1{font-size:2.3rem;margin:0;display:flex;align-items:center;gap:.5em}
h2{font-size:1.5rem;margin:56px 0 4px;padding-top:20px;border-top:1px solid var(--line)}
p{max-width:68ch;margin:.4em 0 1em}
.lede{color:var(--muted);font-size:1.05rem}
a{color:var(--accent);text-underline-offset:2px}
nav a{margin-right:1.2em;white-space:nowrap}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:22px;align-items:start;margin-top:18px}
.grid.wide{grid-template-columns:repeat(auto-fill,minmax(330px,1fr))}
figure{margin:0;background:var(--card);border:1px solid var(--line);border-radius:3px;overflow:hidden}
figure img{display:block;width:100%;height:auto}
figcaption{padding:10px 12px 12px;font-size:.93rem}
figcaption b{font-weight:600;display:block}
figcaption span{color:var(--muted);font-size:.85rem;display:flex;flex-wrap:wrap;gap:.1em .9em;margin-top:2px}
figcaption span a{white-space:nowrap}
footer{margin-top:64px;color:var(--muted);font-size:.86rem;border-top:1px solid var(--line);padding-top:16px}
"""
SEAL = '<svg width="34" height="34" viewBox="0 0 34 34" aria-hidden="true"><rect width="34" height="34" rx="2" fill="#b23b28"/><rect x="19" y="17" width="7.5" height="10" fill="#ecd596"/></svg>'

def main():
    parts = []
    for title, blurb, items in SECTIONS:
        cards = []
        for rel, cap, extras in items:
            if not (ROOT / rel).exists():
                continue
            t, w, h = thumb(rel)
            links = ''.join(f'<a href="{href(u)}">{html.escape(l)}</a>' for l, u in extras if u.startswith('http') or (ROOT / u).exists())
            cards.append(f'<figure><a href="{href(rel)}"><img src="{t}" width="{w}" height="{h}" loading="lazy" alt="{html.escape(cap)}"></a>'
                         f'<figcaption><b>{html.escape(cap)}</b>{f"<span>{links}</span>" if links else ""}</figcaption></figure>')
        if cards:
            wide = ' wide' if title in ('How the style was arrived at', 'Fable Studio') else ''
            parts.append(f'<section><h2>{html.escape(title)}</h2><p>{html.escape(blurb)}</p><div class="grid{wide}">{"".join(cards)}</div></section>')
    nav = ''.join(f'<a href="{u}">{html.escape(l)}</a>' for l, u in DOCS)
    page = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>fablepaint</title><meta name="description" content="Pictures painted by an AI agent through paint programs it wrote for itself, and the notes on how it taught itself a style.">
<style>{CSS}</style></head><body><main>
<header><h1>{SEAL} fablepaint</h1>
<p class="lede">Pictures painted by an AI agent (Claude) through paint programs it wrote for itself, with no window and no stylus: it writes a short script, runs it, looks at the result, and tries again. This page collects the pictures; the repository has the programs, the scripts behind every picture, and the notes on how one style was worked out.</p>
<nav>{nav}</nav></header>
{"".join(parts)}
<footer>Reference prints and photographs used for study are third-party works under their own licences, listed in <a href="{blob('atelier/refs/SOURCES.md')}">atelier/refs/SOURCES.md</a>. Every file in the repository is also reachable directly under {SITE}.</footer>
</main></body></html>
"""
    (ROOT / 'index.html').write_text(page)
    (ROOT / '.nojekyll').write_text('')
    print('index.html', len(page), 'bytes;', sum(1 for _ in (ROOT / 'site' / 'thumbs').glob('*.jpg')), 'thumbnails')

main()
