#!/usr/bin/env python3
"""FanZone panel options:
  - Collapse / expand: the icon (or the title) in the panel header slides the panel down to just
    its header bar, so the match page shows; tapping it again brings the panel back.
  - The "Meet your Fan Card" tip in FanZone and the "Let's make a unique fan profile" tip on Home
    are off by default; the shell turns them on (?fancardtip=1, ?hometip=1).

Run after fanzone-entry.py:  python3 tools/fanzone-panel.py FanZone.dc.html
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

# the opening animation must not hold the transform, so the collapse transform can apply after it
rep("  .fz-over-panel { animation: fzOverIn .38s cubic-bezier(.22,1,.36,1) both; }",
    "  .fz-over-panel { animation: fzOverIn .38s cubic-bezier(.22,1,.36,1) backwards; }\n"
    "  .fz-collapse-btn:focus-visible { outline: 2px solid #F9FAFA; outline-offset: 2px; border-radius: 6px; }")

# panel: slides down to its header when collapsed
rep('<div class="{{ fzPanelCls }}" style="position:absolute;left:0;right:0;bottom:0;top:{{ fzPanelTop }}px;transition:top .55s cubic-bezier(.22,1,.36,1);pointer-events:auto;',
    '<div class="{{ fzPanelCls }}" style="position:absolute;left:0;right:0;bottom:0;top:{{ fzPanelTop }}px;transform:{{ fzPanelTransform }};transition:top .55s cubic-bezier(.22,1,.36,1),transform .45s cubic-bezier(.22,1,.36,1);pointer-events:auto;')

# header: the collapse icon + title become one button
rep('''          <svg width="20" height="20" viewBox="0 0 20 20" fill="none" style="flex-shrink:0;">
            <path d="M17 6H3" stroke="#F9FAFA" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"></path>
            <path d="M14.667 15.667L10 11L5.333 15.667" stroke="#F9FAFA" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"></path>
          </svg>
          <span style="font-size:17px;font-weight:700;letter-spacing:-.01em;color:#F9FAFA;">FanZone</span>''',
'''          <button class="fz-collapse-btn" onClick="{{ toggleFzCollapse }}" aria-label="{{ fzCollapseLabel }}" aria-expanded="{{ fzExpandedAttr }}" style="display:flex;align-items:center;gap:16px;border:0;padding:8px 6px;margin:-8px -6px;background:transparent;cursor:pointer;font-family:inherit;">
            <svg width="20" height="20" viewBox="0 0 20 20" fill="none" aria-hidden="true" style="flex-shrink:0;transform:rotate({{ fzCollapseRot }}deg);transition:transform .3s ease;">
              <path d="M17 6H3" stroke="#F9FAFA" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"></path>
              <path d="M14.667 15.667L10 11L5.333 15.667" stroke="#F9FAFA" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"></path>
            </svg>
            <span style="font-size:17px;font-weight:700;letter-spacing:-.01em;color:#F9FAFA;">FanZone</span>
          </button>''')

# state + values
rep('    this.setState({ screen: "fanzone", fanzoneFrom: "fixture", fzOver: true, fzLoading: true,',
    '    this.setState({ screen: "fanzone", fanzoneFrom: "fixture", fzOver: true, fzLoading: true, fzCollapsed: false,')
rep('      openFanZoneOver: this.openFanZoneOver,',
    '      openFanZoneOver: this.openFanZoneOver,\n'
    '      fzPanelTransform: s.fzCollapsed ? "translateY(calc(100% - 68px))" : "none",\n'
    '      toggleFzCollapse: () => this.setState({ fzCollapsed: !s.fzCollapsed, showFtue: false }),\n'
    '      fzCollapseLabel: s.fzCollapsed ? "Expand FanZone" : "Collapse FanZone",\n'
    '      fzExpandedAttr: s.fzCollapsed ? "false" : "true",\n'
    '      fzCollapseRot: s.fzCollapsed ? 180 : 0,')

# "Meet your Fan Card" tip: off unless the shell turns it on
rep('  startFanZoneFtue = () => {\n    clearTimeout(this._ftueTimer);\n',
    '  startFanZoneFtue = () => {\n    clearTimeout(this._ftueTimer);\n    if (this.P.fanCardTip !== true) return; // off by default; the prototype shell can turn it on\n')
rep('    if (q.get("reset") === "1") o.resetOnLoad = true;',
    '    if (q.get("reset") === "1") o.resetOnLoad = true;\n    if (q.get("fancardtip") === "1") o.fanCardTip = true;')

# "Let's make a unique fan profile" tip on Home: off unless the shell turns it on (?hometip=1)
rep('      this._homeTipTimer = setTimeout(() => { if (!this.state.sheet && this.state.screen === "home") this.setState({ showHomeTip: true }); }, 2000);',
    '      if (this.P.homeTip === true) this._homeTipTimer = setTimeout(() => { if (!this.state.sheet && this.state.screen === "home") this.setState({ showHomeTip: true }); }, 2000);')
rep('    if (q.get("fancardtip") === "1") o.fanCardTip = true;',
    '    if (q.get("fancardtip") === "1") o.fanCardTip = true;\n    if (q.get("hometip") === "1") o.homeTip = true;')

open(PATH, 'w', encoding='utf-8').write(src)
print('ok')
