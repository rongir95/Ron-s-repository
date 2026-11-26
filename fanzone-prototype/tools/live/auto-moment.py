#!/usr/bin/env python3
"""Patch for the live FanZone.dc.html (after auto-poll.py): one more settings key for the feature pages.
   moment=quiz|pin|battle|leaderboard|team   when the prototype starts in FanZone, that live moment opens by itself
   (quiz, pinned image and fan battle as if started from the panel; leaderboard as if the trophy was tapped; team opens Choose your team).
Without the key nothing changes.
   python3 tools/live/auto-moment.py FanZone.dc.html"""
import sys
p = sys.argv[1]; s = open(p, encoding='utf-8').read()
def rep(a, b):
    global s
    if s.count(a) != 1: raise SystemExit('expected once: ' + a[:90])
    s = s.replace(a, b)
rep('    if (["bayern", "bvb", "neutral"].indexOf(q.get("team")) >= 0) o.presetTeam = q.get("team");',
    '    if (["bayern", "bvb", "neutral"].indexOf(q.get("team")) >= 0) o.presetTeam = q.get("team");\n'
    '    if (["quiz", "pin", "battle", "leaderboard", "team"].indexOf(q.get("moment")) >= 0) o.autoMoment = q.get("moment");')
rep('    if (this.P.startScreen === "FanZone" && (this.P.autoPoll || this.P.presetTeam)) {',
    '''    if (this.P.startScreen === "FanZone" && this.P.autoMoment) {
      const m = this.P.autoMoment;
      setTimeout(() => {
        if (this.state.screen !== "fanzone") return;
        if (m === "leaderboard") this.openLeaderboard(false);
        else if (m === "team") this.setState({ fzChoose: true });
        else if (this._onShellMsg) this._onShellMsg({ data: { fz: m, on: true } });
      }, 1200);
    }
    if (this.P.startScreen === "FanZone" && (this.P.autoPoll || this.P.presetTeam)) {''')
open(p, 'w', encoding='utf-8').write(s); print('ok')
