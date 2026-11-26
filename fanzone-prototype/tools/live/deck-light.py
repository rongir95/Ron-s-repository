#!/usr/bin/env python3
"""Patch for the live index.html (after nav-arrows.py): the presentation in the style of the DAZN Product Roadmap
2.0 deck. Light theme (slides and the side panel): #F4F2F6 ground with soft white / grey glows, #111 text, Inter.
 - Title: Inter 700, tight tracking, "<feature> · <em>80-20</em>" with the deck's yellow highlighter (#FFFA00 band
   under the lower part of the words). The explanation line is the grey subtitle under it.
 - Tags above the phones are white cards; the 80-20 / New one is solid #FFFA00 with black text.
 - Footer on every slide: DAZN logo + "FANZONE 80-20 · <category>" bottom left, the slide number bottom right.
 - Navigation is a dark pill at the bottom centre (arrows, page names, count, refresh), over a thin #FFFA00 line.
 - Phones keep their dark bezels; placeholder screens stay dark.
   python3 tools/live/deck-light.py index.html"""
import sys
p = sys.argv[1]; s = open(p, encoding='utf-8').read()
def rep(a, b):
    global s
    if s.count(a) != 1: raise SystemExit('expected once: ' + a[:90])
    s = s.replace(a, b)

CSS = '''
  /* ---------- Deck style (DAZN Product Roadmap 2.0): light theme ---------- */
  :root {
    color-scheme: light;
    --ground: #ecebef;
    --stage: #f4f2f6;
    --rail: #fbfafc;
    --surface: #efeef2;
    --raise: #ffffff;
    --line: rgba(17, 17, 17, 0.07);
    --line-strong: rgba(17, 17, 17, 0.14);
    --text: #111111;
    --muted: #6b6e74;
    --primary: #111111;
    --on-primary: #ffffff;
    --font: "Inter", "DAZN Oscine", system-ui, -apple-system, "Segoe UI", sans-serif;
    --hl: #FFFA00;
  }
  body { background: var(--ground); }
  .stage { background:
      radial-gradient(55% 60% at 18% 8%, #ffffff 0%, rgba(255, 255, 255, 0) 70%),
      radial-gradient(40% 45% at 85% 95%, rgba(140, 146, 158, .32) 0%, rgba(140, 146, 158, 0) 70%),
      radial-gradient(30% 35% at 72% 22%, rgba(160, 166, 178, .16) 0%, rgba(160, 166, 178, 0) 70%),
      var(--stage); }
  .rail { background: var(--rail); border-left-color: var(--line-strong); }
  .brand h1 img { filter: brightness(0); }
  .seg button[aria-pressed="true"] { box-shadow: 0 1px 2px rgba(17, 17, 17, .12), 0 0 0 1px var(--line); }
  .seg button[aria-pressed="true"] small { color: var(--muted); }
  .live-btn:hover:not(:disabled) { background: #2a2a2a; }
  .fp-item.is-drag { box-shadow: 0 0 0 1px var(--line-strong), 0 10px 28px rgba(17, 17, 17, .18); }
  .fp-item[aria-current="page"] { background: #ffffff; box-shadow: 0 1px 2px rgba(17, 17, 17, .1), 0 0 0 1px var(--line); }
  .fp-item[data-cat="Activations"] { --c: #1f7ad1; } .fp-item[data-cat="Chat"] { --c: #7a4fe0; }
  .fp-item[data-cat="General"] { --c: #138a5e; } .fp-item[data-cat="Extras"] { --c: #c96a12; }
  .device { box-shadow: 0 0 0 calc(11px * var(--s, 1)) var(--bezel), 0 0 0 calc(13px * var(--s, 1)) #2c2c31, 0 40px 80px rgba(17, 17, 17, .28); }

  /* slide */
  .fpage { padding: 40px 48px 84px; justify-content: flex-start; }
  .fp-top .fp-cat { display: none; }
  .fp-top h2 { font-family: "Inter", "Helvetica Neue", Helvetica, Arial, sans-serif; font-size: 42px; font-weight: 700; letter-spacing: -1.1px; line-height: 1.1; color: #111; }
  .fp-top h2 em { font-style: normal; background: linear-gradient(transparent 70%, var(--hl) 70%); padding: 0 2px; }
  .fp-top .fp-note { color: var(--muted); font-size: 14px; margin-top: 8px; }
  .fp-top .fp-note b { color: #111; }
  .fp-row { margin-top: auto; margin-bottom: auto; }
  .fp-chip { background: rgba(255, 255, 255, .85); border: 1px solid rgba(17, 17, 17, .06); color: #111; box-shadow: inset 0 1px 0 rgba(255, 255, 255, .9), 0 8px 20px -14px rgba(17, 17, 17, .35); padding: 5px 14px; }
  .fp-chip.hl { background: var(--hl); color: #111; border-color: transparent; }
  .fp-phone { box-shadow: 0 0 0 calc(9px * var(--fs, .6)) var(--bezel), 0 0 0 calc(11px * var(--fs, .6)) #2c2c31, 0 30px 60px rgba(17, 17, 17, .25); }
  .fp-phone.land { box-shadow: 0 0 0 calc(9px * var(--ls, .6)) var(--bezel), 0 0 0 calc(11px * var(--ls, .6)) #2c2c31, 0 30px 60px rgba(17, 17, 17, .25); }
  .fp-phone.empty { background: #0C161C; color: rgba(249, 250, 250, .55); }
  .fp-phone.empty::before { border-color: rgba(249, 250, 250, .16); }
  .fp-orient .only { background: #fff; }

  /* footer: logo + deck line bottom left, slide number bottom right */
  .fp-foot { position: absolute; left: 48px; right: 48px; bottom: 26px; display: flex; align-items: center; justify-content: space-between; pointer-events: none; font-family: "Inter", sans-serif; }
  .fp-foot .fp-brand { display: inline-flex; align-items: center; gap: 12px; font-size: 10px; font-weight: 700; letter-spacing: .12em; text-transform: uppercase; color: #8a8d93; }
  .fp-foot .fp-brand img { width: 24px; height: 24px; filter: brightness(0); opacity: .85; }
  .fp-foot .fp-pnum { font-size: 10px; font-weight: 700; letter-spacing: .12em; color: #8a8d93; font-variant-numeric: tabular-nums; }

  /* navigation: dark pill at the bottom centre over a thin yellow line */
  .fpage::after { content: ""; position: absolute; left: 0; right: 0; bottom: 0; height: 4px; background: var(--hl); }
  .fp-navs.fp-bottom { position: absolute; left: 50%; bottom: 14px; transform: translateX(-50%); z-index: 2; margin: 0; gap: 6px; padding: 6px 8px; border-radius: 16px; background: #1f2226; box-shadow: 0 10px 30px rgba(17, 17, 17, .25); }
  .fp-navs.fp-bottom .fp-step { color: #c9ccd1; font-family: "Inter", sans-serif; font-size: 13px; padding: 0 6px; }
  .fp-navs.fp-bottom .fp-step:hover { color: #fff; }
  .fp-navs.fp-bottom .fp-step svg { width: 32px; height: 32px; padding: 9px; border: 0; background: transparent; color: #fff; }
  .fp-navs.fp-bottom .fp-step:hover svg { background: rgba(255, 255, 255, .1); }
  .fp-navs.fp-bottom .fp-countrow { background: rgba(255, 255, 255, .08); border-radius: 10px; padding: 5px 6px 5px 12px; }
  .fp-navs.fp-bottom .fp-count { color: #fff; font-family: "Inter", sans-serif; }
  .fp-navs.fp-bottom .fp-refresh { background: transparent; border: 0; color: #c9ccd1; }
  .fp-navs.fp-bottom .fp-refresh:hover { color: #fff; background: rgba(255, 255, 255, .1); }
  body[data-panel="closed"] .fp-top { padding-right: 56px; }
'''
rep('''  @media (prefers-reduced-motion: reduce) { * { transition: none !important; } }''',
    '''  @media (prefers-reduced-motion: reduce) { * { transition: none !important; } }''' + CSS)
