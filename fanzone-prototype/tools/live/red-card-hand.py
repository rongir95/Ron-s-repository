#!/usr/bin/env python3
"""Patch for FanZone.dc.html (after live-updates.py): the Red card live update shows the hand holding the red card
(Figma 38:193908, assets/liveupdates/hand.png) instead of the CSS-drawn card.
   python3 tools/live/red-card-hand.py FanZone.dc.html"""
import sys
p = sys.argv[1]; s = open(p, encoding='utf-8').read()
def rep(a, b):
    global s
    if s.count(a) != 1: raise SystemExit('expected once: ' + a[:90])
    s = s.replace(a, b)
rep('''  .lu-art { position: absolute; border-radius: 9%/7%; background: linear-gradient(162deg, #FF5A4E 0%, #F21C1C 38%, #C80A12 100%); box-shadow: inset 0 0 0 1px rgba(255,255,255,.18), 0 18px 40px rgba(0,0,0,.45); pointer-events: none; overflow: hidden; }
  .lu-art::after { content: ""; position: absolute; inset: 0; background: linear-gradient(118deg, rgba(255,255,255,.38) 0%, rgba(255,255,255,.12) 34%, rgba(255,255,255,0) 35%); }''',
    '''  .lu-art { position: absolute; background: url(assets/liveupdates/hand.png) center / contain no-repeat; filter: drop-shadow(0 14px 28px rgba(0,0,0,.45)); pointer-events: none; }''')
rep('''.lu-over .lu-art { right: 34px; bottom: 120px; width: 132px; height: 182px; transform: rotate(16deg);''',
    '''.lu-over .lu-art { right: 0; bottom: 104px; width: 196px; height: 220px; transform-origin: 85% 95%;''')
rep('''.lu-row .lu-art { z-index: 2; right: 26px; top: 0; width: 36px; height: 50px; transform: rotate(16deg);''',
    '''.lu-row .lu-art { z-index: 2; right: 14px; top: 0; width: 54px; height: 61px; transform-origin: 85% 95%;''')
rep('''@keyframes luArt { from { opacity: 0; transform: translate(220px, 40px) rotate(40deg); } to { opacity: 1; transform: rotate(16deg); } }''',
    '''@keyframes luArt { from { opacity: 0; transform: translate(200px, 60px) rotate(24deg); } to { opacity: 1; transform: none; } }''')
rep('''@keyframes luArtMini { from { opacity: 0; transform: translate(20px, 14px) rotate(36deg); } to { opacity: 1; transform: rotate(16deg); } }''',
    '''@keyframes luArtMini { from { opacity: 0; transform: translate(20px, 14px) rotate(20deg); } to { opacity: 1; transform: none; } }''')
open(p, 'w', encoding='utf-8').write(s); print('ok')
