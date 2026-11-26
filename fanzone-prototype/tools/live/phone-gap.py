#!/usr/bin/env python3
"""Patch for the live shell (index.html), after keep-alive.py: more space between the phones on a feature page
(56px instead of 28px; the phone size accounts for it).
   python3 tools/live/phone-gap.py index.html"""
import sys
p = sys.argv[1]; s = open(p, encoding='utf-8').read()
def rep(a, b):
    global s
    if s.count(a) != 1: raise SystemExit('expected once: ' + a[:90])
    s = s.replace(a, b)
rep('  .fp-set { display: flex;', '  .fpage { --fp-gap: 56px; }\n  .fp-set { display: flex;')
rep('    var gap = 28, s = Math.min(', '    var gap = 56, s = Math.min(')
open(p, 'w', encoding='utf-8').write(s); print('ok')
