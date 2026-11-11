#!/usr/bin/env python3
"""Home: the top hero (with Watch now) plays the match video instead of a still image.
Muted, looping, inline; the still stays as the poster while the video loads. The gradient from Figma
(node 492:80673) darkens the top and bottom so the header and the title stay readable.

Run after the other scripts:  python3 tools/home-video.py FanZone.dc.html
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

rep('<img src="assets/home/hero.jpg" alt="" style="position:absolute;inset:0;width:375px;height:564px;object-fit:cover;display:block;">',
    '<video src="assets/video/fixture-bayern-bvb.mp4" poster="assets/home/hero.jpg" ref="{{ heroVidRef }}" autoPlay="{{ true }}" muted="{{ true }}" loop="{{ true }}" playsInline="{{ true }}" preload="auto" '
    'aria-hidden="true" style="position:absolute;inset:0;width:375px;height:564px;object-fit:cover;display:block;background:#080E12;"></video>'
    # the darkening over the video, per Figma "mobile-hero-native" (EyEm3J8Y3qrWV40vOPOkjV, node 492:80673):
    # #080E12 at 80% at the top, clear from 22% to 48%, solid at 84%
    '<div aria-hidden="true" style="position:absolute;inset:0;pointer-events:none;background:linear-gradient(180deg,rgba(8,14,18,.8) 0%,rgba(8,14,18,0) 22%,rgba(8,14,18,0) 48%,#080E12 84%);"></div>')
rep('  fixVidRef = (el) => {',
    '  // muted must be set on the element itself for autoplay to be allowed\n'
    '  heroVidRef = (el) => {\n'
    '    if (!el || el._hero) return;\n'
    '    el._hero = true; el.muted = true; el.defaultMuted = true; el.setAttribute("muted", "");\n'
    '    const go = () => { const p = el.play(); if (p && p.catch) p.catch(() => {}); };\n'
    '    if (el.readyState >= 2) go(); else el.addEventListener("canplay", go, { once: true });\n'
    '  };\n'
    '  fixVidRef = (el) => {')
rep('      fixVidRef: this.fixVidRef,', '      fixVidRef: this.fixVidRef,\n      heroVidRef: this.heroVidRef,')
open(PATH, 'w', encoding='utf-8').write(src)
print('ok')
