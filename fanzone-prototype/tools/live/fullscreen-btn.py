#!/usr/bin/env python3
"""Patch for the live index.html: a full-screen button in the slide's bottom bar (next to Restart). It puts the whole
presentation into browser full screen, like a slideshow; the shell panel hides while in full screen. Press it again or Esc to exit.
   python3 tools/live/fullscreen-btn.py index.html"""
import sys
p = sys.argv[1]; s = open(p, encoding='utf-8').read()
def rep(a, b):
    global s
    if s.count(a) != 1: raise SystemExit('expected once: ' + a[:90])
    s = s.replace(a, b)
EXP = '<svg class="fs-in" width="14" height="14" viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="M2.5 6V2.5H6M10 2.5h3.5V6M13.5 10v3.5H10M6 13.5H2.5V10" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>'
COL = '<svg class="fs-out" width="14" height="14" viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="M6 2.5V6H2.5M13.5 6H10V2.5M10 13.5V10h3.5M2.5 10H6v3.5" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>'
rep('''stroke-linecap="round" stroke-linejoin="round"/></svg></button></span>''',
    '''stroke-linecap="round" stroke-linejoin="round"/></svg></button><button type="button" class="fp-refresh fp-fs" id="fpFull" aria-label="Full screen" title="Full screen (F)">''' + EXP + COL + '''</button></span>''')
rep('''  .fp-refresh:hover, .fp-refresh:focus-visible { color: var(--text); background: var(--raise); }''',
    '''  .fp-refresh:hover, .fp-refresh:focus-visible { color: var(--text); background: var(--raise); }
  .fp-fs svg { display: block; } .fp-fs .fs-out { display: none; }
  body.is-fs .fp-fs .fs-in { display: none; } body.is-fs .fp-fs .fs-out { display: block; }
  body.is-fs .rail, body.is-fs .panel-open, body.is-fs .panel-btn { display: none !important; }
  body.is-fs .shell { grid-template-columns: minmax(0, 1fr) 0 !important; }
  body.is-fs .fp-top { padding-right: 0 !important; }''')
rep('''  document.getElementById("allRefresh").addEventListener("click", function () { location.reload(); });''',
    '''  document.getElementById("allRefresh").addEventListener("click", function () { location.reload(); });
  // full screen, like presenting slides
  (function () {
    var d = document, root = d.documentElement, btn = d.getElementById("fpFull");
    function isFs() { return !!(d.fullscreenElement || d.webkitFullscreenElement); }
    function sync() { var on = isFs(); d.body.classList.toggle("is-fs", on); btn.setAttribute("aria-label", on ? "Exit full screen" : "Full screen"); btn.title = on ? "Exit full screen (F)" : "Full screen (F)"; setTimeout(function () { window.dispatchEvent(new Event("resize")); }, 60); }
    function toggle() {
      try {
        if (isFs()) (d.exitFullscreen || d.webkitExitFullscreen).call(d);
        else { var r = (root.requestFullscreen || root.webkitRequestFullscreen).call(root); if (r && r.catch) r.catch(function () { btn.title = "Your browser blocked full screen here. Open the page in its own tab and try again."; }); }
      } catch (e) {}
    }
    btn.addEventListener("click", toggle);
    d.addEventListener("fullscreenchange", sync); d.addEventListener("webkitfullscreenchange", sync);
    d.addEventListener("keydown", function (e) { var t = e.target && e.target.tagName; if ((e.key === "f" || e.key === "F") && !e.metaKey && !e.ctrlKey && !e.altKey && t !== "INPUT" && t !== "TEXTAREA") toggle(); });
  })();''')
open(p, 'w', encoding='utf-8').write(s); print('ok')
