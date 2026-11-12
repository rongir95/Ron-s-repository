#!/usr/bin/env python3
"""Who reacted: tapping the reactions summary on the match page (the emojis + 2.1K next to the heart) opens a
drawer, per Figma "[DEV] Reactions 1.1" (file 1obxU2PGY0rkO25zHwpy9p): loader node 13746:38741, list node 13746:38645.

  - The video dims behind the drawer; the drawer has our standard grabber and close X.
  - Loader (0.9s): rows of a 52px circle and two bars (#3D4549).
  - List: 52px avatar in the fan's team ring (or the initial), name 14px bold, the fan's reactions (16px).
    If you reacted, you are first.

Run after fixture-reactions.py:  python3 tools/fixture-reaction-list.py FanZone.dc.html
"""
import json, sys

PATH = sys.argv[1]
src = open(PATH, encoding='utf-8').read()

def rep(old, new, count=1):
    global src
    n = src.count(old)
    if n != count:
        raise SystemExit(f'expected {count} occurrence(s), found {n}: {old[:100]!r}')
    src = src.replace(old, new)

FONT = "font-family:'DAZN Oscine',sans-serif;"

# the summary becomes a button
rep('<span style="min-height:32px;box-sizing:border-box;padding:4px 12px;border-radius:0 9999px 9999px 0;background:#242D33;display:flex;align-items:center;gap:6px;"><img src="assets/fixture/emojis.png"',
    '<span onClick="{{ openRxList }}" role="button" aria-label="See who reacted" style="cursor:pointer;min-height:32px;box-sizing:border-box;padding:4px 12px;border-radius:0 9999px 9999px 0;background:#242D33;display:flex;align-items:center;gap:6px;"><img src="assets/fixture/emojis.png"')

SKROW = ('<div style="display:flex;align-items:center;gap:16px;height:72px;padding:0 16px;">'
         '<span style="width:52px;height:52px;border-radius:50%;background:#3D4549;flex-shrink:0;"></span>'
         '<span style="display:flex;flex-direction:column;gap:10px;"><span style="display:block;width:88px;height:8px;border-radius:4px;background:#3D4549;"></span>'
         '<span style="display:block;width:152px;height:6px;border-radius:3px;background:#3D4549;"></span></span></div>')

DRAWER = '''    <!-- Who reacted (Figma 1obxU2PGY0rkO25zHwpy9p 13746:38741 loader / 13746:38645 list) -->
    <sc-if value="{{ rxListOn }}" hint-placeholder-val="{{ false }}">
      <div onClick="{{ closeRxList }}" style="position:absolute;inset:0;z-index:40;background:rgba(8,14,18,.6);animation:fzFadeIn .2s ease;"></div>
      <div role="dialog" aria-label="Reactions" style="position:absolute;left:0;right:0;top:282px;bottom:0;z-index:41;display:flex;flex-direction:column;border-radius:24px 24px 0 0;background:#1B2326;box-shadow:0 -1px 0 rgba(249,250,250,.2);overflow:hidden;animation:fzSlideUp .32s cubic-bezier(.22,1,.36,1);''' + FONT + '''">
        <div style="position:relative;height:48px;flex-shrink:0;">
          <span aria-hidden="true" style="position:absolute;left:50%;top:8px;transform:translateX(-50%);width:44px;height:4px;border-radius:9999px;background:#CED0D2;"></span>
          <button onClick="{{ closeRxList }}" aria-label="Close" title="Close" style="position:absolute;right:16px;top:16px;width:32px;height:32px;border:0;padding:0;border-radius:9999px;background:rgba(255,255,255,.2);display:flex;align-items:center;justify-content:center;cursor:pointer;"><svg width="20" height="20" viewBox="0 0 20 20" fill="none" style="display:block;"><path d="M5 5L15 15M15 5L5 15" stroke="#F9FAFA" stroke-width="1.6" stroke-linecap="round"></path></svg></button>
        </div>
        <div class="fz-scroll" style="flex:1;min-height:0;overflow-y:auto;padding:4px 0 28px;">
          <sc-if value="{{ rxListLoading }}" hint-placeholder-val="{{ true }}">''' + SKROW * 7 + '''</sc-if>
          <sc-if value="{{ rxListReady }}" hint-placeholder-val="{{ false }}">
            <sc-for list="{{ rxListRows }}" as="r" hint-placeholder-count="7">
              <div style="display:flex;align-items:center;gap:16px;height:72px;padding:0 16px;animation:fzMsgIn .35s cubic-bezier(.22,1,.36,1);">
                <span style="width:52px;height:52px;border-radius:50%;flex-shrink:0;box-sizing:border-box;border:3px solid transparent;padding:2px;background:linear-gradient(#1B2326,#1B2326) padding-box,{{ r.ring }} border-box;">
                  <span style="display:flex;align-items:center;justify-content:center;width:100%;height:100%;border-radius:50%;overflow:hidden;background:#080E12;color:#F9FAFA;font-weight:700;font-size:20px;">
                    <sc-if value="{{ r.hasImg }}" hint-placeholder-val="{{ true }}"><img src="{{ r.avatar }}" alt="" style="display:block;width:100%;height:100%;object-fit:cover;{{ r.scale }}"></sc-if>
                    <sc-if value="{{ r.noImg }}" hint-placeholder-val="{{ false }}">{{ r.initial }}</sc-if>
                  </span>
                </span>
                <span style="display:flex;flex-direction:column;gap:4px;min-width:0;">
                  <span style="font-weight:700;font-size:14px;line-height:20px;color:#F9FAFA;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">{{ r.name }}</span>
                  <span style="display:flex;align-items:center;">
                    <sc-for list="{{ r.rx }}" as="e" hint-placeholder-count="3"><img src="{{ e.src }}" alt="{{ e.id }}" width="18" height="18" style="display:block;margin-right:-4px;"></sc-for>
                  </span>
                </span>
              </div>
            </sc-for>
          </sc-if>
        </div>
      </div>
    </sc-if>

'''
rep('    <!-- ===================== COMMENTS & REPLIES OVERLAYS ===================== -->',
    DRAWER + '    <!-- ===================== COMMENTS & REPLIES OVERLAYS ===================== -->')

