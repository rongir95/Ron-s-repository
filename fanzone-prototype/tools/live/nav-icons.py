#!/usr/bin/env python3
"""Patch for the live shell (index.html), after current-pages.py: icons and status badges in the feature list.
   - Each feature gets the icon it has in the FanZone 80-20 plan (tools/live/data/plan-icons.json, the plan's
     own line icons), tinted in its category colour from the plan (Activations blue, Chat purple,
     General green, Extras orange).
   - Status as small badges: Ready (filled), Current (outlined, with a dot), Soon (quiet).
   python3 tools/live/nav-icons.py index.html"""
import json, os, sys
p = sys.argv[1]; s = open(p, encoding='utf-8').read()
def rep(a, b):
    global s
    if s.count(a) != 1: raise SystemExit('expected once: ' + a[:90])
    s = s.replace(a, b)
icons = json.load(open(os.path.join(os.path.dirname(__file__), 'data', 'plan-icons.json')))
ICON = {"poll": "poll", "quiz": "help", "pinned": "image", "battle": "sword", "eb": "film", "landscape": "rotate",
        "smart": "puzzle", "team": "shirt", "reactions": "heart", "leaderboard": "medal", "mute": "ban", "sending": "send",
        "actions": "more", "stats": "score", "fzbutton": "button", "drawers": "drawer", "report": "drawer", "browser": "globe",
        "haptic": "vibrate", "predictions": "chart-up", "drawertab": "tabs", "export": "export", "onboarding": "hand",
        "achievements": "award", "liveupdates": "radio", "alerts": "bell"}
sprite = '<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>' + ''.join(
    '<symbol id="fpi-%s"%s>%s</symbol>' % (n, icons[n][0], icons[n][1]) for n in sorted(set(ICON.values()))) + '</defs></svg>'
rep('    <nav class="fp-nav" id="fpNav" aria-label="Features" hidden></nav>',
    '    ' + sprite + '\n    <nav class="fp-nav" id="fpNav" aria-label="Features" hidden></nav>')
rep('  .fp-item .st { margin-left: auto; flex-shrink: 0; font-size: 10.5px; font-weight: 600; color: var(--muted); }\n  .fp-item .st.ready { color: var(--text); }',
    '''  .fp-item { gap: 10px; padding: 6px 8px; line-height: 1.3; }
  .fp-ic { flex: none; width: 26px; height: 26px; border-radius: 8px; display: flex; align-items: center; justify-content: center; color: var(--c); background: color-mix(in srgb, var(--c) 14%, transparent); box-shadow: inset 0 0 0 1px color-mix(in srgb, var(--c) 24%, transparent); }
  .fp-ic svg { width: 15px; height: 15px; fill: none; stroke: currentColor; stroke-width: 1.8; stroke-linecap: round; stroke-linejoin: round; }
  .fp-item .nm { min-width: 0; }
  .fp-item[data-cat="Activations"] { --c: #7cc4ff; } .fp-item[data-cat="Chat"] { --c: #b79cff; }
  .fp-item[data-cat="General"] { --c: #6fe3b4; } .fp-item[data-cat="Extras"] { --c: #ffb36b; }
  .fp-item .st { margin-left: auto; flex-shrink: 0; display: inline-flex; align-items: center; gap: 5px; font-size: 10.5px; font-weight: 700; letter-spacing: .02em; color: var(--muted); padding: 2px 8px; border-radius: 999px; }
  .fp-item .st.is-ready { background: var(--primary); color: var(--on-primary); }
  .fp-item .st.is-current { color: var(--text); box-shadow: inset 0 0 0 1px var(--line-strong); }
  .fp-item .st.is-current::before { content: ""; width: 5px; height: 5px; border-radius: 50%; background: var(--c); }
  .fp-item .st.is-soon { opacity: .7; }''')
rep("""        return '<button type="button" class="fp-item" data-id="' + f.id + '">' + f.name + '<span class="st' + (PAGES[f.id] ? ' ready' : '') + '">' + pageStatus(f.id) + '</span></button>';""",
    """        var st = pageStatus(f.id);
        return '<button type="button" class="fp-item" data-id="' + f.id + '" data-cat="' + f.cat + '"><span class="fp-ic"><svg viewBox="0 0 24 24" aria-hidden="true"><use href="#fpi-' + (FP_ICON[f.id] || 'poll') + '"/></svg></span><span class="nm">' + f.name + '</span><span class="st is-' + st.toLowerCase() + '">' + st + '</span></button>';""")
rep('  var PAGES = {', '  var FP_ICON = ' + json.dumps(ICON) + ';\n  var PAGES = {')
open(p, 'w', encoding='utf-8').write(s); print('ok')
