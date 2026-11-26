#!/usr/bin/env python3
"""Patch for the live index.html (after chip-yellow.py): the highlighted tag (80-20 / New) is an outlined chip
like the others, tinted DAZN yellow: a light yellow wash, a yellow border and yellow text. No glow.
   python3 tools/live/chip-yellow2.py index.html"""
import sys
p = sys.argv[1]; s = open(p, encoding='utf-8').read()
a = '''  .fp-chip.hl { background: #EEF2A0; color: #15190A; border-color: transparent; box-shadow: 0 0 0 3px rgba(247, 255, 26, .12); }'''
if s.count(a) != 1: raise SystemExit('expected the chip style once')
s = s.replace(a, '''  .fp-chip.hl { background: rgba(247, 255, 26, .12); color: #F4F8A8; border-color: rgba(247, 255, 26, .5); }''')
open(p, 'w', encoding='utf-8').write(s); print('ok')
