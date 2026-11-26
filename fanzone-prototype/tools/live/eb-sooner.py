#!/usr/bin/env python3
"""Patch for the live FanZone.dc.html (after poll-v3-clip.py): the engagement break comes in sooner: 4s after the
page is shown (was 6s); after the X it comes back after 6s (was 8s).
   python3 tools/live/eb-sooner.py FanZone.dc.html"""
import sys
p = sys.argv[1]; s = open(p, encoding='utf-8').read()
def rep(a, b):
    global s
    if s.count(a) != 1: raise SystemExit('expected once: ' + a[:90])
    s = s.replace(a, b)
rep('''        else if (m === "eb") this.ebSoon(6000);''', '''        else if (m === "eb") this.ebSoon(4000);''')
rep('''get("moment") === "eb") this.ebSoon(8000); },''', '''get("moment") === "eb") this.ebSoon(6000); },''')
rep('''      this.setState({ ebOn: false }); this.ebSoon(6000);''', '''      this.setState({ ebOn: false }); this.ebSoon(4000);''')
open(p, 'w', encoding='utf-8').write(s); print('ok')
