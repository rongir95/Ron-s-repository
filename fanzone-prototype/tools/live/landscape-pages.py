#!/usr/bin/env python3
"""Patch for the live index.html (after page-slide.py): landscape on the feature pages.
 - A feature page can have landscape screens (PAGES[id].land). Landscape phones are 812x375, stacked
   (Current on top, then the new version), and run landscape.html (?v=current | ?v=share).
 - Pages with both portrait and landscape get a Portrait / Landscape switch under the title
   (settings.orient); landscape-only pages say "Landscape only".
 - New feature: Share moment (landscape only) under New. Landscape activations becomes the landscape overview.
   python3 tools/live/landscape-pages.py index.html"""
import sys
p = sys.argv[1]; s = open(p, encoding='utf-8').read()
def rep(a, b):
    global s
    if s.count(a) != 1: raise SystemExit('expected once: ' + a[:90])
    s = s.replace(a, b)

# --- styles ---
rep('''  .fp-set.in-next {''', '''  .fp-set.land { flex-direction: column; align-items: center; gap: 44px; padding-top: 12px; }
  .fp-set.land .fp-col { flex-direction: row; gap: 18px; align-items: center; }
  .fp-set.land .fp-col figcaption { width: 120px; align-items: flex-end; }
  .fp-phone.land { width: calc(812px * var(--ls, .6)); height: calc(375px * var(--ls, .6)); border-radius: calc(46px * var(--ls, .6)); box-shadow: 0 0 0 calc(9px * var(--ls, .6)) var(--bezel), 0 0 0 calc(11px * var(--ls, .6)) #2c2c31, 0 30px 70px rgba(0, 0, 0, .5); }
  .fp-phone.land iframe { width: 812px; height: 375px; zoom: var(--ls, .6); }
  @supports not (zoom: 2) { .fp-phone.land iframe { zoom: normal; transform: scale(var(--ls, .6)); } }
  .fp-phone.land.empty::before { border-radius: calc(40px * var(--ls, .6)); }
  .fp-orient { display: flex; justify-content: center; margin-top: 6px; min-height: 30px; }
  .fp-orient[hidden] { display: flex; visibility: hidden; }
  .fp-orient .seg { width: 230px; }
  .fp-orient .only { display: inline-flex; align-items: center; gap: 6px; font-size: 12px; font-weight: 700; color: var(--muted); border: 1px solid var(--line-strong); border-radius: 999px; padding: 5px 12px; }
  .fp-orient .only svg { width: 14px; height: 14px; fill: none; stroke: currentColor; stroke-width: 2; stroke-linecap: round; stroke-linejoin: round; }
  .fp-set.in-next {''')

# --- switch under the title ---
rep('''<span class="fp-count" id="fpCount"></span></div>''',
    '''<span class="fp-count" id="fpCount"></span><div class="fp-orient" id="fpOrient" hidden></div></div>''')

# --- icon ---
rep('<symbol id="fpi-rotate"', '<symbol id="fpi-share" viewBox="0 0 24 24"><path d="M4 12v8a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-8"/><path d="m16 6-4-4-4 4"/><path d="M12 2v13"/></symbol><symbol id="fpi-rotate"')
rep('"onboarding": "hand", "achievements": "award"', '"onboarding": "hand", "share": "share", "achievements": "award"')

# --- the feature ---
rep('{"id": "achievements", "name": "Achievements"',
    '{"id": "share", "name": "Share moment", "cat": "Activations", "kind": "new", "screens": 2}, {"id": "achievements", "name": "Achievements"')

