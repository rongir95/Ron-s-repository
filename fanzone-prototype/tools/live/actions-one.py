"""Actions on messages: one New phone."""
import sys
p = sys.argv[1]; s = open(p).read()
def rep(a, b):
    global s
    assert s.count(a) == 1, a[:80]
    s = s.replace(a, b)
rep('{"id": "actions", "name": "Actions on messages in FanZone", "cat": "Chat", "kind": "new", "screens": 3}', '{"id": "actions", "name": "Actions on messages in FanZone", "cat": "Chat", "kind": "new", "screens": 1}')
rep('PAGES.actions = { phones: [cur("team=bayern"), later, out], note: note("long-press a message to focus it and report it.") };',
    'PAGES.actions = { phones: [cur("team=bayern")], note: "<b>New:</b> long-press a message to focus it and report it." };')
open(p, 'w').write(s); print("actions-one ok")
