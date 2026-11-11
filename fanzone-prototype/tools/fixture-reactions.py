#!/usr/bin/env python3
"""Reactions on the match page heart, per FanZone DS "Fixture 2.0" (file NIgPxOlNU4U3sWMRdoE4Qh,
node 12521:35078) and the "Reaction btn" component (node 12521:19434).

  Tap the heart          -> like (red heart) / unlike (outline heart)
  Long press the heart   -> the reaction picker opens above it: a 280x52 pill (#242D33, 1px white 20% border,
                            background blur 30), six 48px reactions 44px apart: like, happy, cheering,
                            mind blown, angry, sad
  Pick a reaction        -> it replaces the heart in the button; tap the button again to remove it
  Tap outside            -> closes the picker

The picker sits outside the horizontally scrolling action row so it isn't clipped.

Run after the other scripts:  python3 tools/fixture-reactions.py FanZone.dc.html
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

HEART = ('<svg width="24" height="24" viewBox="0 0 24 24" fill="none" aria-hidden="true" style="display:block;">'
         '<path d="M12 20.3s-7.6-4.6-9.1-9.4C1.9 7.7 3.9 4.7 7 4.7c2 0 3.6 1.1 5 2.9 1.4-1.8 3-2.9 5-2.9 3.1 0 5.1 3 4.1 6.2-1.5 4.8-9.1 9.3-9.1 9.3z" '
         'stroke="#F9FAFA" stroke-width="2" stroke-linejoin="round"/></svg>')

# ---------------------------------------------------------------- markup
# the heart becomes a button: outline heart, or the reaction you picked
rep('<span style="min-height:32px;box-sizing:border-box;padding:4px 12px;border-radius:9999px 0 0 9999px;background:#242D33;display:flex;align-items:center;"><img src="assets/fixture/like.png" alt="" width="24" height="24" style="display:block;"></span>',
    '<button onPointerDown="{{ fixRxDown }}" onPointerUp="{{ fixRxUp }}" onPointerLeave="{{ fixRxCancel }}" onPointerCancel="{{ fixRxCancel }}" onContextMenu="{{ fixRxNoMenu }}" '
    'aria-label="{{ fixRxLabel }}" title="Tap to like, press and hold for more reactions" '
    'style="min-height:32px;box-sizing:border-box;padding:4px 12px;border:0;border-radius:9999px 0 0 9999px;background:#242D33;display:flex;align-items:center;cursor:pointer;-webkit-touch-callout:none;user-select:none;touch-action:manipulation;">'
    '<sc-if value="{{ fixRxNone }}" hint-placeholder-val="{{ true }}">' + HEART + '</sc-if>'
    '<sc-if value="{{ fixRxSome }}" hint-placeholder-val="{{ false }}"><img src="{{ fixRxSrc }}" alt="" width="24" height="24" draggable="false" style="display:block;animation:fzRxPop .28s cubic-bezier(.22,1.6,.36,1);"></sc-if>'
    '</button>')

PICKER = '''<div style="position:relative;">
          <sc-if value="{{ fixRxOpen }}" hint-placeholder-val="{{ false }}">
            <div onClick="{{ fixRxClose }}" style="position:fixed;inset:0;z-index:30;"></div>
            <div role="menu" aria-label="Reactions" style="position:absolute;left:16px;bottom:calc(100% - 4px);z-index:31;width:280px;height:52px;box-sizing:border-box;border-radius:9999px;background:rgba(36,45,51,.92);border:1px solid rgba(249,250,250,.2);-webkit-backdrop-filter:blur(30px);backdrop-filter:blur(30px);animation:fzRxIn .22s cubic-bezier(.22,1,.36,1);transform-origin:24px 100%;">
              <sc-for list="{{ fixRxItems }}" as="r" hint-placeholder-count="6">
                <button role="menuitem" class="fz-rx" onClick="{{ r.pick }}" aria-label="{{ r.name }}" style="position:absolute;top:1px;left:{{ r.x }}px;width:48px;height:48px;border:0;padding:0;background:transparent;cursor:pointer;"><img src="{{ r.src }}" alt="" width="48" height="48" draggable="false" style="display:block;"></button>
              </sc-for>
            </div>
          </sc-if>
          <div class="fz-scroll" style="padding:6px 0 6px 16px;'''
rep('<div class="fz-scroll" style="padding:6px 0 6px 16px;', PICKER)
# close the new wrapper after the action row
rep('            <span style="flex-shrink:0;width:8px;"></span>\n          </div>\n          <!-- FanZone card',
    '            <span style="flex-shrink:0;width:8px;"></span>\n          </div>\n          </div>\n          <!-- FanZone card')

# ---------------------------------------------------------------- CSS
rep('  @keyframes fzPushIn {',
    '  @keyframes fzRxIn { from { opacity: 0; transform: scale(.6) translateY(8px); } to { opacity: 1; transform: none; } }\n'
    '  @keyframes fzRxPop { 0% { transform: scale(.4); } 100% { transform: scale(1); } }\n'
    '  .fz-rx { transition: transform .15s ease; }\n'
    '  .fz-rx:hover { transform: translateY(-6px) scale(1.18); }\n'
    '  @keyframes fzPushIn {')

# ---------------------------------------------------------------- logic
LOGIC = '''  // match page heart: tap = like / unlike, long press = reaction picker (FanZone DS "Reaction btn")
  fixRxDown = (e) => {
    clearTimeout(this._fixRxT);
    this._fixRxLong = false;
    this._fixRxT = setTimeout(() => { this._fixRxLong = true; this.setState({ fixRxOpen: true }); }, 420);
  };
  fixRxUp = () => {
    clearTimeout(this._fixRxT);
    if (this._fixRxLong) return;            // the press opened the picker
    this.setState(s => ({ fixRx: s.fixRx ? null : "like" }));
  };
  fixRxCancel = () => { clearTimeout(this._fixRxT); };
  fixRxNoMenu = (e) => { if (e && e.preventDefault) e.preventDefault(); };
  fixRxClose = () => this.setState({ fixRxOpen: false });
  fixRxVals() {
    const s = this.state;
    const R = [["like", "Like"], ["happy", "Happy"], ["cheer", "Cheering"], ["wow", "Mind blown"], ["angry", "Angry"], ["sad", "Sad"]];
    return {
      fixRxOpen: !!s.fixRxOpen, fixRxClose: this.fixRxClose,
      fixRxDown: this.fixRxDown, fixRxUp: this.fixRxUp, fixRxCancel: this.fixRxCancel, fixRxNoMenu: this.fixRxNoMenu,
      fixRxNone: !s.fixRx, fixRxSome: !!s.fixRx, fixRxSrc: s.fixRx ? "assets/reactions/" + s.fixRx + ".png" : "",
      fixRxLabel: s.fixRx ? "Remove your reaction" : "Like",
      fixRxItems: R.map(([id, name], i) => ({ id, name, x: 5 + i * 44, src: "assets/reactions/" + id + ".png", pick: () => this.setState({ fixRx: id, fixRxOpen: false }) })),
    };
  }
  openFanZoneOver = (e) => {'''
rep('  openFanZoneOver = (e) => {', LOGIC)
rep('      ...this.gzVals(),', '      ...this.gzVals(),\n      ...this.fixRxVals(),')

open(PATH, 'w', encoding='utf-8').write(src)
print('ok')
