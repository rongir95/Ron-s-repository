#!/usr/bin/env python3
"""Pinned image in FanZone, started from the prototype shell like the poll and the quiz
(FanZone DS, file NIgPxOlNU4U3sWMRdoE4Qh: closed node 12304:59996, open node 12304:60712).

  Closed (64px): host row (avatar, name, yellow "Host" tag, yellow pin), one line of text, 77x48 thumbnail.
  Open (289px):  host row, the image 351x197 (radius 8, 1px white 20% border, link button bottom-right),
                 two lines of text, a collapse button. Tap the closed bar to open it.

The image in Figma is a bitmap; here the banner is built in HTML/CSS (stadium-light gradients, DAZN logo
SVG, title text) so it stays vector. Icons (pin, link, collapse) are SVGs from Figma in assets/pinned/.

With a poll running, the poll sits under the pinned image (starting a poll closes an open pinned image;
opening the pinned image collapses the poll).

Run after the other scripts:  python3 tools/fanzone-pinned.py FanZone.dc.html
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

FONT = "font-family:'DAZN Oscine',sans-serif;"
TEXT = "Welcome to the Klassiker FanZone! Be kind, back your team and join the live polls and quizzes."

def banner(scale_style=''):
    # 351x197 banner: dark red stadium, two floodlights, pitch, DAZN logo, title
    return ('<div style="position:absolute;left:0;top:0;width:351px;height:197px;' + scale_style +
            'background:radial-gradient(60% 55% at 50% 38%,#7A0A1C 0%,rgba(122,10,28,0) 100%),'
            'radial-gradient(22% 30% at 12% 16%,rgba(255,255,255,.55) 0%,rgba(255,255,255,0) 100%),'
            'radial-gradient(22% 30% at 88% 16%,rgba(255,255,255,.55) 0%,rgba(255,255,255,0) 100%),'
            'linear-gradient(180deg,#1A0508 0%,#3A0710 55%,#160406 100%);overflow:hidden;">'
            '<div style="position:absolute;left:-10%;right:-10%;bottom:-38px;height:80px;border-radius:50% 50% 0 0;'
            'background:linear-gradient(180deg,#3E8E2E 0%,#1D5216 100%);box-shadow:0 -6px 24px rgba(120,200,90,.25);"></div>'
            '<div style="position:absolute;left:0;right:0;top:22px;display:flex;justify-content:center;align-items:center;gap:10px;">'
            '<img src="assets/icons/dazn-logo.svg" alt="DAZN" width="34" height="34" style="display:block;">'
            '<span style="width:1px;height:28px;background:rgba(255,255,255,.6);"></span>'
            '<span style="' + FONT + 'font-weight:800;font-size:15px;letter-spacing:.06em;color:#FFFFFF;">FANZONE</span></div>'
            '<div style="position:absolute;left:0;right:0;top:70px;text-align:center;' + FONT + 'font-weight:800;font-size:38px;line-height:40px;color:#FFFFFF;'
            'text-shadow:0 3px 0 rgba(0,0,0,.35);">Welcome to<br>FanZone!</div></div>')

HOST = ('<div style="display:flex;align-items:center;gap:6px;height:24px;">'
        '<span style="width:24px;height:24px;border-radius:50%;flex-shrink:0;box-sizing:border-box;border:1.5px solid transparent;padding:1.5px;'
        'background:linear-gradient(#242D33,#242D33) padding-box,#F7FF1A border-box;">'
        '<span style="display:flex;align-items:center;justify-content:center;width:18px;height:18px;border-radius:50%;background:#080E12;color:#F9FAFA;font-weight:700;font-size:11px;">R</span></span>'
        '<span style="font-weight:700;font-size:14px;color:#F9FAFA;">Reut</span>'
        '<span style="padding:2px 6px;border-radius:999px;background:rgba(255,250,0,.2);color:#FFFA00;font-weight:700;font-size:12px;line-height:13px;">Host</span>'
        '<span style="flex:1;"></span><img src="assets/pinned/pin.svg" alt="Pinned" width="24" height="24" style="display:block;"></div>')

PANEL = '''        <!-- Pinned image (FanZone DS 12304:59996 closed, 12304:60712 open) -->
        <sc-if value="{{ pinOn }}" hint-placeholder-val="{{ false }}">
          <div style="position:absolute;left:0;right:0;top:48px;z-index:5;background:#242D33;border-bottom:1px solid rgba(255,255,255,.2);animation:pinIn .35s cubic-bezier(.22,1,.36,1);''' + FONT + '''">
            <sc-if value="{{ pinClosed }}" hint-placeholder-val="{{ true }}">
              <button onClick="{{ pinOpen }}" aria-label="Open the pinned message" style="display:flex;gap:8px;width:100%;height:64px;box-sizing:border-box;padding:8px 12px;border:0;background:transparent;cursor:pointer;text-align:left;''' + FONT + '''">
                <span style="flex:1;min-width:0;display:flex;flex-direction:column;gap:4px;">''' + HOST + '''
                  <span style="font-size:14px;line-height:20px;color:#F9FAFA;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">''' + TEXT + '''</span>
                </span>
                <span style="position:relative;width:77px;height:48px;flex-shrink:0;border-radius:8px;overflow:hidden;background:#3D4549;">''' + banner('transform:translate(-50%,-50%) scale(.2437);left:50%;top:50%;transform-origin:center;') + '''</span>
              </button>
            </sc-if>
            <sc-if value="{{ pinExpanded }}" hint-placeholder-val="{{ false }}">
              <div style="padding:8px 12px;">''' + HOST + '''
                <div style="position:relative;margin-top:6px;width:351px;height:197px;box-sizing:border-box;border-radius:8px;overflow:hidden;border:1px solid rgba(255,255,255,.2);background:#080E12;">''' + banner() + '''
                  <span style="position:absolute;right:8px;bottom:8px;width:32px;height:32px;border-radius:8px;background:rgba(8,14,18,.64);display:flex;align-items:center;justify-content:center;"><img src="assets/pinned/link.svg" alt="Open link" width="24" height="24" style="display:block;"></span>
                </div>
                <div style="position:relative;margin-top:6px;min-height:40px;padding-right:32px;font-size:14px;line-height:20px;color:#F9FAFA;">''' + TEXT + '''
                  <button onClick="{{ pinClose }}" aria-label="Collapse the pinned message" style="position:absolute;right:0;bottom:0;width:24px;height:24px;border:0;padding:0;background:transparent;cursor:pointer;"><img src="assets/pinned/collapse.svg" alt="" width="24" height="24" style="display:block;"></button>
                </div>
              </div>
            </sc-if>
          </div>
        </sc-if>
'''
rep('        <!-- chat feed -->\n', PANEL + '        <!-- chat feed -->\n')
rep('  @keyframes fzPushIn {', '  @keyframes pinIn { from { opacity: 0; } to { opacity: 1; } }\n  @keyframes fzPushIn {')

LOGIC = '''  // Pinned image (from the shell)
  pinVals() {
    const s = this.state;
    const on = !!s.pinOn && s.screen === "fanzone";
    return { pinOn: on, pinClosed: on && !s.pinExpanded, pinExpanded: on && !!s.pinExpanded,
      pinOpen: () => this.setState({ pinExpanded: true, pollCollapsed: true }), pinClose: () => this.setState({ pinExpanded: false }) };
  }
  openFanZoneOver = (e) => {'''
rep('  openFanZoneOver = (e) => {', LOGIC)
rep('      ...this.gzVals(),', '      ...this.gzVals(),\n      ...this.pinVals(),')
rep('      if (d && d.fz === "quiz")', '      if (d && d.fz === "pin") { this.setState({ pinOn: !!d.on, pinExpanded: false }); return; }\n      if (d && d.fz === "quiz")')
rep('+ "|" + (s.qzPhase ? "quiz" : "-");', '+ "|" + (s.qzPhase ? "quiz" : "-") + "|" + (s.pinOn ? "pin" : "-");')
rep('quiz: !!s.qzPhase }, "*");', 'quiz: !!s.qzPhase, pin: !!s.pinOn }, "*");')

# Poll + pinned image: the poll comes in under the pinned image. Starting a poll closes an open pinned image;
# if you open the pinned image again, the poll moves down under it.
rep('<div style="position:absolute;left:0;right:0;top:48px;z-index:2;height:{{ pollClipH }}px;',
    '<div style="position:absolute;left:0;right:0;top:{{ pollTop }}px;z-index:2;height:{{ pollClipH }}px;')
rep('height:{{ pollClipH }}px;overflow:hidden;pointer-events:none;transition:opacity .25s ease;', 'height:{{ pollClipH }}px;overflow:hidden;pointer-events:none;transition:opacity .25s ease,top .3s cubic-bezier(.22,1,.36,1);')
rep('      if (d.on) this.pollStart(); else this.pollEnd();',
    '      if (d.on) { if (this.state.pinExpanded) this.setState({ pinExpanded: false }); this.pollStart(); } else this.pollEnd();')
rep("    return { pinOn: on,", "    return { pollTop: on ? (s.pinExpanded ? 48 + 289 : 48 + 64) : 48, pinOn: on,")

open(PATH, 'w', encoding='utf-8').write(src)
print('ok')
