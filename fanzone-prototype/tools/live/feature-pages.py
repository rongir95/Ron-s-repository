#!/usr/bin/env python3
"""Patch for the live shell (index.html): "Feature pages" view for FanZone 80-20.

  - A "Prototype / Feature pages" switch at the top of the side panel. Prototype is the page as it was
    (one phone, untouched). Feature pages swaps the stage for one feature at a time: phones side by side,
    left to right Current -> 80-20 -> Outside FanZone (a new feature: New -> Outside FanZone; a feature that
    only lives inside FanZone: two screens), and a "What changed" line under them.
  - The panel lists the features from the plan (FanZone 80-20, backlog of 26-Nov-2026) in two groups:
    Improvements and New. Pages not built yet show empty phone frames.
  - Settings keys: view=proto|pages, feature=<id>, notes=1|0 (the "What changed" line). They are kept in
    the panel's saved settings like the others, so the Current prototype never changes.
  - Live moments, Settings and Things to try keep working in both views.

   python3 tools/live/feature-pages.py index.html
"""
import json, sys
p = sys.argv[1]; s = open(p, encoding='utf-8').read()
def rep(a, b):
    global s
    if s.count(a) != 1: raise SystemExit('expected once: ' + a[:90])
    s = s.replace(a, b)

# Features from the plan's backlog. screens: 3 = Current, 80-20, Outside; 2 = Current, 80-20 (inside FanZone only);
# new features: New, Outside.
FEATURES = [
  ("poll", "Poll", "Activations", "imp", 3), ("quiz", "Quiz", "Activations", "imp", 3),
  ("pinned", "Pinned messages (Images)", "Activations", "imp", 3), ("battle", "Fan battle", "Activations", "imp", 3),
  ("eb", "Engagement break (EB)", "Activations", "imp", 3), ("landscape", "Landscape activations", "Activations", "imp", 3),
  ("smart", "Smart component for activations", "Activations", "imp", 3),
  ("team", "Choose your team (by my favorite team)", "Chat", "imp", 3), ("reactions", "Reactions", "Chat", "imp", 2),
  ("leaderboard", "Leaderboard", "Chat", "imp", 3), ("mute", "FanZone blockers & Mute", "Chat", "imp", 3),
  ("sending", "Message sending", "Chat", "imp", 2), ("actions", "Actions on messages in FanZone", "Chat", "imp", 3),
  ("stats", "Stats and scores inside FanZone", "Chat", "imp", 3),
  ("fzbutton", "FanZone button on fixture", "General", "imp", 3), ("drawers", "Drawers alignment and navigation", "General", "imp", 3),
  ("report", "Align report drawers", "General", "imp", 3), ("browser", "In-app browser", "General", "imp", 3),
  ("haptic", "Haptic", "General", "imp", 3), ("predictions", "Predictions + Leaderboard", "General", "imp", 3),
  ("drawertab", "FanZone as a drawer/tab", "General", "imp", 3),
  ("export", "Exporting FanZone activations and assets to DAZN", "General", "imp", 3),
  ("onboarding", "Align with the new Onboarding", "General", "imp", 3),
  ("achievements", "Achievements", "Extras", "new", 2), ("liveupdates", "Live updates for the current event", "Extras", "new", 2),
  ("alerts", "Alerts on all DAZN", "Extras", "new", 2),
]
FJSON = json.dumps([{"id": a, "name": b, "cat": c, "kind": d, "screens": e} for a, b, c, d, e in FEATURES])

