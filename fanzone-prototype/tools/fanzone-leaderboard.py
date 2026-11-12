#!/usr/bin/env python3
"""FanZone leaderboard, opened from the trophy in the FanZone header (FanZone DS, file NIgPxOlNU4U3sWMRdoE4Qh).

  Before any quiz   -> the empty state (node 12304:62639): outlined 2nd / 1st / 3rd places with skeleton
                       bars, a skeleton list and "Check back after the first quiz to see your ranking".
  After a quiz      -> the same skeleton while it loads (1.2s), then the leaderboard (node 12930:55217):
                       medals for the top 3, places 4-10, and your own row pinned at the bottom (white).
  The trophy turns into a white circle while the leaderboard is open; tap it again for the chat.

Every graphic is vector: medals and pictograms were exported as SVG from Figma (assets/leaderboard/).
openLeaderboard(true) is what the quiz calls when it ends. Every avatar and name opens that fan's card
(the medal and name for the top 3, yours opens your own).

Run after the other scripts:  python3 tools/fanzone-leaderboard.py FanZone.dc.html
"""
import json, re, sys

PATH = sys.argv[1]
src = open(PATH, encoding='utf-8').read()

def rep(old, new, count=1):
    global src
    n = src.count(old)
    if n != count:
        raise SystemExit(f'expected {count} occurrence(s), found {n}: {old[:100]!r}')
    src = src.replace(old, new)

FONT = "font-family:'DAZN Oscine',sans-serif;"

# ---------------------------------------------------------------- trophy button (both headers)
TROPHY = '<img src="assets/icons/fz-leaderboard.svg" alt="" width="32" height="32" style="display:block;">'
n = src.count(TROPHY)
if n < 1:
    raise SystemExit('trophy not found')
src = src.replace(TROPHY,
    '<button onClick="{{ toggleLeaderboard }}" aria-label="Leaderboard" aria-pressed="{{ lbPressed }}" title="Leaderboard" '
    'style="width:32px;height:32px;border:0;padding:0;border-radius:999px;background:{{ lbBtnBg }};cursor:pointer;display:block;transition:background .2s ease;">'
    '<img src="assets/icons/fz-leaderboard.svg" alt="" width="32" height="32" style="display:block;{{ lbIconStyle }}"></button>')

# the regular header draws the trophy inline
m = re.search(r'          <svg width="17" height="18" viewBox="0 0 19 20" fill="none" style="flex-shrink:0;">.*?</svg>\n', src, re.S)
if not m:
    raise SystemExit('regular-header trophy not found')
svg = m.group(0).strip().replace('style="flex-shrink:0;"', 'style="display:block;{{ lbIconStyle }}"')
src = (src[:m.start()] + '          <button onClick="{{ toggleLeaderboard }}" aria-label="Leaderboard" aria-pressed="{{ lbPressed }}" title="Leaderboard" '
       'style="flex-shrink:0;width:32px;height:32px;margin:-7px -7px;border:0;padding:0;border-radius:999px;background:{{ lbBtnBg }};cursor:pointer;display:flex;align-items:center;justify-content:center;transition:background .2s ease;">'
       + svg + '</button>\n' + src[m.end():])

# ---------------------------------------------------------------- the panel
SK = 'display:block;border-radius:4px;background:#1B2326;'
PODIUM_EMPTY = ''.join(
    f'<div style="position:absolute;left:{x}px;top:0;width:114px;display:flex;flex-direction:column;align-items:center;">'
    f'<img src="assets/leaderboard/empty-{p}.svg" alt="" width="60" height="{h}" style="display:block;margin-top:{mt}px;">'
    f'<span style="{SK}width:72px;height:8px;margin-top:{18 if p != "1st" else 6}px;background:#2A3439;"></span>'
    f'<span style="{SK}width:36px;height:8px;margin-top:8px;background:#2A3439;"></span>'
    f'<span style="{SK}width:72px;height:8px;margin-top:8px;background:#2A3439;"></span></div>'
    for x, p, h, mt in ((16, '2nd', 60, 10), (130, '1st', 76, 0), (245, '3rd', 60, 10)))
