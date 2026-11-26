#!/usr/bin/env python3
"""Patch for the live index.html (after actions-new.py): bigger phones with more room between them. The phone size
comes from the real free height under the slide header (down to the bottom bar) instead of a fixed estimate, and
the gap between phones goes from 56px to 72px, the slide side margins from 48px to 32px, no 0.9 size cap (it also counts in the width limit, so the three always fit).
   python3 tools/live/phones-bigger.py index.html"""
import sys
p = sys.argv[1]; s = open(p, encoding='utf-8').read()
def rep(a, b):
    global s
    if s.count(a) != 1: raise SystemExit('expected once: ' + a[:90])
    s = s.replace(a, b)
rep('''    var gap = 56, s = Math.min((w - gap * (n - 1) - n * 22) / (n * 375), (h - 40) / 812);''',
    '''    var top = document.querySelector(".fp-top"), fr = fpage.getBoundingClientRect();
    var headBottom = top && top.offsetParent ? top.getBoundingClientRect().bottom - fr.top : 150;
    h = fpage.clientHeight - headBottom - 84 - 58;   // bottom bar + the tag above the phones and its gap
    var gap = 72, s = Math.min((w - gap * (n - 1) - n * 22) / (n * 375), h / 812);''')
rep('''var w = stage.clientWidth - 96, h =''', '''var w = stage.clientWidth - 64, h =''')
rep('''    s = Math.max(0.3, Math.min(s, 0.9));
    fpage.style.setProperty("--fs"''', '''    s = Math.max(0.3, Math.min(s, 1));
    fpage.style.setProperty("--fs"''')
rep('''  .fpage { padding: 40px 48px 84px; justify-content: flex-start; }''', '''  .fpage { padding: 40px 32px 84px; justify-content: flex-start; }''')
rep('''  .fp-foot { position: absolute; left: 48px; right: 48px;''', '''  .fp-foot { position: absolute; left: 32px; right: 32px;''')
rep('''  .fpage { --fp-gap: 56px; }''', '''  .fpage { --fp-gap: 72px; }''')
open(p, 'w', encoding='utf-8').write(s); print('ok')
