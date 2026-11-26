"""Landscape slides: Current screens for Poll, Fan battle, Share moment; new Pinned image slide."""
import sys
p = sys.argv[1]; s = open(p).read()
def rep(a, b):
    global s
    assert s.count(a) == 1, a[:80]
    s = s.replace(a, b)
rep('{"id": "lbattle", "name": "Fan battle", "cat": "Activations", "kind": "land", "screens": 2}',
    '{"id": "lbattle", "name": "Fan battle", "cat": "Activations", "kind": "land", "screens": 2}, {"id": "lpin", "name": "Pinned image", "cat": "Activations", "kind": "land", "screens": 2}')
rep('var FP_ICON = {', 'var FP_ICON = {"lpin": "image", ')
rep('    land: [{ q: "v=current", label: "Current" }, { q: "v=share", label: "New" }],',
    '    land: [{ q: "v=sharecur", label: "Current" }, { q: "v=share", label: "New" }],')
rep('''    PAGES.lpoll = { land: [cur, nxt], note: "<b>Landscape:</b> the poll in landscape. The Current and 80-20 designs are on their way." };''',
    '''    PAGES.lpoll = { land: [{ q: "v=poll", label: "Current" }, nxt], note: "<b>Current:</b> in landscape the poll sits over the match: the question with its timer bar, and the answers under it. Tap one to vote and see the results. The 80-20 version isn't designed yet." };
    PAGES.lpin = { land: [{ q: "v=pin", label: "Current" }, nxt], note: "<b>Current:</b> in landscape the pinned image sits over the match, bottom right, with an X to close it. The 80-20 version isn't designed yet." };''')
rep('''    PAGES.lbattle = { land: [cur, nxt], note: "<b>Landscape:</b> the fan battle in landscape. The Current and 80-20 designs are on their way." };''',
    '''    PAGES.lbattle = { land: [{ q: "v=battle", label: "Current" }, nxt], note: "<b>Current:</b> in landscape the fan battle bar sits over the match with your coins and three gifts. Send a gift to push your team; fans' gifts float up the right side. The 80-20 version isn't designed yet." };''')
open(p, 'w').write(s); print("land-currents-pages ok")
