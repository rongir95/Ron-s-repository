#!/usr/bin/env python3
"""Patch for the live index.html (after shown-msg.py): no white flash while a phone loads. Each phone stays hidden
until the prototype inside has actually drawn (the FanZone app root, or the landscape stage); meanwhile the phone
shows a small loader on the dark screen. Then it appears with a short fade.
   python3 tools/live/phone-loader.py index.html"""
import sys
p = sys.argv[1]; s = open(p, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    if s.count(a) != n: raise SystemExit('expected %d: %s' % (n, a[:90]))
    s = s.replace(a, b)
rep('''  .fp-phone { box-sizing: border-box; }''', '''  .fp-phone { box-sizing: border-box; }
  .fp-phone:not(.empty) { background: #0C161C; }
  .fp-phone:not(.empty)::before { content: ""; position: absolute; left: 50%; top: 50%; width: 26px; height: 26px; margin: -13px 0 0 -13px; border-radius: 50%; border: 2.5px solid rgba(249, 250, 250, .12); border-top-color: rgba(249, 250, 250, .7); animation: fpSpin .8s linear infinite; }
  @keyframes fpSpin { to { transform: rotate(360deg); } }
  .fp-phone iframe { visibility: hidden; opacity: 0; }
  .fp-phone iframe.ready { visibility: visible; opacity: 1; transition: opacity .2s ease; }''')
rep('''onload="this.classList.add(\\'on\\')"''', '''onload="this.classList.add(\\'on\\'); fpReady(this)"''', 2)
rep('''  function setHTML(f) {''', '''  // a phone shows once the prototype inside has drawn (not on the browser's blank white page)
  window.fpReady = function (fr) {
    var t0 = Date.now();
    (function check() {
      var d = null; try { d = fr.contentDocument; } catch (err) {}
      var ok = d && d.querySelector("[data-fz-root], .stage");
      if (ok || Date.now() - t0 > 8000) { fr.classList.add("ready"); return; }
      setTimeout(check, 60);
    })();
  };
  function setHTML(f) {''')
open(p, 'w', encoding='utf-8').write(s); print('ok')
