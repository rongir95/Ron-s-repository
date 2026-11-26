#!/usr/bin/env python3
"""Patch for the live index.html: Standalone predictions. The Scores tag uses the plain chip (like the second phone's),
and "Match page" is renamed "Fixture page" (tag and note). A phone can opt out of the highlighted chip with plain: true.
   python3 tools/live/fixture-chip.py index.html"""
import sys
p = sys.argv[1]; s = open(p, encoding='utf-8').read()
def rep(a, b):
    global s
    if s.count(a) != 1: raise SystemExit('expected once: ' + a[:90])
    s = s.replace(a, b)
rep('''{ src: "screens.html?v=predict", label: "Scores" }, { src: "screens.html?v=predictfix", label: "Match page" }]''',
    '''{ src: "screens.html?v=predict", label: "Scores", plain: true }, { src: "screens.html?v=predictfix", label: "Fixture page" }]''')
rep('''The match page has the prediction card too." };''', '''The fixture page has the prediction card too." };''')
rep('''(labels[i] === "80-20" || labels[i] === "New" ? ' hl' : '')''', '''((labels[i] === "80-20" || labels[i] === "New") && !(ph && ph.plain) ? ' hl' : '')''')
open(p, 'w', encoding='utf-8').write(s); print('ok')
