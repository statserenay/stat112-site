"""
Build recitation6-slides.qmd (a Quarto reveal.js deck) from exported slide images.

Run from your site folder:
    pip install python-pptx
    python make_r6_slides.py

It expects:
    _sources/recitation6/tableau_presentation.pptx      (for slide titles + search text)
    _sources/recitation6/tableau_presentation_part2.pptx
    images/recitation6/part1/   one image per slide (Slide1.png, Slide2.png, ...)
    images/recitation6/part2/
"""
import re
from pathlib import Path

try:
    from pptx import Presentation
except ImportError:
    Presentation = None

DECKS = [
    ("Part 1: Superstore", "_sources/recitation6/tableau_presentation.pptx", "images/recitation6/part1"),
    ("Part 2: Customer data & dashboard", "_sources/recitation6/tableau_presentation_part2.pptx", "images/recitation6/part2"),
]
OUT = "recitation6-slides.qmd"

HEADER = """---
title: "Recitation 6: Tableau"
format:
  revealjs:
    width: 1600
    height: 900
    margin: 0
    slide-number: c/t
    controls: true
    progress: true
    hash: true
    transition: fade
    background-transition: fade
    menu:
      side: left
      numbers: true
    chalkboard:
      theme: whiteboard
      buttons: true
    footer: "STAT 112 · Recitation 6 · Tableau"
    css: r6-slides.css
---

"""


def natural_key(p):
    return [int(t) if t.isdigit() else t.lower() for t in re.split(r"(\d+)", p.name)]


def slide_texts(pptx_path):
    """Return a list of (title, full_text) per slide, or [] if unavailable."""
    if Presentation is None or not Path(pptx_path).exists():
        return []
    out = []
    for s in Presentation(pptx_path).slides:
        parts = [sh.text_frame.text.strip() for sh in s.shapes
                 if sh.has_text_frame and sh.text_frame.text.strip()]
        title = parts[0].split("\n")[0] if parts else ""
        out.append((title, "\n\n".join(parts)))
    return out


def clean(t, n=None):
    t = re.sub(r"\s+", " ", t).replace('"', "'").strip()
    return t[:n] if n else t


lines = [HEADER]
for part_title, pptx_path, img_dir in DECKS:
    imgs = sorted([p for p in Path(img_dir).glob("*")
                   if p.suffix.lower() in (".png", ".jpg", ".jpeg", ".webp")], key=natural_key)
    if not imgs:
        raise SystemExit(f"No images found in {img_dir}")
    texts = slide_texts(pptx_path)
    if texts and len(texts) != len(imgs):
        print(f"WARNING: {pptx_path} has {len(texts)} slides but {img_dir} has {len(imgs)} images")
    lines.append(f'# {part_title} {{.part-divider}}\n\n')
    for i, img in enumerate(imgs):
        title, body = texts[i] if i < len(texts) else (f"Slide {i+1}", "")
        menu = clean(title, 70) or f"Slide {i+1}"
        lines.append(
            f'## {{background-image="{img.as_posix()}" background-size="contain" '
            f'background-color="white" data-menu-title="{menu}"}}\n\n'
        )
        if body:
            # Speaker notes: shown in presenter view (S) and searchable.
            lines.append("::: notes\n" + body.replace(":::", "") + "\n:::\n\n")

Path(OUT).write_text("".join(lines), encoding="utf-8")
Path("r6-slides.css").write_text(""".reveal .part-divider h1 { font-size: 2.6em; color: #2c3e50; }
.reveal .slide-number { font-size: 18px; }
.reveal .footer { font-size: 16px; }
""", encoding="utf-8")
print(f"Wrote {OUT} with {sum(1 for l in lines if l.startswith('## '))} slides")
