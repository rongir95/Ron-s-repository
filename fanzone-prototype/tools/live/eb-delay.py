#!/usr/bin/env python3
"""Patch for the live FanZone.dc.html (after start-still.py): the engagement break waits longer before it comes
in (6s instead of 3s; after the X it comes back after 8s). On the feature pages the countdown starts when the page
is shown: the shell sends {fz: "shown"} to the phone, which closes any EB that came in while it was loading
in the background and starts the 6s again.
   python3 tools/live/eb-delay.py FanZone.dc.html"""
import sys
p = sys.argv[1]; s = open(p, encoding='utf-8').read()
def rep(a, b):
    global s
    if s.count(a) != 1: raise SystemExit('expected once: ' + a[:90])
    s = s.replace(a, b)
rep('''        else if (m === "eb") this.ebSoon(3000);''', '''        else if (m === "eb") this.ebSoon(6000);''')
rep('''get("moment") === "eb") this.ebSoon(5000); },''', '''get("moment") === "eb") this.ebSoon(8000); },''')
rep('''    this.skipIntro();''', '''    this.skipIntro();
    window.addEventListener("message", (e) => {
      if (!e.data || e.data.fz !== "shown" || new URLSearchParams(location.search).get("moment") !== "eb") return;
      this.setState({ ebOn: false }); this.ebSoon(6000);
    });''')
open(p, 'w', encoding='utf-8').write(s); print('ok')
