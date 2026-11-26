#!/usr/bin/env python3
"""Patch for the live shell (index.html), after poll-page.py: the Current screen on every feature page whose
feature already exists in the prototype (80-20 and Outside FanZone stay placeholders until there is a design).
The list marks them "Current"; Poll, with all its screens, is "Ready".
   python3 tools/live/current-pages.py index.html"""
import sys
p = sys.argv[1]; s = open(p, encoding='utf-8').read()
def rep(a, b):
    global s
    if s.count(a) != 1: raise SystemExit('expected once: ' + a[:90])
    s = s.replace(a, b)
rep('  // a phone in a feature page: the real prototype with the panel\'s settings, opening in FanZone',
    '''  PAGES.poll.ready = true;
  // pages with only the Current screen so far
  (function () {
    var later = { empty: "80-20<br>Not designed yet" }, out = { empty: "Outside FanZone<br>Waiting for a design" };
    var cur = function (q, hint) { return { q: q, hint: hint }; };
    var note = function (t) { return "<b>Current:</b> " + t + " The 80-20 version isn't designed yet."; };
    PAGES.quiz = { phones: [cur("moment=quiz&team=bayern"), later, out], note: note("the quiz as it is today, from the toast and countdown to the questions, the result and the leaderboard.") };
    PAGES.pinned = { phones: [cur("moment=pin&team=bayern"), later, out], note: note("the pinned image under the FanZone header; tap it to open it.") };
    PAGES.battle = { phones: [cur("moment=battle&team=bayern"), later, out], note: note("the fan battle strip and the gifts; send gifts to push your team's bar.") };
    PAGES.leaderboard = { phones: [cur("moment=leaderboard&team=bayern"), later, out], note: note("the leaderboard from the trophy in the FanZone header; tap a fan to open their card.") };
    PAGES.team = { phones: [cur("moment=team"), later, out], note: note("Choose your team when you enter FanZone; your pick sets the colour of your ring and your gifts.") };
    PAGES.reactions = { phones: [cur("team=bayern"), later], note: note("the reactions next to the message field float up the chat.") };
    PAGES.sending = { phones: [cur("team=bayern"), later], note: note("tap the Message field, type on the keyboard and send.") };
    PAGES.actions = { phones: [cur("team=bayern"), later, out], note: note("long-press a message to focus it and report it.") };
  })();
  function pageStatus(id) { var pg = PAGES[id]; return pg ? (pg.ready ? "Ready" : "Current") : "Soon"; }
  // a phone in a feature page: the real prototype with the panel's settings, opening in FanZone''')
rep("""'<span class="st' + (PAGES[f.id] ? ' ready' : '') + '">' + (PAGES[f.id] ? 'Ready' : 'Soon') + '</span>""",
    """'<span class="st' + (PAGES[f.id] ? ' ready' : '') + '">' + pageStatus(f.id) + '</span>""")
open(p, 'w', encoding='utf-8').write(s); print('ok')
