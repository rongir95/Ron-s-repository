#!/usr/bin/env python3
"""Patch for the live FanZone.dc.html (after eb-enter.py): when the prototype opens straight on the match page
(fixture=1, the Outside FanZone phone on the feature pages) the match page is just there: no push-in from the
right over FanZone. Opening it from inside the prototype still pushes in as before.
   python3 tools/live/fixture-still.py FanZone.dc.html"""
import sys
p = sys.argv[1]; s = open(p, encoding='utf-8').read()
def rep(a, b):
    global s
    if s.count(a) != 1: raise SystemExit('expected once: ' + a[:90])
    s = s.replace(a, b)
rep('''      <div style="position:absolute;inset:0;z-index:8;background:#080E12;overflow:hidden;animation:fzPushIn .32s cubic-bezier(.22,1,.36,1);">''',
    '''      <div style="position:absolute;inset:0;z-index:8;background:#080E12;overflow:hidden;{{ fxPushAnim }}">''')
rep('      ...this.gzVals(),', '      ...this.gzVals(),\n      fxPushAnim: this.P.startFixture ? "" : "animation:fzPushIn .32s cubic-bezier(.22,1,.36,1);",')
open(p, 'w', encoding='utf-8').write(s); print('ok')
