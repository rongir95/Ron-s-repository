#!/usr/bin/env python3
"""Patch for the live FanZone.dc.html (after fz-header.py): phones on the feature pages (fp= in the URL) skip the
runtime's second download of this whole file (it fetches its own page again after it has drawn, ~860KB, and
re-compiles the template), by giving the runtime an empty resource map. The prototype on its own is unchanged.
   python3 tools/live/fast-boot.py FanZone.dc.html"""
import sys
p = sys.argv[1]; s = open(p, encoding='utf-8').read()
a = '<script src="./support.js"></script>'
if s.count(a) != 1: raise SystemExit('expected the support.js tag once')
s = s.replace(a, '<script>if (/[?&]fp=/.test(location.search)) window.__resources = {};</script>\n' + a)
open(p, 'w', encoding='utf-8').write(s); print('ok')
