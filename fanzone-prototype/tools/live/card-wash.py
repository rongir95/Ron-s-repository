#!/usr/bin/env python3
"""Patch for the live (co-edited) FanZone.dc.html: My Card's team colour is painted on the card's scroller,
so it stays put while the content scrolls and the sticky top strip shows the same slice of it (no seam),
like other fans' cards.   python3 tools/live/card-wash.py FanZone.dc.html"""
import sys
p = sys.argv[1]; s = open(p, encoding='utf-8').read()
def rep(a, b):
    global s
    if s.count(a) != 1: raise SystemExit('not found once: ' + a[:90])
    s = s.replace(a, b)
rep('''        <!-- Background color team (375x350) -->
        <sc-if value="{{ cardReady }}" hint-placeholder-val="{{ true }}">
          <div class="fz-r-wash" style="position:absolute;left:0;right:0;top:0;height:350px;pointer-events:none;background:{{ cardWash }};"></div>
        </sc-if>
''', '''        <!-- Background color team (375x350): painted on the scroller itself, so it stays put while the content
             scrolls and the sticky top strip shows the same slice of it (no seam), like other fans' cards -->
''')
i = s.index('<div ref="{{ cardRef }}" class="fz-scroll" style="position:absolute;left:0;right:0;bottom:0;z-index:20;')
j = s.index('>', i); tag = s[i:j]
if 'background:#080E12;' not in tag: raise SystemExit('scroller background not found')
s = s[:i] + tag.replace('background:#080E12;', 'background-color:#080E12;background-image:{{ cardWashBg }};background-size:100% 350px;background-repeat:no-repeat;background-position:top;', 1) + s[j:]
rep('      cardWash, avatarGlow, avatarGlowRGB,', '      cardWash, cardWashBg: s.cardLoading ? "none" : cardWash, avatarGlow, avatarGlowRGB,')
W = '"linear-gradient(180deg,rgba(165,0,68,.6) 0%,rgba(165,0,68,0) 64.442%,rgba(165,0,68,0) 100%)"'
rep('...((isMe && s.cardFromComments) ? { cardWash: ' + W + ' } : {}),',
    '...((isMe && s.cardFromComments) ? { cardWash: ' + W + ', cardWashBg: s.cardLoading ? "none" : ' + W + ' } : {}),')
open(p, 'w', encoding='utf-8').write(s); print('ok')
