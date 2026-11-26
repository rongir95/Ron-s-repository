#!/usr/bin/env python3
"""Patch for the live index.html (after landscape-pages.py): the side panel can be collapsed on desktop.
A button next to the FanZone title hides the panel and the stage takes the whole width; a round button at the
top right of the stage brings it back. Remembered in this browser (localStorage "fz-panel").
   python3 tools/live/panel-collapse.py index.html"""
import sys
p = sys.argv[1]; s = open(p, encoding='utf-8').read()
def rep(a, b):
    global s
    if s.count(a) != 1: raise SystemExit('expected once: ' + a[:90])
    s = s.replace(a, b)
ICON_IN = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="2"/><path d="M15 3v18"/><path d="m8 9 3 3-3 3"/></svg>'
ICON_OUT = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="2"/><path d="M15 3v18"/><path d="m11 9-3 3 3 3"/></svg>'
rep('''  @media (prefers-reduced-motion: reduce) { * { transition: none !important; } }''',
'''  .panel-btn { display: none; }
  @media (min-width: 861px) {
    .panel-btn { display: flex; align-items: center; justify-content: center; width: 36px; height: 36px; padding: 0; border: 1px solid var(--line-strong); border-radius: 10px; background: var(--surface); color: var(--text); cursor: pointer; flex: none; }
    .panel-btn:hover, .panel-btn:focus-visible { background: var(--raise); }
    .brand h1 .panel-btn { margin-left: auto; width: 32px; height: 32px; }
    .panel-open { position: absolute; top: 20px; right: 20px; z-index: 3; border-radius: 50%; }
    body:not([data-panel="closed"]) .panel-open { display: none; }
    body[data-panel="closed"] .shell { grid-template-columns: minmax(0, 1fr) 0; }
    body[data-panel="closed"] .rail { display: none; }
    body[data-panel="closed"] .stage-restart { right: 64px; }
  }
  @media (prefers-reduced-motion: reduce) { * { transition: none !important; } }''')
rep('''      <h1><img src="assets/icons/fanzone-mark.svg" alt="" width="30" height="30">FanZone</h1>''',
    '''      <h1><img src="assets/icons/fanzone-mark.svg" alt="" width="30" height="30">FanZone<button type="button" class="panel-btn" id="panelClose" aria-label="Collapse the panel" title="Collapse the panel">''' + ICON_IN + '''</button></h1>''')
rep('''    <div class="device" id="device">''',
    '''    <button type="button" class="panel-btn panel-open" id="panelOpen" aria-label="Show the panel" title="Show the panel">''' + ICON_OUT + '''</button>
    <div class="device" id="device">''')
rep('''  paint();
  fit();
  load();''', '''  // collapse / show the side panel (desktop)
  function setPanel(closed) {
    if (closed) document.body.setAttribute("data-panel", "closed"); else document.body.removeAttribute("data-panel");
    try { localStorage.setItem("fz-panel", closed ? "closed" : "open"); } catch (err) {}
    window.dispatchEvent(new Event("resize"));
  }
  document.getElementById("panelClose").addEventListener("click", function () { setPanel(true); document.getElementById("panelOpen").focus(); });
  document.getElementById("panelOpen").addEventListener("click", function () { setPanel(false); document.getElementById("panelClose").focus(); });
  try { if (localStorage.getItem("fz-panel") === "closed") document.body.setAttribute("data-panel", "closed"); } catch (err) {}

  paint();
  fit();
  load();''')
# the Portrait/Landscape row under the title takes ~36px: keep the page inside the stage height
rep('var w = stage.clientWidth - 48, h = stage.clientHeight - 56 - 40 - 32 - (settings.notes === "1" ? 70 : 0);',
    'var w = stage.clientWidth - 48, h = stage.clientHeight - 56 - 40 - 32 - 36 - (settings.notes === "1" ? 70 : 0);')
open(p, 'w', encoding='utf-8').write(s); print('ok')
