#!/usr/bin/env python3
"""Patch for the live index.html (after mute-page.py): a phone can show a still screen from Figma (ph.img).
FanZone button on fixture: the third phone is "Outside - Stats and scores", the Scores screen from Figma FanZone 80-20
(a38ncus4fbwkPfnlFQIUPt 56:211394, assets/screens/scores-outside.png): the match tile with "5.7K fans are in the
FanZone" and Join.
FanZone blockers & Mute shows only Current and 80-20 (no Outside phone).
   python3 tools/live/outside-scores.py index.html"""
import sys
p = sys.argv[1]; s = open(p, encoding='utf-8').read()
def rep(a, b):
    global s
    if s.count(a) != 1: raise SystemExit('expected once: ' + a[:90])
    s = s.replace(a, b)
rep('''        if (l === "Outside FanZone" && !(ph && ph.q)) ph =''', '''        if (l === "Outside FanZone" && !(ph && (ph.q || ph.img))) ph =''')
rep('''          (ph && ph.q ? '<div class="fp-phone"><iframe''', '''          (ph && ph.img ? '<div class="fp-phone fp-still"><img src="' + ph.img + '" alt="' + f.name + ': ' + (ph.label || l) + '"></div>' : '') +
          (ph && ph.img ? '' : ph && ph.q ? '<div class="fp-phone"><iframe''')
rep('''    PAGES.fzbutton = { phones: [cur("fixture=1"), later, out], note: note("the FanZone card on the match page: FanZone, Join chat and quick reactions; tap it to open FanZone.") };''',
    '''    PAGES.fzbutton = { phones: [cur("fixture=1"), later, { img: "assets/screens/scores-outside.png", label: "Outside - Stats and scores" }], note: note("the FanZone card on the match page: FanZone, Join chat and quick reactions; tap it to open FanZone. Outside: on Scores, the live match tile shows how many fans are in the FanZone, with Join.") };''')
rep('''  .fp-foot { position: absolute;''', '''  .fp-phone.fp-still img { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; display: block; z-index: 1; }
  .fp-foot { position: absolute;''')
# FanZone blockers & Mute: no Outside phone (Current and 80-20 only)
rep('{"id": "mute", "name": "FanZone blockers & Mute", "cat": "Chat", "kind": "imp", "screens": 3}', '{"id": "mute", "name": "FanZone blockers & Mute", "cat": "Chat", "kind": "imp", "screens": 2}')
rep('''PAGES.mute = { phones: [cur("moment=blocked&team=bayern"), later, out]''', '''PAGES.mute = { phones: [cur("moment=blocked&team=bayern"), later]''')
open(p, 'w', encoding='utf-8').write(s); print('ok')
