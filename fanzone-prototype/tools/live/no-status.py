#!/usr/bin/env python3
"""Patch for the live index.html (after hide-slides.py): status badges (Ready / Current / Soon) are hidden from the
side list for now, and so is the Status part of the row menu. One switch to bring them back: remove the
body class "fz-no-status" (statuses and their saved overrides are kept).
   python3 tools/live/no-status.py index.html"""
import sys
p = sys.argv[1]; s = open(p, encoding='utf-8').read()
def rep(a, b):
    global s
    if s.count(a) != 1: raise SystemExit('expected once: ' + a[:90])
    s = s.replace(a, b)
rep('''  .fp-item.is-hid { opacity: .5; }''', '''  body.fz-no-status .fp-item .st, body.fz-no-status .fp-menu-label, body.fz-no-status .fp-menu [data-st], body.fz-no-status .fp-menu-label + button + button + button + .fp-menu-sep { display: none !important; }
  .fp-item.is-hid { opacity: .5; }''')
rep('''  paint();
  fit();
  load();''', '''  document.body.classList.add("fz-no-status");
  paint();
  fit();
  load();''')
open(p, 'w', encoding='utf-8').write(s); print('ok')
