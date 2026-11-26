#!/usr/bin/env python3
"""Patch for the live index.html (after no-status.py): the third phone's title "Outside FanZone" is now "Standalone"
(tags such as "Standalone · Match page" and "Standalone - Stats and scores", placeholders and the explanation lines).
   python3 tools/live/standalone.py index.html"""
import sys
p = sys.argv[1]; s = open(p, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    if s.count(a) != n: raise SystemExit('expected %d: %s' % (n, a[:90]))
    s = s.replace(a, b)
rep('label: "Outside FanZone · Match page"', 'label: "Standalone · Match page"')
rep('label: "Outside FanZone · Home"', 'label: "Standalone · Home"')
rep('label: "Outside - Stats and scores"', 'label: "Standalone - Stats and scores"')
rep('out = { empty: "Outside FanZone', 'out = { empty: "Standalone')
rep('Outside FanZone it shows on the match page', 'Standalone, it shows on the match page')
rep('Outside: on Scores', 'Standalone: on Scores')
n = s.count("(ph && ph.label || l)")
if n < 1: raise SystemExit('chip label expression changed')
s = s.replace("(ph && ph.label || l)", "(ph && ph.label || l).replace(/^Outside FanZone/, 'Standalone')")
open(p, 'w', encoding='utf-8').write(s); print('ok', n)
