#!/usr/bin/env python3
"""Patch for the live shell (index.html), after current-pages.py: the Engagement break page's Current screen
(the prototype with moment=eb).
   python3 tools/live/eb-page.py index.html"""
import sys
p = sys.argv[1]; s = open(p, encoding='utf-8').read()
old = '    PAGES.team = {'
if s.count(old) != 1: raise SystemExit('anchor not found')
s = s.replace(old, '''    PAGES.eb = { phones: [cur("moment=eb&team=bayern"), later, out], note: note("a promo or sponsored video takes over FanZone under its header for a few seconds; the X closes it.") };
    PAGES.team = {''')
open(p, 'w', encoding='utf-8').write(s); print('ok')
