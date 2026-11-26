#!/usr/bin/env python3
"""Patch for the live index.html (after coded-screens.py):
 - Hide slides: the row menu has "Hide slide" / "Show slide". A hidden slide leaves the slide order (Prev / Next and
   the count skip it) and is listed greyed in its own "Hidden" group at the bottom of the side list; a click on a
   hidden row opens its menu. Kept in this browser (localStorage "fz-hidden-slides"); "Align with the new Onboarding"
   is hidden by default.
 - FanZone button on fixture: "Outside - Stats and scores" is now the Scores screen built in code
   (screens.html?v=scores) instead of the still image.
 - Engagement break: no Outside phone (Current and 80-20 only).
   python3 tools/live/hide-slides.py index.html"""
import sys
p = sys.argv[1]; s = open(p, encoding='utf-8').read()
def rep(a, b):
    global s
    if s.count(a) != 1: raise SystemExit('expected once: ' + a[:90])
    s = s.replace(a, b)
rep('''  FEATURES.forEach(function (f) { if (NAMES[f.id]) f.name = NAMES[f.id]; });''', '''  FEATURES.forEach(function (f) { if (NAMES[f.id]) f.name = NAMES[f.id]; });
  // ---- hidden slides (kept, listed in their own group, out of the slide order) ----
  var DEFAULT_HIDDEN = ["onboarding"];
  var HIDDEN_SL = {}; try { HIDDEN_SL = JSON.parse(localStorage.getItem("fz-hidden-slides") || "{}") || {}; } catch (err) {}
  function isHid(id) { return HIDDEN_SL[id] != null ? !!HIDDEN_SL[id] : DEFAULT_HIDDEN.indexOf(id) >= 0; }
  var HIDDEN_FEATS = [];
  for (var hs = FEATURES.length - 1; hs >= 0; hs--) if (isHid(FEATURES[hs].id)) HIDDEN_FEATS.unshift(FEATURES.splice(hs, 1)[0]);
  function saveHid(id, on) {
    if (on === (DEFAULT_HIDDEN.indexOf(id) >= 0)) delete HIDDEN_SL[id]; else HIDDEN_SL[id] = on;
    try { localStorage.setItem("fz-hidden-slides", JSON.stringify(HIDDEN_SL)); } catch (err) {}
  }
  function hideSlide(id) {
    var i = FEATURES.findIndex(function (q) { return q.id === id; }); if (i < 0) return;
    var f = FEATURES.splice(i, 1)[0]; HIDDEN_FEATS.push(f); saveHid(id, true);
    var el = setFor(id); if (el) el.remove();
    setOrder = setOrder.filter(function (x) { return x !== id; });
    if (settings.feature === id) { settings.feature = FEATURES[Math.min(i, FEATURES.length - 1)].id; try { localStorage.setItem(KEY, JSON.stringify(settings)); } catch (err) {} }
    shownFeature = null; buildNav(); paintPages();
  }
  function showSlide(id) {
    var i = HIDDEN_FEATS.findIndex(function (q) { return q.id === id; }); if (i < 0) return;
    var f = HIDDEN_FEATS.splice(i, 1)[0]; saveHid(id, false);
    var d = FEATURES_DEFAULT.indexOf(id);
    var at = FEATURES.findIndex(function (q) { return !q.section && q.kind === f.kind && FEATURES_DEFAULT.indexOf(q.id) > d; });
    if (at < 0) { at = -1; FEATURES.forEach(function (q, k) { if (q.kind === f.kind) at = k + 1; }); if (at < 0) at = FEATURES.length; }
    FEATURES.splice(at, 0, f); placeSections();
    buildNav(); paintPages();
  }''')
rep('''    }).join("") + '<div class="fp-reorder"><span>Drag a feature to reorder</span>''',
    '''    }).join("") + (HIDDEN_FEATS.length ? '<div class="fp-group fp-hid-group"><span class="label">Hidden</span>' + HIDDEN_FEATS.map(function (f) {
      return '<button type="button" class="fp-item is-hid" data-id="' + f.id + '" data-cat="' + f.cat + '" title="Hidden slide: click for options"><span class="fp-ic"><svg viewBox="0 0 24 24" aria-hidden="true"><use href="#fpi-' + (FP_ICON[f.id] || 'poll') + '"/></svg></span><span class="nm">' + f.name + '</span><span class="fp-more" role="button" aria-label="More for ' + f.name + '" title="More">&#8943;</span></button>';
    }).join("") + '</div>' : '') + '<div class="fp-reorder"><span>Drag a feature to reorder</span>''')
