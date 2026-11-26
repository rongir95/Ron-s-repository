#!/usr/bin/env python3
"""Patch for FanZone.dc.html: host avatar per Figma FanZone 80-20 1:44398 (Avatar/PublicView): the yellow DAZN avatar
(assets/pinned/host-avatar.png) inside the host gradient ring (#8923A0 70% -> #F1A322 -> #FFFA00), in chat messages
and on the host's profile.
   python3 tools/live/host-avatar-fig.py FanZone.dc.html"""
import sys
p = sys.argv[1]; s = open(p, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    if s.count(a) != n: raise SystemExit('expected %d: %s' % (n, a[:90]))
    s = s.replace(a, b)
rep('assets/pinned/host-avatar.svg', 'assets/pinned/host-avatar.png', s.count('assets/pinned/host-avatar.svg') or 1)
rep('''// focus mode: the host's messages (Figma 23:97199)''',
    '''// host ring (Figma 1:44398 Progress): purple -> orange -> brand yellow, bottom-left to top-right
const HOST_RING = "linear-gradient(45deg,rgba(137,35,160,.7) 0%,#F1A322 22.6%,#FFFA00 100%)";
// focus mode: the host's messages (Figma 23:97199)''')
rep('''ring: t ? t.card : "#F2C400", onOpen: () => this.openUserCard(m), onPress: (e) => this.msgPressStart(m, t ? t.card : "#F2C400", fzAv) };''',
    '''ring: m.host ? HOST_RING : (t ? t.card : "#F2C400"), onOpen: () => this.openUserCard(m), onPress: (e) => this.msgPressStart(m, m.host ? HOST_RING : (t ? t.card : "#F2C400"), fzAv) };''')
rep('''    const i = this.crProfileFor({ name, img: (msg && msg.avatar) || "" });
''', '''    const i = this.crProfileFor({ name, img: (msg && msg.avatar) || "" });
    if (/host-avatar/.test((msg && msg.avatar) || "")) Object.assign(OTHER_PROFILES[i], { avatar: "assets/pinned/host-avatar.png", ring: HOST_RING, glow: "255,250,0" });
''')
open(p, 'w', encoding='utf-8').write(s); print('ok')
