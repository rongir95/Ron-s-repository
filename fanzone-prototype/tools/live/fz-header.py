#!/usr/bin/env python3
"""Patch for the live FanZone.dc.html (after eb-delay.py): the regular FanZone header per Figma FanZone 80-20
"Live chat header" (a38ncus4fbwkPfnlFQIUPt 1:40888): 48px, #1B2326, 12px top corners, a 1px light line on top
(drop shadow 0 -1px rgba(249,250,250,.2)) and no shadow under it. Left 12px: minimize icon 20px, 16px gap, the
FanZone logotype (66x24, assets/icons/fz-logotype.svg exported from Figma). Right 16px: leaderboard 32px, divider
(10px / 15px around it), close 20px (assets/icons/fz-leaderboard.svg, fz-close.svg). Same layout as the sponsor header.
   python3 tools/live/fz-header.py FanZone.dc.html"""
import sys
p = sys.argv[1]; s = open(p, encoding='utf-8').read()
start = s.find('        <div onPointerDown="{{ fzHeadDown }}" style="touch-action:none;position:relative;z-index:3;flex-shrink:0;height:48px;display:flex;align-items:center;gap:16px;padding:0 20px 0 16px;background:#1B2326;')
if start < 0 or s.count('padding:0 20px 0 16px;background:#1B2326;') != 1: raise SystemExit('regular header not found')
end = s.find('        </div>\n        </sc-if>', start)
if end < 0: raise SystemExit('header end not found')
end += len('        </div>\n')
new = '''        <div onPointerDown="{{ fzHeadDown }}" style="touch-action:none;position:relative;z-index:3;flex-shrink:0;height:48px;box-sizing:border-box;background:#1B2326;border-radius:12px 12px 0 0;box-shadow:0 -1px 0 rgba(249,250,250,.2);">
          <button class="fz-collapse-btn" onClick="{{ toggleFzCollapse }}" aria-label="{{ fzCollapseLabel }}" aria-expanded="{{ fzExpandedAttr }}" style="position:absolute;left:12px;top:50%;transform:translateY(-50%);display:flex;align-items:center;gap:16px;border:0;padding:0;background:transparent;cursor:pointer;">
            <svg width="20" height="20" viewBox="0 0 20 20" fill="none" aria-hidden="true" style="display:block;flex-shrink:0;transform:rotate({{ fzCollapseRot }}deg);transition:transform .3s ease;">
              <path d="M17 6L3 6" stroke="#F9FAFA" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"></path>
              <path d="M14.6665 15.6667L9.99984 11L5.33317 15.6667" stroke="#F9FAFA" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"></path>
            </svg>
            <img src="assets/icons/fz-logotype.svg" alt="FanZone" width="66" height="24" style="display:block;flex-shrink:0;">
          </button>
          <div style="position:absolute;right:16px;top:0;bottom:0;display:flex;align-items:center;">
            <button onClick="{{ toggleLeaderboard }}" aria-label="Leaderboard" aria-pressed="{{ lbPressed }}" title="Leaderboard" style="width:32px;height:32px;border:0;padding:0;border-radius:999px;background:{{ lbBtnBg }};cursor:pointer;display:block;transition:background .2s ease;"><img src="assets/icons/fz-leaderboard.svg" alt="" width="32" height="32" style="display:block;{{ lbIconStyle }}"></button>
            <span aria-hidden="true" style="width:1px;height:17px;margin:0 15px 0 10px;background:rgba(249,250,250,.6);"></span>
            <button onClick="{{ goHome }}" aria-label="Close FanZone" title="Close FanZone" style="width:20px;height:20px;border:0;padding:0;background:transparent;cursor:pointer;display:block;"><img src="assets/icons/fz-close.svg" alt="" width="20" height="20" style="display:block;"></button>
          </div>
        </div>
'''
s = s[:start] + new + s[end:]
open(p, 'w', encoding='utf-8').write(s); print('ok')
