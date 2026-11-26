#!/usr/bin/env python3
"""Patch for the live index.html (after head-fixed.py): the row menu also has Rename. A dialog with the current name;
Save (or Enter) renames the feature everywhere (side list, slide title, Prev / Next). An empty name brings back the
original one. Kept in this browser (localStorage "fz-names").
   python3 tools/live/row-rename.py index.html"""
import sys
p = sys.argv[1]; s = open(p, encoding='utf-8').read()
def rep(a, b):
    global s
    if s.count(a) != 1: raise SystemExit('expected once: ' + a[:90])
    s = s.replace(a, b)
rep('''  for (var hi = FEATURES.length - 1; hi >= 0; hi--) if (HIDDEN.indexOf(FEATURES[hi].id) >= 0) FEATURES.splice(hi, 1);''',
    '''  for (var hi = FEATURES.length - 1; hi >= 0; hi--) if (HIDDEN.indexOf(FEATURES[hi].id) >= 0) FEATURES.splice(hi, 1);
  var DEFAULT_NAMES = {}; FEATURES.forEach(function (f) { DEFAULT_NAMES[f.id] = f.name; });
  var NAMES = {}; try { NAMES = JSON.parse(localStorage.getItem("fz-names") || "{}") || {}; } catch (err) {}
  FEATURES.forEach(function (f) { if (NAMES[f.id]) f.name = NAMES[f.id]; });''')
rep('''    rowMenu.innerHTML = '<button type="button" role="menuitem" class="danger" data-act="delete">''',
    '''    rowMenu.innerHTML = '<button type="button" role="menuitem" data-act="rename"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 20h9"/><path d="M16.5 3.5a2.1 2.1 0 0 1 3 3L7 19l-4 1 1-4Z"/></svg>Rename</button><button type="button" role="menuitem" class="danger" data-act="delete">''')
rep('''    rowMenu.querySelector('[data-act="delete"]').addEventListener("click", function () { closeRowMenu(); confirmDelete(f); });''',
    '''    rowMenu.querySelector('[data-act="delete"]').addEventListener("click", function () { closeRowMenu(); confirmDelete(f); });
    rowMenu.querySelector('[data-act="rename"]').addEventListener("click", function () { closeRowMenu(); renameDialog(f); });''')
rep('''  function deleteFeature(id) {''', '''  function renameDialog(f) {
    var ov = document.createElement("div"); ov.className = "fp-dialog-bd";
    ov.innerHTML = '<form class="fp-dialog" role="dialog" aria-modal="true" aria-labelledby="fpRnT"><h3 id="fpRnT">Rename</h3><p>The name in the side list and on the slide. Leave it empty to bring back the original name.</p><input class="fp-input" type="text" maxlength="80" aria-label="Name"><div class="fp-dialog-act"><button type="button" class="cancel">Cancel</button><button type="submit" class="save">Save</button></div></form>';
    document.body.appendChild(ov);
    var inp = ov.querySelector("input"); inp.value = f.name;
    var done = function () { ov.remove(); document.removeEventListener("keydown", onKey, true); };
    var onKey = function (e) { if (e.key === "Escape") { e.stopPropagation(); done(); } };
    document.addEventListener("keydown", onKey, true);
    ov.addEventListener("click", function (e) { if (e.target === ov) done(); });
    ov.querySelector(".cancel").addEventListener("click", done);
    ov.querySelector("form").addEventListener("submit", function (e) {
      e.preventDefault();
      var v = inp.value.trim(), def = DEFAULT_NAMES[f.id] || f.name;
      if (!v || v === def) { delete NAMES[f.id]; f.name = def; } else { NAMES[f.id] = v; f.name = v; }
      try { localStorage.setItem("fz-names", JSON.stringify(NAMES)); } catch (err) {}
      done(); buildNav(); paintPages();
    });
    inp.focus(); inp.select();
  }
  function deleteFeature(id) {''')
rep('''  .fp-dialog-act { display: flex;''', '''  .fp-input { width: 100%; box-sizing: border-box; margin-top: 16px; padding: 11px 12px; border: 1px solid var(--line-strong); border-radius: 10px; background: #fff; color: #111; font: inherit; font-size: 15px; }
  .fp-input:focus { outline: 2px solid #111; outline-offset: 0; border-color: transparent; }
  .fp-dialog-act .save { background: #111; color: #fff; }
  .fp-dialog-act .save:hover { background: #2a2a2a; }
  .fp-dialog-act { display: flex;''')
open(p, 'w', encoding='utf-8').write(s); print('ok')