# Inter (the deck's typeface)
rep('<title>FanZone Prototype</title>', '<title>FanZone Prototype</title>\n<link rel="preconnect" href="https://fonts.googleapis.com">\n<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap">')
# footer markup
rep('''      <div class="fp-row" id="fpRow"></div>\n''', '''      <div class="fp-row" id="fpRow"></div>
      <div class="fp-foot" aria-hidden="true"><span class="fp-brand"><img src="assets/icons/dazn-logo.svg" alt=""><span>FanZone 80-20<span id="fpFootCat"></span></span></span><span class="fp-pnum" id="fpPnum"></span></div>\n''')
# title with the highlighted kind, footer texts
rep('''    document.getElementById("fpTitle").textContent = f.name;''',
    '''    var escH = function (t) { return String(t).replace(/&/g, "&amp;").replace(/</g, "&lt;"); };
    document.getElementById("fpTitle").innerHTML = escH(f.name) + ' · <em>' + (f.kind === "new" ? "New" : "80-20") + '</em>';
    document.getElementById("fpFootCat").textContent = f.cat ? " · " + f.cat : "";''')
rep('''    document.getElementById("fpCount").textContent = (idx + 1) + " / " + n;''',
    '''    document.getElementById("fpCount").textContent = (idx + 1) + " / " + n;
    document.getElementById("fpPnum").textContent = (idx + 1 < 10 ? "0" : "") + (idx + 1);''')
# room for the bigger title and the bottom bar
rep('''var w = stage.clientWidth - 48, h = stage.clientHeight - 56 - 40 - 32 - 36 - (settings.notes === "1" ? 70 : 0);''',
    '''var w = stage.clientWidth - 96, h = stage.clientHeight - 56 - 40 - 32 - 36 - 40 - (settings.notes === "1" ? 70 : 0);''')
open(p, 'w', encoding='utf-8').write(s); print('ok')
