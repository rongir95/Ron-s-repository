#!/usr/bin/env python3
"""Patch for the live index.html (after fonts-oscine.py): the slide header has the same height on every slide, so
the phones don't jump when you move between slides. The title is one line (cut with "..." if too long) and the
explanation line always takes exactly two lines (shorter ones keep the room, longer ones are cut with "..."; the
full text shows on hover). The Portrait / Landscape switch ("Landscape only") moves to the top right of the slide.
   python3 tools/live/head-fixed.py index.html"""
import sys
p = sys.argv[1]; s = open(p, encoding='utf-8').read()
def rep(a, b):
    global s
    if s.count(a) != 1: raise SystemExit('expected once: ' + a[:90])
    s = s.replace(a, b)
rep('''  .fp-foot { position: absolute;''', '''  .fp-top .fp-head { max-width: 100%; }
  .fp-top h2 { white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 100%; padding-bottom: 2px; }
  .fp-top .fp-note { display: -webkit-box; -webkit-box-orient: vertical; -webkit-line-clamp: 2; line-clamp: 2; overflow: hidden; height: calc(2 * 1.45em); }
  .fp-top .fp-note[hidden] { display: none; }
  .fp-top { position: relative; }
  .fp-top .fp-orient { position: absolute; right: 0; top: 6px; margin: 0; min-height: 0; }
  body[data-panel="closed"] .fp-top .fp-orient { right: 56px; }
  .fp-foot { position: absolute;''')
rep('''    note.hidden = settings.notes !== "1";''', '''    note.hidden = settings.notes !== "1";
    note.title = note.textContent;
    document.getElementById("fpTitle").title = f.name;''')
open(p, 'w', encoding='utf-8').write(s); print('ok')
