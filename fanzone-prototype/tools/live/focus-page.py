"""New feature slide: FanZone focus mode (one phone)."""
import sys
p = sys.argv[1]; s = open(p).read()
def rep(a, b):
    global s
    assert s.count(a) == 1, a[:80]
    s = s.replace(a, b)
rep('{"id": "actions", "name": "Actions on messages in FanZone", "cat": "Chat", "kind": "new", "screens": 3}',
    '{"id": "actions", "name": "Actions on messages in FanZone", "cat": "Chat", "kind": "new", "screens": 3}, {"id": "focus", "name": "FanZone focus mode", "cat": "Chat", "kind": "new", "screens": 1}')
rep('var FP_ICON = {', 'var FP_ICON = {"focus": "hand", ')
rep('    PAGES.liveupdates = {', '    PAGES.focus = { phones: [{ q: "moment=focus&team=bayern" }], note: "<b>New:</b> a toggle in the FanZone header shows only the host\'s messages. A tooltip introduces it the first time; tap the toggle to focus on the host, tap again to see everyone." };\n    PAGES.liveupdates = {')
open(p, 'w').write(s); print("focus-page ok")
