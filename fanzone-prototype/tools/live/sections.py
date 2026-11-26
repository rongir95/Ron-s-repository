#!/usr/bin/env python3
"""Patch for the live index.html (after deck-light.py):
 - Section slides, like the deck's "Trading tools" slides: "FanZone 80-20" opens the 80-20 group and "FanZone New"
   opens the New group (a huge centred title with the yellow highlight, and a line under it). They sit in the
   slide order (Prev / Next / count) and the group names in the side list open them. Dragging features keeps
   each section at the head of its group.
 - Haptic is removed from the feature pages.
   python3 tools/live/sections.py index.html"""
import sys
p = sys.argv[1]; s = open(p, encoding='utf-8').read()
def rep(a, b):
    global s
    if s.count(a) != 1: raise SystemExit('expected once: ' + a[:90])
    s = s.replace(a, b)
rep('{"id": "haptic", "name": "Haptic", "cat": "General", "kind": "imp", "screens": 3}, ', '')
rep('''  function pageStatus(id) {''', '''  // ---- section slides ----
  var SECTIONS = {
    imp: { id: "sec-8020", name: "FanZone 80-20", cat: "", kind: "imp", section: true, title: 'FanZone <em>80-20</em>', sub: "Improvements to FanZone" },
    "new": { id: "sec-new", name: "FanZone New", cat: "", kind: "new", section: true, title: 'FanZone <em>New</em>', sub: "New features" }
  };
  function placeSections() {
    for (var i = FEATURES.length - 1; i >= 0; i--) if (FEATURES[i].section) FEATURES.splice(i, 1);
    FEATURES.unshift(SECTIONS.imp);
    var j = FEATURES.findIndex(function (f) { return f.kind === "new"; });
    FEATURES.splice(j < 0 ? FEATURES.length : j, 0, SECTIONS["new"]);
  }
  placeSections();
  var applyOrderBase = applyOrder;
  applyOrder = function (ids) { applyOrderBase(ids); placeSections(); };
  function pageStatus(id) {''')
rep('''FEATURES.sort(function (a, b) { return FEATURES_DEFAULT.indexOf(a.id) - FEATURES_DEFAULT.indexOf(b.id); });''',
    '''FEATURES.sort(function (a, b) { return FEATURES_DEFAULT.indexOf(a.id) - FEATURES_DEFAULT.indexOf(b.id); }); placeSections();''')
# side list: features only; the group name opens its section slide
rep('''      return '<div class="fp-group"><span class="label">' + g[1] + '</span>' + FEATURES.filter(function (f) { return f.kind === g[0]; }).map(function (f) {''',
    '''      return '<div class="fp-group"><button type="button" class="label fp-sec" data-id="' + SECTIONS[g[0]].id + '" title="Open the ' + g[1] + ' section slide">' + g[1] + '</button>' + FEATURES.filter(function (f) { return f.kind === g[0] && !f.section; }).map(function (f) {''')
rep('''    if (dragJustEnded) { e.preventDefault(); return; }''', '''    if (dragJustEnded) { e.preventDefault(); return; }
    var sb = e.target.closest(".fp-sec");
    if (sb) { settings.feature = sb.getAttribute("data-id"); try { localStorage.setItem(KEY, JSON.stringify(settings)); } catch (err) {} paintPages(); setOpen(false); return; }''')
rep('''    var page = PAGES[f.id];
    document.getElementById("fpCat")''', '''    var page = PAGES[f.id];
    fpage.setAttribute("data-sec", f.section ? "1" : "0");
    fpNav.querySelectorAll(".fp-sec").forEach(function (b) { if (b.getAttribute("data-id") === f.id) b.setAttribute("aria-current", "page"); else b.removeAttribute("aria-current"); });
    document.getElementById("fpCat")''')
rep('''  function setHTML(f) {
    var page = PAGES[f.id];''', '''  function setHTML(f) {
    var page = PAGES[f.id];
    if (f.section) {
      var cnt = FEATURES.filter(function (x) { return x.kind === f.kind && !x.section; }).length;
      return '<div class="fp-section"><h1>' + f.title + '</h1><p>' + f.sub + ' · ' + cnt + ' features</p></div>';
    }''')
rep('''  .fp-foot { position: absolute;''', '''  .fpage[data-sec="1"] .fp-top { visibility: hidden; }
  .fp-section { text-align: center; font-family: "Inter", "Helvetica Neue", Helvetica, Arial, sans-serif; }
  .fp-section h1 { margin: 0; font-size: clamp(56px, 7.5vw, 104px); font-weight: 700; letter-spacing: -0.035em; line-height: 1; color: #111; }
  .fp-section h1 em { font-style: normal; background: linear-gradient(transparent 70%, var(--hl) 70%); padding: 0 4px; }
  .fp-section p { margin: 18px 0 0; font-size: 18px; color: var(--muted); }
  .fp-group .fp-sec { border: 0; background: transparent; padding: 2px 6px; margin: 0 0 6px -6px; border-radius: 6px; cursor: pointer; text-align: left; align-self: flex-start; font: inherit; font-size: 11px; font-weight: 700; letter-spacing: .08em; text-transform: uppercase; color: var(--muted); }
  .fp-group .fp-sec:hover { color: var(--text); background: var(--surface); }
  .fp-group .fp-sec[aria-current="page"] { color: #111; background: var(--hl); }
  .fp-foot { position: absolute;''')
open(p, 'w', encoding='utf-8').write(s); print('ok')