SKROWS = ''.join(
    f'<div style="display:flex;align-items:center;height:40px;margin-top:4px;padding:0 12px;opacity:{o};">'
    f'<span style="{SK}width:12px;height:8px;"></span><span style="display:block;width:24px;height:24px;border-radius:50%;background:#1B2326;margin-left:47px;"></span>'
    f'<span style="{SK}width:62px;height:8px;margin-left:8px;"></span><span style="flex:1;"></span>'
    f'<span style="{SK}width:42px;height:8px;"></span><span style="{SK}width:60px;height:8px;margin-left:12px;"></span></div>'
    for o in (1, .85, .7, .55, .4, .25))

PANEL = '''        <!-- Leaderboard (FanZone DS 12304:62639 empty / loading, 12930:55217 loaded) -->
        <sc-if value="{{ lbOpen }}" hint-placeholder-val="{{ false }}">
          <div role="region" aria-label="Leaderboard" class="fz-scroll" style="position:absolute;left:0;right:0;top:48px;bottom:0;z-index:7;overflow-y:auto;overflow-x:hidden;background:#080E12;animation:fzFadeIn .2s ease;''' + FONT + '''">
            <div style="position:relative;height:48px;background:#0C161C;">
              <span style="position:absolute;left:16px;top:11px;font-weight:800;font-size:20px;line-height:26px;color:#F9FAFA;">Leaderboard</span>
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" aria-hidden="true" style="position:absolute;right:16px;top:12px;display:block;"><circle cx="12" cy="12" r="9" stroke="#B3B9BB" stroke-width="2"/><path d="M9.6 9.4a2.5 2.5 0 0 1 4.8.9c0 1.7-2.4 2-2.4 3.6" stroke="#B3B9BB" stroke-width="2" stroke-linecap="round"/><circle cx="12" cy="16.9" r="1.2" fill="#B3B9BB"/></svg>
            </div>
            <!-- top 3 -->
            <div style="position:relative;height:146px;background:linear-gradient(180deg,#0C161C 0%,#1C2529 100%);">
              <sc-if value="{{ lbSkeleton }}" hint-placeholder-val="{{ true }}">''' + PODIUM_EMPTY + '''</sc-if>
              <sc-if value="{{ lbLoaded }}" hint-placeholder-val="{{ false }}">
                <sc-for list="{{ lbTop }}" as="w" hint-placeholder-count="3">
                  <div style="position:absolute;left:{{ w.x }}px;top:0;width:114px;display:flex;flex-direction:column;align-items:center;animation:fzRxPop .35s cubic-bezier(.22,1.4,.36,1);">
                    <img onClick="{{ w.open }}" src="{{ w.medal }}" alt="{{ w.place }}" width="76" height="76" style="display:block;cursor:pointer;">
                    <span onClick="{{ w.open }}" style="cursor:pointer;margin-top:6px;font-weight:700;font-size:14px;line-height:20px;color:#F9FAFA;max-width:106px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">{{ w.name }}</span>
                    <span style="font-size:14px;line-height:14px;color:#F9FAFA;"><b style="color:#5ADC8C;font-weight:700;">{{ w.good }}</b>/10</span>
                    <span style="margin-top:2px;font-size:14px;line-height:14px;color:#9EA2A4;">{{ w.time }}</span>
                  </div>
                </sc-for>
              </sc-if>
            </div>
            <sc-if value="{{ lbSkeleton }}" hint-placeholder-val="{{ true }}">
              <div style="position:relative;">''' + SKROWS + '''
                <div style="position:absolute;left:0;right:0;bottom:0;height:170px;background:linear-gradient(180deg,rgba(8,14,18,0) 0%,#080E12 42%);display:flex;flex-direction:column;align-items:center;justify-content:flex-end;padding-bottom:30px;box-sizing:border-box;">
                  <sc-if value="{{ lbEmpty }}" hint-placeholder-val="{{ true }}">
                    <img src="assets/leaderboard/tip-bulb.svg" alt="" width="40" height="40" style="display:block;">
                    <span style="margin-top:4px;font-size:16px;line-height:24px;color:#F9FAFA;text-align:center;padding:0 12px;">Check back after the first quiz to see your ranking</span>
                  </sc-if>
                  <sc-if value="{{ lbLoading }}" hint-placeholder-val="{{ false }}">
                    <span style="width:26px;height:26px;border-radius:50%;border:2.5px solid rgba(249,250,250,.18);border-top-color:#F9FAFA;animation:fzSpin .8s linear infinite;"></span>
                  </sc-if>
                </div>
              </div>
            </sc-if>
            <sc-if value="{{ lbLoaded }}" hint-placeholder-val="{{ false }}">
              <div style="padding-bottom:56px;">
                <sc-for list="{{ lbRows }}" as="r" hint-placeholder-count="7">
                  <div style="display:flex;align-items:center;height:40px;margin-top:4px;padding:0 12px;">
                    <span style="width:47px;font-size:16px;color:#F9FAFA;">{{ r.rank }}</span>
                    <span onClick="{{ r.open }}" role="button" aria-label="Open {{ r.name }}'s card" style="cursor:pointer;margin-left:12px;width:24px;height:24px;border-radius:50%;flex-shrink:0;box-sizing:border-box;border:1.5px solid transparent;padding:1.5px;background:linear-gradient(#080E12,#080E12) padding-box,{{ r.ring }} border-box;">
                      <span style="display:block;width:18px;height:18px;border-radius:50%;overflow:hidden;"><img src="{{ r.avatar }}" alt="" style="display:block;width:18px;height:18px;object-fit:cover;transform:scale(1.207);"></span>
                    </span>
                    <span style="margin-left:8px;flex:1;min-width:0;display:flex;"><span onClick="{{ r.open }}" style="cursor:pointer;font-weight:700;font-size:16px;color:#F9FAFA;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">{{ r.name }}</span></span>
                    <span style="width:42px;font-size:16px;color:#F9FAFA;"><b style="color:#5ADC8C;font-weight:700;">{{ r.good }}</b>/10</span>
                    <span style="width:61px;margin-left:12px;font-size:16px;color:#9EA2A4;text-align:right;">{{ r.time }}</span>
                  </div>
                </sc-for>
              </div>
              <!-- you -->
              <div style="position:sticky;bottom:0;display:flex;align-items:center;height:48px;padding:0 12px;background:#F9FAFA;color:#080E12;">
                <span style="width:47px;font-size:16px;">{{ lbMeRank }}</span>
                <span onClick="{{ openCard }}" role="button" aria-label="Open your Fan Card" style="cursor:pointer;margin-left:12px;width:24px;height:24px;border-radius:50%;flex-shrink:0;box-sizing:border-box;border:1.5px solid transparent;padding:1.5px;background:linear-gradient(#F9FAFA,#F9FAFA) padding-box,{{ ringBg }} border-box;">
                  <span style="display:flex;align-items:center;justify-content:center;width:18px;height:18px;border-radius:50%;overflow:hidden;background:#080E12;color:#F9FAFA;font-weight:700;font-size:11px;">
                    <sc-if value="{{ hasAvatarImg }}" hint-placeholder-val="{{ true }}"><img src="{{ avatarImg }}" alt="" style="display:block;width:18px;height:18px;object-fit:cover;{{ avatarImgScale }}"></sc-if>
                    <sc-if value="{{ barShowInitial }}" hint-placeholder-val="{{ false }}">{{ cardInitial }}</sc-if>
                  </span>
                </span>
                <span onClick="{{ openCard }}" style="cursor:pointer;margin-left:8px;font-size:16px;max-width:99px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">{{ cardName }}</span>
                <span style="margin-left:8px;padding:1px 2px;border-radius:2px;background:#080E12;color:#F9FAFA;font-weight:800;font-size:12px;line-height:10px;">YOU</span>
                <span style="flex:1;"></span>
                <span style="width:42px;font-size:16px;"><b style="font-weight:700;">{{ lbMeGood }}</b>/10</span>
                <span style="width:61px;margin-left:12px;font-size:16px;text-align:right;">{{ lbMeTime }}</span>
              </div>
            </sc-if>
          </div>
        </sc-if>
'''
rep('        <!-- chat feed -->\n', PANEL + '        <!-- chat feed -->\n')

