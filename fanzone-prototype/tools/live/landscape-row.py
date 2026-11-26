#!/usr/bin/env python3
"""Patch for the live index.html (after page-still.py): landscape phones sit side by side (Current, then the new
version), with their labels above like the portrait phones, sized to fit the width.
   python3 tools/live/landscape-row.py index.html"""
import sys
p = sys.argv[1]; s = open(p, encoding='utf-8').read()
def rep(a, b):
    global s
    if s.count(a) != 1: raise SystemExit('expected once: ' + a[:90])
    s = s.replace(a, b)
rep('''  .fp-set.land { flex-direction: column; align-items: center; gap: 44px; padding-top: 12px; }
  .fp-set.land .fp-col { flex-direction: row; gap: 18px; align-items: center; }
  .fp-set.land .fp-col figcaption { width: 120px; align-items: flex-end; }''',
'''  .fp-set.land { flex-direction: row; align-items: center; gap: 40px; min-height: calc(812px * var(--fs, .6) - 2px); }''')
rep('''    var ls = Math.min((w - 160) / 812, (h - 36 - 44 - 2 * 24) / (2 * 375));
    if (narrow) ls = Math.min((stage.clientWidth - 40) / 812, ls);''',
'''    var ls = Math.min((w - 40 - 2 * 22) / (2 * 812), (h - 30) / 375);
    if (narrow) ls = Math.min((stage.clientWidth - 40) / 812, ls);''')
open(p, 'w', encoding='utf-8').write(s); print('ok')
