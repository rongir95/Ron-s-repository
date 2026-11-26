#!/usr/bin/env python3
"""Patch for the live FanZone.dc.html: the "YOU" tag in the leaderboard's own row per Figma
(FanZone 80-20 a38ncus4fbwkPfnlFQIUPt, I1:43659;1765:3592): 12px high, #080E12 fill with a 1px #080E12
border, 2px radius, 1px side padding, DAZN Oscine ExtraBold 12 uppercase trimmed to the cap height; it sits
at the end of the name area (the name takes the free space), 12px before the points.
   python3 tools/live/lb-you-tag.py FanZone.dc.html"""
import sys
p = sys.argv[1]; s = open(p, encoding='utf-8').read()
old = ('''<span onClick="{{ openCard }}" style="cursor:pointer;margin-left:8px;font-size:16px;max-width:99px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">{{ cardName }}</span>
                <span style="margin-left:8px;padding:1px 2px;border-radius:2px;background:#080E12;color:#F9FAFA;font-weight:800;font-size:12px;line-height:10px;">YOU</span>
                <span style="flex:1;"></span>
                <span style="width:42px;font-size:16px;">''')
new = ('''<span onClick="{{ openCard }}" style="cursor:pointer;margin-left:8px;flex:1;min-width:0;font-size:16px;line-height:24px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">{{ cardName }}</span>
                <span style="flex-shrink:0;margin-left:8px;height:12px;box-sizing:border-box;padding:0 1px;border:1px solid #080E12;border-radius:2px;background:#080E12;display:inline-flex;align-items:center;justify-content:flex-end;overflow:hidden;color:#F9FAFA;font-weight:800;font-size:12px;line-height:12px;text-transform:uppercase;text-box:trim-both cap alphabetic;">You</span>
                <span style="width:42px;margin-left:12px;font-size:16px;">''')
if s.count(old) != 1: raise SystemExit('you row not found')
s = s.replace(old, new)
open(p, 'w', encoding='utf-8').write(s); print('ok')
