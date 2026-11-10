#!/usr/bin/env python3
"""One avatar style for every fan in the FanZone chat, per FanZone DS ".UserIndicator"
(file NIgPxOlNU4U3sWMRdoE4Qh, node 13299:56861):

  24x24 box, 1.5px ring on the inside edge in the fan's team color, 18px picture centred (1.5px gap),
  or, with no picture, an 18px #080E12 circle with the nickname's first letter (11px bold #F9FAFA).

The avatar files come in two kinds: assets/img/* fill their circle, uploads/* carry a transparent
margin (the circle is 232 of 280 px). Those are scaled by 280/232 so every picture fills the same 18px.
My own messages use my chosen avatar, or my initial (the old file had a ring baked in).

Run last:  python3 tools/chat-avatars.py FanZone.dc.html
"""
import re, sys

PATH = sys.argv[1]
src = open(PATH, encoding='utf-8').read()

def rep(old, new, count=1):
    global src
    n = src.count(old)
    if n != count:
        raise SystemExit(f'expected {count} occurrence(s), found {n}: {old[:100]!r}')
    src = src.replace(old, new)

# ---------------------------------------------------------------- markup: picture or initial inside the ring
rep('                  <img src="{{ m.avatar }}" alt="" style="display:block;width:18px;height:18px;border-radius:50%;object-fit:cover;{{ m.imgScale }}">',
    '                  <sc-if value="{{ m.hasImg }}" hint-placeholder-val="{{ true }}">\n'
    '                    <img src="{{ m.avatar }}" alt="" style="display:block;width:18px;height:18px;border-radius:50%;object-fit:cover;{{ m.imgScale }}">\n'
    '                  </sc-if>\n'
    '                  <sc-if value="{{ m.noImg }}" hint-placeholder-val="{{ false }}">\n'
    '                    <span style="display:flex;align-items:center;justify-content:center;width:18px;height:18px;border-radius:50%;background:#080E12;color:#F9FAFA;font-family:\'DAZN Oscine\',sans-serif;font-size:11px;font-weight:700;line-height:1;">{{ m.initial }}</span>\n'
    '                  </sc-if>')

# ---------------------------------------------------------------- data
rep("        if (m.mine) { const myFav = s.favoriteId ? teamById(s.favoriteId) : null; return { ...m, ring: myFav ? myFav.card : \"linear-gradient(210deg,#8923A0 0%,#F1A322 38%,#FFFA00 100%)\", imgScale: \"\", onOpen: this.openCard }; }\n"
    "        return { ...m, ring: t ? t.card : \"#F2C400\", imgScale: \"transform:scale(1.05);\", onOpen: () => this.openUserCard(m) };",
    "        const fzAv = { hasImg: !!m.avatar, noImg: !m.avatar, initial: String(m.name || \"?\").charAt(0).toUpperCase(), imgScale: /(^|\\/)uploads\\//.test(m.avatar || \"\") ? \"transform:scale(1.207);\" : \"\" };\n"
    "        if (m.mine) { const myFav = s.favoriteId ? teamById(s.favoriteId) : null; return { ...m, ...fzAv, ring: myFav ? myFav.card : \"linear-gradient(210deg,#8923A0 0%,#F1A322 38%,#FFFA00 100%)\", onOpen: this.openCard }; }\n"
    "        return { ...m, ...fzAv, ring: t ? t.card : \"#F2C400\", onOpen: () => this.openUserCard(m) };")
# my messages: my chosen avatar, else my initial
rep('const av = s.avatar && AV_MAP[s.avatar] && AV_MAP[s.avatar].src ? AV_MAP[s.avatar].src : "assets/comments/avin.png";',
    'const av = s.avatar && AV_MAP[s.avatar] && AV_MAP[s.avatar].src ? AV_MAP[s.avatar].src : "";')
# two fans without a picture, so the initial variant shows in the chat
for name in ('Daiki', 'Sho'):
    n = 0
    def sub(mm):
        global n
        n += 1
        return mm.group(1) + 'avatar: ""'
    new, k = re.subn(r'(\{ name: "' + name + r'",[^\n]*?)avatar: "[^"]*"', lambda mm: mm.group(1) + 'avatar: ""', src, count=1)
    if k != 1:
        raise SystemExit('chat fan not found: ' + name)
    src = new

open(PATH, 'w', encoding='utf-8').write(src)
print('ok')
