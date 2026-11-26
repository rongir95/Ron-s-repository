#!/usr/bin/env python3
"""Patch for the live shell (index.html), after current-pages.py: every "Outside FanZone" screen is the match page
(prototype with fixture=1) with a placeholder of that feature where the FanZone card sits (slot=<feature name>),
until the feature has its own outside design.
   python3 tools/live/outside-fixture.py index.html"""
import sys
p = sys.argv[1]; s = open(p, encoding='utf-8').read()
old = "        var ph = page && page.phones && page.phones[i];"
if s.count(old) != 1: raise SystemExit('phone line not found')
s = s.replace(old, old + '''
        if (l === "Outside FanZone" && !(ph && ph.q)) ph = { label: "Outside FanZone · Match page", q: "fixture=1&slot=" + encodeURIComponent(f.name) };''')
old2 = "Outside FanZone it comes to Home as a card (design to come)."
if s.count(old2) != 1: raise SystemExit('poll note not found')
s = s.replace(old2, "Outside FanZone it shows on the match page, in place of the FanZone button when there's no live event (design to come).")
open(p, 'w', encoding='utf-8').write(s); print('ok')