rep('''    var f = FEATURES.filter(function (q) { return q.id === id; })[0]; if (!f) return;''',
    '''    var f = FEATURES.filter(function (q) { return q.id === id; })[0] || HIDDEN_FEATS.filter(function (q) { return q.id === id; })[0]; if (!f) return;
    var hidNow = HIDDEN_FEATS.indexOf(f) >= 0;''')
rep('''+ '<div class="fp-menu-sep"></div><button type="button" role="menuitem" data-act="rename">''',
    '''+ '<div class="fp-menu-sep"></div><button type="button" role="menuitem" data-act="hide"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' + (hidNow ? '<path d="M2 12s3.6-7 10-7 10 7 10 7-3.6 7-10 7-10-7-10-7Z"/><circle cx="12" cy="12" r="3"/>' : '<path d="M3 3l18 18M10.6 5.1A10.6 10.6 0 0 1 12 5c6.4 0 10 7 10 7a17.5 17.5 0 0 1-2.9 3.9M6.6 6.6A17.3 17.3 0 0 0 2 12s3.6 7 10 7a9.7 9.7 0 0 0 5.4-1.6M9.9 9.9a3 3 0 0 0 4.2 4.2"/>') + '</svg>' + (hidNow ? 'Show slide' : 'Hide slide') + '</button><button type="button" role="menuitem" data-act="rename">''')
rep('''    rowMenu.querySelector('[data-act="rename"]').addEventListener("click", function () { closeRowMenu(); renameDialog(f); });''',
    '''    rowMenu.querySelector('[data-act="rename"]').addEventListener("click", function () { closeRowMenu(); renameDialog(f); });
    rowMenu.querySelector('[data-act="hide"]').addEventListener("click", function () { closeRowMenu(); if (hidNow) showSlide(f.id); else hideSlide(f.id); });''')
rep('''    var b = e.target.closest(".fp-item"); if (!b) return;
    settings.feature = b.getAttribute("data-id");''', '''    var b = e.target.closest(".fp-item"); if (!b) return;
    if (b.classList.contains("is-hid")) { var rr = b.getBoundingClientRect(); openRowMenu(b.getAttribute("data-id"), rr.right - 8, rr.bottom + 4, true); return; }
    settings.feature = b.getAttribute("data-id");''')
rep('''  function deleteFeature(id) {
    var i = FEATURES.findIndex(function (q) { return q.id === id; }); if (i < 0) return;''', '''  function deleteFeature(id) {
    var hi = HIDDEN_FEATS.findIndex(function (q) { return q.id === id; });
    if (hi >= 0) { HIDDEN_FEATS.splice(hi, 1); if (HIDDEN.indexOf(id) < 0) HIDDEN.push(id); try { localStorage.setItem("fz-hidden", JSON.stringify(HIDDEN)); } catch (err) {} buildNav(); return; }
    var i = FEATURES.findIndex(function (q) { return q.id === id; }); if (i < 0) return;''')
rep('''    var b = e.target.closest(".fp-item"); if (!b || e.button !== 0 || e.pointerType === "touch") return;''',
    '''    var b = e.target.closest(".fp-item"); if (!b || b.classList.contains("is-hid") || e.button !== 0 || e.pointerType === "touch") return;''')
rep('''  .fp-menu-sep {''', '''  .fp-item.is-hid { opacity: .5; }
  .fp-item.is-hid:hover { opacity: .8; }
  .fp-hid-group { margin-top: 6px; padding-top: 12px; border-top: 1px dashed var(--line-strong); }
  .fp-menu-sep {''')
# Scores screen in code; EB without Outside
rep('''{ img: "assets/screens/scores-outside.png", label: "Outside - Stats and scores" }''', '''{ src: "screens.html?v=scores", label: "Outside - Stats and scores" }''')
rep('{"id": "eb", "name": "Engagement break (EB)", "cat": "Activations", "kind": "imp", "screens": 3}', '{"id": "eb", "name": "Engagement break (EB)", "cat": "Activations", "kind": "imp", "screens": 2}')
rep('''PAGES.eb = { phones: [cur("moment=eb&team=bayern"), later, out]''', '''PAGES.eb = { phones: [cur("moment=eb&team=bayern"), later]''')
open(p, 'w', encoding='utf-8').write(s); print('ok')
