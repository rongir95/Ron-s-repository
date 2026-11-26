#!/usr/bin/env python3
"""Patch for the live index.html (after eb-page.py): moving between feature pages slides the whole page
(all its phones together) in from the side you're going to, instead of each phone fading its new screen
in place. Next comes in from the right, Previous from the left; the side list picks the side by order.
   python3 tools/live/page-slide.py index.html"""
import sys
p = sys.argv[1]; s = open(p, encoding='utf-8').read()
def rep(a, b):
    global s
    if s.count(a) != 1: raise SystemExit('expected once: ' + a[:90])
    s = s.replace(a, b)
rep('''  .fp-phone iframe { opacity: 0; transition: opacity .25s ease; }
  .fp-phone iframe.on { opacity: 1; }''',
'''  .fp-set.in-next { animation: fpInNext .34s cubic-bezier(.2, .8, .2, 1); }
  .fp-set.in-prev { animation: fpInPrev .34s cubic-bezier(.2, .8, .2, 1); }
  .fp-set.in-fade { animation: fpInFade .25s ease; }
  @keyframes fpInNext { from { opacity: 0; transform: translateX(64px); } to { opacity: 1; transform: none; } }
  @keyframes fpInPrev { from { opacity: 0; transform: translateX(-64px); } to { opacity: 1; transform: none; } }
  @keyframes fpInFade { from { opacity: 0; } to { opacity: 1; } }
  @media (prefers-reduced-motion: reduce) { .fp-set.in-next, .fp-set.in-prev { animation: fpInFade .2s ease; } }''')
rep('''      row.querySelectorAll(".fp-set").forEach(function (x) { x.hidden = x !== el; });''',
'''      row.querySelectorAll(".fp-set").forEach(function (x) { x.hidden = x !== el; });
      el.classList.remove("in-next", "in-prev", "in-fade");
      if (fpAnim) { void el.offsetWidth; el.classList.add(fpAnim > 0 ? "in-next" : fpAnim < 0 ? "in-prev" : "in-fade"); }''')
rep('''    if (shownFeature !== f.id) {
      shownFeature = f.id;''',
'''    if (shownFeature !== f.id) {
      var oldI = FEATURES.findIndex(function (x) { return x.id === shownFeature; });
      fpAnim = oldI < 0 ? 0 : (fpDir || (idx > oldI ? 1 : -1)); fpDir = 0;
      shownFeature = f.id;''')
rep('''  var shownFeature = null;''', '''  var shownFeature = null, fpDir = 0, fpAnim = 0;''')
rep('''    settings.feature = FEATURES[(i + d + FEATURES.length) % FEATURES.length].id;''',
'''    settings.feature = FEATURES[(i + d + FEATURES.length) % FEATURES.length].id; fpDir = d;''')
open(p, 'w', encoding='utf-8').write(s); print('ok')
