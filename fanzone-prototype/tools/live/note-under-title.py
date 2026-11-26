#!/usr/bin/env python3
"""Patch for the live index.html (after top-left-title.py):
 - The "What changed / Current" line moves up under the feature title (top left), instead of under the phones.
 - With the side panel collapsed, the slide header leaves room for the round "Show the panel" button at the
   top right, so it no longer sits on the Next button.
   python3 tools/live/note-under-title.py index.html"""
import sys
p = sys.argv[1]; s = open(p, encoding='utf-8').read()
def rep(a, b):
    global s
    if s.count(a) != 1: raise SystemExit('expected once: ' + a[:90])
    s = s.replace(a, b)
rep('''      <p class="fp-note" id="fpNote"></p>\n''', '')
rep('''<h2 id="fpTitle"></h2>''', '''<h2 id="fpTitle"></h2><p class="fp-note" id="fpNote"></p>''')
rep('''  .fp-navs { display: flex; align-items: center; gap: 10px; flex: none; }''', '''  .fp-navs { display: flex; align-items: center; gap: 10px; flex: none; }
  .fp-top .fp-head { flex: 1 1 auto; }
  .fp-top .fp-note { margin: 4px 0 0; max-width: 640px; min-height: 0; padding: 0; border: 0; text-align: left; font-size: 13px; line-height: 1.45; }
  @media (min-width: 861px) { body[data-panel="closed"] .fp-top { padding-right: 56px; box-sizing: border-box; } }''')
open(p, 'w', encoding='utf-8').write(s); print('ok')
