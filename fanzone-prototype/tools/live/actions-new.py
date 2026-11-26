#!/usr/bin/env python3
"""Patch for the live index.html (after slide-comments.py): "Actions on messages in FanZone" moves to the New group.
A New feature that already has a Current screen (screens: 3) shows Current, New, Outside FanZone; the New tag is
the highlighted one.
   python3 tools/live/actions-new.py index.html"""
import sys
p = sys.argv[1]; s = open(p, encoding='utf-8').read()
def rep(a, b):
    global s
    if s.count(a) != 1: raise SystemExit('expected once: ' + a[:90])
    s = s.replace(a, b)
item = '{"id": "actions", "name": "Actions on messages in FanZone", "cat": "Chat", "kind": "imp", "screens": 3}, '
if s.count(item) != 1: raise SystemExit('actions entry changed')
s = s.replace(item, '')
rep('{"id": "achievements", "name": "Achievements"', '{"id": "actions", "name": "Actions on messages in FanZone", "cat": "Chat", "kind": "new", "screens": 3}, {"id": "achievements", "name": "Achievements"')
rep('''    var labels = f.kind === "new" ? ["New", "Outside FanZone"] :''', '''    var labels = f.kind === "new" ? (f.screens === 3 ? ["Current", "New", "Outside FanZone"] : ["New", "Outside FanZone"]) :''')
rep('''(i === 1 || f.kind === "new" && i === 0 ? ' hl' : '')''', '''(labels[i] === "80-20" || labels[i] === "New" ? ' hl' : '')''')
open(p, 'w', encoding='utf-8').write(s); print('ok')
