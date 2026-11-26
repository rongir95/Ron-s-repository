#!/usr/bin/env python3
"""Patch for the live FanZone.dc.html (after eb-video.py): the EB comes in a few seconds after FanZone opens,
sliding up over the chat, and its video really plays (the runtime doesn't set `muted`, so the browser blocked
autoplay; now it's muted and started from code). After the X, on the feature page (moment=eb) it comes back
after a few seconds so the page keeps showing it.
   python3 tools/live/eb-enter.py FanZone.dc.html"""
import sys
p = sys.argv[1]; s = open(p, encoding='utf-8').read()
def rep(a, b):
    global s
    if s.count(a) != 1: raise SystemExit('expected once: ' + a[:90])
    s = s.replace(a, b)
rep('  @keyframes fzPushIn {', '  @keyframes fzEbIn { from { transform: translateY(100%); } to { transform: translateY(0); } }\n  @keyframes fzPushIn {')
rep('''<div role="dialog" aria-label="Engagement break" style="position:absolute;left:0;right:0;top:48px;bottom:0;z-index:30;overflow:hidden;background:#080E12;animation:fzFadeIn .3s ease;">''',
    '''<div role="dialog" aria-label="Engagement break" style="position:absolute;left:0;right:0;top:48px;bottom:0;z-index:30;overflow:hidden;background:#080E12;animation:fzEbIn .5s cubic-bezier(.2,.8,.2,1);">''')
rep('''        else if (m === "eb") this.setState({ ebOn: true });''', '''        else if (m === "eb") this.ebSoon(3000);''')
rep('''ebClose: () => this.setState({ ebOn: false }),''',
    '''ebClose: () => { this.setState({ ebOn: false }); if (new URLSearchParams(location.search).get("moment") === "eb") this.ebSoon(5000); },''')
rep('  openFanZoneOver = (e) => {', '''  // Engagement break: comes in after a delay and plays its video (muted, started from code)
  ebSoon(ms) {
    clearTimeout(this._ebT);
    this._ebT = setTimeout(() => {
      if (this.state.screen !== "fanzone") { this.ebSoon(1500); return; }
      this.setState({ ebOn: true }, () => this.ebPlay());
    }, ms);
  }
  ebPlay(n) {
    const v = document.querySelector('[aria-label="Engagement break"] video');
    if (!v) { if ((n || 0) < 20) setTimeout(() => this.ebPlay((n || 0) + 1), 50); return; }
    v.muted = true; v.defaultMuted = true; v.setAttribute("muted", "");
    try { v.currentTime = 0; } catch (e) {}
    const pr = v.play(); if (pr && pr.catch) pr.catch(() => {});
  }
  openFanZoneOver = (e) => {''')
open(p, 'w', encoding='utf-8').write(s); print('ok')
