"""Remove Landscape activations; move Predictions and FanZone as a drawer/tab to New."""
import sys
p = sys.argv[1]; s = open(p).read()
rep = [
  (', {"id": "landscape", "name": "Landscape activations", "cat": "Activations", "kind": "imp", "screens": 3}', ''),
  ('{"id": "predictions", "name": "Predictions + Leaderboard", "cat": "General", "kind": "imp", "screens": 3}', '{"id": "predictions", "name": "Predictions + Leaderboard", "cat": "General", "kind": "new", "screens": 2}'),
  ('{"id": "drawertab", "name": "FanZone as a drawer/tab", "cat": "General", "kind": "imp", "screens": 3}', '{"id": "drawertab", "name": "FanZone as a drawer/tab", "cat": "General", "kind": "new", "screens": 2}'),
]
for a, b in rep:
    assert s.count(a) == 1, a[:60]
    s = s.replace(a, b)
open(p, 'w').write(s); print("new-moves ok")
