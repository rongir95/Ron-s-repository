#!/usr/bin/env python3
"""Patch for the live index.html (after landscape-row.py): pages that loaded in the background (hidden) hold
their intro animations until they're shown, so the match page push-in, FanZone sliding up and the chat
pop-in used to play the moment you switched to them. Now, when a page is shown, those intro animations in its
phones are finished at once, so each phone is already where it should be (FanZone open).
   python3 tools/live/intro-still.py index.html"""
import sys
p = sys.argv[1]; s = open(p, encoding='utf-8').read()
def rep(a, b):
    global s
    if s.count(a) != 1: raise SystemExit('expected once: ' + a[:90])
    s = s.replace(a, b)
rep('''      row.querySelectorAll(".fp-set").forEach(function (x) { x.hidden = x !== el; });''',
    '''      row.querySelectorAll(".fp-set").forEach(function (x) { x.hidden = x !== el; });
      stillIntro(el);''')
rep('''  function setHTML(f) {''', '''  // finish the phones' intro animations (they wait while the page is hidden, then play when it's shown)
  var INTRO_ANIMS = ["fzPushIn", "fzOverIn", "fzMsgIn", "fzSlideUp", "fzFadeIn"];
  function stillIntro(el) {
    var t0 = Date.now();
    (function tick() {
      el.querySelectorAll("iframe").forEach(function (f) {
        try { f.contentDocument.getAnimations().forEach(function (a) { if (INTRO_ANIMS.indexOf(a.animationName) >= 0) a.finish(); }); } catch (err) {}
      });
      if (Date.now() - t0 < 900 && !el.hidden) requestAnimationFrame(tick);
    })();
  }
  function setHTML(f) {''')
open(p, 'w', encoding='utf-8').write(s); print('ok')
