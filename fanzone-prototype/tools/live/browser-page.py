#!/usr/bin/env python3
"""Patch for the live index.html (after outside-scores.py): In-app browser gets its Current screen: the in-app
browser sheet under the video (back and minimize, web view), from Figma FanZone 80-20 (a38ncus4fbwkPfnlFQIUPt 1:41036,
assets/screens/inapp-browser-current.png).
   python3 tools/live/browser-page.py index.html"""
import sys
p = sys.argv[1]; s = open(p, encoding='utf-8').read()
a = '''    PAGES.fzbutton = {'''
if s.count(a) != 1: raise SystemExit('pages block changed')
s = s.replace(a, '''    PAGES.browser = { phones: [{ img: "assets/screens/inapp-browser-current.png", label: "Current" }, later, out], note: note("links open in a browser sheet under the video, with back and minimize, so the match keeps playing.") };
''' + a)
open(p, 'w', encoding='utf-8').write(s); print('ok')
