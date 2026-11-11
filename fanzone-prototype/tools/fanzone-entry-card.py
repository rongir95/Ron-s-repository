#!/usr/bin/env python3
"""The FanZone card on the match page, per FanZone DS "fan-zone" (file NIgPxOlNU4U3sWMRdoE4Qh, node 12521:28566):
343x76, radius 18, #0C161C with a 1px #3D4549 border; the FanZone mark (SVG from Figma) and "FanZone" 14px bold;
a "Join chat" field (215x24, radius 10, #242D33, 1px #3D4549, 12px #B3B9BB) and three 36px reactions.
The reactions are animated bitmaps (lottie) in Figma; the prototype's reaction images stand in for them.

Run after fanzone-entry.py:  python3 tools/fanzone-entry-card.py FanZone.dc.html
"""
import re, sys

PATH = sys.argv[1]
src = open(PATH, encoding='utf-8').read()
m = re.search(r'            <div style="padding:10px 16px 2px;">\n              <button class="fz-entry" onClick="\{\{ openFanZoneOver \}\}".*?</button>\n            </div>', src, re.S)
if not m:
    raise SystemExit('FanZone card not found')
CARD = '''            <div style="padding:16px 16px 4px;">
              <button class="fz-entry" onClick="{{ openFanZoneOver }}" aria-label="Open FanZone" style="position:relative;display:block;width:343px;height:76px;box-sizing:border-box;border:1px solid #3D4549;border-radius:18px;background:#0C161C;padding:0;cursor:pointer;text-align:left;font-family:'DAZN Oscine',sans-serif;">
                <span style="position:absolute;left:12px;top:8px;display:flex;align-items:center;gap:4px;">
                  <img src="assets/icons/fanzone-mark.svg" alt="" width="24" height="24" style="display:block;">
                  <span style="font-size:14px;font-weight:700;line-height:20px;color:#F9FAFA;">FanZone</span>
                </span>
                <span style="position:absolute;left:12px;top:40px;width:215px;height:24px;box-sizing:border-box;padding:0 12px;border:1px solid #3D4549;border-radius:10px;background:#242D33;display:flex;align-items:center;font-size:12px;color:#B3B9BB;">Join chat</span>
                <span style="position:absolute;left:235px;top:34px;display:flex;gap:0;">
                  <img src="assets/img/reaction1.png" alt="" width="36" height="36" style="display:block;object-fit:contain;">
                  <img src="assets/img/reaction2.png" alt="" width="36" height="36" style="display:block;object-fit:contain;margin-left:-4px;">
                  <img src="assets/img/reaction3.png" alt="" width="36" height="36" style="display:block;object-fit:contain;margin-left:-4px;">
                </span>
              </button>
            </div>'''
src = src[:m.start()] + CARD + src[m.end():]
open(PATH, 'w', encoding='utf-8').write(src)
print('ok')
