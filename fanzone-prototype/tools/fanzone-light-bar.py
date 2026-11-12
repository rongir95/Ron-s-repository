#!/usr/bin/env python3
"""FanZone Light: the message bar per FanZone DS (file NIgPxOlNU4U3sWMRdoE4Qh, node 12371:24497).

  12px padding, the 56px quick-message button (yellow NEW badge) on the left, and on the right the five
  reactions at 36px with 12px between them, then the change-team button 6px after them. The bar does
  not scroll in Light (everything fits in 375px).

Run after fanzone-fly-reactions.py:  python3 tools/fanzone-light-bar.py FanZone.dc.html
"""
import sys

PATH = sys.argv[1]
src = open(PATH, encoding='utf-8').read()

def rep(old, new, count=1):
    global src
    n = src.count(old)
    if n != count:
        raise SystemExit(f'expected {count} occurrence(s), found {n}: {old[:100]!r}')
    src = src.replace(old, new)

rep('<div data-fz-msgbar="1" style="', '<div data-fz-msgbar="1" class="{{ fzBarCls }}" style="')
rep('  @keyframes fzPushIn {',
    '  .fz-lightbar [data-fz-bar-row] { width: 375px !important; box-sizing: border-box; padding-right: 12px; justify-content: space-between; gap: 0 !important; cursor: default; }\n'
    '  .fz-lightbar [data-fz-bar-row] > div:last-child { gap: 12px !important; padding-right: 0 !important; }\n'
    '  .fz-lightbar [data-fz-bar-row] > div:last-child > img { width: 36px !important; height: 36px !important; margin: 0 !important; }\n'
    '  .fz-lightbar [data-fz-bar-row] > div:last-child > button[aria-label="Change team"] { margin-left: -6px; }\n'
    '  @keyframes fzPushIn {')
rep('      ...this.gzVals(),', '      ...this.gzVals(),\n      fzBarCls: this.isLight() && !this.state.fzTyping ? "fz-lightbar" : "",')

open(PATH, 'w', encoding='utf-8').write(src)
print('ok')
