#!/usr/bin/env python3
"""Patch for the live index.html: the Actions on messages note mentions reactions (Figma 90:104486).
   python3 tools/live/actions-note.py index.html"""
import sys
p = sys.argv[1]; s = open(p, encoding='utf-8').read()
a = '''note: "<b>New:</b> long-press a message to focus it and report it." };'''
if s.count(a) != 1: raise SystemExit('actions note changed')
s = s.replace(a, '''note: "<b>New:</b> long-press a message to react to it, or report it. Your reaction shows under the message; tap it to remove it." };''')
open(p, 'w', encoding='utf-8').write(s); print('ok')
