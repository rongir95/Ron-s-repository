#!/usr/bin/env python3
"""FanZone panel options:
  - Collapse / expand: the icon (or the title) in the panel header slides the panel down to just
    its header bar, so the match page shows; tapping it again brings the panel back.
  - The "Meet your Fan Card" tip in FanZone and the "Let's make a unique fan profile" tip on Home
    are off by default; the shell turns them on (?fancardtip=1, ?hometip=1).

Run after fanzone-entry.py:  python3 tools/fanzone-panel.py FanZone.dc.html
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

# the opening animation must not hold the transform, so the collapse transform can apply after it
rep("  .fz-over-panel { animation: fzOverIn .38s cubic-bezier(.22,1,.36,1) both; }",
    "  .fz-over-panel { animation: fzOverIn .38s cubic-bezier(.22,1,.36,1) backwards; }\n"
    "  .fz-collapse-btn:focus-visible { outline: 2px solid #F9FAFA; outline-offset: 2px; border-radius: 6px; }")

# panel: slides down to its header when collapsed
rep('<div class="{{ fzPanelCls }}" style="position:absolute;left:0;right:0;bottom:0;top:{{ fzPanelTop }}px;transition:top .55s cubic-bezier(.22,1,.36,1);pointer-events:auto;',
    '<div class="{{ fzPanelCls }}" style="position:absolute;left:0;right:0;bottom:0;top:{{ fzPanelTop }}px;transform:{{ fzPanelTransform }};transition:top .55s cubic-bezier(.22,1,.36,1),transform .45s cubic-bezier(.22,1,.36,1);pointer-events:auto;')

# header: the collapse icon + title become one button
rep('''          <svg width="20" height="20" viewBox="0 0 20 20" fill="none" style="flex-shrink:0;">
            <path d="M17 6H3" stroke="#F9FAFA" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"></path>
            <path d="M14.667 15.667L10 11L5.333 15.667" stroke="#F9FAFA" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"></path>
          </svg>
          <span style="font-size:17px;font-weight:700;letter-spacing:-.01em;color:#F9FAFA;">FanZone</span>''',
'''          <button class="fz-collapse-btn" onClick="{{ toggleFzCollapse }}" aria-label="{{ fzCollapseLabel }}" aria-expanded="{{ fzExpandedAttr }}" style="display:flex;align-items:center;gap:16px;border:0;padding:8px 6px;margin:-8px -6px;background:transparent;cursor:pointer;font-family:inherit;">
            <svg width="20" height="20" viewBox="0 0 20 20" fill="none" aria-hidden="true" style="flex-shrink:0;transform:rotate({{ fzCollapseRot }}deg);transition:transform .3s ease;">
              <path d="M17 6H3" stroke="#F9FAFA" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"></path>
              <path d="M14.667 15.667L10 11L5.333 15.667" stroke="#F9FAFA" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"></path>
            </svg>
            <span style="font-size:17px;font-weight:700;letter-spacing:-.01em;color:#F9FAFA;">FanZone</span>
          </button>''')

# state + values
rep('    this.setState({ screen: "fanzone", fanzoneFrom: "fixture", fzOver: true, fzLoading: true,',
    '    this.setState({ screen: "fanzone", fanzoneFrom: "fixture", fzOver: true, fzLoading: true, fzCollapsed: false,')
rep('      openFanZoneOver: this.openFanZoneOver,',
    '      openFanZoneOver: this.openFanZoneOver,\n'
    '      fzPanelTransform: s.fzCollapsed ? "translateY(calc(100% - 68px))" : "none",\n'
    '      toggleFzCollapse: () => this.setState({ fzCollapsed: !s.fzCollapsed, showFtue: false }),\n'
    '      fzCollapseLabel: s.fzCollapsed ? "Expand FanZone" : "Collapse FanZone",\n'
    '      fzExpandedAttr: s.fzCollapsed ? "false" : "true",\n'
    '      fzCollapseRot: s.fzCollapsed ? 180 : 0,')

# "Meet your Fan Card" tip: off unless the shell turns it on
rep('  startFanZoneFtue = () => {\n    clearTimeout(this._ftueTimer);\n',
    '  startFanZoneFtue = () => {\n    clearTimeout(this._ftueTimer);\n    if (this.P.fanCardTip !== true) return; // off by default; the prototype shell can turn it on\n')
rep('    if (q.get("reset") === "1") o.resetOnLoad = true;',
    '    if (q.get("reset") === "1") o.resetOnLoad = true;\n    if (q.get("fancardtip") === "1") o.fanCardTip = true;')

# every drawer (FanZone included) has the same 24px top corners
rep('border-radius:12px 12px 0 0', 'border-radius:24px 24px 0 0', count=3)

# poll inside the drawer: hidden while the drawer is collapsed (only the header shows)
rep('<div style="position:absolute;left:0;right:0;top:48px;z-index:2;height:{{ pollClipH }}px;overflow:hidden;pointer-events:none;">',
    '<div style="position:absolute;left:0;right:0;top:48px;z-index:2;height:{{ pollClipH }}px;overflow:hidden;pointer-events:none;transition:opacity .25s ease;{{ fzPollWrapStyle }}">')
rep('      fzCollapseRot: s.fzCollapsed ? 180 : 0,',
    '      fzCollapseRot: s.fzCollapsed ? 180 : 0,\n      fzPollWrapStyle: s.fzCollapsed ? "opacity:0;visibility:hidden;" : "",')

# ---------------------------------------------------------------- FanZone: write and send a message
rep('              <span style="flex:1;color:#7C868C;font-size:16px;">Message</span>\n              <svg width="22" height="22" viewBox="0 0 24 24" fill="none" style="flex-shrink:0;">',
    '              <input class="fz-msg-input" type="text" value="{{ fzDraft }}" onInput="{{ onFzDraft }}" onKeyDown="{{ onFzKey }}" placeholder="Message" aria-label="Message" maxlength="200" enterkeyhint="send" autocomplete="off" style="flex:1;min-width:0;border:0;outline:0;background:transparent;color:#F9FAFA;font-size:16px;font-family:inherit;padding:0;margin:0;">\n'
    '              <sc-if value="{{ fzHasDraft }}" hint-placeholder-val="{{ false }}">\n'
    '                <button onClick="{{ sendFzMessage }}" aria-label="Send message" style="flex-shrink:0;width:36px;height:36px;margin-right:-8px;border:0;padding:0;border-radius:50%;background:#F9FAFA;display:flex;align-items:center;justify-content:center;cursor:pointer;"><svg width="18" height="18" viewBox="335 69 18 18" aria-hidden="true"><path d="M337.004 71.9394C336.683 70.6769 338.031 69.6447 339.166 70.2831L350.59 76.7089C351.597 77.2753 351.597 78.7255 350.59 79.2919L339.166 85.7177C338.031 86.3562 336.683 85.3239 337.004 84.0615L337.891 80.5673L341.227 78.6415C341.721 78.3564 341.721 77.6435 341.227 77.3583L337.891 75.4316L337.004 71.9394Z" fill="#1B2326"></path></svg></button>\n'
    '              </sc-if>\n'
    '              <svg width="22" height="22" viewBox="0 0 24 24" fill="none" style="flex-shrink:0;{{ fzStickerStyle }}">')
rep("  .fz-collapse-btn:focus-visible {",
    "  .fz-msg-input::placeholder { color: #7C868C; opacity: 1; }\n  .fz-collapse-btn:focus-visible {")
rep('        return { ...m, stroke: t ? t.card : "#F2C400", imgScale: "transform:scale(1.05);", onOpen: () => this.openUserCard(m) };',
    '        // my messages: the same ring as my avatar next to the Message field (my favorite team, or the default gradient)\n'
    '        if (m.mine) { const myFav = s.favoriteId ? teamById(s.favoriteId) : null; return { ...m, ring: myFav ? myFav.card : "linear-gradient(210deg,#8923A0 0%,#F1A322 38%,#FFFA00 100%)", imgScale: "", onOpen: this.openCard }; }\n'
    '        return { ...m, ring: t ? t.card : "#F2C400", imgScale: "transform:scale(1.05);", onOpen: () => this.openUserCard(m) };')
# chat avatars: the ring is drawn as a background so it can be a team color or a gradient
rep('<div onClick="{{ m.onOpen }}" style="width:26px;height:26px;border-radius:50%;flex-shrink:0;overflow:hidden;cursor:pointer;box-shadow:0 0 0 1.5px {{ m.stroke }};border:1px solid #080E12;">',
    '<div onClick="{{ m.onOpen }}" style="width:24px;height:24px;border-radius:50%;flex-shrink:0;overflow:hidden;cursor:pointer;box-sizing:content-box;border:1.5px solid transparent;padding:1px;margin:-1.5px;background:linear-gradient(#080E12,#080E12) padding-box,{{ m.ring }} border-box;">')
rep('  openFanZoneOver = (e) => {',
    '''  onFzDraft = (e) => this.setState({ fzDraft: String((e && e.target && e.target.value) || "").slice(0, 200) });
  onFzKey = (e) => { if (e && e.key === "Enter" && !e.shiftKey) { e.preventDefault(); this.sendFzMessage(); } };
  sendFzMessage = () => {
    const text = (this.state.fzDraft || "").trim();
    if (!text) return;
    const s = this.state;
    const av = s.avatar && AV_MAP[s.avatar] && AV_MAP[s.avatar].src ? AV_MAP[s.avatar].src : "assets/comments/avin.png";
    const msg = { id: "me" + Date.now(), name: s.nickname || "Charlie", avatar: av, text, mine: true };
    this.setState(st => ({ feed: st.feed.concat(msg).slice(-40), fzDraft: "", atBottom: true, showFtue: false }));
  };
  openFanZoneOver = (e) => {''')
rep('      openFanZoneOver: this.openFanZoneOver,',
    '      openFanZoneOver: this.openFanZoneOver,\n'
    '      fzDraft: s.fzDraft || "",\n'
    '      fzHasDraft: !!(s.fzDraft || "").trim(),\n'
    '      fzStickerStyle: (s.fzDraft || "").trim() ? "display:none;" : "",\n'
    '      onFzDraft: this.onFzDraft, onFzKey: this.onFzKey, sendFzMessage: this.sendFzMessage,')

# "Let's make a unique fan profile" tip on Home: off unless the shell turns it on (?hometip=1)
rep('      this._homeTipTimer = setTimeout(() => { if (!this.state.sheet && this.state.screen === "home") this.setState({ showHomeTip: true }); }, 2000);',
    '      if (this.P.homeTip === true) this._homeTipTimer = setTimeout(() => { if (!this.state.sheet && this.state.screen === "home") this.setState({ showHomeTip: true }); }, 2000);')
rep('    if (q.get("fancardtip") === "1") o.fanCardTip = true;',
    '    if (q.get("fancardtip") === "1") o.fanCardTip = true;\n    if (q.get("hometip") === "1") o.homeTip = true;')

open(PATH, 'w', encoding='utf-8').write(src)
print('ok')
