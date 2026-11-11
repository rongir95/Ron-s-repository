#!/usr/bin/env python3
"""The updated iOS keyboard everywhere the prototype shows one, per Figma "[Dev] Public Profile"
(file ZERpW2GRsRMrd1URSjoeRB, screen "Empty status field" node 6377:235075, Keyboard node 8003:175519).

  375 x 317, light glass panel (radius 27), keys 45px tall with radius 8.5 (#EDF4F9, glyphs #474E53),
  blue return key (#0088FF), emoji and mic below. Key positions are Figma's. Built in HTML and CSS
  (letters are text, symbols are SVGs from Figma in assets/icons/kb-*.svg), so it stays sharp at any zoom.

Two places use it: the status editor on the Fan Card (replaces the dark 291px keyboard; the sheet above
it moves up to match) and the Comments composer (replaces the dark keyboard; Return still sends).

Run after the other scripts:  python3 tools/ios-keyboard.py FanZone.dc.html
"""
import re, sys

PATH = sys.argv[1]
src = open(PATH, encoding='utf-8').read()

KB_H = 317

ROW1 = [(8.5 + i * 36.4, 'qwertyuiop'[i]) for i in range(10)]
ROW2 = [(28.5 + i * 36, 'asdfghjkl'[i]) for i in range(9)]
ROW3 = [(x, c) for x, c in zip([67.4, 102.5, 137.7, 172.8, 207.9, 243, 278.1], 'zxcvbnm')]

KEY = ("position:absolute;top:{y}px;left:{x}px;width:{w}px;height:45px;border-radius:8.5px;background:#EDF4F9;"
       "display:flex;align-items:center;justify-content:center;box-sizing:border-box;")
GLYPH = ("font-family:-apple-system,'SF Pro Text','SF Compact Text',system-ui,'Helvetica Neue',Arial,sans-serif;"
         "font-size:25px;line-height:1;color:#474E53;padding-bottom:5px;")

def keyboard(position_style, return_attr=''):
    keys = []
    for y, row, w in ((24, ROW1, 30.4), (80, ROW2, 30), (136, ROW3, 29.1)):
        for x, c in row:
            keys.append(f'<span style="{KEY.format(x=x, y=y, w=w)}{GLYPH}">{c}</span>')
    keys.append(f'<span style="{KEY.format(x=8.5, y=136, w=44.7)}"><img src="assets/icons/kb-shift.svg" alt="" width="24" height="20" style="display:block;"></span>')
    keys.append(f'<span style="{KEY.format(x=321.5, y=136, w=45)}"><img src="assets/icons/kb-delete.svg" alt="" width="24" height="20" style="display:block;"></span>')
    keys.append(f'<span style="{KEY.format(x=8.5, y=192, w=91.7)}font-family:-apple-system,\'SF Pro Rounded\',system-ui,\'Helvetica Neue\',Arial,sans-serif;font-size:18px;color:#474E53;">ABC</span>')
    keys.append(f'<span style="{KEY.format(x=106.2, y=192, w=162.3)}"></span>')
    keys.append(f'<span{return_attr} style="{KEY.format(x=274.5, y=192, w=92)}background:#0088FF;"><img src="assets/icons/kb-return.svg" alt="" width="20" height="18" style="display:block;"></span>')
    keys.append('<img src="assets/icons/kb-emoji.svg" alt="" width="27" height="27" style="position:absolute;left:36px;top:264px;display:block;">')
    keys.append('<img src="assets/icons/kb-mic.svg" alt="" width="19" height="29" style="position:absolute;left:317px;top:263px;display:block;">')
    return (f'<div aria-hidden="true" style="{position_style}height:{KB_H}px;border-radius:27px;overflow:hidden;'
            'background:rgba(206,213,220,.78);-webkit-backdrop-filter:blur(20px) saturate(1.4);backdrop-filter:blur(20px) saturate(1.4);'
            'box-shadow:0 0 0 .5px rgba(255,255,255,.35) inset;">'
            '<div style="position:relative;width:375px;height:317px;margin:0 auto;">' + ''.join(keys) + '</div></div>')

# ---------------------------------------------------------------- status editor (Fan Card)
m = re.search(r'      <!-- iOS keyboard -->\n      <div style="position:absolute;left:0;right:0;bottom:0;height:291px;.*?\n      </div>\n(?=    </sc-if>\n\n    <!-- ===================== COMMENTS & REPLIES OVERLAYS)', src, re.S)
if not m:
    raise SystemExit('status keyboard not found')
src = src[:m.start()] + '      <!-- iOS keyboard (Figma 8003:175519) -->\n      ' + keyboard('position:absolute;left:0;right:0;bottom:0;z-index:25;') + '\n' + src[m.end():]
n = src.count('top:282px;bottom:291px;z-index:26;')
if n != 1:
    raise SystemExit(f'status sheet offset: {n}')
src = src.replace('top:282px;bottom:291px;z-index:26;', f'top:282px;bottom:{KB_H}px;z-index:26;')

# ---------------------------------------------------------------- Comments composer
m = re.search(r'      <!-- iOS keyboard \(decorative\) -->\n      <div style="background:#1a1c1e;padding-bottom:8px;">.*?\n        <div style="display:flex;justify-content:center;padding-top:8px;"><div style="width:134px;height:5px;border-radius:3px;background:#fff;"></div></div>\n      </div>\n', src, re.S)
if not m:
    raise SystemExit('composer keyboard not found')
src = (src[:m.start()] + '      <!-- iOS keyboard (Figma 8003:175519) -->\n      '
       + keyboard('position:relative;flex-shrink:0;', ' onClick="{{ crOnSend }}" title="Send"').replace('<span onClick', '<span onClick', 1)
       + '\n' + src[m.end():])

# the keyboard's rounded corners show the composer's own background, not the comments behind it
old = '<div style="position:absolute;left:0;right:0;bottom:0;z-index:45;display:flex;flex-direction:column;">'
if src.count(old) != 1:
    raise SystemExit('composer wrapper not found')
src = src.replace(old, '<div style="position:absolute;left:0;right:0;bottom:0;z-index:45;display:flex;flex-direction:column;background:#0c161c;">')

open(PATH, 'w', encoding='utf-8').write(src)
print('ok')
