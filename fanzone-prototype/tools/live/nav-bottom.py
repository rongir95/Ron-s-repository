#!/usr/bin/env python3
"""Patch for the live index.html (after note-under-title.py): the navigation (Prev, page count with refresh, Next)
moves from the top right to the bottom of the screen, centred under the phones.
   python3 tools/live/nav-bottom.py index.html"""
import re, sys
p = sys.argv[1]; s = open(p, encoding='utf-8').read()
m = re.search(r'        <div class="fp-navs">\n.*?\n        </div>\n', s, re.S)
if not m or s.count('<div class="fp-navs">') != 1: raise SystemExit('nav markup changed')
navs = m.group(0); s = s[:m.start()] + s[m.end():]
a = '''      <div class="fp-row" id="fpRow"></div>\n'''
if s.count(a) != 1: raise SystemExit('row markup changed')
s = s.replace(a, a + navs.replace('        <div class="fp-navs">', '      <div class="fp-navs fp-bottom">', 1))
b = '''  .fp-navs { display: flex; align-items: center; gap: 10px; flex: none; }'''
if s.count(b) != 1: raise SystemExit('nav css changed')
s = s.replace(b, b + '''
  .fp-navs.fp-bottom { justify-content: center; margin-top: 4px; }''')
open(p, 'w', encoding='utf-8').write(s); print('ok')