# fans who reacted: chat fans, their team ring and their reactions
FANS = [("Ayaka", "uploads/11.png", "#DC052D", ["like"]),
        ("Kaito", "", "#FDE100", ["like", "happy", "cheer"]),
        ("Hina", "uploads/12.png", "#DC052D", ["like", "wow"]),
        ("Ren", "uploads/13.png", "#FDE100", ["cheer", "happy"]),
        ("Sora", "uploads/14.png", "#DC052D", ["like", "happy", "cheer"]),
        ("Misaki", "uploads/17.png", "#FDE100", ["angry"]),
        ("Riku", "uploads/18.png", "#DC052D", ["like", "cheer"]),
        ("Haruto", "uploads/19.png", "#FDE100", ["sad", "like"]),
        ("Nao", "uploads/8.png", "#DC052D", ["happy"])]

LOGIC = '''  // Who reacted (match page)
  openRxList = (e) => {
    if (e && e.stopPropagation) e.stopPropagation();
    clearTimeout(this._rxlT);
    this.setState({ rxList: true, rxListLoading: true });
    this._rxlT = setTimeout(() => this.setState({ rxListLoading: false }), 900);
  };
  closeRxList = () => { clearTimeout(this._rxlT); this.setState({ rxList: false }); };
  rxListVals() {
    const s = this.state;
    const on = !!s.rxList && s.screen === "fixture";
    const R = (ids) => ids.map(id => ({ id, src: "assets/reactions/" + id + ".png" }));
    const rows = RX_FANS.map(([name, avatar, ring, rx]) => ({ id: name, name, avatar, ring, hasImg: !!avatar, noImg: !avatar,
      initial: name.charAt(0), scale: /(^|\\/)uploads\\//.test(avatar) ? "transform:scale(1.25);clip-path:circle(40%);" : "", rx: R(rx) }));
    if (s.fixRx) {
      const av = s.avatar && AV_MAP[s.avatar] && AV_MAP[s.avatar].src ? AV_MAP[s.avatar].src : "";
      const fav = s.favoriteId ? teamById(s.favoriteId) : null;
      rows.unshift({ id: "me", name: (s.nickname || "Charlie") + " (you)", avatar: av, ring: fav ? fav.card : "linear-gradient(210deg,#8923A0 0%,#F1A322 38%,#FFFA00 100%)",
        hasImg: !!av, noImg: !av, initial: String(s.nickname || "C").charAt(0).toUpperCase(), scale: /(^|\\/)uploads\\//.test(av) ? "transform:scale(1.25);clip-path:circle(40%);" : "", rx: R([s.fixRx]) });
    }
    return { rxListOn: on, openRxList: this.openRxList, closeRxList: this.closeRxList,
      rxListLoading: on && !!s.rxListLoading, rxListReady: on && !s.rxListLoading, rxListRows: rows };
  }
  openFanZoneOver = (e) => {'''
rep('  openFanZoneOver = (e) => {', LOGIC)
rep('      ...this.gzVals(),', '      ...this.gzVals(),\n      ...this.rxListVals(),')
rep('// FanZone chat: which team each fan supports', '// Who reacted on the match page\nconst RX_FANS = ' + json.dumps(FANS) + ';\n// FanZone chat: which team each fan supports')

open(PATH, 'w', encoding='utf-8').write(src)
print('ok')
