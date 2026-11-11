#!/usr/bin/env python3
""""Choose your team" when you enter FanZone, per FanZone DS (file NIgPxOlNU4U3sWMRdoE4Qh, node 12521:41534),
with the two teams of the match on screen: Bayern München and Borussia Dortmund.

  - After the FanZone loading spinner, the panel covers the chat until you choose. It comes back on the
    next entry until you have chosen (a team or Go neutral).
  - Tap a team: a check appears on its tile and the panel closes. If you have no favorite team yet, the
    team becomes your favorite, so your ring takes its color.
  - Go neutral or X: closes it without a team.
  - The "Change team" button at the end of the message bar opens it again.

Layout from Figma (panel under the 48px header): radial background #191970 -> #0C161C (from the Figma gradient
transform: centre 50.1% / 45.2%, radii 263 x 253px), FanZone logo 71x56
at the top, 32px close button, title 18px bold, two 100x100 tiles (radius 22) with "VS" between them, team
names 16px bold, tiles in the DS colours (Light red #F40101, yellow #F4CE00), "Go neutral" button 127x40 (white 20%, radius 7.3).

Run after the other scripts:  python3 tools/fanzone-team.py FanZone.dc.html
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

TILE = ('position:relative;width:100px;height:100px;border-radius:22px;overflow:hidden;box-sizing:border-box;'
        'border:2px solid rgba(255,255,255,.12);display:flex;align-items:center;justify-content:center;'
        # the DS tile pattern: a lighter band over the top, a darker one at the bottom
        'background:radial-gradient(130% 55% at 15% -8%,rgba(0,0,0,.04) 0 50%,transparent 51%),'
        'radial-gradient(140% 60% at 90% 112%,rgba(0,0,0,.1) 0 50%,transparent 51%),{bg};')
CHECK = ('<sc-if value="{{ t.picked }}" hint-placeholder-val="{{ false }}"><span style="position:absolute;left:38px;top:88px;width:24px;height:24px;border-radius:50%;'
         'background:#F9FAFA;display:flex;align-items:center;justify-content:center;box-shadow:0 2px 6px rgba(0,0,0,.35);animation:fzRxPop .25s cubic-bezier(.22,1.6,.36,1);">'
         '<svg width="14" height="14" viewBox="0 0 14 14" fill="none" aria-hidden="true"><path d="M2.5 7.3l3 3 6-6.6" stroke="#080E12" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg></span></sc-if>')

PANEL = '''        <!-- Choose your team (FanZone DS 12521:41534) -->
        <sc-if value="{{ fzChoose }}" hint-placeholder-val="{{ false }}">
          <div role="dialog" aria-label="Choose your team" style="position:absolute;left:0;right:0;top:48px;bottom:0;z-index:6;overflow:hidden;background:radial-gradient(263px 253px at 50.1% 45.2%,#191970 0%,#0C161C 100%);animation:fzFadeIn .3s ease;">
            <img src="assets/icons/fanzone-logo.svg" alt="FanZone" width="71" height="56" style="position:absolute;left:151px;top:24px;display:block;">
            <button onClick="{{ fzGoNeutral }}" aria-label="Close" title="Close" style="position:absolute;right:12px;top:12px;width:32px;height:32px;border:0;padding:0;border-radius:9999px;background:rgba(255,255,255,.2);display:flex;align-items:center;justify-content:center;cursor:pointer;"><svg width="20" height="20" viewBox="0 0 20 20" fill="none" aria-hidden="true" style="display:block;"><path d="M5 5L15 15M15 5L5 15" stroke="#F9FAFA" stroke-width="1.6" stroke-linecap="round"></path></svg></button>
            <div style="position:absolute;left:0;right:0;top:{{ fzChooseTop }}px;display:flex;flex-direction:column;align-items:center;">
              <div style="font-family:'DAZN Oscine',sans-serif;font-weight:700;font-size:18px;line-height:25px;color:#F9FAFA;">Choose your team</div>
              <div style="margin-top:16px;display:flex;align-items:flex-start;gap:20px;">
                <sc-for list="{{ fzTeams }}" as="t" hint-placeholder-count="2">
                  <div style="display:flex;align-items:flex-start;gap:20px;">
                    <sc-if value="{{ t.second }}" hint-placeholder-val="{{ false }}"><span style="width:15px;margin-top:38px;font-family:'DAZN Oscine',sans-serif;font-weight:800;font-size:12px;line-height:24px;color:#FFFFFF;text-align:center;">VS</span></sc-if>
                    <button onClick="{{ t.pick }}" aria-label="{{ t.name }}" style="position:relative;width:100px;border:0;padding:0;background:transparent;cursor:pointer;display:flex;flex-direction:column;align-items:center;gap:15px;">
                      <span style="{{ t.tileStyle }}"><img src="{{ t.crest }}" alt="" width="64" height="64" style="display:block;filter:drop-shadow(0 2px 4px rgba(0,0,0,.25));"></span>
                      ''' + CHECK + '''
                      <span style="font-family:'DAZN Oscine',sans-serif;font-weight:700;font-size:16px;line-height:1;color:#FFFFFF;white-space:nowrap;">{{ t.name }}</span>
                    </button>
                  </div>
                </sc-for>
              </div>
              <button onClick="{{ fzGoNeutral }}" style="margin-top:58px;width:127px;height:40px;border:0;border-radius:7.3px;background:rgba(255,255,255,.2);font-family:'DAZN Oscine',sans-serif;font-weight:700;font-size:14px;color:#F9FAFA;cursor:pointer;">Go neutral</button>
            </div>
          </div>
        </sc-if>
'''
rep('        <!-- chat feed -->\n', PANEL + '        <!-- chat feed -->\n')

rep('  @keyframes fzPushIn {', '  @keyframes fzFadeIn { from { opacity: 0; } to { opacity: 1; } }\n  @keyframes fzPushIn {')

# after the FanZone loading spinner: choose your team until you have
rep('    this._fzLoadT = setTimeout(() => this.setState({ fzLoading: false }), 1300);',
    '    this._fzLoadT = setTimeout(() => this.setState(st => ({ fzLoading: false, fzChoose: !st.fzTeamPicked })), 1300);')

# the "Change team" button in the message bar opens it again
rep('<button aria-label="Change team" style="', '<button onClick="{{ openTeamChooser }}" aria-label="Change team" style="')

LOGIC = '''  // Choose your team (FanZone DS 12521:41534)
  pickFzTeam = (id) => {
    clearTimeout(this._fzTeamT);
    this.setState(st => ({ fzTeam: id, fzTeamPicked: true, favoriteId: st.favoriteId || id }));
    this._fzTeamT = setTimeout(() => this.setState({ fzChoose: false }), 650);
  };
  fzGoNeutral = () => { clearTimeout(this._fzTeamT); this.setState({ fzTeam: "neutral", fzTeamPicked: true, fzChoose: false }); };
  openTeamChooser = (e) => { if (e && e.stopPropagation) e.stopPropagation(); this.setState({ fzChoose: true }); };
  fzTeamVals() {
    const s = this.state;
    const T = [
      { id: "bayern", name: "Bayern München", crest: "assets/vec/tiles/img-logo-bayern.svg", bg: "#F40101" },
      { id: "bvb", name: "Dortmund", crest: "assets/poll/logo-bvb.png", bg: "#F4CE00" },
    ];
    return {
      fzChoose: !!s.fzChoose && s.screen === "fanzone" && !s.fzLoading,
      fzChooseTop: 159,
      fzGoNeutral: this.fzGoNeutral, openTeamChooser: this.openTeamChooser,
      fzTeams: T.map((t, i) => ({ ...t, second: i > 0, picked: s.fzTeam === t.id, pick: () => this.pickFzTeam(t.id),
        tileStyle: TILE_STYLE.replace("{bg}", t.bg) })),
    };
  }
  openFanZoneOver = (e) => {'''
rep('  openFanZoneOver = (e) => {', LOGIC)
rep('      ...this.gzVals(),', '      ...this.gzVals(),\n      ...this.fzTeamVals(),')
rep('// FanZone chat: which team each fan supports', '// Choose your team tile (FanZone DS)\nconst TILE_STYLE = ' + repr(TILE) + ';\n// FanZone chat: which team each fan supports')

open(PATH, 'w', encoding='utf-8').write(src)
print('ok')
