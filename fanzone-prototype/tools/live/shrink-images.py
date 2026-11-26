#!/usr/bin/env python3
"""Make smaller copies of the prototype's heaviest images into _opt/ (same paths), for publishing over the originals.
The avatar pictures were 1125x1125 (~1MB each, ~16MB together) but show at a few dozen pixels; 450px keeps them
sharp. Crown 240px, Bayern logo 320px. 16.8MB -> 3.8MB.
   python3 tools/live/shrink-images.py    (run in fanzone-prototype/)"""
from PIL import Image
import glob, os
jobs = [(f, 450) for f in sorted(glob.glob('assets/img/av1*.png') + glob.glob('assets/img/av2*.png') + glob.glob('assets/img/na*.png'))]
jobs += [('assets/img/crown.png', 240), ('assets/img/logo-bayern.png', 320)]
for f, size in jobs:
    im = Image.open(f); im.load()
    w, h = im.size; s = size / max(w, h)
    if s < 1: im = im.resize((round(w * s), round(h * s)), Image.LANCZOS)
    out = '_opt/' + f; os.makedirs(os.path.dirname(out), exist_ok=True)
    im.save(out, optimize=True)
    print(f, os.path.getsize(f) // 1024, '->', os.path.getsize(out) // 1024, 'KB')
