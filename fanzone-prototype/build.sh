#!/usr/bin/env bash
# Rebuilds FanZone.dc.html from the two source prototypes in sources/.
# FanZone.dc.html is generated: change the scripts in tools/ (or the sources), never the output.
set -euo pipefail
cd "$(dirname "$0")"
OUT=FanZone.dc.html
python3 tools/merge-prototypes.py "sources/Personal Fan Card.dc.html" "sources/Comments & Replies.dc.html" "$OUT"
for t in add-poll fanzone-entry fanzone-panel chat-bayern-bvb fan-status fanzone-figma chat-avatars fanzone-bar fanzone-giphy vector-assets ios-keyboard fixture-reactions fanzone-team; do
  python3 "tools/$t.py" "$OUT"
done
echo "Built $OUT"