CSS = '''
  /* ---------- Feature pages (FanZone 80-20) ---------- */
  .view-seg { margin-top: -8px; }
  .fp-nav { display: flex; flex-direction: column; gap: 14px; }
  .fp-nav[hidden] { display: none; }
  .fp-group { display: flex; flex-direction: column; gap: 2px; }
  .fp-group .label { margin-bottom: 6px; }
  .fp-item { display: flex; align-items: center; gap: 8px; width: 100%; border: 0; background: transparent; border-radius: 8px; padding: 7px 10px; text-align: left; font-size: 13px; font-weight: 600; color: var(--muted); cursor: pointer; }
  .fp-item:hover { color: var(--text); background: var(--surface); }
  .fp-item[aria-current="page"] { color: var(--text); background: var(--raise); box-shadow: inset 0 0 0 1px var(--line-strong); }
  .fp-item .st { margin-left: auto; flex-shrink: 0; font-size: 10.5px; font-weight: 600; color: var(--muted); }
  .fp-item .st.ready { color: var(--text); }
  .fpage { position: absolute; inset: 0; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 20px; padding: 28px 24px 24px; overflow: auto; }
  .fpage[hidden] { display: none; }
  .fp-head { text-align: center; display: flex; flex-direction: column; gap: 4px; }
  .fp-head .fp-cat { font-size: 11px; font-weight: 700; letter-spacing: .08em; text-transform: uppercase; color: var(--muted); }
  .fp-head h2 { margin: 0; font-size: 24px; font-weight: 800; letter-spacing: -.01em; }
  .fp-row { display: flex; align-items: flex-start; justify-content: center; gap: var(--fp-gap, 28px); }
  .fp-col { display: flex; flex-direction: column; align-items: center; gap: 12px; margin: 0; }
  .fp-col figcaption { display: flex; flex-direction: column; align-items: center; gap: 4px; }
  .fp-chip { font-size: 12px; font-weight: 700; padding: 4px 12px; border-radius: 999px; border: 1px solid var(--line-strong); color: var(--text); white-space: nowrap; }
  .fp-chip.hl { background: var(--primary); color: var(--on-primary); border-color: transparent; }
  .fp-phone { position: relative; flex: none; width: calc(375px * var(--fs, .6)); height: calc(812px * var(--fs, .6)); border-radius: calc(46px * var(--fs, .6)); overflow: hidden; background: #000; box-shadow: 0 0 0 calc(9px * var(--fs, .6)) var(--bezel), 0 0 0 calc(11px * var(--fs, .6)) #2c2c31, 0 30px 70px rgba(0, 0, 0, .5); }
  .fp-phone iframe { position: absolute; left: 0; top: 0; width: 375px; height: 812px; border: 0; zoom: var(--fs, .6); display: block; background: #000; }
  @supports not (zoom: 2) { .fp-phone iframe { zoom: normal; transform-origin: 0 0; transform: scale(var(--fs, .6)); } }
  .fp-phone.empty { background: var(--stage); box-shadow: inset 0 0 0 1.5px var(--line-strong); display: flex; align-items: center; justify-content: center; text-align: center; padding: 16px; color: var(--muted); font-size: 13px; }
  .fp-phone.empty::before { content: ""; position: absolute; inset: 10px; border-radius: calc(40px * var(--fs, .6)); border: 1.5px dashed var(--line-strong); }
  .fp-note { margin: 0; max-width: 680px; text-align: center; font-size: 14px; color: var(--muted); border-top: 1px solid var(--line); padding-top: 14px; }
  .fp-note b { color: var(--text); }
  .fp-note[hidden] { display: none; }
  body[data-view="pages"] .device, body[data-view="pages"] .stage-restart { display: none; }
  @media (max-width: 860px) {
    .fpage { justify-content: flex-start; padding: 16px; }
    .fp-row { overflow-x: auto; max-width: 100%; justify-content: flex-start; padding-bottom: 8px; }
  }
'''
rep('  @media (max-width: 860px) {\n    .shell {', CSS + '  @media (max-width: 860px) {\n    .shell {')

# the feature page lives in the stage, next to the single phone
rep('''    <div class="device" id="device">
      <iframe id="app" title="FanZone app prototype" allow="autoplay; fullscreen"></iframe>
    </div>
  </main>''', '''    <div class="device" id="device">
      <iframe id="app" title="FanZone app prototype" allow="autoplay; fullscreen"></iframe>
    </div>
    <section class="fpage" id="fpage" aria-labelledby="fpTitle" hidden>
      <div class="fp-head"><span class="fp-cat" id="fpCat"></span><h2 id="fpTitle"></h2></div>
      <div class="fp-row" id="fpRow"></div>
      <p class="fp-note" id="fpNote"></p>
    </section>
  </main>''')

# view switch + feature list at the top of the panel
rep('''    <div class="live">
      <span class="label">Live moments</span>''', '''    <div class="seg view-seg" role="group" aria-label="View" data-key="view">
      <button type="button" data-val="proto">Prototype<small>one phone</small></button>
      <button type="button" data-val="pages">Feature pages<small>FanZone 80-20</small></button>
    </div>

    <nav class="fp-nav" id="fpNav" aria-label="Features" hidden></nav>

    <div class="live">
      <span class="label">Live moments</span>''')

# "What changed" switch, in Settings
rep('''    <div class="group">
      <span class="label"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="4" width="18" height="16" rx="2.5"/><path d="M3 9.5h18"/><path d="M7 6.8h4"/></svg>FanZone header</span>''',
'''    <div class="group">
      <span class="label"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="2.5" y="5" width="6" height="14" rx="1.5"/><rect x="9" y="5" width="6" height="14" rx="1.5"/><rect x="15.5" y="5" width="6" height="14" rx="1.5"/></svg>Feature pages</span>
      <div class="switches">
        <div class="switch-row">
          <span class="switch-text" id="l-notes">"What changed" line<small>The note under the phones on every feature page</small></span>
          <button type="button" class="switch" role="switch" aria-checked="true" aria-labelledby="l-notes" data-key="notes"><span class="knob"></span></button>
        </div>
      </div>
    </div>

    <div class="group">
      <span class="label"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="4" width="18" height="16" rx="2.5"/><path d="M3 9.5h18"/><path d="M7 6.8h4"/></svg>FanZone header</span>''')

rep('var DEFAULTS = { start: "home", profile: "empty", card: "D", following: "1", hometip: "0", fancardtip: "0", sponsor: "0", light: "0", tenure: "since" };',
    'var DEFAULTS = { start: "home", profile: "empty", card: "D", following: "1", hometip: "0", fancardtip: "0", sponsor: "0", light: "0", tenure: "since", view: "proto", feature: "poll", notes: "1" };')

