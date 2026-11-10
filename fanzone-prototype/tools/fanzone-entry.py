#!/usr/bin/env python3
"""FanZone entry flow (from the product screen recording):

  Home > Watch now  -> the match page opens and FanZone opens by itself over it, under the video,
                       with a short loading spinner.
  FanZone > X       -> back to the match page, which now shows a FanZone card ("Join chat").
  FanZone card      -> opens FanZone over the match page again.

Run after merge-prototypes.py and add-poll.py:  python3 tools/fanzone-entry.py FanZone.dc.html
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

# ---------------------------------------------------------------- CSS
rep("  @keyframes fzPushIn {",
"""  /* FanZone opening over the match page */
  @keyframes fzOverIn { from { opacity: 0; transform: translateY(28px); } to { opacity: 1; transform: none; } }
  .fz-over-panel { animation: fzOverIn .38s cubic-bezier(.22,1,.36,1) both; }
  .fz-entry:hover { background: #222C31 !important; }
  @keyframes fzPushIn {""")

# ---------------------------------------------------------------- FanZone base: overlay mode
# z-order: Home 8 < match page 8 (later in the DOM) < FanZone over the match 9 < Profile 9 (later) < scrim 10 < card 20
rep('<sc-if value="{{ isFixture }}" hint-placeholder-val="{{ false }}">\n      <div style="position:absolute;inset:0;z-index:9;background:#080E12;overflow:hidden;animation:fzPushIn',
    '<sc-if value="{{ isFixture }}" hint-placeholder-val="{{ false }}">\n      <div style="position:absolute;inset:0;z-index:8;background:#080E12;overflow:hidden;animation:fzPushIn')
rep('    <!-- ===================== FANZONE BASE ===================== -->\n    <div style="position:absolute;inset:0;background:#000;overflow:hidden;">',
    '    <!-- ===================== FANZONE BASE (over the match page: only its panel shows, under the match video) ===================== -->\n    <div style="position:absolute;inset:0;overflow:hidden;{{ fzBaseStyle }}">')
rep('      <div style="position:absolute;top:0;left:0;right:0;height:54px;z-index:2;background:#000;">\n        <img src="assets/img/status-bar.svg"',
    '      <div style="position:absolute;top:0;left:0;right:0;height:54px;z-index:2;background:#000;{{ fzOwnStageStyle }}">\n        <img src="assets/img/status-bar.svg"')
rep('      <div style="position:absolute;top:54px;left:0;right:0;height:211px;z-index:2;">',
    '      <div style="position:absolute;top:54px;left:0;right:0;height:211px;z-index:2;{{ fzOwnStageStyle }}">')

# panel: opening animation + loading spinner
rep('      <div style="position:absolute;left:0;right:0;bottom:0;top:{{ fzPanelTop }}px;transition:top .55s cubic-bezier(.22,1,.36,1);background:#080E12;',
    '      <div class="{{ fzPanelCls }}" style="position:absolute;left:0;right:0;bottom:0;top:{{ fzPanelTop }}px;transition:top .55s cubic-bezier(.22,1,.36,1);pointer-events:auto;background:#080E12;')
rep('        <!-- chat feed -->\n',
'''        <!-- loading (FanZone just opened) -->
        <sc-if value="{{ fzLoading }}" hint-placeholder-val="{{ false }}">
          <div style="position:absolute;left:0;right:0;top:48px;bottom:72px;z-index:2;background:#080E12;display:flex;align-items:center;justify-content:center;" aria-label="Loading FanZone">
            <span style="width:30px;height:30px;border-radius:50%;border:2.5px solid rgba(249,250,250,.18);border-top-color:#F9FAFA;animation:fzSpin .8s linear infinite;"></span>
          </div>
        </sc-if>
        <!-- chat feed -->
''')

# ---------------------------------------------------------------- match page: FanZone card
rep('          <!-- tab system -->\n',
'''          <!-- FanZone card (shown after FanZone was closed): opens FanZone over the match again -->
          <sc-if value="{{ showFzEntry }}" hint-placeholder-val="{{ false }}">
            <div style="padding:10px 16px 2px;">
              <button class="fz-entry" onClick="{{ openFanZoneOver }}" aria-label="Open FanZone" style="width:100%;box-sizing:border-box;border:1px solid rgba(249,250,250,.12);border-radius:12px;background:#1B2326;padding:12px 14px;display:flex;flex-direction:column;gap:10px;cursor:pointer;text-align:left;font-family:'DAZN Oscine',sans-serif;animation:fzFadeIn .3s ease;">
                <span style="display:flex;align-items:center;gap:8px;">
                  <img src="assets/icons/bubbles.svg" alt="" width="18" height="21" style="display:block;">
                  <span style="font-size:15px;font-weight:700;color:#F9FAFA;">FanZone</span>
                </span>
                <span style="display:flex;align-items:center;gap:10px;width:100%;">
                  <span style="flex:1;min-width:0;height:32px;box-sizing:border-box;padding:0 12px;border-radius:10px;background:rgba(249,250,250,.12);display:flex;align-items:center;font-size:13px;color:#C5C7CA;">Join chat</span>
                  <img src="assets/img/reaction1.png" alt="" width="26" height="26" style="display:block;">
                  <img src="assets/img/reaction2.png" alt="" width="26" height="26" style="display:block;">
                  <img src="assets/img/reaction3.png" alt="" width="26" height="26" style="display:block;">
                </span>
              </button>
            </div>
          </sc-if>
          <!-- tab system -->
''')

# ---------------------------------------------------------------- logic
rep('      screen: this.P.startScreen === "FanZone" ? "fanzone" : "home", // flow entry: home -> fanzone',
    '      screen: this.P.startScreen === "FanZone" ? "fanzone" : "home", // flow entry: home -> fanzone\n'
    '      fzOver: this.P.startScreen === "FanZone", fanzoneFrom: this.P.startScreen === "FanZone" ? "fixture" : "home", fzEntrySeen: this.P.startScreen === "FanZone",')
# Watch now: match page, then FanZone opens by itself
rep('  goFixture = (e) => { if (e && e.stopPropagation) e.stopPropagation(); clearTimeout(this._homeTipTimer); this.setState({ screen: "fixture", showHomeTip: false }); };',
    '  goFixture = (e) => { if (e && e.stopPropagation) e.stopPropagation(); clearTimeout(this._homeTipTimer); this.setState({ screen: "fixture", showHomeTip: false, fzEntrySeen: false });\n'
    '    clearTimeout(this._fzAutoT); this._fzAutoT = setTimeout(() => { if (this.state.screen === "fixture" && !this.state.commentsOpen) this.openFanZoneOver(); }, 650); };\n'
    '  openFanZoneOver = (e) => {\n'
    '    if (e && e.stopPropagation) e.stopPropagation();\n'
    '    clearTimeout(this._fzLoadT);\n'
    '    this.setState({ screen: "fanzone", fanzoneFrom: "fixture", fzOver: true, fzLoading: true, fzEntrySeen: true, fzOpenN: (this.state.fzOpenN || 0) + 1 }, this.startFanZoneFtue);\n'
    '    this._fzLoadT = setTimeout(() => this.setState({ fzLoading: false }), 1300);\n'
    '  };')
rep('  backFromFixture = (e) => { if (e && e.stopPropagation) e.stopPropagation(); clearTimeout(this._fixHideT);',
    '  backFromFixture = (e) => { if (e && e.stopPropagation) e.stopPropagation(); clearTimeout(this._fixHideT); clearTimeout(this._fzAutoT); this.pollEnd(true);')
rep('      isFixture: s.screen === "fixture",',
    '      isFixture: s.screen === "fixture" || (s.screen === "fanzone" && !!s.fzOver),\n'
    '      fzBaseStyle: (s.screen === "fanzone" && s.fzOver) ? "z-index:9;background:transparent;pointer-events:none;" : "background:#000;",\n'
    '      fzOwnStageStyle: s.fzOver ? "display:none;" : "",\n'
    '      fzPanelCls: (s.screen === "fanzone" && s.fzOver) ? "fz-over-panel" : "",\n'
    '      fzLoading: !!s.fzLoading && s.screen === "fanzone",\n'
    '      showFzEntry: s.screen === "fixture" && !!s.fzEntrySeen,\n'
    '      openFanZoneOver: this.openFanZoneOver,')
# poll + panel positions follow the video bottom (match video ends at 274, FanZone's own at 265)
rep('      fzPanelTop: 273,',
    '      fzPanelTop: s.fzOver ? 282 : 273, // 8px below the stream (match video ends at 274, FanZone\'s own at 265)')
rep('  componentWillUnmount() { ', '  componentWillUnmount() { clearTimeout(this._fzAutoT); clearTimeout(this._fzLoadT); ')

open(PATH, 'w', encoding='utf-8').write(src)
print('ok')
