#!/usr/bin/env python3
"""Patch for the live index.html (after intro-still.py): the highlighted tag above the new version's phone
(80-20 / New) is a soft yellow (a pale DAZN yellow, not the full neon) instead of white.
   python3 tools/live/chip-yellow.py index.html"""
import sys
p = sys.argv[1]; s = open(p, encoding='utf-8').read()
a = '''  .fp-chip.hl { background: var(--primary); color: var(--on-primary); border-color: transparent; }'''
if s.count(a) != 1: raise SystemExit('expected the chip style once')
s = s.replace(a, '''  .fp-chip.hl { background: #EEF2A0; color: #15190A; border-color: transparent; box-shadow: 0 0 0 3px rgba(247, 255, 26, .12); }''')
open(p, 'w', encoding='utf-8').write(s); print('ok')
