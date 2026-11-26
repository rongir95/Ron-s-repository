#!/usr/bin/env python3
"""Patch for the live shell (index.html), after feature-pages.py: the Poll feature page.
   Current = the existing "Current poll", 80-20 = Poll V3, Outside FanZone = placeholder for the Poll card on Home
   (waiting for a design). Each phone is the real prototype (FanZone.dc.html) with the panel's settings plus
   start=fanzone, poll=<kind> and team=bayern, so it opens straight into the running poll.
   python3 tools/live/poll-page.py index.html"""
import sys
p = sys.argv[1]; s = open(p, encoding='utf-8').read()
def rep(a, b):
    global s
    if s.count(a) != 1: raise SystemExit('expected once: ' + a[:90])
    s = s.replace(a, b)
rep('  var PAGES = {};', '''  var PAGES = {
    poll: {
      phones: [{ q: "poll=current&team=bayern" }, { q: "poll=v3&team=bayern" }, { label: "Outside FanZone · Home", empty: "Poll card on Home<br>Waiting for a design" }],
      note: "<b>What changed:</b> the poll becomes a card with the clubs: pick one and the results fill in, with a white border on your pick. Outside FanZone it comes to Home as a card (design to come)."
    }
  };
  // a phone in a feature page: the real prototype with the panel's settings, opening in FanZone
  function phoneSrc(q) { return "FanZone.dc.html?fp=" + (++loads) + "&" + query().replace(/start=\\w+/, "start=fanzone") + "&" + q; }''')
rep("(ph && ph.src ? '<div class=\"fp-phone\"><iframe title=\"' + f.name + ': ' + l + '\" allow=\"autoplay; fullscreen\" src=\"' + ph.src + '\"></iframe></div>'",
    "(ph && ph.q ? '<div class=\"fp-phone\"><iframe title=\"' + f.name + ': ' + l + '\" allow=\"autoplay; fullscreen\" src=\"' + phoneSrc(ph.q) + '\"></iframe></div>'")
# settings changes (and Restart) reload the feature page phones too
rep('''    frame.src = "FanZone.dc.html?n=" + loads + "&" + q + "#" + q;''',
    '''    frame.src = "FanZone.dc.html?n=" + loads + "&" + q + "#" + q;
    if (typeof paintPages === "function" && settings.view === "pages") { shownFeature = null; paintPages(); }''')
open(p, 'w', encoding='utf-8').write(s); print('ok')
