#!/usr/bin/env python3
"""Patch for the live shell (index.html): the Start screen setting defaults to FanZone (was Home).
   python3 tools/live/default-fanzone.py index.html"""
import sys
p = sys.argv[1]; s = open(p, encoding='utf-8').read()
old = 'var DEFAULTS = { start: "home",'
if s.count(old) != 1: raise SystemExit('defaults not found')
s = s.replace(old, 'var DEFAULTS = { start: "fanzone",')
open(p, 'w', encoding='utf-8').write(s); print('ok')
