#!/usr/bin/env python3
"""Patch for the live index.html (after cat-8020.py): slide header layout. The category line and the feature title
sit at the top left (with the Portrait / Landscape switch under them when there is one); Prev, the page count with
its refresh button, and Next sit together at the top right.
   python3 tools/live/top-left-title.py index.html"""
import re, sys
p = sys.argv[1]; s = open(p, encoding='utf-8').read()
def rep(a, b):
    global s
    if s.count(a) != 1: raise SystemExit('expected once: ' + a[:90])
    s = s.replace(a, b)
m = re.search(r'(        <button type="button" class="fp-step fp-prev"[^\n]*</button>\n)(        <div class="fp-head">.*?)(<span class="fp-countrow">.*?</button></span>)(.*?</div></div>\n)(        <button type="button" class="fp-step fp-next"[^\n]*</button>\n)', s, re.S)
if not m: raise SystemExit('slide header markup changed')
prev, head_a, count, head_b, nxt = m.groups()
new = head_a + head_b + '        <div class="fp-navs">\n  ' + prev + '          ' + count + '\n  ' + nxt + '        </div>\n'
s = s[:m.start()] + new + s[m.end():]
rep('''  .fp-top { display: grid; grid-template-columns: minmax(0, 1fr) auto minmax(0, 1fr); align-items: center; gap: 16px; width: 100%; max-width: 1100px; }''',
    '''  .fp-top { display: grid; grid-template-columns: minmax(0, 1fr) auto minmax(0, 1fr); align-items: center; gap: 16px; width: 100%; max-width: 1100px; }
  .fp-top { display: flex; align-items: flex-start; justify-content: space-between; gap: 24px; max-width: none; }
  .fp-top .fp-head { text-align: left; align-items: flex-start; min-width: 0; }
  .fp-top .fp-orient { justify-content: flex-start; }
  .fp-navs { display: flex; align-items: center; gap: 10px; flex: none; }
  .fp-navs .fp-step { max-width: 230px; }''')
open(p, 'w', encoding='utf-8').write(s); print('ok')
