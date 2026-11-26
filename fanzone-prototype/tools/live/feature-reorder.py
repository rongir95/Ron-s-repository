#!/usr/bin/env python3
"""Patch for the live index.html (after landscape-order.py): reorder the features in the side list by dragging.
Grab a feature and drag it up or down inside its group (Improvements / New); Prev / Next and the page count
follow the new order. The order is kept in this browser (localStorage "fz-order"); "Reset order" under the
list brings back the original order.
   python3 tools/live/feature-reorder.py index.html"""
import sys
p = sys.argv[1]; s = open(p, encoding='utf-8').read()
def rep(a, b):
    global s
    if s.count(a) != 1: raise SystemExit('expected once: ' + a[:90])
    s = s.replace(a, b)
rep('''  .fp-group { display: flex; flex-direction: column; gap: 2px; }''',
'''  .fp-group { display: flex; flex-direction: column; gap: 2px; }
  .fp-item { position: relative; }
  .fp-item .grip { position: absolute; left: -14px; top: 50%; width: 10px; height: 16px; margin-top: -8px; opacity: 0; color: var(--muted); transition: opacity .15s ease; pointer-events: none; }
  .fp-item:hover .grip { opacity: .8; }
  .fp-nav.dragging .fp-item { cursor: grabbing; transition: transform .15s ease; }
  .fp-nav.dragging .fp-item:hover .grip { opacity: 0; }
  .fp-item.is-drag { z-index: 2; background: var(--raise); color: var(--text); box-shadow: 0 0 0 1px var(--line-strong), 0 10px 28px rgba(0, 0, 0, .45); transition: none !important; }
  .fp-reorder { display: flex; align-items: center; justify-content: space-between; gap: 8px; margin-top: 4px; font-size: 11px; color: var(--muted); }
  .fp-reorder button { border: 0; background: transparent; color: var(--muted); font: inherit; font-weight: 700; text-decoration: underline; cursor: pointer; padding: 2px 0; }
  .fp-reorder button:hover { color: var(--text); }
  .fp-reorder button[hidden] { display: none; }''')

# saved order applied to FEATURES before anything is built
rep('''  function pageStatus(id) {''', '''  // ---- your order of the features (drag in the side list) ----
  var FEATURES_DEFAULT = FEATURES.map(function (f) { return f.id; });
  function applyOrder(ids) {
    var rank = function (f) { var i = ids ? ids.indexOf(f.id) : -1; return i < 0 ? 1000 + FEATURES_DEFAULT.indexOf(f.id) : i; };
    FEATURES.sort(function (a, b) { return rank(a) - rank(b); });
  }
  try { var savedOrder = JSON.parse(localStorage.getItem("fz-order") || "null"); if (Array.isArray(savedOrder)) applyOrder(savedOrder); } catch (err) {}
  function pageStatus(id) {''')

# grip + reset line in the list
rep('''        return '<button type="button" class="fp-item" data-id="' + f.id + '" data-cat="' + f.cat + '"><span class="fp-ic">''',
    '''        return '<button type="button" class="fp-item" data-id="' + f.id + '" data-cat="' + f.cat + '" title="Drag to reorder"><svg class="grip" viewBox="0 0 10 16" aria-hidden="true"><g fill="currentColor"><circle cx="3" cy="3" r="1.3"/><circle cx="7" cy="3" r="1.3"/><circle cx="3" cy="8" r="1.3"/><circle cx="7" cy="8" r="1.3"/><circle cx="3" cy="13" r="1.3"/><circle cx="7" cy="13" r="1.3"/></g></svg><span class="fp-ic">''')
rep('''      }).join("") + '</div>';
    }).join("");''', '''      }).join("") + '</div>';
    }).join("") + '<div class="fp-reorder"><span>Drag a feature to reorder</span><button type="button" id="fpResetOrder"' + (localStorage.getItem("fz-order") ? '' : ' hidden') + '>Reset order</button></div>';''')

# dragging (mouse / pen; a plain click still opens the page)
rep('''  fpNav.addEventListener("click", function (e) {
    var b = e.target.closest(".fp-item"); if (!b) return;''', '''  var drag = null, dragJustEnded = false;
  fpNav.addEventListener("pointerdown", function (e) {
    var b = e.target.closest(".fp-item"); if (!b || e.button !== 0 || e.pointerType === "touch") return;
    drag = { el: b, y0: e.clientY, on: false, id: e.pointerId };
  });
  window.addEventListener("pointermove", function (e) {
    if (!drag || e.pointerId !== drag.id) return;
    var dy = e.clientY - drag.y0;
    if (!drag.on) {
      if (Math.abs(dy) < 6) return;
      drag.on = true; fpNav.classList.add("dragging"); drag.el.classList.add("is-drag");
      try { drag.el.setPointerCapture(e.pointerId); } catch (err) {}
    }
    e.preventDefault();
    var group = drag.el.parentNode, items = [].slice.call(group.querySelectorAll(".fp-item"));
    var r = drag.el.getBoundingClientRect(), mid = r.top + r.height / 2 + 0;
    drag.el.style.transform = "translateY(" + dy + "px)";
    var cur = e.clientY, idx = items.indexOf(drag.el);
    var next = items[idx + 1], prev = items[idx - 1];
    if (next) { var nr = next.getBoundingClientRect(); if (cur > nr.top + nr.height / 2) { var before = drag.el.getBoundingClientRect().top; group.insertBefore(next, drag.el); var after = drag.el.getBoundingClientRect().top; drag.y0 += after - before; drag.el.style.transform = "translateY(" + (e.clientY - drag.y0) + "px)"; } }
    if (prev) { var pr = prev.getBoundingClientRect(); if (cur < pr.top + pr.height / 2) { var before2 = drag.el.getBoundingClientRect().top; group.insertBefore(drag.el, prev); var after2 = drag.el.getBoundingClientRect().top; drag.y0 += after2 - before2; drag.el.style.transform = "translateY(" + (e.clientY - drag.y0) + "px)"; } }
  });
  function endDrag(e) {
    if (!drag || (e && e.pointerId !== drag.id)) return;
    var was = drag.on, el = drag.el; drag = null;
    if (!was) return;
    el.style.transform = ""; el.classList.remove("is-drag"); fpNav.classList.remove("dragging");
    dragJustEnded = true; setTimeout(function () { dragJustEnded = false; }, 0);
    var ids = [].slice.call(fpNav.querySelectorAll(".fp-item")).map(function (x) { return x.getAttribute("data-id"); });
    applyOrder(ids);
    try { localStorage.setItem("fz-order", JSON.stringify(ids)); } catch (err) {}
    var rs = document.getElementById("fpResetOrder"); if (rs) rs.hidden = false;
    paintPages();
  }
  window.addEventListener("pointerup", endDrag);
  window.addEventListener("pointercancel", endDrag);
  fpNav.addEventListener("click", function (e) {
    if (e.target.closest("#fpResetOrder")) {
      try { localStorage.removeItem("fz-order"); } catch (err) {}
      FEATURES.sort(function (a, b) { return FEATURES_DEFAULT.indexOf(a.id) - FEATURES_DEFAULT.indexOf(b.id); });
      buildNav(); paintPages(); return;
    }
    if (dragJustEnded) { e.preventDefault(); return; }
    var b = e.target.closest(".fp-item"); if (!b) return;''')
open(p, 'w', encoding='utf-8').write(s); print('ok')
