#!/usr/bin/env python3
"""Every fan's status on their Fan Card fits their favorite team.

Chat fans support Bayern or Dortmund (FZ_FAN_TEAM, chat-bayern-bvb.py), so each gets a status from
their team's list, picked by name so the same fan always shows the same line. A fan whose favorite has
no list of its own gets a line built around the team's name. Sandra45 (Atlético) gets an Atlético status.

Run after chat-bayern-bvb.py:  python3 tools/fan-status.py FanZone.dc.html
"""
import json, sys

PATH = sys.argv[1]
src = open(PATH, encoding='utf-8').read()

def rep(old, new, count=1):
    global src
    n = src.count(old)
    if n != count:
        raise SystemExit(f'expected {count} occurrence(s), found {n}: {old[:100]!r}')
    src = src.replace(old, new)

TEAM_STATUS = {
    "bayern": [
        "Mia san mia ❤️",
        "Allianz Arena is my second home",
        "Red and white till I die 🔴⚪",
        "Another Meisterschale, please 🏆",
        "Südkurve every home game",
        "Musiala is a generational talent, fight me",
        "Klassiker day = best day of the year",
    ],
    "bvb": [
        "Echte Liebe 🖤💛",
        "Gelbe Wand forever",
        "Black and yellow, through everything 🐝",
        "Südtribüne is the best stand in the world",
        "Heja BVB!",
        "Westfalenstadion gives me goosebumps every time",
        "This is the year we beat Bayern",
    ],
    "atletico": ["Aúpa Atleti ❤️🤍", "Partido a partido", "Metropolitano or nowhere"],
    "athletic": ["Aupa Athletic! 🦁", "San Mamés is my cathedral"],
}
GENERIC = ["{team} till the end", "Proud {team} fan, every single match", "My week depends on how {team} plays"]

rep('const STATUS_POOL = [',
    '// Fan Card status by favorite team\n'
    'const TEAM_STATUS = ' + json.dumps(TEAM_STATUS, ensure_ascii=False) + ';\n'
    'const TEAM_STATUS_GENERIC = ' + json.dumps(GENERIC) + ';\n'
    'function fanStatusFor(teamId, h) {\n'
    '  const list = TEAM_STATUS[teamId];\n'
    '  if (list) return list[h % list.length];\n'
    '  const t = TEAMS[teamId];\n'
    '  return t ? TEAM_STATUS_GENERIC[h % TEAM_STATUS_GENERIC.length].replace("{team}", t.name) : STATUS_POOL[h % STATUS_POOL.length];\n'
    '}\n'
    'const STATUS_POOL = [')
rep('status: STATUS_POOL[h % STATUS_POOL.length] };', 'status: fanStatusFor(favoriteId, h) };')
rep('status: "Here for the chaos, staying for the goals", team: "atletico"', 'status: "Aúpa Atleti ❤️🤍 Partido a partido", team: "atletico"')

open(PATH, 'w', encoding='utf-8').write(src)
print('ok')
