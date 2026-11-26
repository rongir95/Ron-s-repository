#!/usr/bin/env python3
"""Patch for the live FanZone.dc.html: lite=1 uses a light copy of the match video
(assets/video/fixture-bayern-bvb-lite.mp4: 640px, first 45s, no sound, 1.4MB instead of 13MB).
The feature-page phones use it, so several phones on one page don't each download the full video.
Without the key nothing changes.
   python3 tools/live/lite-video.py FanZone.dc.html"""
import sys
p = sys.argv[1]; s = open(p, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    if s.count(a) != n: raise SystemExit(f'expected {n}: ' + a[:90])
    s = s.replace(a, b)
rep('    if (q.get("reset") === "1") o.resetOnLoad = true;',
    '    if (q.get("reset") === "1") o.resetOnLoad = true;\n    if (q.get("lite") === "1") o.liteVideo = true;')
rep('src="assets/video/fixture-bayern-bvb.mp4"', 'src="{{ fxVideoSrc }}"', 2)
rep('      ...this.gzVals(),', '      ...this.gzVals(),\n      fxVideoSrc: this.P.liteVideo ? "assets/video/fixture-bayern-bvb-lite.mp4" : "assets/video/fixture-bayern-bvb.mp4",')
open(p, 'w', encoding='utf-8').write(s); print('ok')
