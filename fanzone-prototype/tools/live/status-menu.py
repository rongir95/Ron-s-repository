#!/usr/bin/env python3
"""Patch for the live index.html (after phones-bigger.py):
 - The row menu (right-click / "...") can set a feature's status: Ready, Current or Soon (the badge in the side
   list). Kept in this browser (localStorage "fz-status"); picking the status the page would have anyway clears it.
 - Stats and scores inside FanZone moves to the New group.
 - Message sending: the Current phone opens with the Message field active (keyboard up).
   python3 tools/live/status-menu.py index.html"""
import sys
p = sys.argv[1]; s = open(p, encoding='utf-8').read()
def rep(a, b):
    global s
    if s.count(a) != 1: raise SystemExit('expected once: ' + a[:90])
    s = s.replace(a, b)
item = '{"id": "stats", "name": "Stats and scores inside FanZone", "cat": "Chat", "kind": "imp", "screens": 3}, '
if s.count(item) != 1: raise SystemExit('stats entry changed')
s = s.replace(item, '')
rep('{"id": "achievements", "name": "Achievements"', '{"id": "stats", "name": "Stats and scores inside FanZone", "cat": "Chat", "kind": "new", "screens": 2}, {"id": "achievements", "name": "Achievements"')
rep('''PAGES.sending = { phones: [cur("team=bayern"), later]''', '''PAGES.sending = { phones: [cur("moment=typing&team=bayern"), later]''')
rep('''  function pageStatus(id) { var pg = PAGES[id]; return pg ? (pg.ready ? "Ready" : "Current") : "Soon"; }''',
    '''  var STATUS = {}; try { STATUS = JSON.parse(localStorage.getItem("fz-status") || "{}") || {}; } catch (err) {}
  function pageStatusBase(id) { var pg = PAGES[id]; return pg ? (pg.ready ? "Ready" : "Current") : "Soon"; }
  function pageStatus(id) { return STATUS[id] || pageStatusBase(id); }''')
rep('''    rowMenu.innerHTML = '<button type="button" role="menuitem" data-act="rename">''',
    '''    var stNow = pageStatus(f.id);
    rowMenu.innerHTML = '<div class="fp-menu-label">Status</div>' + ["Ready", "Current", "Soon"].map(function (v) { return '<button type="button" role="menuitemradio" aria-checked="' + (v === stNow) + '" data-st="' + v + '"><span class="fp-menu-check">' + (v === stNow ? '&#10003;' : '') + '</span><span class="st is-' + v.toLowerCase() + '">' + v + '</span></button>'; }).join("") + '<div class="fp-menu-sep"></div><button type="button" role="menuitem" data-act="rename">''')
rep('''    rowMenu.querySelector('[data-act="rename"]').addEventListener("click", function () { closeRowMenu(); renameDialog(f); });''',
    '''    rowMenu.querySelector('[data-act="rename"]').addEventListener("click", function () { closeRowMenu(); renameDialog(f); });
    rowMenu.querySelectorAll("[data-st]").forEach(function (b) { b.addEventListener("click", function () {
      var v = b.getAttribute("data-st");
      if (v === pageStatusBase(f.id)) delete STATUS[f.id]; else STATUS[f.id] = v;
      try { localStorage.setItem("fz-status", JSON.stringify(STATUS)); } catch (err) {}
      closeRowMenu(); buildNav(); paintPages();
    }); });''')
rep('''  .fp-menu button.danger { color: #c62828; }''', '''  .fp-menu button.danger { color: #c62828; }
  .fp-menu-label { padding: 6px 10px 4px; font-size: 10.5px; font-weight: 700; letter-spacing: .08em; text-transform: uppercase; color: var(--muted); }
  .fp-menu-sep { height: 1px; margin: 6px 4px; background: var(--line); }
  .fp-menu-check { width: 14px; flex: none; text-align: center; font-size: 12px; }
  .fp-menu .st { display: inline-flex; align-items: center; gap: 5px; font-size: 10.5px; font-weight: 700; padding: 2px 8px; border-radius: 999px; color: var(--muted); }
  .fp-menu .st.is-ready { background: var(--primary); color: var(--on-primary); }
  .fp-menu .st.is-current { color: var(--text); box-shadow: inset 0 0 0 1px var(--line-strong); }''')
open(p, 'w', encoding='utf-8').write(s); print('ok')
