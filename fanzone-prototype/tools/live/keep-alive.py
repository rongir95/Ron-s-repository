#!/usr/bin/env python3
"""Patch for the live shell (index.html), after outside-fixture.py: fast moves between feature pages.
   - Every page's phones live in their own set inside the row. Moving to another page hides the old set
     instead of throwing it away, so going back is instant.
   - Once the current page has loaded, the next and then the previous page load in the background, one at a
     time, so Next / Previous (and the arrow keys) open a page that is already loaded.
   - At most 6 pages stay loaded (the current one, its neighbours and the most recently seen); older ones are
     dropped to keep memory in check. Changing a setting or Restart reloads them.
   - Phones are always sized for three across, so a 2-phone page has the same phone size as a 3-phone page.
   python3 tools/live/keep-alive.py index.html"""
import sys
p = sys.argv[1]; s = open(p, encoding='utf-8').read()
def rep(a, b):
    global s
    if s.count(a) != 1: raise SystemExit('expected once: ' + a[:90])
    s = s.replace(a, b)
rep('  .fp-row { display: flex; align-items: flex-start; justify-content: center; gap: var(--fp-gap, 28px); }',
    '  .fp-row { display: flex; align-items: flex-start; justify-content: center; gap: var(--fp-gap, 28px); }\n'
    '  .fp-set { display: flex; align-items: flex-start; justify-content: center; gap: var(--fp-gap, 28px); }\n'
    '  .fp-set[hidden] { display: flex; position: absolute; left: -10000px; top: 0; visibility: hidden; pointer-events: none; }')
rep('''    if (!pages) { shownFeature = null; document.getElementById("fpRow").innerHTML = ""; return; }''',
    '''    if (!pages) { shownFeature = null; dropSets(); return; }''')
old_build_start = '''    if (shownFeature !== f.id) {
      shownFeature = f.id;
      var labels = f.kind === "new"'''
rep(old_build_start, '''    if (shownFeature !== f.id) {
      shownFeature = f.id;
      showSet(f);
      trimSets([f.id, prev.id, next.id]);
      preloadAfter(f, [next, prev]);
    }
    fitPages();
  }
  // ---- page sets: one per feature, kept loaded while you move around ----
  var setOrder = [];
  function dropSets() { setOrder = []; document.getElementById("fpRow").innerHTML = ""; }
  function setFor(id) { return document.querySelector('#fpRow .fp-set[data-id="' + id + '"]'); }
  function showSet(f, background) {
    var row = document.getElementById("fpRow"), el = setFor(f.id);
    if (!el) {
      el = document.createElement("div"); el.className = "fp-set"; el.setAttribute("data-id", f.id); el.hidden = true;
      el.innerHTML = setHTML(f);
      row.appendChild(el);
    }
    if (!background) {
      row.querySelectorAll(".fp-set").forEach(function (x) { x.hidden = x !== el; });
      setOrder = setOrder.filter(function (x) { return x !== f.id; }); setOrder.unshift(f.id);
    } else if (setOrder.indexOf(f.id) < 0) setOrder.push(f.id);
  }
  // neighbours load only after the page you're looking at has finished loading, one after the other
  var preloadToken = 0;
  function whenLoaded(el, cb) {
    var fr = [].slice.call(el.querySelectorAll("iframe")).filter(function (x) { return !x.classList.contains("on"); });
    if (!fr.length) { setTimeout(cb, 300); return; }
    var left = fr.length, done = false, fin = function () { if (!done && --left <= 0) { done = true; setTimeout(cb, 300); } };
    fr.forEach(function (x) { x.addEventListener("load", fin, { once: true }); });
    setTimeout(function () { if (!done) { done = true; cb(); } }, 8000);
  }
  function preloadAfter(f, list) {
    var token = ++preloadToken;
    (function step(prevEl, i) {
      if (i >= list.length) return;
      whenLoaded(prevEl, function () {
        if (token !== preloadToken || settings.view !== "pages") return;
        showSet(list[i], true);
        step(setFor(list[i].id) || prevEl, i + 1);
      });
    })(setFor(f.id), 0);
  }
  function trimSets(keep) {
    var max = 6, kept = [];
    setOrder.forEach(function (id) { if (keep.indexOf(id) >= 0 || kept.length < max) kept.push(id); else { var el = setFor(id); if (el) el.remove(); } });
    setOrder = kept;
  }
  function setHTML(f) {
    var page = PAGES[f.id];
    var labels = f.kind === "new"''')
# the old innerHTML builder becomes setHTML's return
rep('''      document.getElementById("fpRow").innerHTML = labels.map(function (l, i) {''',
    '''      return labels.map(function (l, i) {''')
rep('''                        : '<div class="fp-phone empty">' + (ph && ph.empty || 'Placeholder') + '</div>') + '</figure>';
      }).join("");
    }
    fitPages();
  }''', '''                        : '<div class="fp-phone empty">' + (ph && ph.empty || 'Placeholder') + '</div>') + '</figure>';
      }).join("");
  }''')
rep('''    var row = document.getElementById("fpRow"), n = row.children.length || 3;''',
    '''    var n = 3; // always sized for three phones, so 2- and 3-phone pages match''')
# settings changes / Restart: reload every kept page
rep('''    if (typeof paintPages === "function" && settings.view === "pages") { shownFeature = null; paintPages(); }''',
    '''    if (typeof paintPages === "function" && settings.view === "pages") { shownFeature = null; dropSets(); paintPages(); }''')
# room for a three-line "What changed" note on every page (no jump when a note wraps to three lines)
rep('min-height: 57px;', 'min-height: 78px;')
# feature-page phones use the light match video
rep('  function phoneSrc(q) { return "FanZone.dc.html?fp=" + (++loads) + "&" + query().replace(/start=\\w+/, "start=fanzone") + "&" + q; }',
    '  function phoneSrc(q) { return "FanZone.dc.html?fp=" + (++loads) + "&" + query().replace(/start=\\w+/, "start=fanzone") + "&lite=1&" + q; }')
open(p, 'w', encoding='utf-8').write(s); print('ok')
