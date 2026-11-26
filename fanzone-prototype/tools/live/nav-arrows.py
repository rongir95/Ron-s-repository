#!/usr/bin/env python3
"""Patch for the live index.html (after nav-bottom.py): Prev / Next are a round arrow button with the page name next
to it as plain text (no pill around the text). The whole thing stays clickable.
   python3 tools/live/nav-arrows.py index.html"""
import sys
p = sys.argv[1]; s = open(p, encoding='utf-8').read()
a = '''  .fp-navs.fp-bottom { justify-content: center; margin-top: 4px; }'''
if s.count(a) != 1: raise SystemExit('nav css changed')
s = s.replace(a, a + '''
  .fp-navs .fp-step { border: 0; background: transparent; padding: 0; gap: 10px; color: var(--muted); font-weight: 600; }
  .fp-navs .fp-step:hover { background: transparent; color: var(--text); }
  .fp-navs .fp-step svg { width: 36px; height: 36px; padding: 10px; box-sizing: border-box; border: 1px solid var(--line-strong); border-radius: 50%; background: var(--surface); color: var(--text); transition: background .15s ease; }
  .fp-navs .fp-step:hover svg, .fp-navs .fp-step:focus-visible svg { background: var(--raise); }
  .fp-navs { gap: 18px; }''')
open(p, 'w', encoding='utf-8').write(s); print('ok')