# the view switch and the notes switch don't reload the prototype
rep('''      settings[g.getAttribute("data-key")] = b.getAttribute("data-val");
      try { localStorage.setItem(KEY, JSON.stringify(settings)); } catch (err) {}
      paint();
      load();''', '''      settings[g.getAttribute("data-key")] = b.getAttribute("data-val");
      try { localStorage.setItem(KEY, JSON.stringify(settings)); } catch (err) {}
      paint();
      if (g.getAttribute("data-key") === "view") { paintPages(); return; }
      load();''')
rep('''      if (k === "light") {''', '''      if (k === "notes") { paintPages(); return; }
      if (k === "light") {''')

JS = '''
  // ---------- Feature pages (FanZone 80-20) ----------
  var FEATURES = ''' + FJSON + ''';
  // pages that are built: the phones (src = settings query for that phone) and the "What changed" line
  var PAGES = {};
  var fpNav = document.getElementById("fpNav"), fpage = document.getElementById("fpage");
  function buildNav() {
    var groups = [["imp", "Improvements"], ["new", "New"]];
    fpNav.innerHTML = groups.map(function (g) {
      return '<div class="fp-group"><span class="label">' + g[1] + '</span>' + FEATURES.filter(function (f) { return f.kind === g[0]; }).map(function (f) {
        return '<button type="button" class="fp-item" data-id="' + f.id + '">' + f.name + '<span class="st' + (PAGES[f.id] ? ' ready' : '') + '">' + (PAGES[f.id] ? 'Ready' : 'Soon') + '</span></button>';
      }).join("") + '</div>';
    }).join("");
  }
  fpNav.addEventListener("click", function (e) {
    var b = e.target.closest(".fp-item"); if (!b) return;
    settings.feature = b.getAttribute("data-id");
    try { localStorage.setItem(KEY, JSON.stringify(settings)); } catch (err) {}
    paintPages(); setOpen(false);
  });
  var shownFeature = null;
  function paintPages() {
    var pages = settings.view === "pages";
    document.body.setAttribute("data-view", pages ? "pages" : "proto");
    fpNav.hidden = !pages; fpage.hidden = !pages;
    if (!pages) { shownFeature = null; document.getElementById("fpRow").innerHTML = ""; return; }
    var f = FEATURES.filter(function (x) { return x.id === settings.feature; })[0] || FEATURES[0];
    fpNav.querySelectorAll(".fp-item").forEach(function (b) { if (b.getAttribute("data-id") === f.id) b.setAttribute("aria-current", "page"); else b.removeAttribute("aria-current"); });
    var page = PAGES[f.id];
    document.getElementById("fpCat").textContent = f.cat + (f.kind === "new" ? " · New" : " · Improvement");
    document.getElementById("fpTitle").textContent = f.name;
    var note = document.getElementById("fpNote");
    note.innerHTML = page && page.note ? page.note : '<b>What changed:</b> this page isn\\'t built yet.';
    note.hidden = settings.notes !== "1";
    if (shownFeature !== f.id) {
      shownFeature = f.id;
      var labels = f.kind === "new" ? ["New", "Outside FanZone"] : (f.screens === 2 ? ["Current", "80-20"] : ["Current", "80-20", "Outside FanZone"]);
      document.getElementById("fpRow").innerHTML = labels.map(function (l, i) {
        var ph = page && page.phones && page.phones[i];
        return '<figure class="fp-col"><figcaption><span class="fp-chip' + (i === 1 || f.kind === "new" && i === 0 ? ' hl' : '') + '">' + (ph && ph.label || l) + '</span></figcaption>' +
          (ph && ph.src ? '<div class="fp-phone"><iframe title="' + f.name + ': ' + l + '" allow="autoplay; fullscreen" src="' + ph.src + '"></iframe></div>'
                        : '<div class="fp-phone empty">' + (ph && ph.empty || 'Placeholder') + '</div>') + '</figure>';
      }).join("");
    }
    fitPages();
  }
  function fitPages() {
    if (settings.view !== "pages") return;
    var row = document.getElementById("fpRow"), n = row.children.length || 3;
    var narrow = !window.matchMedia("(min-width: 861px)").matches;
    var w = stage.clientWidth - 48, h = stage.clientHeight - 56 - 40 - 32 - (settings.notes === "1" ? 70 : 0);
    var gap = 28, s = Math.min((w - gap * (n - 1) - n * 22) / (n * 375), (h - 30) / 812);
    if (narrow) s = Math.min(0.62, (stage.clientHeight - 200) / 812);
    s = Math.max(0.3, Math.min(s, 0.9));
    fpage.style.setProperty("--fs", s.toFixed(4));
  }
  window.addEventListener("resize", fitPages);
'''
rep('''  paint();
  fit();
  load();
})();''', JS + '''
  paint();
  fit();
  load();
  buildNav();
  paintPages();
})();''')
open(p, 'w', encoding='utf-8').write(s); print('ok')
