#!/usr/bin/env python3
"""Patch for the live index.html (after panel-collapse.py): no animation at all when moving between feature
pages: the next page simply replaces the previous one (the slide from page-slide.py is switched off).
   python3 tools/live/page-still.py index.html"""
import sys
p = sys.argv[1]; s = open(p, encoding='utf-8').read()
a = '''  .fp-set.in-next { animation: fpInNext .34s cubic-bezier(.2, .8, .2, 1); }
  .fp-set.in-prev { animation: fpInPrev .34s cubic-bezier(.2, .8, .2, 1); }
  .fp-set.in-fade { animation: fpInFade .25s ease; }'''
if s.count(a) != 1: raise SystemExit('expected the page slide once')
s = s.replace(a, '''  .fp-set.in-next, .fp-set.in-prev, .fp-set.in-fade { animation: none; }''')
s = s.replace('''  @media (prefers-reduced-motion: reduce) { .fp-set.in-next, .fp-set.in-prev { animation: fpInFade .2s ease; } }''', '')
open(p, 'w', encoding='utf-8').write(s); print('ok')
