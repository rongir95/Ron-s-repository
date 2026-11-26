#!/usr/bin/env python3
"""Patch for the live shell (index.html), after current-pages.py: move between the feature pages.
   Previous / Next buttons at the top of each page (with the neighbouring feature's name), a "3 / 26" counter,
   and the left / right arrow keys. The order is the panel's list (Improvements, then New); it wraps around.
   python3 tools/live/page-nav.py index.html"""
import sys
p = sys.argv[1]; s = open(p, encoding='utf-8').read()
def rep(a, b):
    global s
    if s.count(a) != 1: raise SystemExit('expected once: ' + a[:90])
    s = s.replace(a, b)
rep('  .fp-head { text-align: center; display: flex; flex-direction: column; gap: 4px; }',
    '''  .fp-head { text-align: center; display: flex; flex-direction: column; gap: 4px; }
  .fp-top { display: grid; grid-template-columns: minmax(0, 1fr) auto minmax(0, 1fr); align-items: center; gap: 16px; width: 100%; max-width: 1100px; }
  .fp-step { display: inline-flex; align-items: center; gap: 8px; max-width: 100%; min-width: 0; border: 1px solid var(--line-strong); background: var(--surface); color: var(--text); border-radius: 999px; padding: 7px 14px; font-weight: 700; font-size: 13px; cursor: pointer; }
  .fp-step:hover { background: var(--raise); }
  .fp-step svg { width: 16px; height: 16px; flex: none; }
  .fp-step span { min-width: 0; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
  .fp-step small { color: var(--muted); font-weight: 600; font-size: 11px; }
  .fp-prev { justify-self: start; }
  .fp-next { justify-self: end; }
  .fp-count { font-size: 11px; font-weight: 700; letter-spacing: .08em; color: var(--muted); font-variant-numeric: tabular-nums; }
  @media (max-width: 860px) { .fp-step span { display: none; } }''')
rep('''      <div class="fp-head"><span class="fp-cat" id="fpCat"></span><h2 id="fpTitle"></h2></div>''',
    '''      <div class="fp-top">
        <button type="button" class="fp-step fp-prev" id="fpPrev" aria-label="Previous feature"><svg viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="M10 3 5 8l5 5" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg><span id="fpPrevName"></span></button>
        <div class="fp-head"><span class="fp-cat" id="fpCat"></span><h2 id="fpTitle"></h2><span class="fp-count" id="fpCount"></span></div>
        <button type="button" class="fp-step fp-next" id="fpNext" aria-label="Next feature"><span id="fpNextName"></span><svg viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="M6 3l5 5-5 5" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg></button>
      </div>''')
rep('''    document.getElementById("fpTitle").textContent = f.name;''',
    '''    document.getElementById("fpTitle").textContent = f.name;
    var idx = FEATURES.indexOf(f), n = FEATURES.length;
    var prev = FEATURES[(idx - 1 + n) % n], next = FEATURES[(idx + 1) % n];
    document.getElementById("fpCount").textContent = (idx + 1) + " / " + n;
    document.getElementById("fpPrevName").textContent = prev.name;
    document.getElementById("fpNextName").textContent = next.name;
    document.getElementById("fpPrev").setAttribute("aria-label", "Previous feature: " + prev.name);
    document.getElementById("fpNext").setAttribute("aria-label", "Next feature: " + next.name);''')
rep('''  window.addEventListener("resize", fitPages);''',
    '''  window.addEventListener("resize", fitPages);
  function stepPage(d) {
    var i = FEATURES.findIndex(function (x) { return x.id === settings.feature; });
    if (i < 0) i = 0;
    settings.feature = FEATURES[(i + d + FEATURES.length) % FEATURES.length].id;
    try { localStorage.setItem(KEY, JSON.stringify(settings)); } catch (err) {}
    paintPages();
    var cur = fpNav.querySelector('[aria-current="page"]'); if (cur && cur.scrollIntoView) cur.scrollIntoView({ block: "nearest" });
  }
  document.getElementById("fpPrev").addEventListener("click", function () { stepPage(-1); });
  document.getElementById("fpNext").addEventListener("click", function () { stepPage(1); });
  document.addEventListener("keydown", function (e) {
    if (settings.view !== "pages" || e.altKey || e.ctrlKey || e.metaKey) return;
    var t = e.target; if (t && (/^(INPUT|TEXTAREA|SELECT)$/.test(t.tagName) || t.isContentEditable || (t.closest && t.closest('[role="tablist"],.seg')))) return;
    if (e.key === "ArrowLeft") { e.preventDefault(); stepPage(-1); }
    else if (e.key === "ArrowRight") { e.preventDefault(); stepPage(1); }
  });''')
open(p, 'w', encoding='utf-8').write(s); print('ok')
