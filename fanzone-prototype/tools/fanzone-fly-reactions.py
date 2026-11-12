#!/usr/bin/env python3
"""FanZone: tapping a reaction next to the message field sends a copy of it up the chat.

  - The copy appears right above the reaction you tapped, pops a little, then rises to the top of
    the chat, swaying from side to side, getting smaller and fading out on the way (about 1.8s).
  - You can tap again and again; every tap sends its own copy.
  - The copies sit over the chat and do not take taps.

Run after the other scripts:  python3 tools/fanzone-fly-reactions.py FanZone.dc.html
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

# the reactions take a tap
rep('<img src="{{ r }}" alt="" draggable="false" style="flex-shrink:0;width:40px;height:40px;margin:-2px;object-fit:contain;cursor:pointer;">',
    '<img src="{{ r }}" alt="" role="button" aria-label="Send reaction" onClick="{{ flyReaction }}" draggable="false" style="flex-shrink:0;width:40px;height:40px;margin:-2px;object-fit:contain;cursor:pointer;">')

# the flying copies live on the message bar (it is not clipped), positioned from the tapped reaction
rep('''        <!-- message bar -->
        <div style="position:relative;display:flex;align-items:center;gap:12px;padding:8px 0;height:72px;box-sizing:border-box;background:#0C161C;">
''', '''        <!-- message bar -->
        <div data-fz-msgbar="1" style="position:relative;display:flex;align-items:center;gap:12px;padding:8px 0;height:72px;box-sizing:border-box;background:#0C161C;">
          <!-- reactions you send float up the chat -->
          <sc-for list="{{ flyList }}" as="f" hint-placeholder-count="0">
            <span aria-hidden="true" style="position:absolute;left:{{ f.x }}px;top:{{ f.y }}px;width:40px;height:40px;z-index:9;pointer-events:none;--rise:{{ f.rise }}px;--sway:{{ f.sway }}px;animation:fzFlyUp 1.8s cubic-bezier(.33,.0,.4,1) both;">
              <img src="{{ f.src }}" alt="" width="40" height="40" draggable="false" style="display:block;width:40px;height:40px;object-fit:contain;animation:fzFlySway 1.8s ease-in-out both;">
            </span>
          </sc-for>
''')

rep('  @keyframes fzPushIn {',
    '  @keyframes fzFlyUp { 0% { transform: translateY(0) scale(.6); opacity: 0; } 8% { transform: translateY(-46px) scale(1.15); opacity: 1; } 16% { transform: translateY(-58px) scale(1); opacity: 1; } 55% { opacity: .9; } 100% { transform: translateY(calc(-1 * var(--rise))) scale(.35); opacity: 0; } }\n'
    '  @keyframes fzFlySway { 0%, 16% { transform: none; } 40% { transform: translateX(var(--sway)) rotate(6deg); } 65% { transform: translateX(calc(-1 * var(--sway))) rotate(-6deg); } 100% { transform: translateX(calc(var(--sway) / 2)); } }\n'
    '  @keyframes fzPushIn {')

LOGIC = '''  // Reactions by the message field float up the chat
  flyReaction = (e) => {
    const img = e && e.currentTarget;
    const bar = img && img.closest("[data-fz-msgbar]");
    if (!bar) return;
    const ir = img.getBoundingClientRect(), br = bar.getBoundingClientRect();
    const col = bar.parentElement ? bar.parentElement.getBoundingClientRect() : br;
    const zoom = br.width ? bar.offsetWidth / br.width : 1;
    const x = (ir.left - br.left) * zoom, y = (ir.top - br.top) * zoom;
    // up to just under the FanZone header (48px)
    const rise = Math.max(160, (ir.top - col.top) * zoom - 48 - 20);
    const n = (this._flyN = (this._flyN || 0) + 1);
    const sway = (n % 2 ? 1 : -1) * (8 + (n * 7) % 10);
    this.setState(st => ({ flyList: [...(st.flyList || []), { id: n, src: img.getAttribute("src"), x: Math.round(x), y: Math.round(y), rise: Math.round(rise), sway }] }));
    clearTimeout(this._flyT);
    this._flyT = setTimeout(() => this.setState({ flyList: [] }), 1900);
  };
  openFanZoneOver = (e) => {'''
rep('  openFanZoneOver = (e) => {', LOGIC)
rep('      ...this.gzVals(),', '      ...this.gzVals(),\n      flyList: this.state.screen === "fanzone" ? (this.state.flyList || []) : [], flyReaction: this.flyReaction,')

open(PATH, 'w', encoding='utf-8').write(src)
print('ok')
