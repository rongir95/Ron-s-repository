#!/usr/bin/env python3
"""The "Choose your avatar" drawer per Figma "[Dev] Public Profile" (file ZERpW2GRsRMrd1URSjoeRB, node 9427:150304).

  Sheet #1B2326, radius 24; grabber 36x5 (white 16%); title 16px bold; close 32px (white 12%).
  Grid: 4 columns of 70px cells, 18px apart, 12px between rows, 20px top / 24px side padding.
  Each cell: a 58px avatar on #080E12 at 80% with a 1px white 10% border (the initial in 30px bold, or the
  picture filling the circle). The selected one gets your ring (vector, 3px) and a yellow check badge
  (24px, #FFFA00, cut out from the ring). The bottom fade is a CSS gradient (it was a PNG, like the ring).

Run after the other scripts:  python3 tools/avatar-drawer.py FanZone.dc.html
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

FONT = "font-family:'DAZN Oscine',sans-serif;"
start = src.index('    <!-- ===================== AVATARS DRAWER ===================== -->')
end = src.index('    <!-- ===================== OTHER USER\'S FOLLOWINGS ===================== -->')
block = src[start:end]

# header per Figma
block = block.replace('<div style="position:absolute;left:50%;top:8px;transform:translateX(-50%);width:36px;height:5px;border-radius:3px;background:rgba(255,255,255,.2);"></div>',
                      '<div style="position:absolute;left:50%;top:5px;transform:translateX(-50%);width:36px;height:5px;border-radius:100px;background:rgba(249,250,250,.16);"></div>', 1)
block = block.replace('<div style="position:relative;height:64px;flex-shrink:0;">', '<div style="position:relative;height:60px;flex-shrink:0;">', 1)
block = block.replace('<div style="position:absolute;left:0;right:0;top:26px;text-align:center;font-size:16px;font-weight:700;pointer-events:none;">Choose your avatar</div>',
                      '<div style="position:absolute;left:0;right:0;top:20px;text-align:center;font-size:16px;font-weight:700;line-height:25px;color:#F9FAFA;pointer-events:none;">Choose your avatar</div>', 1)
block = block.replace('style="position:absolute;right:16px;top:22px;width:32px;height:32px;border:0;cursor:pointer;border-radius:50%;background:rgba(255,255,255,.14);',
                      'style="position:absolute;right:16px;top:16px;width:32px;height:32px;border:0;cursor:pointer;border-radius:9999px;background:rgba(249,250,250,.12);', 1)

GRID = '''        <!-- grid -->
        <div class="fz-scroll" style="flex:1;overflow-y:auto;padding:20px 24px 96px;">
          <div style="display:grid;grid-template-columns:repeat(4,70px);justify-content:space-between;row-gap:12px;">
            <sc-for list="{{ avatarGrid }}" as="a" hint-placeholder-count="16">
              <div onClick="{{ a.onTap }}" role="button" aria-label="Avatar" aria-pressed="{{ a.pressed }}" style="position:relative;width:70px;height:70px;cursor:pointer;">
                <sc-if value="{{ a.selected }}" hint-placeholder-val="{{ false }}">
                  <span aria-hidden="true" style="position:absolute;inset:0;border-radius:50%;box-sizing:border-box;border:3px solid transparent;background:linear-gradient(#1B2326,#1B2326) padding-box,{{ ringBg }} border-box;animation:fzRxPop .25s cubic-bezier(.22,1.4,.36,1);"></span>
                </sc-if>
                <span style="position:absolute;left:6px;top:6px;width:58px;height:58px;box-sizing:border-box;border-radius:50%;overflow:hidden;border:1px solid rgba(255,255,255,.1);background:rgba(8,14,18,.8);display:flex;align-items:center;justify-content:center;">
                  <sc-if value="{{ a.isInitial }}" hint-placeholder-val="{{ false }}">
                    <span style="''' + FONT + '''font-weight:700;font-size:30px;line-height:1;color:#F9FAFA;">{{ a.initialLetter }}</span>
                  </sc-if>
                  <sc-if value="{{ a.notInitial }}" hint-placeholder-val="{{ true }}">
                    <img src="{{ a.src }}" alt="" style="display:block;width:100%;height:100%;object-fit:cover;{{ a.scaleStyle }}">
                  </sc-if>
                </span>
                <sc-if value="{{ a.selected }}" hint-placeholder-val="{{ false }}">
                  <span aria-hidden="true" style="position:absolute;left:40px;top:40px;width:30px;height:30px;box-sizing:border-box;border-radius:50%;border:3px solid #1B2326;background:#FFFA00;display:flex;align-items:center;justify-content:center;animation:fzRxPop .3s cubic-bezier(.22,1.6,.36,1);">
                    <svg width="14" height="12" viewBox="0 0 14 12" fill="none"><path d="M1.5 6.3l3.6 3.6L12.5 2" stroke="#080E12" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg>
                  </span>
                </sc-if>
              </div>
            </sc-for>
          </div>
        </div>
        <div aria-hidden="true" style="position:absolute;left:0;right:0;bottom:0;height:96px;pointer-events:none;background:linear-gradient(180deg,rgba(27,35,38,0) 0%,#1B2326 85%);"></div>
'''
m = re.search(r'        <!-- grid -->\n.*?        <img src="assets/img/avatars-bottom-fade.png"[^\n]*\n', block, re.S)
if not m:
    raise SystemExit('avatar grid not found')
block = block[:m.start()] + GRID + block[m.end():]
src = src[:start] + block + src[end:]

# every picture fills the same circle (uploads/* carry a transparent margin)
rep('      scaleStyle: "",\n      innerSizeStyle: s.dAvatar === a.id ? "width:84%;height:84%;" : "width:84%;height:84%;",',
    '      scaleStyle: /(^|\\/)uploads\\//.test(a.src || "") ? "transform:scale(1.207);" : "",\n      pressed: s.dAvatar === a.id ? "true" : "false",')

open(PATH, 'w', encoding='utf-8').write(src)
print('ok')