# ---------------------------------------------------------------- data + logic
TOP = [("Ronen", "assets/leaderboard/medal-2nd.svg", "2nd place", 16, "10", "01:34:35"),
       ("Guybenita", "assets/leaderboard/medal-1st.svg", "1st place", 130, "10", "01:34:35"),
       ("Whitepanda", "assets/leaderboard/medal-3rd.svg", "3rd place", 245, "10", "01:34:35")]
ROWS = [("4", "Mariposa", "uploads/11.png", "#DC052D", "10", "01:34:35"),
        ("5", "Bravewale", "uploads/12.png", "#FDE100", "9", "01:35:03"),
        ("6", "Briana", "uploads/13.png", "#DC052D", "9", "01:36:53"),
        ("7", "Carla", "uploads/14.png", "#FDE100", "8", "01:36:13"),
        ("8", "Michaelb", "uploads/17.png", "#DC052D", "8", "01:36:11"),
        ("9", "Americanx", "uploads/18.png", "#FDE100", "8", "01:43:11"),
        ("10", "Rojumi", "uploads/19.png", "#DC052D", "7", "02:12:46")]
LOGIC = '''  // Leaderboard (trophy in the FanZone header)
  openLeaderboard = (afterQuiz) => {
    clearTimeout(this._lbT);
    const loading = !!(afterQuiz || this.state.quizDone);
    this.setState({ lbOpen: true, lbLoading: loading, fzTyping: false });
    if (loading) this._lbT = setTimeout(() => this.setState({ lbLoading: false }), 1200);
  };
  toggleLeaderboard = (e) => {
    if (e && e.stopPropagation) e.stopPropagation();
    if (this.state.lbOpen) { clearTimeout(this._lbT); this.setState({ lbOpen: false, lbLoading: false }); }
    else this.openLeaderboard(false);
  };
  lbVals() {
    const s = this.state;
    const open = !!s.lbOpen && s.screen === "fanzone";
    const loaded = !!s.quizDone && !s.lbLoading;
    return {
      lbOpen: open, toggleLeaderboard: this.toggleLeaderboard,
      lbPressed: open ? "true" : "false", lbBtnBg: open ? "#F9FAFA" : "transparent", lbIconStyle: open ? "filter:brightness(0);" : "",
      lbSkeleton: !loaded, lbLoaded: loaded, lbEmpty: !s.quizDone, lbLoading: !!s.quizDone && !!s.lbLoading,
      lbTop: LB_TOP.map(([name, medal, place, x, good, time]) => ({ id: place, name, medal, place, x, good, time, open: () => this.openUserCard({ name, avatar: "" }) })),
      lbRows: LB_ROWS.map(([rank, name, avatar, ring, good, time]) => ({ id: rank, rank, name, avatar, ring, good, time, open: () => this.openUserCard({ name, avatar }) })),
      lbMeRank: s.quizScore != null ? String(s.quizRank || "4,568") : "4,568",
      lbMeGood: s.quizScore != null ? String(s.quizScore).padStart(2, "0") : "01",
      lbMeTime: "05:19:11",
    };
  }
  openFanZoneOver = (e) => {'''
rep('  openFanZoneOver = (e) => {', LOGIC)
rep('      ...this.gzVals(),', '      ...this.gzVals(),\n      ...this.lbVals(),')
rep('// FanZone chat: which team each fan supports',
    '// Leaderboard (FanZone DS)\nconst LB_TOP = ' + json.dumps(TOP) + ';\nconst LB_ROWS = ' + json.dumps(ROWS) + ';\n// FanZone chat: which team each fan supports')
# leaving FanZone closes it
rep('  goHome = () => { this.pollEnd(true);', '  goHome = () => { this.pollEnd(true); clearTimeout(this._lbT); if (this.state.lbOpen) this.setState({ lbOpen: false, lbLoading: false });')

open(PATH, 'w', encoding='utf-8').write(src)
print('ok')
