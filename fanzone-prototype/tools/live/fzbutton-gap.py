#!/usr/bin/env python3
"""Patch for the live index.html (after chip-yellow3.py):
 - FanZone button on fixture: Current is the match page with the FanZone card (Figma FanZone 80-20 23:153607:
   FanZone, Join chat and the reactions), opened straight on the match page (fixture=1).
 - More room between the tags (Current / 80-20 / Outside FanZone) and the screens under them: 12px -> 22px.
   python3 tools/live/fzbutton-gap.py index.html"""
import sys
p = sys.argv[1]; s = open(p, encoding='utf-8').read()
def rep(a, b):
    global s
    if s.count(a) != 1: raise SystemExit('expected once: ' + a[:90])
    s = s.replace(a, b)
rep('''    PAGES.actions = {''', '''    PAGES.fzbutton = { phones: [cur("fixture=1"), later, out], note: note("the FanZone card on the match page: FanZone, Join chat and quick reactions; tap it to open FanZone.") };
    PAGES.actions = {''')
rep('''  .fp-col { display: flex; flex-direction: column; align-items: center; gap: 12px; margin: 0; }''',
    '''  .fp-col { display: flex; flex-direction: column; align-items: center; gap: 22px; margin: 0; }''')
rep('''(h - 30) / 812);''', '''(h - 40) / 812);''')
rep('''min-height: calc(812px * var(--fs, .6) - 2px)''', '''min-height: calc(812px * var(--fs, .6) + 8px)''')
open(p, 'w', encoding='utf-8').write(s); print('ok')