# --- pages ---
rep('''  function pageStatus(id) {''', '''  // landscape screens (812x375, stacked): q is the query for landscape.html
  PAGES.share = { ready: true,
    land: [{ q: "v=current", label: "Current" }, { q: "v=share", label: "New" }],
    note: "<b>What's new:</b> in landscape a Share moment appears over the match: the share icon pops in, opens into a Share button, and the moment card (sponsor, clip and caption) rises above it. The X closes it. It exists only in landscape." };
  PAGES.landscape = {
    land: [{ q: "v=current", label: "Current" }, { empty: "80-20 · Landscape<br>Activations in landscape: not designed yet", label: "80-20" }],
    note: "<b>Landscape:</b> the player full screen, as it is today. Landscape features so far: <b>Share moment</b> (in the New list). Features that get a landscape version show a Portrait / Landscape switch under their title." };
  function orientOf(f) { var pg = PAGES[f.id]; if (!pg || !pg.land) return "port"; if (!pg.phones) return "land"; return settings.orient === "land" ? "land" : "port"; }
  function keyOf(id) { var f = FEATURES.filter(function (x) { return x.id === id; })[0]; return id + (f && orientOf(f) === "land" ? "@l" : ""); }
  function landSrc(q) { return "landscape.html?fp=" + (++loads) + "&" + q; }
  function pageStatus(id) {''')

# sets are keyed by feature + orientation
rep('''  function setFor(id) { return document.querySelector('#fpRow .fp-set[data-id="' + id + '"]'); }''',
    '''  function setFor(id) { return document.querySelector('#fpRow .fp-set[data-id="' + keyOf(id) + '"]'); }''')
rep('''      el = document.createElement("div"); el.className = "fp-set"; el.setAttribute("data-id", f.id); el.hidden = true;''',
    '''      el = document.createElement("div"); el.className = "fp-set" + (orientOf(f) === "land" ? " land" : ""); el.setAttribute("data-id", keyOf(f.id)); el.hidden = true;''')

# landscape phones
rep('''  function setHTML(f) {
    var page = PAGES[f.id];''', '''  function setHTML(f) {
    var page = PAGES[f.id];
    if (orientOf(f) === "land") return page.land.map(function (ph, i) {
      return '<figure class="fp-col"><figcaption><span class="fp-chip' + (i === 1 ? ' hl' : '') + '">' + ph.label + '</span></figcaption>' +
        (ph.q ? '<div class="fp-phone land"><iframe title="' + f.name + ': ' + ph.label + ' (landscape)" allow="autoplay; fullscreen" onload="this.classList.add(\\'on\\')" src="' + landSrc(ph.q) + '"></iframe></div>'
              : '<div class="fp-phone land empty">' + ph.empty + '</div>') + '</figure>';
    }).join("");''')

# switch
rep('''    note.hidden = settings.notes !== "1";''', '''    note.hidden = settings.notes !== "1";
    var or = document.getElementById("fpOrient"), pgl = page && page.land;
    or.hidden = !pgl;
    if (pgl && page.phones) {
      var o = orientOf(f);
      or.innerHTML = '<div class="seg" role="group" aria-label="Orientation"><button type="button" data-o="port" aria-pressed="' + (o === "port") + '">Portrait</button><button type="button" data-o="land" aria-pressed="' + (o === "land") + '">Landscape</button></div>';
    } else if (pgl) or.innerHTML = '<span class="only"><svg viewBox="0 0 24 24" aria-hidden="true"><rect x="2" y="6" width="20" height="12" rx="2"/></svg>Landscape only</span>';''')
rep('''  document.getElementById("fpPrev").addEventListener("click",''', '''  document.getElementById("fpOrient").addEventListener("click", function (e) {
    var b = e.target.closest("button[data-o]"); if (!b) return;
    settings.orient = b.getAttribute("data-o");
    try { localStorage.setItem(KEY, JSON.stringify(settings)); } catch (err) {}
    shownFeature = null; fpDir = 0; paintPages();
  });
  document.getElementById("fpPrev").addEventListener("click",''')

# size: landscape phones fill the width, two stacked
rep('''    fpage.style.setProperty("--fs", s.toFixed(4));''', '''    fpage.style.setProperty("--fs", s.toFixed(4));
    var ls = Math.min((w - 160) / 812, (h - 36 - 44 - 2 * 24) / (2 * 375));
    if (narrow) ls = Math.min((stage.clientWidth - 40) / 812, ls);
    fpage.style.setProperty("--ls", Math.max(0.3, Math.min(ls, 1)).toFixed(4));''')
open(p, 'w', encoding='utf-8').write(s); print('ok')
