#!/usr/bin/env python3
"""Patch for the live FanZone.dc.html (after fixture-still.py): a prototype that opens on FanZone (start=fanzone,
every phone on the feature pages) is just there when it appears: the match page push-in, FanZone sliding up
and the chat messages popping in are finished at once on load. The feature's own animation (the poll, the
pinned image, the quiz toast...) still plays, and everything you open later animates as before.
   python3 tools/live/start-still.py FanZone.dc.html"""
import sys
p = sys.argv[1]; s = open(p, encoding='utf-8').read()
def rep(a, b):
    global s
    if s.count(a) != 1: raise SystemExit('expected once: ' + a[:90])
    s = s.replace(a, b)
rep('  componentDidMount() {', '''  componentDidMount() {
    this.skipIntro();''', )
rep('  openFanZoneOver = (e) => {', '''  // Opening on FanZone: finish the intro animations at once (match page push, FanZone slide-up, chat pop-in)
  skipIntro() {
    const q = new URLSearchParams(location.search);
    if (q.get("start") !== "fanzone" && !q.get("fp")) return;
    const INTRO = ["fzPushIn", "fzOverIn", "fzMsgIn", "fzSlideUp", "fzFadeIn"];
    const t0 = Date.now();
    const done = () => { try { document.getAnimations().forEach((a) => { if (INTRO.indexOf(a.animationName) >= 0) a.finish(); }); } catch (e) {} };
    done();
    const tick = () => { done(); if (Date.now() - t0 < 700) setTimeout(tick, 16); };
    setTimeout(tick, 0);
  }
  openFanZoneOver = (e) => {''')
open(p, 'w', encoding='utf-8').write(s); print('ok')
