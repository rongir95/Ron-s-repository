#!/usr/bin/env python3
"""Patch for the live FanZone.dc.html: the reactions by the message field use square images with the
drawing centred (assets/reactions-bar/r1..r5.png, made from assets/img/reaction*.png, which are 177x144 with
the drawing off to one side), so the gaps read evenly.
   python3 tools/live/reaction-images.py FanZone.dc.html"""
import sys
p = sys.argv[1]; s = open(p, encoding='utf-8').read()
old = 'reactions: ["assets/img/reaction1.png","assets/img/reaction2.png","assets/img/reaction3.png","assets/img/reaction4.png","assets/img/reaction5.png"]'
if s.count(old) != 1: raise SystemExit('reactions list not found')
s = s.replace(old, 'reactions: ["assets/reactions-bar/r1.png","assets/reactions-bar/r2.png","assets/reactions-bar/r3.png","assets/reactions-bar/r4.png","assets/reactions-bar/r5.png"]')
# and the change-team button keeps the same 12px as between the reactions (the 6px of Figma read as touching)
for a, b in [('aria-label="Change team" style="flex-shrink:0;margin-left:-6px;width:32px;', 'aria-label="Change team" style="flex-shrink:0;width:32px;'),
             ('    const SHIFT = 259;', '    const SHIFT = 265;'), ('(s.fzBar2 ? -259 : 0),', '(s.fzBar2 ? -265 : 0),')]:
    if s.count(a) != 1: raise SystemExit('not found: ' + a[:60])
    s = s.replace(a, b)
open(p, 'w', encoding='utf-8').write(s); print('ok')
