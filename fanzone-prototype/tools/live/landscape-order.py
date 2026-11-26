#!/usr/bin/env python3
"""Patch for the live index.html (after chip-yellow.py): Smart component for activations and Landscape activations
move down the feature list, to the end of Improvements (after Align with the new Onboarding). Prev / Next follow.
   python3 tools/live/landscape-order.py index.html"""
import sys
p = sys.argv[1]; s = open(p, encoding='utf-8').read()
smart = '{"id": "smart", "name": "Smart component for activations", "cat": "Activations", "kind": "imp", "screens": 3}, '
land = '{"id": "landscape", "name": "Landscape activations", "cat": "Activations", "kind": "imp", "screens": 3}, '
anchor = '{"id": "onboarding", "name": "Align with the new Onboarding", "cat": "General", "kind": "imp", "screens": 3}, '
for x in (smart, land, anchor):
    if s.count(x) != 1: raise SystemExit('feature list changed: ' + x[:40])
s = s.replace(smart, '').replace(land, '').replace(anchor, anchor + smart + land)
open(p, 'w', encoding='utf-8').write(s); print('ok')
