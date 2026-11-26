"""Standalone predictions: Scores (Predict, drawer, predicted) and the match page, both coded."""
import sys
p = sys.argv[1]; s = open(p).read()
a = '    PAGES.focus = {'
assert s.count(a) == 1
s = s.replace(a, '    PAGES.predictions = { phones: [{ src: "screens.html?v=predict", label: "Scores" }, { src: "screens.html?v=predictfix", label: "Match page" }], note: "<b>New:</b> predictions outside FanZone. On Scores, tap Predict under a match: the drawer opens, pick an answer and it shows your prediction. The match page has the prediction card too." };\n' + a)
open(p, 'w').write(s); print("predict-page ok")
