#!/usr/bin/env python3
"""Small UI fixes.

  - Drawers pushed over the Fan Card (My Favorite, Followings, Avatars, ...): the card slides left and dims under
    them, and its team-colour gradient showed through the new drawer's rounded top-left corner. Once the push
    animation is over the card is hidden (it comes back at once when you go back).

  - Other fans' cards: "<name> and you have N interests in common" shows only the text (no avatars).

Run after the other scripts:  python3 tools/ui-fixes.py FanZone.dc.html
"""
import sys

PATH = sys.argv[1]
src = open(PATH, encoding='utf-8').read()

def rep(old, new, count=1):
    global src
    n = src.count(old)
    if n != count:
        raise SystemExit(f'expected {count} occurrence(s), found {n}: {old[:100]!r}')
    src = src.replace(old, new)

rep('''        ? "transform:translateX(-30%);filter:brightness(.55);pointer-events:none;"
        : "transform:translateX(0);filter:none;") + "transition:transform .32s cubic-bezier(.2,0,0,1), filter .32s ease;",''',
    '''        ? "transform:translateX(-30%);filter:brightness(.55);pointer-events:none;visibility:hidden;transition:transform .32s cubic-bezier(.2,0,0,1), filter .32s ease, visibility 0s linear .32s;"
        : "transform:translateX(0);filter:none;visibility:visible;transition:transform .32s cubic-bezier(.2,0,0,1), filter .32s ease, visibility 0s;"),''')

import re
m = re.search(r'(              <div style="display:flex;align-items:center;gap:6px;margin:0 16px 12px;">\n)                <span style="display:flex;flex-direction:row-reverse;align-items:center;flex-shrink:0;padding-left:8px;">\n.*?\n                </span>\n(                <span style="font-size:12px;line-height:1.52;color:#B3B9BB;min-width:0;"><strong style="color:#B3B9BB;font-weight:700;">\{\{ commonWho \}\}</strong>)', src, re.S)
if not m:
    raise SystemExit('common-interests avatars not found')
src = src[:m.start()] + m.group(1) + m.group(2) + src[m.end():]

open(PATH, 'w', encoding='utf-8').write(src)
print('ok')
