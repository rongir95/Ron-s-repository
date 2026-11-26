#!/usr/bin/env python3
"""Patch for the live FanZone.dc.html (after eb-sooner.py): moment=typing opens FanZone with the Message field in
its typing state (keyboard up, panel above it), for the Message sending feature page.
   python3 tools/live/typing-moment.py FanZone.dc.html"""
import sys
p = sys.argv[1]; s = open(p, encoding='utf-8').read()
def rep(a, b):
    global s
    if s.count(a) != 1: raise SystemExit('expected once: ' + a[:90])
    s = s.replace(a, b)
rep('["quiz", "pin", "battle", "leaderboard", "team", "eb"].indexOf(q.get("moment"))', '["quiz", "pin", "battle", "leaderboard", "team", "eb", "typing"].indexOf(q.get("moment"))')
rep('''        else if (m === "eb") this.ebSoon(4000);''', '''        else if (m === "eb") this.ebSoon(4000);
        else if (m === "typing") this.fzTypeOn();''')
open(p, 'w', encoding='utf-8').write(s); print('ok')
