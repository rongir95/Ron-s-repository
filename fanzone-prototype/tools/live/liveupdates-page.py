"""Live updates page: one New phone with the red card live update."""
import sys
p = sys.argv[1]; s = open(p).read()
def rep(a, b):
    global s
    assert s.count(a) == 1, a[:80]
    s = s.replace(a, b)
rep('{"id": "liveupdates", "name": "Live updates for the current event", "cat": "Extras", "kind": "new", "screens": 2}',
    '{"id": "liveupdates", "name": "Live updates for the current event", "cat": "Extras", "kind": "new", "screens": 1}')
rep('var labels = f.kind === "new" ? (f.screens === 3 ?', 'var labels = f.screens === 1 ? [f.kind === "new" ? "New" : "Current"] : f.kind === "new" ? (f.screens === 3 ?')
rep('    PAGES.actions = {', '    PAGES.liveupdates = { phones: [{ q: "moment=liveupdate&team=bayern" }], note: "<b>New:</b> match events show up in FanZone. A red card takes over the chat for a few seconds, then drops into the chat as a card and scrolls up with the messages." };\n    PAGES.actions = {')
open(p, 'w').write(s); print("liveupdates-page ok")
