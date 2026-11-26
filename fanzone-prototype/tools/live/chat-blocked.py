#!/usr/bin/env python3
"""Patch for the live FanZone.dc.html (after typing-moment.py): the blocked-chat state per Figma FanZone 80-20
(a38ncus4fbwkPfnlFQIUPt 14:64611, bar 14:66136). moment=blocked replaces the message bar with the "Chat disabled"
bar: 82px, 16px sides, 48px alert icon (#FD7777, assets/icons/fz-alert.svg), 8px gap, "Chat disabled (Can be from
earlier activity)" Oscine Bold 14 #FD7777, then "Read our Community guidelines to understand why." Oscine 15/20
#F9FAFA with "Community guidelines" underlined in #70C8FF.
   python3 tools/live/chat-blocked.py FanZone.dc.html"""
import sys
p = sys.argv[1]; s = open(p, encoding='utf-8').read()
def rep(a, b):
    global s
    if s.count(a) != 1: raise SystemExit('expected once: ' + a[:90])
    s = s.replace(a, b)
BAR = '''        <!-- chat disabled (Figma FanZone 80-20 14:66136): replaces the message bar while you are blocked -->
        <sc-if value="{{ fzBlocked }}" hint-placeholder-val="{{ false }}">
          <div role="status" style="flex-shrink:0;display:flex;align-items:center;gap:8px;height:82px;padding:0 16px;box-sizing:border-box;background:#0C161C;font-family:'DAZN Oscine',sans-serif;">
            <img src="assets/icons/fz-alert.svg" alt="" width="48" height="48" style="display:block;flex-shrink:0;">
            <div style="display:flex;flex-direction:column;gap:4px;min-width:0;">
              <div style="font-weight:700;font-size:14px;line-height:1;color:#FD7777;white-space:nowrap;">Chat disabled (Can be from earlier activity)</div>
              <div style="font-size:15px;line-height:20px;color:#F9FAFA;width:239px;">Read our <span style="color:#70C8FF;text-decoration:underline;cursor:pointer;">Community guidelines</span> to understand why.</div>
            </div>
          </div>
        </sc-if>
        <!-- message bar -->
'''
rep('''        <!-- message bar -->\n''', BAR)
rep('''<div data-fz-msgbar="1" class="{{ fzBarCls }}" style="position:relative;display:flex;align-items:center;gap:12px;padding:8px 0;height:72px;box-sizing:border-box;background:#0C161C;">''',
    '''<div data-fz-msgbar="1" class="{{ fzBarCls }}" style="position:relative;display:flex;align-items:center;gap:12px;padding:8px 0;height:72px;box-sizing:border-box;background:#0C161C;{{ fzBarHide }}">''')
rep('      ...this.gzVals(),', '      ...this.gzVals(),\n      fzBlocked: !!this.state.fzBlocked, fzBarHide: this.state.fzBlocked ? "display:none;" : "",')
rep('"eb", "typing"].indexOf(q.get("moment"))', '"eb", "typing", "blocked"].indexOf(q.get("moment"))')
rep('''        else if (m === "typing") this.fzTypeOn();''', '''        else if (m === "typing") this.fzTypeOn();
        else if (m === "blocked") this.setState({ fzBlocked: true });''')
open(p, 'w', encoding='utf-8').write(s); print('ok')
