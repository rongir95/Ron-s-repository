#!/usr/bin/env python3
"""Patch for the live FanZone.dc.html: no hover state on the FanZone card on the match page (it's mobile).
   python3 tools/live/no-entry-hover.py FanZone.dc.html"""
import sys
p = sys.argv[1]; s = open(p, encoding='utf-8').read()
old = '  .fz-entry:hover { background: #222C31 !important; }\n'
if s.count(old) != 1: raise SystemExit('hover rule not found')
s = s.replace(old, '')
open(p, 'w', encoding='utf-8').write(s); print('ok')
