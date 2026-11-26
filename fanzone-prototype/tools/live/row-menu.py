#!/usr/bin/env python3
"""Patch for the live index.html (after sections.py): a menu on every feature row in the side list.
 - Opens with a right-click on the row, or with the "..." button that shows on the row on hover (left click).
 - For now it has one action: Delete. A dialog asks to confirm; Delete removes the feature from the feature pages
   and the side list (kept in this browser, localStorage "fz-hidden"). "Restore deleted" under the list brings
   them all back.
   python3 tools/live/row-menu.py index.html"""
import sys
p = sys.argv[1]; s = open(p, encoding='utf-8').read()
def rep(a, b):
    global s
    if s.count(a) != 1: raise SystemExit('expected once: ' + a[:90])
    s = s.replace(a, b)
# deleted features are left out from the start
rep('''  try { var savedOrder = JSON.parse(localStorage.getItem("fz-order") || "null"); if (Array.isArray(savedOrder)) applyOrder(savedOrder); } catch (err) {}''',
    '''  try { var savedOrder = JSON.parse(localStorage.getItem("fz-order") || "null"); if (Array.isArray(savedOrder)) applyOrder(savedOrder); } catch (err) {}
  var HIDDEN = []; try { HIDDEN = JSON.parse(localStorage.getItem("fz-hidden") || "[]") || []; } catch (err) {}
  for (var hi = FEATURES.length - 1; hi >= 0; hi--) if (HIDDEN.indexOf(FEATURES[hi].id) >= 0) FEATURES.splice(hi, 1);''')
# "..." on each row
rep('''<span class="st is-' + st.toLowerCase() + '">' + st + '</span></button>';''',
    '''<span class="st is-' + st.toLowerCase() + '">' + st + '</span><span class="fp-more" role="button" aria-label="More for ' + f.name + '" title="More">&#8943;</span></button>';''')
# restore link
rep('''+ '>Reset order</button></div>';''', '''+ '>Reset order</button>' + (HIDDEN.length ? '<button type="button" id="fpRestore">Restore deleted (' + HIDDEN.length + ')</button>' : '') + '</div>';''')
rep('''    if (dragJustEnded) { e.preventDefault(); return; }''', '''    if (dragJustEnded) { e.preventDefault(); return; }
    if (e.target.closest("#fpRestore")) { try { localStorage.removeItem("fz-hidden"); } catch (err) {} location.reload(); return; }
    var more = e.target.closest(".fp-more");
    if (more) { e.preventDefault(); var r = more.getBoundingClientRect(); openRowMenu(more.closest(".fp-item").getAttribute("data-id"), r.right, r.bottom + 4, true); return; }''')
rep('''  var drag = null, dragJustEnded = false;''', '''  // ---- row menu (right-click or "...") ----
  fpNav.addEventListener("contextmenu", function (e) {
    var b = e.target.closest(".fp-item"); if (!b) return;
    e.preventDefault(); openRowMenu(b.getAttribute("data-id"), e.clientX, e.clientY, false);
  });
  var rowMenu = null;
  function closeRowMenu() { if (rowMenu) { rowMenu.remove(); rowMenu = null; } }
  function openRowMenu(id, x, y, alignRight) {
    closeRowMenu();
    var f = FEATURES.filter(function (q) { return q.id === id; })[0]; if (!f) return;
    rowMenu = document.createElement("div"); rowMenu.className = "fp-menu"; rowMenu.setAttribute("role", "menu");
    rowMenu.innerHTML = '<button type="button" role="menuitem" class="danger" data-act="delete"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 6h18M8 6V4h8v2M19 6l-1 14H6L5 6M10 11v6M14 11v6"/></svg>Delete</button>';
    document.body.appendChild(rowMenu);
    var w = rowMenu.offsetWidth, h = rowMenu.offsetHeight;
    var left = alignRight ? x - w : x, top = y;
    left = Math.max(8, Math.min(left, innerWidth - w - 8)); top = Math.max(8, Math.min(top, innerHeight - h - 8));
    rowMenu.style.left = left + "px"; rowMenu.style.top = top + "px";
    rowMenu.querySelector('[data-act="delete"]').addEventListener("click", function () { closeRowMenu(); confirmDelete(f); });
    rowMenu.querySelector("button").focus();
  }
  document.addEventListener("pointerdown", function (e) { if (rowMenu && !rowMenu.contains(e.target)) closeRowMenu(); }, true);
  document.addEventListener("keydown", function (e) { if (e.key === "Escape") closeRowMenu(); });
  window.addEventListener("resize", closeRowMenu);
  function confirmDelete(f) {
    var ov = document.createElement("div"); ov.className = "fp-dialog-bd";
    var esc = function (t) { return String(t).replace(/&/g, "&amp;").replace(/</g, "&lt;"); };
    ov.innerHTML = '<div class="fp-dialog" role="alertdialog" aria-modal="true" aria-labelledby="fpDlgT" aria-describedby="fpDlgD"><h3 id="fpDlgT">Delete \\u201c' + esc(f.name) + '\\u201d?</h3><p id="fpDlgD">It will be removed from the feature pages and the side list in this browser. You can bring it back with \\u201cRestore deleted\\u201d under the list.</p><div class="fp-dialog-act"><button type="button" class="cancel">Cancel</button><button type="button" class="del">Delete</button></div></div>';
    document.body.appendChild(ov);
    var done = function () { ov.remove(); document.removeEventListener("keydown", onKey, true); };
    var onKey = function (e) { if (e.key === "Escape") { e.stopPropagation(); done(); } };
    document.addEventListener("keydown", onKey, true);
    ov.addEventListener("click", function (e) { if (e.target === ov) done(); });
    ov.querySelector(".cancel").addEventListener("click", done);
    ov.querySelector(".del").addEventListener("click", function () { done(); deleteFeature(f.id); });
    ov.querySelector(".cancel").focus();
  }
  function deleteFeature(id) {
    var i = FEATURES.findIndex(function (q) { return q.id === id; }); if (i < 0) return;
    if (HIDDEN.indexOf(id) < 0) HIDDEN.push(id);
    try { localStorage.setItem("fz-hidden", JSON.stringify(HIDDEN)); } catch (err) {}
    var el = setFor(id); if (el) el.remove();
    setOrder = setOrder.filter(function (x) { return x !== id; });
    FEATURES.splice(i, 1);
    if (settings.feature === id) { settings.feature = FEATURES[Math.min(i, FEATURES.length - 1)].id; try { localStorage.setItem(KEY, JSON.stringify(settings)); } catch (err) {} }
    shownFeature = null; buildNav(); paintPages();
  }
  var drag = null, dragJustEnded = false;''')
