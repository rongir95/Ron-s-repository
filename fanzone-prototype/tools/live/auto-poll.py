#!/usr/bin/env python3
"""Patch for the live FanZone.dc.html: settings keys for the feature pages.
   poll=current|v2|v3   FanZone opens with that poll already running (and starts it again a few seconds after it ends)
   team=bayern|bvb|neutral   the team is already chosen, so Choose your team doesn't cover FanZone
Without these keys nothing changes.
   python3 tools/live/auto-poll.py FanZone.dc.html"""
import sys
p = sys.argv[1]; s = open(p, encoding='utf-8').read()
def rep(a, b):
    global s
    if s.count(a) != 1: raise SystemExit('expected once: ' + a[:90])
    s = s.replace(a, b)
rep('    if (q.get("reset") === "1") o.resetOnLoad = true;',
    '    if (q.get("reset") === "1") o.resetOnLoad = true;\n'
    '    if (["current", "v2", "v3"].indexOf(q.get("poll")) >= 0) o.autoPoll = q.get("poll");\n'
    '    if (["bayern", "bvb", "neutral"].indexOf(q.get("team")) >= 0) o.presetTeam = q.get("team");')
rep('    this._fzLoadT = setTimeout(() => this.setState(st => ({ fzLoading: false, fzChoose: !st.fzTeamPicked })), 1300);',
    '''    this._fzLoadT = setTimeout(() => {
      const P = this.P;
      this.setState(st => (P.presetTeam && !st.fzTeamPicked) ? { fzLoading: false, fzChoose: false, fzTeam: P.presetTeam, fzTeamPicked: true } : ({ fzLoading: false, fzChoose: !st.fzTeamPicked }));
      // feature pages: the poll runs by itself, and again a few seconds after it ends
      if (P.autoPoll && !this._autoPollT) {
        const go = () => { if (this.state.screen === "fanzone" && !this.state.pollOn) { this._pollKind = P.autoPoll; this.pollStart(); } };
        setTimeout(go, 500);
        this._autoPollT = setInterval(go, 4000);
      }
    }, 1300);''')
# when the prototype starts in FanZone there is no loading step: do the same right after mount
rep('  componentDidMount() {\n',
    '''  componentDidMount() {
    if (this.P.startScreen === "FanZone" && (this.P.autoPoll || this.P.presetTeam)) {
      const P = this.P;
      if (P.presetTeam) this.setState({ fzChoose: false, fzTeam: P.presetTeam, fzTeamPicked: true });
      if (P.autoPoll && !this._autoPollT) {
        const go = () => { if (this.state.screen === "fanzone" && !this.state.pollOn) { this._pollKind = P.autoPoll; this.pollStart(); } };
        setTimeout(go, 1200);
        this._autoPollT = setInterval(go, 4000);
      }
    }
''')
open(p, 'w', encoding='utf-8').write(s); print('ok')
