#!/usr/bin/env python3
"""Patch for the live FanZone.dc.html (after fast-boot.py): the 80-20 poll (V3) slides in from under the FanZone
header instead of over the stream: its wrapper clips the top edge (clip-path, so nothing else is cut), like the
other polls whose wrappers already hide overflow.
   python3 tools/live/poll-v3-clip.py FanZone.dc.html"""
import sys
p = sys.argv[1]; s = open(p, encoding='utf-8').read()
a = '''        <sc-if value="{{ v3On }}" hint-placeholder-val="{{ false }}">
          <div style="position:absolute;left:0;right:0;top:{{ pollTop }}px;z-index:2;pointer-events:none;'''
if s.count(a) != 1: raise SystemExit('expected the V3 poll wrapper once')
s = s.replace(a, '''        <sc-if value="{{ v3On }}" hint-placeholder-val="{{ false }}">
          <div style="position:absolute;left:0;right:0;top:{{ pollTop }}px;z-index:2;pointer-events:none;clip-path:inset(0 -60px -2000px -60px);''')
open(p, 'w', encoding='utf-8').write(s); print('ok')
