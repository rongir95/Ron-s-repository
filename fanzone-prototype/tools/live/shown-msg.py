#!/usr/bin/env python3
"""Patch for the live index.html (after fzbutton-gap.py): when a feature page is shown, its phones get a
{fz: "shown"} message, so timed moments (the engagement break) count from when you see the page, not from
when it loaded in the background.
   python3 tools/live/shown-msg.py index.html"""
import sys
p = sys.argv[1]; s = open(p, encoding='utf-8').read()
a = '''  function stillIntro(el) {
    var t0 = Date.now();'''
if s.count(a) != 1: raise SystemExit('expected stillIntro once')
s = s.replace(a, '''  function stillIntro(el) {
    var t0 = Date.now();
    el.querySelectorAll("iframe").forEach(function (f) { try { f.contentWindow.postMessage({ fz: "shown" }, "*"); } catch (err) {} });''')
open(p, 'w', encoding='utf-8').write(s); print('ok')
