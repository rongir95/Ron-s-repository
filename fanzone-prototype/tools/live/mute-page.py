#!/usr/bin/env python3
"""Patch for the live index.html (after status-menu.py): FanZone blockers & Mute gets its Current screen: FanZone with
the chat disabled (moment=blocked, Figma FanZone 80-20 14:64611).
   python3 tools/live/mute-page.py index.html"""
import sys
p = sys.argv[1]; s = open(p, encoding='utf-8').read()
a = '''    PAGES.fzbutton = {'''
if s.count(a) != 1: raise SystemExit('pages block changed')
s = s.replace(a, '''    PAGES.mute = { phones: [cur("moment=blocked&team=bayern"), later, out], note: note("when you're blocked the message bar becomes \\u201cChat disabled\\u201d, with a link to the Community guidelines; you can still read the chat.") };
''' + a)
open(p, 'w', encoding='utf-8').write(s); print('ok')
