#!/usr/bin/env python3
"""Patch for the live FanZone.dc.html (after eb.py ran without the video): the EB plays the real video
(assets/eb/eb.mp4, EB_POLL_EN, 5s loop) instead of the still poster.
   python3 tools/live/eb-video.py FanZone.dc.html"""
import sys
p = sys.argv[1]; s = open(p, encoding='utf-8').read()
a = '<img src="assets/eb/eb-poster.png" alt="" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;display:block;">'
b = ('<video src="assets/eb/eb.mp4" poster="assets/eb/eb-poster.png" autoplay="" muted="" loop="" playsinline="" '
     'style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;display:block;"></video>')
if s.count(a) != 1: raise SystemExit('expected the EB poster once')
open(p, 'w', encoding='utf-8').write(s.replace(a, b)); print('ok')
