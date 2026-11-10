#!/usr/bin/env python3
"""FanZone message bar: two states with a swipe between them.

  State 1: avatar + Message field (+ the first reactions peeking).  State 2: the bar slid left, all reactions.
  - A drag that starts anywhere on the bar, the Message field included, switches states (it used to start a
    text selection in the field instead); a plain tap on the field still focuses it.
  - Trackpad / touch scrolling snaps to exactly one of the two states (only two snap points).

Run after fanzone-figma.py:  python3 tools/fanzone-bar.py FanZone.dc.html
"""
import sys

PATH = sys.argv[1]
src = open(PATH, encoding='utf-8').read()

def rep(old, new, count=1):
    global src
    n = src.count(old)
    if n != count:
        raise SystemExit(f'expected {count} occurrence(s), found {n}: {old[:100]!r}')
    src = src.replace(old, new)

# two snap points only: the avatar (state 1) and the end of the reactions (state 2)
rep('overflow-x:auto;scroll-snap-type:x proximity;height:72px;cursor:grab;',
    'overflow-x:auto;scroll-snap-type:x mandatory;height:72px;cursor:grab;')
rep('<img src="{{ r }}" alt="" style="scroll-snap-align:end;flex-shrink:0;width:40px;height:40px;margin:-2px;',
    '<img src="{{ r }}" alt="" style="flex-shrink:0;width:40px;height:40px;margin:-2px;')
rep('            <div style="display:flex;align-items:center;gap:8px;flex-shrink:0;height:48px;">\n              <sc-for list="{{ reactions }}"',
    '            <div style="display:flex;align-items:center;gap:8px;flex-shrink:0;height:48px;scroll-snap-align:end;">\n              <sc-for list="{{ reactions }}"')

# drag from the Message field too: don't let the field start a text selection; focus it on a plain tap
rep('''    el.addEventListener("pointerdown", (e) => {
      down = true; moved = false; captured = false; startX = e.clientX; startLeft = el.scrollLeft;
    });''',
'''    let fieldTap = null;
    el.addEventListener("dragstart", (e) => e.preventDefault()); // the reaction images must not start a native image drag
    el.addEventListener("pointerdown", (e) => {
      down = true; moved = false; captured = false; startX = e.clientX; startLeft = el.scrollLeft;
      fieldTap = (e.pointerType === "mouse" && e.target && e.target.tagName === "INPUT") ? e.target : null;
      if (fieldTap && document.activeElement !== fieldTap) e.preventDefault();
    });''')
rep('''      down = false; el.style.cursor = "grab";
      if (!moved) return;''',
'''      down = false; el.style.cursor = "grab";
      if (!moved) { if (fieldTap) { try { fieldTap.focus(); } catch (err) {} } return; }''')
# the swipe direction decides (about 40px is enough), not passing half the bar
rep('''      const page = el.clientWidth - 82;
      const target = el.scrollLeft > page / 2 ? el.scrollWidth : 0;''',
'''      const dragged = el.scrollLeft - startLeft;
      const target = dragged > 40 ? el.scrollWidth : (dragged < -40 ? 0 : startLeft);''')
rep('''      el.style.scrollSnapType = "x proximity";
      el.scrollTo({ left: target, behavior: "smooth" });''',
'''      el.scrollTo({ left: target, behavior: "smooth" });
      clearTimeout(el._snapT); el._snapT = setTimeout(() => { el.style.scrollSnapType = "x mandatory"; }, 450);''')

open(PATH, 'w', encoding='utf-8').write(src)
print('ok')
