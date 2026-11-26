#!/usr/bin/env python3
"""Patch for the live index.html (after standalone.py): a "Landscape" group in the side list (between 80-20 and New)
with its own section slide "FanZone Landscape". In it: Share moment (moved from 80-20), and Poll, Quiz and Fan battle
in landscape. Landscape slides have two landscape phones, Current and 80-20 (no Standalone); Poll / Quiz / Fan battle
show placeholders until their designs come in.
   python3 tools/live/landscape-group.py index.html"""
import sys
p = sys.argv[1]; s = open(p, encoding='utf-8').read()
def rep(a, b):
    global s
    if s.count(a) != 1: raise SystemExit('expected once: ' + a[:90])
    s = s.replace(a, b)
rep('{"id": "share", "name": "Share moment", "cat": "Activations", "kind": "imp", "screens": 2}',
    '{"id": "share", "name": "Share moment", "cat": "Activations", "kind": "land", "screens": 2}, '
    '{"id": "lpoll", "name": "Poll", "cat": "Activations", "kind": "land", "screens": 2}, '
    '{"id": "lquiz", "name": "Quiz", "cat": "Activations", "kind": "land", "screens": 2}, '
    '{"id": "lbattle", "name": "Fan battle", "cat": "Activations", "kind": "land", "screens": 2}')
rep('''"share": "share",''', '''"share": "share", "lpoll": "poll", "lquiz": "help", "lbattle": "sword",''')
rep('''    "new": { id: "sec-new", name: "FanZone New",''', '''    land: { id: "sec-land", name: "FanZone Landscape", cat: "", kind: "land", section: true, title: 'FanZone <em>Landscape</em>', sub: "Landscape features" },
    "new": { id: "sec-new", name: "FanZone New",''')
rep('''    var groups = [["imp", "80-20"], ["new", "New"]];''', '''    var groups = [["imp", "80-20"], ["land", "Landscape"], ["new", "New"]];''')
rep('''(f.kind === "new" ? " · New" : " · 80-20")''', '''(f.kind === "new" ? " · New" : f.kind === "land" ? " · Landscape" : " · 80-20")''')
rep('''(f.kind === "new" ? "New" : "80-20") + '</em>';''', '''(f.kind === "new" ? "New" : f.kind === "land" ? "Landscape" : "80-20") + '</em>';''')
# groups in order (80-20, Landscape, New), each led by its section slide
rep('''  function pageStatus(id) {''', '''  function placeSections() {
    var KIND_ORDER = ["imp", "land", "new"];
    for (var i = FEATURES.length - 1; i >= 0; i--) if (FEATURES[i].section) FEATURES.splice(i, 1);
    var keyed = FEATURES.map(function (f, k) { return [KIND_ORDER.indexOf(f.kind), k, f]; });
    keyed.sort(function (a, b) { return a[0] - b[0] || a[1] - b[1]; });
    FEATURES.length = 0; keyed.forEach(function (x) { FEATURES.push(x[2]); });
    KIND_ORDER.forEach(function (kd) {
      var j = FEATURES.findIndex(function (f) { return f.kind === kd; });
      if (j >= 0 || kd !== "land") FEATURES.splice(j < 0 ? FEATURES.length : j, 0, SECTIONS[kd]);
    });
  }
  placeSections();
  // landscape slides: Current and 80-20 in landscape (no Standalone)
  (function () {
    var cur = { empty: "Current \\u00b7 Landscape<br>Waiting for the design", label: "Current" }, nxt = { empty: "80-20 \\u00b7 Landscape<br>Not designed yet", label: "80-20" };
    PAGES.lpoll = { land: [cur, nxt], note: "<b>Landscape:</b> the poll in landscape. The Current and 80-20 designs are on their way." };
    PAGES.lquiz = { land: [cur, nxt], note: "<b>Landscape:</b> the quiz in landscape. The Current and 80-20 designs are on their way." };
    PAGES.lbattle = { land: [cur, nxt], note: "<b>Landscape:</b> the fan battle in landscape. The Current and 80-20 designs are on their way." };
  })();
  function pageStatus(id) {''')
open(p, 'w', encoding='utf-8').write(s); print('ok')
