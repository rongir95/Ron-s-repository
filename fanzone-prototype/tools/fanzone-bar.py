#!/usr/bin/env python3
"""FanZone message bar: the two states of FanZone DS "Chat Input Field" (file NIgPxOlNU4U3sWMRdoE4Qh, node 13299:57986),
with a swipe between them.

  State 1: my avatar (x 12), Message field 240px (x 64), reactions start at x 316 (peeking).
  State 2: everything slides 245px left and the Message field widens to 280px: the field's right end, then
           5 reactions + the "Change team" icon button (32px, #3D4549, radius 8), ending 12px from the edge.
  - A drag from anywhere on the bar (field included) follows the finger; ~40px either way switches state.
  - A horizontal trackpad / wheel swipe switches state; a plain tap on the field still focuses it.

Run after fanzone-figma.py (and chat-avatars.py):  python3 tools/fanzone-bar.py FanZone.dc.html
"""
import re, sys

PATH = sys.argv[1]
src = open(PATH, encoding='utf-8').read()

def rep(old, new, count=1):
    global src
    n = src.count(old)
    if n != count:
        raise SystemExit(f'expected {count} occurrence(s), found {n}: {old[:100]!r}')
    src = src.replace(old, new)

SHIFT, W1, W2 = 245, 240, 280

# ---------------------------------------------------------------- markup
# the bar's own left padding moves into the sliding row, so in state 2 the field runs to the screen edge
rep('        <div style="position:relative;display:flex;align-items:center;gap:12px;padding:8px 0 8px 12px;height:72px;box-sizing:border-box;background:#0C161C;">',
    '        <div style="position:relative;display:flex;align-items:center;gap:12px;padding:8px 0;height:72px;box-sizing:border-box;background:#0C161C;">')
# the track no longer scrolls natively; an inner row slides between the two states
rep('<div class="fz-scroll" ref="{{ barRef }}" style="flex:1;min-width:0;display:flex;align-items:center;gap:12px;overflow-x:auto;scroll-snap-type:x proximity;height:72px;cursor:grab;padding-right:12px;">',
    '<div ref="{{ barRef }}" style="flex:1;min-width:0;height:72px;overflow:hidden;cursor:grab;touch-action:pan-y;">\n'
    '          <div data-fz-bar-row="1" style="display:flex;align-items:center;gap:12px;height:72px;padding-left:12px;width:max-content;transform:translateX({{ fzBarX }}px);transition:transform .35s cubic-bezier(.22,1,.36,1);">')
rep('style="position:relative;scroll-snap-align:start;border:0;padding:5px;', 'style="position:relative;border:0;padding:5px;')
rep('<div style="flex:0 0 235px;width:235px;box-sizing:border-box;display:flex;align-items:center;gap:8px;height:57px;',
    '<div style="flex:0 0 auto;width:{{ fzInputW }}px;transition:width .35s cubic-bezier(.22,1,.36,1);box-sizing:border-box;display:flex;align-items:center;gap:8px;height:57px;')
rep('<div style="display:flex;align-items:center;gap:8px;flex-shrink:0;height:48px;">\n              <sc-for list="{{ reactions }}"',
    '<div style="display:flex;align-items:center;gap:8px;flex-shrink:0;height:48px;padding-right:12px;">\n              <sc-for list="{{ reactions }}"')
rep('<img src="{{ r }}" alt="" style="scroll-snap-align:end;flex-shrink:0;width:40px;height:40px;margin:-2px;',
    '<img src="{{ r }}" alt="" draggable="false" style="flex-shrink:0;width:40px;height:40px;margin:-2px;')
# the last item is the "Change team" icon button
m = re.search(r'              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" style="flex-shrink:0;margin-left:6px;">(.*?)</svg>\n            </div>\n          </div>', src, re.S)
if not m:
    raise SystemExit('change-team icon not found')
src = (src[:m.start()]
       + '              <button aria-label="Change team" style="flex-shrink:0;width:32px;height:32px;border:0;padding:0;border-radius:8px;background:#3D4549;display:flex;align-items:center;justify-content:center;cursor:pointer;">'
       + '<img src="assets/icons/change-team.svg" alt="" width="20" height="20" style="display:block;"></button>\n'
       + '            </div>\n          </div>\n          </div>'
       + src[m.end():])

# ---------------------------------------------------------------- values
rep('      openFanZoneOver: this.openFanZoneOver,',
    '      openFanZoneOver: this.openFanZoneOver,\n'
    f'      fzBarX: s.fzBar2 ? -{SHIFT} : 0,\n'
    f'      fzInputW: s.fzBar2 ? {W2} : {W1},')

# ---------------------------------------------------------------- gesture
m = re.search(r'  barRef = \(el\) => \{\n.*?\n  \};\n', src, re.S)
if not m:
    raise SystemExit('barRef not found')
BAR = f'''  barRef = (el) => {{
    if (!el || el._dragBound) return;
    el._dragBound = true;
    const row = () => el.querySelector("[data-fz-bar-row]");
    const SHIFT = {SHIFT};
    let down = false, moved = false, startX = 0, base = 0, dx = 0, fieldTap = null;
    el.addEventListener("dragstart", (e) => e.preventDefault());
    el.addEventListener("pointerdown", (e) => {{
      down = true; moved = false; dx = 0; startX = e.clientX; base = this.state.fzBar2 ? -SHIFT : 0;
      fieldTap = (e.pointerType === "mouse" && e.target && e.target.tagName === "INPUT") ? e.target : null;
      if (fieldTap && document.activeElement !== fieldTap) e.preventDefault();
    }});
    el.addEventListener("pointermove", (e) => {{
      if (!down) return;
      dx = e.clientX - startX;
      if (!moved && Math.abs(dx) > 4) {{
        moved = true; el.style.cursor = "grabbing";
        const r = row(); if (r) r.style.transition = "none";
        try {{ el.setPointerCapture(e.pointerId); }} catch (err) {{}}
      }}
      if (moved) {{ const r = row(); if (r) r.style.transform = "translateX(" + Math.max(-SHIFT, Math.min(0, base + dx)) + "px)"; }}
    }});
    const end = () => {{
      if (!down) return;
      down = false; el.style.cursor = "grab";
      if (!moved) {{ if (fieldTap) {{ try {{ fieldTap.focus(); }} catch (err) {{}} }} return; }}
      const r = row(); if (r) {{ r.style.transition = ""; r.style.transform = ""; }}
      const want = dx < -40 ? true : (dx > 40 ? false : !!this.state.fzBar2);
      if (want !== !!this.state.fzBar2) this.setState({{ fzBar2: want }}); else this.forceUpdate();
    }};
    el.addEventListener("pointerup", end);
    el.addEventListener("pointercancel", end);
    let wheelLock = 0;
    el.addEventListener("wheel", (e) => {{
      const d = Math.abs(e.deltaX) > Math.abs(e.deltaY) ? e.deltaX : 0;
      if (!d) return;
      e.preventDefault();
      const now = Date.now(); if (now < wheelLock) return;
      if (d > 8 && !this.state.fzBar2) {{ wheelLock = now + 450; this.setState({{ fzBar2: true }}); }}
      if (d < -8 && this.state.fzBar2) {{ wheelLock = now + 450; this.setState({{ fzBar2: false }}); }}
    }}, {{ passive: false }});
    el.addEventListener("click", (e) => {{ if (moved) {{ e.stopPropagation(); e.preventDefault(); moved = false; }} }}, true);
  }};
'''
src = src[:m.start()] + BAR + src[m.end():]

open(PATH, 'w', encoding='utf-8').write(src)
print('ok')
