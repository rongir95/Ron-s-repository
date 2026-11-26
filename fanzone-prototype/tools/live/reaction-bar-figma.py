#!/usr/bin/env python3
"""Patch for the live FanZone.dc.html: the message-bar reactions and the change-team button from the Figma SVG
(FanZone 80-20, a38ncus4fbwkPfnlFQIUPt 23:136816), as vectors: assets/reactions-bar/rx1..rx5.svg (each 36px box
with the 28px emoji centred) and assets/reactions-bar/change-team.svg (the icon alone, no grey box).
Spacing per Figma: reactions 12px apart, the 32px change-team button 6px after them.
   python3 tools/live/reaction-bar-figma.py FanZone.dc.html"""
import re, sys
p = sys.argv[1]; s = open(p, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    if s.count(a) != n: raise SystemExit(f'expected {n}: ' + a[:90])
    s = s.replace(a, b)
rep('reactions: ["assets/reactions-bar/r1.png","assets/reactions-bar/r2.png","assets/reactions-bar/r3.png","assets/reactions-bar/r4.png","assets/reactions-bar/r5.png"]',
    'reactions: ["assets/reactions-bar/rx1.svg","assets/reactions-bar/rx2.svg","assets/reactions-bar/rx3.svg","assets/reactions-bar/rx4.svg","assets/reactions-bar/rx5.svg"]')
# the change-team button: icon only (Figma), 6px after the last reaction
m = re.search(r'<button onClick="\{\{ openTeamChooser \}\}" aria-label="Change team" style="flex-shrink:0;width:32px;height:32px;border:0;padding:0;border-radius:8px;background:#3D4549;display:flex;align-items:center;justify-content:center;cursor:pointer;"><img src="assets/icons/change-team.svg" alt="" width="20" height="20" style="[^"]*"></button>', s)
if not m: raise SystemExit('change-team button not found')
s = s[:m.start()] + '<button onClick="{{ openTeamChooser }}" aria-label="Change team" style="flex-shrink:0;margin-left:-6px;width:32px;height:32px;border:0;padding:0;border-radius:8px;background:transparent;display:flex;align-items:center;justify-content:center;cursor:pointer;"><img src="assets/reactions-bar/change-team.svg" alt="" width="24" height="24" style="display:block;"></button>' + s[m.end():]
rep('    const SHIFT = 265;', '    const SHIFT = 259;')
rep('(s.fzBar2 ? -265 : 0),', '(s.fzBar2 ? -259 : 0),')
open(p, 'w', encoding='utf-8').write(s); print('ok')
