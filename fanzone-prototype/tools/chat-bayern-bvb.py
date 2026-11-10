#!/usr/bin/env python3
"""Rewrite the FanZone chat so it fits the match on screen: Bayern München vs Borussia Dortmund
(Der Klassiker at the Allianz Arena, 0-0 on the scoreboard). Names and avatars stay as they were.

Run last:  python3 tools/chat-bayern-bvb.py FanZone.dc.html
"""
import json, re, sys

PATH = sys.argv[1]
src = open(PATH, encoding='utf-8').read()

OPENING = [
    "Mia san mia‼️",
    "Musiala is unplayable tonight, Dortmund can’t get near him",
    "how is that not a yellow 😡",
    "Honestly the midfield battle is what’s deciding this, Kimmich and Brandt haven’t given each other a second of space all half",
]
POOL = [
    "Kane offside AGAIN",
    "SO CLOSE ‼️ Musiala hits the post 🔥🔥",
    "Kobel with the save of the season, what a wall",
    "var check… here we go again 😒",
    "Guirassy has been so quiet this half, Dortmund need to get him on the ball more or Bayern just run the game",
    "Der Klassiker never disappoints ❤️",
    "penalty!!!",
    "Neuer rushing off his line every time, it’s going to cost them one of these days",
    "Olise’s work rate is insane",
    "still 0-0 and my nerves are gone 😭",
    "Adeyemi coming on changes everything, Dortmund finally have pace on the break",
    "ref is a joke",
    "that Musiala turn 🤯",
    "Bayern need to stop giving the ball away in their own half, BVB are pressing every mistake",
    "CORNER",
    "Olise vs Schlotterbeck is the matchup to watch second half",
    "why is he shooting from there 😭",
    "level at the break, this is exactly the Klassiker we were promised 👏",
    "foul all day",
    "Bayern’s high line is so risky against Adeyemi’s pace, one ball over the top and it’s a 1v1 every time",
]

def rewrite(block_name, texts):
    global src
    m = re.search(r'const ' + block_name + r' = \[\n(.*?)\n\];', src, re.S)
    if not m:
        raise SystemExit('list not found: ' + block_name)
    lines = m.group(1).split('\n')
    if len(lines) != len(texts):
        raise SystemExit(f'{block_name}: {len(lines)} messages, {len(texts)} new texts')
    out = []
    for line, text in zip(lines, texts):
        new, n = re.subn(r'text: "(?:[^"\\]|\\.)*"', lambda _m, t=text: 'text: ' + json.dumps(t), line, count=1)
        if n != 1:
            raise SystemExit('no text in: ' + line[:80])
        out.append(new)
    src = src[:m.start(1)] + '\n'.join(out) + src[m.end(1):]

rewrite('CHAT', OPENING)
rewrite('CHAT_POOL', POOL)

# never post the same message twice in a row
old = '      const pick = CHAT_POOL[Math.floor(Math.random() * CHAT_POOL.length)];'
if src.count(old) != 1:
    raise SystemExit('message picker not found')
src = src.replace(old,
    '      const recent = this.state.feed.slice(-4).map(m => m.text);\n'
    '      let pick = CHAT_POOL[Math.floor(Math.random() * CHAT_POOL.length)];\n'
    '      for (let i = 0; i < 8 && recent.indexOf(pick.text) >= 0; i++) pick = CHAT_POOL[Math.floor(Math.random() * CHAT_POOL.length)];')
open(PATH, 'w', encoding='utf-8').write(src)
print('ok')
