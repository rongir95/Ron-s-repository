"""Live updates page: two phones, Red card and Goal."""
import sys
p = sys.argv[1]; s = open(p).read()
def rep(a, b):
    global s
    assert s.count(a) == 1, a[:80]
    s = s.replace(a, b)
rep('"kind": "new", "screens": 1}', '"kind": "new", "screens": 2}')
rep('PAGES.liveupdates = { phones: [{ q: "moment=liveupdate&team=bayern" }], note: "<b>New:</b> match events show up in FanZone. A red card takes over the chat for a few seconds, then drops into the chat as a card and scrolls up with the messages." };',
    'PAGES.liveupdates = { phones: [{ q: "moment=liveupdate&team=bayern", label: "Red card" }, { q: "moment=liveupdate&lu=goal&team=bayern", label: "Goal" }], note: "<b>New:</b> match events show up in FanZone. The event takes over the chat for a few seconds, then drops into the chat as a card and scrolls up with the messages. A goal card opens to show where it was scored." };')
open(p, 'w').write(s); print("liveupdates-goal-page ok")
