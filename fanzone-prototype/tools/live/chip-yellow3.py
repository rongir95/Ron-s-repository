#!/usr/bin/env python3
"""Patch for the live index.html (after chip-yellow2.py): the highlighted tag uses the project yellow #FFFA00
(text #FFFA00; the border and the wash are the same yellow with transparency).
   python3 tools/live/chip-yellow3.py index.html"""
import sys
p = sys.argv[1]; s = open(p, encoding='utf-8').read()
a = '''  .fp-chip.hl { background: rgba(247, 255, 26, .12); color: #F4F8A8; border-color: rgba(247, 255, 26, .5); }'''
if s.count(a) != 1: raise SystemExit('expected the chip style once')
s = s.replace(a, '''  .fp-chip.hl { background: rgba(255, 250, 0, .12); color: #FFFA00; border-color: rgba(255, 250, 0, .5); }''')
open(p, 'w', encoding='utf-8').write(s); print('ok')
