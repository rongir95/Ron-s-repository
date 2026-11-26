#!/usr/bin/env python3
"""Patch for the live shell (index.html), after feature-pages.py: the page opens on Feature pages (FanZone 80-20)
by default instead of Prototype (one phone).
   python3 tools/live/default-pages.py index.html"""
import sys
p = sys.argv[1]; s = open(p, encoding='utf-8').read()
old = 'view: "proto", feature: "poll", notes: "1" };'
if s.count(old) != 1: raise SystemExit('defaults not found')
s = s.replace(old, 'view: "pages", feature: "poll", notes: "1" };')
open(p, 'w', encoding='utf-8').write(s); print('ok')
