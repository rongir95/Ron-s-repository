#!/usr/bin/env python3
"""Patch for the live FanZone.dc.html: reactions by the message field per Figma "FanZone 80-20"
(a38ncus4fbwkPfnlFQIUPt 23:136814): 36px reactions 12px apart, then 6px to the 32px change-team button.
The bar's second page shifts 14px further so the right edge keeps its 12px.
   python3 tools/live/reaction-spacing.py FanZone.dc.html"""
import sys
p = sys.argv[1]; s = open(p, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    if s.count(a) != n: raise SystemExit(f'expected {n}: ' + a[:90])
    s = s.replace(a, b)
rep('<div style="display:flex;align-items:center;gap:8px;flex-shrink:0;height:48px;padding-right:12px;{{ fzRxDisplay }}">',
    '<div style="display:flex;align-items:center;gap:12px;flex-shrink:0;height:48px;padding-right:12px;{{ fzRxDisplay }}">')
rep('draggable="false" style="flex-shrink:0;width:40px;height:40px;margin:-2px;object-fit:contain;cursor:pointer;">',
    'draggable="false" style="flex-shrink:0;width:36px;height:36px;object-fit:contain;cursor:pointer;">')
rep('<button onClick="{{ openTeamChooser }}" aria-label="Change team" style="flex-shrink:0;width:32px;',
    '<button onClick="{{ openTeamChooser }}" aria-label="Change team" style="flex-shrink:0;margin-left:-6px;width:32px;')
rep('    const SHIFT = 245;', '    const SHIFT = 259;')
rep('(s.fzBar2 ? -245 : 0),', '(s.fzBar2 ? -259 : 0),')
open(p, 'w', encoding='utf-8').write(s); print('ok')