rep('''  .fp-foot { position: absolute;''', '''  .fp-item .fp-more { flex: none; width: 22px; height: 22px; margin: 0 -4px 0 2px; border-radius: 6px; display: inline-flex; align-items: center; justify-content: center; font-size: 16px; line-height: 1; color: var(--muted); opacity: 0; transition: opacity .12s ease; }
  .fp-item:hover .fp-more, .fp-item:focus-visible .fp-more { opacity: 1; }
  .fp-item .fp-more:hover { background: var(--surface); color: var(--text); }
  .fp-reorder { flex-wrap: wrap; }
  .fp-menu { position: fixed; z-index: 60; min-width: 160px; padding: 6px; border-radius: 12px; background: #fff; border: 1px solid rgba(17, 17, 17, .08); box-shadow: 0 16px 40px -12px rgba(17, 17, 17, .3); font-family: var(--font); }
  .fp-menu button { width: 100%; display: flex; align-items: center; gap: 10px; border: 0; background: transparent; padding: 8px 10px; border-radius: 8px; font-size: 13px; font-weight: 600; text-align: left; cursor: pointer; color: var(--text); }
  .fp-menu button:hover, .fp-menu button:focus-visible { background: var(--surface); outline: none; }
  .fp-menu button.danger { color: #c62828; }
  .fp-dialog-bd { position: fixed; inset: 0; z-index: 70; background: rgba(17, 17, 17, .32); display: flex; align-items: center; justify-content: center; padding: 16px; animation: fpFadeIn .15s ease; }
  @keyframes fpFadeIn { from { opacity: 0; } to { opacity: 1; } }
  .fp-dialog { width: min(420px, 100%); background: #fff; border-radius: 20px; padding: 24px; box-shadow: 0 30px 80px -20px rgba(17, 17, 17, .45); font-family: var(--font); color: #111; }
  .fp-dialog h3 { margin: 0 0 8px; font-family: "Inter", sans-serif; font-size: 20px; font-weight: 700; letter-spacing: -.3px; }
  .fp-dialog p { margin: 0; color: var(--muted); font-size: 14px; }
  .fp-dialog-act { display: flex; justify-content: flex-end; gap: 8px; margin-top: 20px; }
  .fp-dialog-act button { border: 0; border-radius: 10px; padding: 10px 16px; font-weight: 700; font-size: 14px; cursor: pointer; }
  .fp-dialog-act .cancel { background: var(--surface); color: #111; }
  .fp-dialog-act .cancel:hover { background: #e4e3e8; }
  .fp-dialog-act .del { background: #c62828; color: #fff; }
  .fp-dialog-act .del:hover { background: #a91f1f; }
  .fp-foot { position: absolute;''')
open(p, 'w', encoding='utf-8').write(s); print('ok')
