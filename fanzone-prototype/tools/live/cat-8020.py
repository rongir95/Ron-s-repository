#!/usr/bin/env python3
"""Patch for the live index.html (after refresh.py): the line above each page title says "· 80-20" instead of
"· Improvement", matching the side list's group name.
   python3 tools/live/cat-8020.py index.html"""
import sys
p = sys.argv[1]; s = open(p, encoding='utf-8').read()
a = '''(f.kind === "new" ? " · New" : " · Improvement")'''
if s.count(a) != 1: raise SystemExit('expected the category label once')
s = s.replace(a, '''(f.kind === "new" ? " · New" : " · 80-20")''')
open(p, 'w', encoding='utf-8').write(s); print('ok')
