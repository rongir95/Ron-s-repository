#!/usr/bin/env python3
"""Patch for the live shell (index.html), after page-nav.py: no jumps when moving between feature pages.
   - The "What changed" line always takes two lines' height, so the page doesn't re-centre when the note is
     one line on one page and two on the next.
   - A phone fades in once its prototype has loaded (no flash while it loads).
   python3 tools/live/page-steady.py index.html"""
import sys
p = sys.argv[1]; s = open(p, encoding='utf-8').read()
def rep(a, b):
    global s
    if s.count(a) != 1: raise SystemExit('expected once: ' + a[:90])
    s = s.replace(a, b)
rep('  .fp-note { margin: 0; max-width: 680px; text-align: center; font-size: 14px; color: var(--muted); border-top: 1px solid var(--line); padding-top: 14px; }',
    '  .fp-note { margin: 0; max-width: 680px; min-height: 57px; box-sizing: border-box; text-align: center; font-size: 14px; color: var(--muted); border-top: 1px solid var(--line); padding-top: 14px; }\n'
    '  .fp-phone iframe { opacity: 0; transition: opacity .25s ease; }\n'
    '  .fp-phone iframe.on { opacity: 1; }')
rep("""'<div class="fp-phone"><iframe title="' + f.name + ': ' + l + '" allow="autoplay; fullscreen" src="' + phoneSrc(ph.q) + '"></iframe></div>'""",
    """'<div class="fp-phone"><iframe title="' + f.name + ': ' + l + '" allow="autoplay; fullscreen" onload="this.classList.add(\\'on\\')" src="' + phoneSrc(ph.q) + '"></iframe></div>'""")
open(p, 'w', encoding='utf-8').write(s); print('ok')
