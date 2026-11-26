#!/usr/bin/env python3
"""Patch for the live shell (index.html), after feature-pages.py: every phone on a feature page has the same
size and frame, placeholders included (their padding no longer adds to the size; they get the same bezel,
with the dashed outline inside the screen).
   python3 tools/live/phone-size.py index.html"""
import sys
p = sys.argv[1]; s = open(p, encoding='utf-8').read()
old = '  .fp-phone.empty { background: var(--stage); box-shadow: inset 0 0 0 1.5px var(--line-strong); display: flex; align-items: center; justify-content: center; text-align: center; padding: 16px; color: var(--muted); font-size: 13px; }'
new = '  .fp-phone { box-sizing: border-box; }\n  .fp-phone.empty { background: var(--stage); display: flex; align-items: center; justify-content: center; text-align: center; padding: 16px; color: var(--muted); font-size: 13px; }'
if s.count(old) != 1: raise SystemExit('placeholder rule not found')
s = s.replace(old, new)
open(p, 'w', encoding='utf-8').write(s); print('ok')
