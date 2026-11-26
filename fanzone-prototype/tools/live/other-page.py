"""New feature slide: Around the league (a key moment from another match)."""
import sys
p = sys.argv[1]; s = open(p).read()
def rep(a, b):
    global s
    assert s.count(a) == 1, a[:80]
    s = s.replace(a, b)
rep('{"id": "liveupdates", ', '{"id": "otherevent", "name": "Around the league", "cat": "Extras", "kind": "new", "screens": 1}, {"id": "liveupdates", ')
rep('var FP_ICON = {', 'var FP_ICON = {"otherevent": "globe", ')
rep('    PAGES.focus = {', '    PAGES.otherevent = { phones: [{ q: "moment=liveupdate&lu=other&team=bayern" }], note: "<b>New:</b> a key moment from another match that matters to this one. Here Leverkusen concede late, so the title race opens up for Bayern and Dortmund. It takes over the chat for a few seconds, then drops into the chat as a card." };\n    PAGES.focus = {')
open(p, 'w').write(s); print("other-page ok")
