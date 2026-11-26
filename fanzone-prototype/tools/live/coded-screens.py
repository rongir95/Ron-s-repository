#!/usr/bin/env python3
"""Patch for the live index.html (after browser-page.py): a phone can run a screen built in code (ph.src, a page such
as screens.html?v=browser) instead of a still image, so it stays sharp at any size. In-app browser's Current phone
now uses screens.html?v=browser (Figma FanZone 80-20 1:41036) instead of the image.
   python3 tools/live/coded-screens.py index.html"""
import sys
p = sys.argv[1]; s = open(p, encoding='utf-8').read()
def rep(a, b):
    global s
    if s.count(a) != 1: raise SystemExit('expected once: ' + a[:90])
    s = s.replace(a, b)
rep('''(ph && ph.img ? '' : ph && ph.q ? '<div class="fp-phone"><iframe title="' + f.name + ': ' + l + '" allow="autoplay; fullscreen" onload="this.classList.add(\\'on\\'); fpReady(this)" data-src="' + phoneSrc(ph.q) + '"></iframe></div>\'''',
    '''(ph && ph.img ? '' : ph && (ph.q || ph.src) ? '<div class="fp-phone"><iframe title="' + f.name + ': ' + l + '" allow="autoplay; fullscreen" onload="this.classList.add(\\'on\\'); fpReady(this)" data-src="' + (ph.src ? ph.src + (ph.src.indexOf("?") < 0 ? "?" : "&") + "fp=" + (++loads) : phoneSrc(ph.q)) + '"></iframe></div>\'''')
rep('''        if (l === "Outside FanZone" && !(ph && (ph.q || ph.img))) ph =''', '''        if (l === "Outside FanZone" && !(ph && (ph.q || ph.img || ph.src))) ph =''')
rep('''PAGES.browser = { phones: [{ img: "assets/screens/inapp-browser-current.png", label: "Current" }''', '''PAGES.browser = { phones: [{ src: "screens.html?v=browser", label: "Current" }''')
open(p, 'w', encoding='utf-8').write(s); print('ok')
