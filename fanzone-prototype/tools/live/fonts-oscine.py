#!/usr/bin/env python3
"""Patch for the live index.html (after row-menu.py): every text on the slides and in the side panel is DAZN Oscine
(the deck style had brought in Inter for titles, footer, navigation and dialogs). The Inter font link is removed.
   python3 tools/live/fonts-oscine.py index.html"""
import re, sys
p = sys.argv[1]; s = open(p, encoding='utf-8').read()
a = '''    --font: "Inter", "DAZN Oscine", system-ui, -apple-system, "Segoe UI", sans-serif;'''
if s.count(a) != 1: raise SystemExit('font variable changed')
s = s.replace(a, '''    --font: "DAZN Oscine", system-ui, -apple-system, "Segoe UI", sans-serif;''')
n0 = len(re.findall(r'font-family: "Inter"[^;]*;', s))
s = re.sub(r'font-family: "Inter"[^;]*;', 'font-family: var(--font);', s)
b = '<link rel="preconnect" href="https://fonts.googleapis.com">\n<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap">'
if s.count(b) != 1: raise SystemExit('Inter link changed')
s = s.replace(b + '\n', '')
s = s.replace('--font: "DAZN Oscine", "Inter", system-ui', '--font: "DAZN Oscine", system-ui')
if '"Inter"' in s or 'family=Inter' in s: raise SystemExit('Inter still in the styles')
open(p, 'w', encoding='utf-8').write(s); print('ok', n0, 'rules')
