# fablepaint

Pictures painted by an AI agent (Claude) through paint programs it wrote for itself, and the
notes on how it taught itself one style. There is no window and no stylus: the agent writes a
short script, runs it, looks at the rendered result, and tries again.

**Gallery:** https://eleanor-lockhart.github.io/fablepaint/

## What is here

| | |
|---|---|
| `fpaint.py` | a period-limited paint program: VGA mode 13h, EGA, CGA, early Mac. `./fpaint.py help` |
| `studio/` | Fable Studio, a full-featured headless paint program. Manual for any agent: `studio/AGENTS.md` |
| `styles/` | styles worked out on purpose, one folder each. `styles/lit-window/`: colour woodblock prints (`STYLE.md` is the guide, `journal.md` the evidence) |
| `gallery/` | finished pictures from the first two programs |
| `sessions/`, `house/` | fpaint working files, so those pictures can be reopened |
| `site/build.py`, `index.html` | the gallery page |

Both programs are single-file Python scripts with inline dependencies; with
[`uv`](https://docs.astral.sh/uv/) installed they run as they are.

## Publishing a new picture

Every file in the repository is served at
`https://eleanor-lockhart.github.io/fablepaint/<path in the repository>`, so a pushed file
already has a link. To show it on the gallery page as well, add a line to `SECTIONS` in
`site/build.py`, then:

```
./site/build.py && git add -A && git commit -m "Add <picture>" && git push
```

Pages rebuilds in about a minute. `studio/sessions/` is deliberately not in the repository
(several gigabytes of working layers).

## Third-party material

The reference prints and photographs in `styles/lit-window/refs/` were used for study and are the work
of others, under the licences listed in `styles/lit-window/refs/SOURCES.md` (public domain, CC0,
CC BY and CC BY-SA, from Wikimedia Commons). `font8x8.hex` is the public-domain 8x8 ROM font.
