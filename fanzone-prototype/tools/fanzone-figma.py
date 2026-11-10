#!/usr/bin/env python3
"""Align the FanZone drawer with the Figma screen "FanZone" (file EyEm3J8Y3qrWV40vOPOkjV, node 496:103459):

  - Live chat header, sponsored variant (shell setting, ?sponsor=1): sponsor red (#F40009) with the Coca-Cola logo,
    leaderboard + close icons as exported from Figma; the regular header stays the default
  - Messages: #0C161C, rows 8px/12px, 24px avatars (18px image inside the team ring), 14px bold names, 16px text
  - My avatar by the Message field: 30px image inside a 2px ring in my favorite team's color

Icons and the logo were exported from Figma as SVG into assets/icons/ (sponsor-cocacola, fz-leaderboard, fz-close).
Run last:  python3 tools/fanzone-figma.py FanZone.dc.html
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

# ---------------------------------------------------------------- drawer background
rep('pointer-events:auto;background:#080E12;border-radius:24px 24px 0 0;display:flex;flex-direction:column;',
    'pointer-events:auto;background:#0C161C;border-radius:24px 24px 0 0;display:flex;flex-direction:column;padding-bottom:21px;box-sizing:border-box;')
# 21px home-indicator strip under the message bar, as in the Figma frame
rep('<div class="{{ fzPanelCls }}" style="position:absolute;left:0;right:0;bottom:0;top:{{ fzPanelTop }}px;',
    '<div class="fz-fzpanel {{ fzPanelCls }}" style="position:absolute;left:0;right:0;bottom:0;top:{{ fzPanelTop }}px;')
rep("  @keyframes fzPushIn {",
    "  .fz-fzpanel::after { content: \"\"; position: absolute; left: 50%; bottom: 8px; transform: translateX(-50%); width: 134px; height: 5px; border-radius: 100px; background: #F9FAFA; pointer-events: none; }\n  @keyframes fzPushIn {")

# ---------------------------------------------------------------- header
m = re.search(r'        <!-- header -->\n        <div style="position:relative;z-index:3;flex-shrink:0;height:48px;display:flex;align-items:center;gap:16px;padding:0 20px 0 16px;background:#1B2326;.*?\n        </div>\n(?=        <!-- ===================== LIVE POLL)', src, re.S)
if not m:
    raise SystemExit('FanZone header not found')
HEADER = '''        <!-- header (Figma "Live chat header", sponsor-branded) -->
        <div style="position:relative;z-index:3;flex-shrink:0;height:48px;box-sizing:border-box;background:#F40009;border-radius:24px 24px 0 0;border-bottom:1px solid rgba(8,14,18,.6);box-shadow:0 -1px 0 rgba(249,250,250,.2);">
          <button class="fz-collapse-btn" onClick="{{ toggleFzCollapse }}" aria-label="{{ fzCollapseLabel }}" aria-expanded="{{ fzExpandedAttr }}" style="position:absolute;left:12px;top:50%;transform:translateY(-50%);display:flex;align-items:center;gap:16px;border:0;padding:0;background:transparent;cursor:pointer;">
            <svg width="20" height="20" viewBox="0 0 20 20" fill="none" aria-hidden="true" style="display:block;flex-shrink:0;transform:rotate({{ fzCollapseRot }}deg);transition:transform .3s ease;">
              <path d="M17 6L3 6" stroke="#F9FAFA" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"></path>
              <path d="M14.668 15.6667L10.0013 11L5.33464 15.6667" stroke="#F9FAFA" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"></path>
            </svg>
            <img src="assets/icons/sponsor-cocacola.svg" alt="FanZone, presented by Coca-Cola" width="74" height="24" style="display:block;flex-shrink:0;">
          </button>
          <div style="position:absolute;right:16px;top:0;bottom:0;display:flex;align-items:center;">
            <img src="assets/icons/fz-leaderboard.svg" alt="" width="32" height="32" style="display:block;">
            <span aria-hidden="true" style="width:1px;height:17px;margin:0 15px 0 10px;background:rgba(249,250,250,.6);"></span>
            <button onClick="{{ goHome }}" aria-label="Close FanZone" title="Close FanZone" style="width:20px;height:20px;border:0;padding:0;background:transparent;cursor:pointer;display:block;"><img src="assets/icons/fz-close.svg" alt="" width="20" height="20" style="display:block;"></button>
          </div>
        </div>
'''
# both headers stay: the regular one by default, the sponsored one when the shell turns it on (?sponsor=1)
PLAIN = m.group(0).replace('        <!-- header -->\n', '        <!-- header (regular) -->\n', 1)
HEADER = HEADER.replace('        <!-- header (Figma "Live chat header", sponsor-branded) -->\n', '        <!-- header (Figma "Live chat header", sponsor-branded) -->\n', 1)
both = ('        <sc-if value="{{ fzPlainHeader }}" hint-placeholder-val="{{ true }}">\n' + PLAIN + '        </sc-if>\n'
        '        <sc-if value="{{ fzSponsorHeader }}" hint-placeholder-val="{{ false }}">\n' + HEADER + '        </sc-if>\n')
src = src[:m.start()] + both + src[m.end():]
rep('    if (q.get("reset") === "1") o.resetOnLoad = true;',
    '    if (q.get("reset") === "1") o.resetOnLoad = true;\n    if (q.get("sponsor") === "1") o.fzSponsor = true;')
rep('      openFanZoneOver: this.openFanZoneOver,',
    '      openFanZoneOver: this.openFanZoneOver,\n      fzSponsorHeader: this.P.fzSponsor === true,\n      fzPlainHeader: this.P.fzSponsor !== true,')

# ---------------------------------------------------------------- messages
rep('<div style="min-height:100%;display:flex;flex-direction:column;justify-content:flex-end;padding:2px 16px 2px;">',
    '<div style="min-height:100%;box-sizing:border-box;display:flex;flex-direction:column;justify-content:flex-end;gap:2px;padding:0 12px 12px;">')
rep('              <div style="flex-shrink:0;display:flex;gap:10px;margin-bottom:16px;animation:fzMsgIn .45s cubic-bezier(.22,1,.36,1);">',
    '              <div style="flex-shrink:0;display:flex;align-items:flex-start;gap:6px;padding:8px 0;animation:fzMsgIn .45s cubic-bezier(.22,1,.36,1);">')
rep('<div onClick="{{ m.onOpen }}" style="width:24px;height:24px;border-radius:50%;flex-shrink:0;overflow:hidden;cursor:pointer;box-sizing:content-box;border:1.5px solid transparent;padding:1px;margin:-1.5px;background:linear-gradient(#080E12,#080E12) padding-box,{{ m.ring }} border-box;">\n                  <img src="{{ m.avatar }}" alt="" style="width:100%;height:100%;border-radius:50%;object-fit:cover;{{ m.imgScale }}">',
    '<div onClick="{{ m.onOpen }}" style="width:24px;height:24px;border-radius:50%;flex-shrink:0;cursor:pointer;box-sizing:border-box;border:1.5px solid transparent;padding:1.5px;background:linear-gradient(#0C161C,#0C161C) padding-box,{{ m.ring }} border-box;">\n                  <img src="{{ m.avatar }}" alt="" style="display:block;width:18px;height:18px;border-radius:50%;object-fit:cover;{{ m.imgScale }}">')
rep('<div onClick="{{ m.onOpen }}" style="font-size:13px;font-weight:700;color:#F9FAFA;line-height:1.15;cursor:pointer;display:inline-block;">{{ m.name }}</div>\n                  <div style="font-size:15px;color:#B3B9BB;line-height:1.35;margin-top:2px;">{{ m.text }}</div>',
    '<div onClick="{{ m.onOpen }}" style="font-size:14px;font-weight:700;color:#F9FAFA;line-height:24px;height:24px;cursor:pointer;display:inline-block;">{{ m.name }}</div>\n                  <div style="font-size:16px;font-weight:400;color:#B3B9BB;line-height:1.3;margin-top:4px;">{{ m.text }}</div>')
rep('<div style="min-width:0;">\n                  <div onClick="{{ m.onOpen }}" style="font-size:14px;',
    '<div style="flex:1;min-width:0;">\n                  <div onClick="{{ m.onOpen }}" style="font-size:14px;')

# collapsed drawer: only the header shows (no chat peeking out under it)
rep('<div class="fz-scroll" ref="{{ feedRef }}" onScroll="{{ onFeedScroll }}" style="flex:1;overflow-y:auto;min-height:0;">',
    '<div class="fz-scroll" ref="{{ feedRef }}" onScroll="{{ onFeedScroll }}" style="flex:1;overflow-y:auto;min-height:0;transition:opacity .25s ease;{{ fzPollWrapStyle }}">')

# ---------------------------------------------------------------- my avatar by the Message field
rep('<button onClick="{{ openCard }}" title="Open your Fan Card" style="scroll-snap-align:start;border:0;padding:2px;{{ selfCardCursor }}flex-shrink:0;width:40px;height:40px;border-radius:50%;background:{{ ringBg }};">\n              <span style="position:relative;display:block;width:100%;height:100%;border-radius:50%;overflow:hidden;background:#080E12;padding:3px;box-sizing:border-box;">',
    '<button onClick="{{ openCard }}" title="Open your Fan Card" style="position:relative;scroll-snap-align:start;border:0;padding:5px;{{ selfCardCursor }}flex-shrink:0;width:40px;height:40px;box-sizing:border-box;border-radius:50%;background:transparent;">\n'
    '              <span aria-hidden="true" style="position:absolute;inset:0;border-radius:50%;background:{{ ringBg }};-webkit-mask:radial-gradient(circle closest-side,transparent calc(100% - 2px),#000 calc(100% - 2px));mask:radial-gradient(circle closest-side,transparent calc(100% - 2px),#000 calc(100% - 2px));"></span>\n'
    '              <span style="position:relative;display:block;width:30px;height:30px;border-radius:50%;overflow:hidden;background:#0C161C;box-sizing:border-box;">')

open(PATH, 'w', encoding='utf-8').write(src)
print('ok')
