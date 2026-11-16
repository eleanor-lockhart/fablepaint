"""backlot.reader: the cold reader. The one instrument that measures what a picture says.

Everything else in the screening room measures what the picture *does*. The maker cannot measure what it
*says*, because the maker looks at every frame already knowing what it means: in the first self-critique that
was checked against an outside review, three of the six things listed as working were failures. A cold reader
is a fresh agent that has read nothing. It is shown the frames, says what happens, and only afterwards is asked
anything. Its story is then scored against what the piece was meant to say.

    pack_film(frames, questions, intent)      every frame, on numbered sheets, in a new empty folder
    pack_stills(images, task, questions)      the same for pictures (for example: "draw the plan of this place")

Protocol (the pack writes this out as PROTOCOL.md):

  1. The reader must not inherit this repository's instructions. Use an agent type that does not have the
     project's CLAUDE.md / AGENTS.md put in front of it (in Claude Code: `Explore`, which is also read-only),
     and point it at the pack's folder, which is outside the repository and holds only sheets and one prompt.
  2. Send PROMPT.txt. The reader answers with its narration. Save it unedited.
  3. Only then send QUESTIONS.txt to the same reader (resume it; do not start another). Save the answers unedited.
  4. Score against INTENT.md, which the reader never sees: for each beat, landed / half / missed, quoting the
     reader's own words. A beat the reader gets only in answer to a question counts as half.
  5. A reader works once. After the fix, use a new one.

Before any of this, write your own verdict and seal it. The gap between the two is the measurement of how much
your own eye can be trusted on this kind of thing.
"""
import tempfile
from pathlib import Path

FILM_PROMPT = """You are the first person to see a short silent film. You know nothing about it and nobody will tell you anything.

In the folder {dir} there are {n} numbered contact sheets ({first} to {last}). Together they hold every frame of the film in order, {per} frames to a sheet, each captioned with its frame number and time in seconds. Read them in order, all of them, with the Read tool. Look at nothing else: no other folders, no web, no notes.

Then write, as your whole answer, a plain narration of what you saw happen, in order, with times. Say what is on screen, what moves or changes, and what you take it to mean. Where you are guessing, say so and say what else it might be. Where you cannot tell what something is, describe its shape and colour instead of naming it. Do not be kind and do not fill gaps with what a film like this would probably do: if you did not see it, it did not happen.

Finish with: who the people or things in it are, as far as you can tell; what the story is in three sentences; and the three moments you understood least."""

STILLS_PROMPT = """You are shown {n} pictures and know nothing else about them. They are in the folder {dir} ({names}). Read each with the Read tool. Look at nothing else: no other folders, no web, no notes.

{task}

Where you are guessing, say so. If something cannot be worked out from the pictures, say that instead of supplying what would be usual."""

def _new_dir(out_dir):
    d = Path(out_dir) if out_dir else Path(tempfile.mkdtemp(prefix='coldread_'))
    d.mkdir(parents=True, exist_ok=True)
    if any(d.iterdir()): raise RuntimeError(f'{d} is not empty: a cold reader gets a folder with nothing else in it')
    return d

def _protocol(d, intent, questions):
    side = Path(str(d) + '_director'); side.mkdir(parents=True, exist_ok=True)       # beside the pack, never inside it
    (side / 'PROTOCOL.md').write_text(__doc__)
    (side / 'QUESTIONS.txt').write_text('Thank you. Now some questions. Answer from what you saw; do not revise your narration, and say "I did not see that" where that is the truth.\n\n'
                                        + '\n'.join(f'{k + 1}. {q}' for k, q in enumerate(questions or [])))
    (side / 'INTENT.md').write_text('# What the piece was meant to say (the reader never sees this)\n\n' + '\n'.join(f'{k + 1}. {b}' for k, b in enumerate(intent or [])) + '\n')
    return side

def pack_film(frames_dir, questions=None, intent=None, out_dir=None, fps=12, cols=6, cell_w=320):
    """Every frame of a film on contact sheets of one second each, in a new empty folder outside the repository.
    Returns dict(dir, director, prompt, sheets). `director` holds the protocol, the sealed questions and the intent."""
    from . import core, screen
    files = sorted(Path(frames_dir).glob('f_*.png')); d = _new_dir(out_dir); sheets = []
    for k in range(0, len(files), fps):
        run = files[k:k + fps]; f = d / f'sheet_{k // fps + 1:03d}.jpg'
        screen.sheet([core.load(str(x)) for x in run], str(f), [f'{k + j}   {(k + j) / fps:.2f} s' for j in range(len(run))], cols=cols, cell_w=cell_w)
        sheets.append(str(f))
    prompt = FILM_PROMPT.format(dir=d, n=len(sheets), first=Path(sheets[0]).name, last=Path(sheets[-1]).name, per=fps)
    side = _protocol(d, intent, questions); (side / 'PROMPT.txt').write_text(prompt)
    return dict(dir=str(d), director=str(side), prompt=prompt, sheets=sheets)

def pack_stills(images, task, questions=None, intent=None, out_dir=None, width=1280):
    """Pictures for a cold reader, with one task (for example: "these are views of one place; draw its plan as a
    list of objects with positions in metres"). `images` is a list of paths or of (name, path)."""
    import cv2
    d = _new_dir(out_dir); names = []
    for k, it in enumerate(images):
        name, path = it if isinstance(it, (tuple, list)) else (f'picture_{k + 1}', it)
        im = cv2.imread(str(path)); h, w = im.shape[:2]
        if w > width: im = cv2.resize(im, (width, round(h * width / w)), interpolation=cv2.INTER_AREA)
        cv2.imwrite(str(d / f'{name}.jpg'), im, [cv2.IMWRITE_JPEG_QUALITY, 92]); names.append(f'{name}.jpg')
    prompt = STILLS_PROMPT.format(dir=d, n=len(names), names=', '.join(names), task=task)
    side = _protocol(d, intent, questions); (side / 'PROMPT.txt').write_text(prompt)
    return dict(dir=str(d), director=str(side), prompt=prompt, sheets=[str(d / n) for n in names])
