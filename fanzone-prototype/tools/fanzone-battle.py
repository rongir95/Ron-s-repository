#!/usr/bin/env python3
"""Fan Battle in FanZone, started from the prototype shell (Figma "Fan Battle", file QRYQoParO5SQY1djfuBnB5,
section 4935:35973 "Fan Battle Animation FLOW"). Bayern (home, left) v Dortmund (away, right).

  entry   a 40px strip slides in under the FanZone header with both crests (500ms)
  text    moderator message scrolls right to left at 150px/s
  ready / set / go   1s each: scale 0 -> 200%, opacity 0 -> 100% -> 0
  build   the team bars grow in from the sides (2s)
  battle  20s timer; the bar split follows the gift totals; other fans keep sending gifts.
          The gift row (5 / 10 / 50 / 100 / 500 coins) shows above the message bar while the battle runs.
          Your gifts go to your Choose-your-team pick (neutral: the team chooser opens first); your crest
          does a heartbeat and your bar flashes.
  finish  "And the Winner is:" stays still in the strip; then the winner's crest shows big over the chat
          with the Figma medal (a frame of its GIF, assets/battle/medal-figma.png) dropping in (Figma 6090:64167).

Decided with the product owner: no Beck's header and no coin balance in the header.
Text on the strip is the dot-matrix font from Figma, AB-megadot9 (Latin subset, uploads/AB-megadot9-latin.otf). Gifts: the FanZone DS "Gift pictograms" (NIgPxOlNU4U3sWMRdoE4Qh 4482:41428), Light red for Bayern and
Yellow primary for Dortmund, exported at 4x (assets/gifts/; they are bitmaps in the DS).
Strip per Figma 6372:237056: 40px, 32px crests in the team colour with a 1px white border, points in
DAZN Oscine ExtraBold 12 (white, thin dark outline) 56px from each side, a white 00:18 pill in the middle.

Run after the other scripts:  python3 tools/fanzone-battle.py FanZone.dc.html
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

DOT = "font-family:'AB-megadot9','DAZN Oscine',monospace;"
FONT = "font-family:'DAZN Oscine',sans-serif;"

# ---------------------------------------------------------------- gift pictograms (SVG, team colours via CSS vars)
G = {
 'finger': '<path d="M16 6c0-2 1.6-3.5 3.5-3.5S23 4 23 6v15h1.5v-3c0-1.7 1.3-3 3-3s3 1.3 3 3v3c.4-1.4 1.6-2.4 3-2.4 1.7 0 3 1.3 3 3V36c0 5-4 9-9 9H20c-5 0-9-4-9-9v-5l-4-4c-1.3-1.3-1.3-3.3 0-4.6 1.2-1.2 3.2-1.3 4.5-.2L16 26z" fill="var(--g1)" stroke="var(--g3)" stroke-width="2" stroke-linejoin="round"/><path d="M24.5 21v5M30.5 21v5" stroke="var(--g3)" stroke-width="1.6" stroke-linecap="round"/><text x="25" y="40" text-anchor="middle" font-family="DAZN Oscine,sans-serif" font-weight="800" font-size="9" fill="var(--g2)">#1</text>',
 'flag': '<path d="M12 6l26 36" stroke="var(--g3)" stroke-width="3.5" stroke-linecap="round"/><path d="M13 7c8-4 14 3 22-1 2 7 4 12 6 18-8 4-14-3-22 1z" fill="var(--g2)" stroke="var(--g3)" stroke-width="1.6" stroke-linejoin="round"/><path d="M16 11c4-1 6 1 9 0l3 6c-3 1-5-1-9 0zM25 18l3 6c3-1 5 1 9 0l-3-6c-3 1-5-1-9 0zM31 8c2 0 3 0 4-1l2 5c-1 1-2 1-4 1z" fill="var(--g1)"/>',
 'horn': '<path d="M8 30l14-8 12 18-14 6z" fill="var(--g1)" stroke="var(--g3)" stroke-width="1.8" stroke-linejoin="round"/><path d="M14 27l4 6M19 24l5 7" stroke="var(--g2)" stroke-width="2"/><ellipse cx="38" cy="16" rx="7" ry="8" transform="rotate(30 38 16)" fill="var(--g2)" stroke="var(--g3)" stroke-width="1.8"/><path d="M27 28l7-9" stroke="var(--g3)" stroke-width="4" stroke-linecap="round"/><circle cx="12" cy="40" r="5" fill="var(--g1)" stroke="var(--g3)" stroke-width="1.6"/>',
 'drum': '<path d="M8 22v14c0 5 7 8 16 8s16-3 16-8V22" fill="var(--g1)" stroke="var(--g3)" stroke-width="1.8"/><ellipse cx="24" cy="22" rx="16" ry="7" fill="var(--g2)" stroke="var(--g3)" stroke-width="1.8"/><path d="M10 28l6 12M18 30l4 13M30 30l-4 13M38 28l-6 12" stroke="var(--g2)" stroke-width="1.6"/><path d="M30 4l-7 17" stroke="var(--g3)" stroke-width="2.6" stroke-linecap="round"/><circle cx="30.5" cy="4" r="2.6" fill="var(--g1)" stroke="var(--g3)" stroke-width="1.2"/>',
 'popper': '<path d="M14 44l-4-20 20 4z" fill="var(--g1)" stroke="var(--g3)" stroke-width="1.8" stroke-linejoin="round"/><path d="M11 30l12 2M12 37l9 2" stroke="var(--g2)" stroke-width="2.4"/><path d="M27 20l3-9M33 23l8-5M30 16l2-2" stroke="var(--g1)" stroke-width="3" stroke-linecap="round"/><circle cx="38" cy="10" r="2.6" fill="var(--g2)"/><circle cx="24" cy="9" r="2.2" fill="var(--g1)"/><rect x="40" y="25" width="4" height="7" rx="1.5" transform="rotate(25 40 25)" fill="var(--g2)"/>',
}
COIN = ('<svg width="12" height="12" viewBox="0 0 12 12" fill="none" aria-hidden="true" style="display:block;"><circle cx="6" cy="6" r="5" fill="#F1A322"/>'
        '<circle cx="6" cy="6" r="4.3" fill="#FFD23A"/><path d="M6.6 2.9 3.9 6.4h2.2l-.7 2.7 2.7-3.5H5.9z" fill="#F1A322"/></svg>')
GIFTS = [('finger', 5), ('flag', 10), ('horn', 50), ('drum', 100), ('fireworks', 500)]
GIFT_ROW = ''.join(
    f'<button class="fb-gift" onClick="{{{{ fbGift{v} }}}}" aria-label="Send {v} coins" style="width:64px;flex-shrink:0;border:0;padding:4px 0 0;background:transparent;cursor:pointer;display:flex;flex-direction:column;align-items:center;gap:2px;">'
    f'<img src="assets/gifts/{{{{ fbGiftColor }}}}-{k}.png" alt="" width="56" height="48" draggable="false" style="display:block;">'
    f'<span style="display:flex;align-items:center;gap:4px;{FONT}font-size:12px;color:#F9FAFA;">{v}{COIN}</span></button>'
    for k, v in GIFTS)

STRIP = '''        <!-- Fan Battle strip (Figma 4935:35973) -->
        <sc-if value="{{ fbOn }}" hint-placeholder-val="{{ false }}">
          <div class="fb-strip" style="position:absolute;left:0;right:0;top:48px;z-index:7;height:40px;overflow:hidden;background:#080E12;{{ fbStripAnim }}''' + DOT + '''">
            <!-- bars -->
            <sc-if value="{{ fbBars }}" hint-placeholder-val="{{ false }}">
              <div style="position:absolute;left:0;top:0;bottom:0;width:{{ fbHomePct }}%;background:{{ fbHomeColor }};transform-origin:left center;transition:width .45s cubic-bezier(.22,1,.36,1);{{ fbBuildL }}">
                <span style="position:absolute;inset:0;background:linear-gradient(90deg,rgba(0,0,0,.5) 0,rgba(0,0,0,0) 90px);"></span>
                <span style="position:absolute;inset:0;{{ fbFlashHome }}"></span>
              </div>
              <div style="position:absolute;right:0;top:0;bottom:0;width:{{ fbAwayPct }}%;background:{{ fbAwayColor }};transform-origin:right center;transition:width .45s cubic-bezier(.22,1,.36,1);{{ fbBuildR }}">
                <span style="position:absolute;inset:0;background:linear-gradient(270deg,rgba(0,0,0,.5) 0,rgba(0,0,0,0) 90px);"></span>
                <span style="position:absolute;inset:0;{{ fbFlashAway }}"></span>
              </div>
            </sc-if>
            <sc-if value="{{ fbScores }}" hint-placeholder-val="{{ false }}">
              <span style="position:absolute;left:56px;top:13px;font-family:'DAZN Oscine',sans-serif;font-weight:800;font-size:12px;line-height:13px;color:#F9FAFA;-webkit-text-stroke:1px rgba(36,32,37,.5);paint-order:stroke fill;animation:fzFadeIn .5s ease both;">{{ fbHomeScore }}</span>
              <span style="position:absolute;right:56px;top:13px;font-family:'DAZN Oscine',sans-serif;font-weight:800;font-size:12px;line-height:13px;color:#F9FAFA;-webkit-text-stroke:1px rgba(36,32,37,.5);paint-order:stroke fill;animation:fzFadeIn .5s ease both;">{{ fbAwayScore }}</span>
              <span style="position:absolute;top:12px;left:50%;transform:translateX(-50%);height:16px;box-sizing:border-box;padding:2px 4px;border-radius:8px;background:#F9FAFA;border:1px solid rgba(36,32,37,.2);display:flex;align-items:center;''' + FONT + '''font-weight:700;font-size:12px;line-height:12px;color:#0C161C;font-variant-numeric:tabular-nums;animation:fzFadeIn .5s ease both;">{{ fbClock }}</span>
            </sc-if>
            <!-- moderator text / winner text -->
            <sc-if value="{{ fbMarquee }}" hint-placeholder-val="{{ false }}">
              <!-- the text runs between the crests and disappears under them (Fan Battle 13467:76612) -->
              <div style="position:absolute;left:44px;right:44px;top:0;bottom:0;overflow:hidden;">
                <span style="position:absolute;left:0;top:0;bottom:0;display:flex;align-items:center;white-space:nowrap;font-size:17px;color:#F9FAFA;animation:fbMarquee {{ fbMarqueeS }}s linear both;">{{ fbMarqueeText }}</span>
              </div>
            </sc-if>
            <!-- ready / set / go -->
            <sc-if value="{{ fbCallReady }}" hint-placeholder-val="{{ false }}">
              <span style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font-size:16px;line-height:1;color:#FF7466;animation:fbCallPop 1s ease-out both;">READY</span>
            </sc-if>
            <sc-if value="{{ fbCallSet }}" hint-placeholder-val="{{ false }}">
              <span style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font-size:16px;line-height:1;color:#F7FF1A;animation:fbCallPop 1s ease-out both;">SET</span>
            </sc-if>
            <sc-if value="{{ fbCallGo }}" hint-placeholder-val="{{ false }}">
              <span style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font-size:16px;line-height:1;color:#1DBF00;animation:fbCallPop 1s ease-out both;">GO!!</span>
            </sc-if>
            <!-- finish / winner: "And the Winner is:" stays still between the crests (Fan Battle 6090:64167) -->
            <sc-if value="{{ fbWinLine }}" hint-placeholder-val="{{ false }}">
              <span style="position:absolute;left:17px;right:17px;top:0;bottom:0;display:flex;align-items:center;justify-content:center;white-space:nowrap;font-size:16px;color:#F9FAFA;animation:fzFadeIn .3s ease both;">And the Winner is:</span>
              <span style="position:absolute;left:0;top:0;bottom:0;width:40px;background:linear-gradient(90deg,#080E12,rgba(8,14,18,0));"></span>
              <span style="position:absolute;right:0;top:0;bottom:0;width:40px;background:linear-gradient(270deg,#080E12,rgba(8,14,18,0));"></span>
            </sc-if>
            <!-- crests -->
            <span style="position:absolute;left:8px;top:4px;width:32px;height:32px;box-sizing:border-box;border-radius:32px;border:1px solid #FFFFFF;background:#DC052D;display:flex;align-items:center;justify-content:center;{{ fbBeatHome }}"><img src="assets/vec/tiles/img-logo-bayern.svg" alt="Bayern München" width="24" height="24" style="display:block;"></span>
            <span style="position:absolute;right:8px;top:4px;width:32px;height:32px;box-sizing:border-box;border-radius:32px;border:1px solid #FFFFFF;background:#FDE100;display:flex;align-items:center;justify-content:center;{{ fbBeatAway }}"><img src="assets/poll/logo-bvb.png" alt="Borussia Dortmund" width="24" height="24" style="display:block;"></span>
          </div>
        </sc-if>
'''
WIN = '''        <!-- Fan Battle winner: the winning team's crest over the chat with the medal from Figma (Fan Battle 6090:64167) -->
        <sc-if value="{{ fbWin }}" hint-placeholder-val="{{ false }}">
          <div aria-label="{{ fbWinName }} wins the Fan Battle" role="img" style="position:absolute;left:49px;top:78px;width:278px;height:278px;z-index:6;pointer-events:none;">
            <img src="{{ fbWinCrest }}" alt="" width="200" height="200" style="position:absolute;left:39px;top:26px;width:200px;height:200px;display:block;filter:drop-shadow(0 8px 18px rgba(0,0,0,.5));animation:fbWinCrest .7s cubic-bezier(.22,1.4,.36,1) both;">
            <img src="assets/battle/medal-figma.png" alt="" width="278" height="278" style="position:absolute;inset:0;width:278px;height:278px;display:block;transform-origin:68% 75%;animation:fbWinMedal .8s .35s cubic-bezier(.22,1.5,.36,1) both;">
          </div>
        </sc-if>
'''
rep('        <!-- chat feed -->\n', STRIP + WIN + '        <!-- chat feed -->\n')

ROW = ('        <!-- Fan Battle gifts (only while the battle runs) -->\n'
       '        <sc-if value="{{ fbGifts }}" hint-placeholder-val="{{ false }}">\n'
       '          <div style="flex-shrink:0;display:flex;align-items:flex-start;padding:4px 8px 0;height:76px;box-sizing:border-box;background:#0C161C;--g1:{{ fbG1 }};--g2:{{ fbG2 }};--g3:{{ fbG3 }};animation:fbRowIn .35s cubic-bezier(.22,1,.36,1);">'
       + GIFT_ROW + '</div>\n        </sc-if>\n')
rep('        <!-- message bar -->\n', ROW + '        <!-- message bar -->\n')

rep('  * { -webkit-font-smoothing: antialiased; box-sizing: border-box; }',
    '  @font-face { font-family: "AB-megadot9"; src: url("uploads/AB-megadot9-latin.otf") format("opentype"); font-weight: 400; font-style: normal; font-display: swap; }\n'
    '  * { -webkit-font-smoothing: antialiased; box-sizing: border-box; }')
rep('  @keyframes fzPushIn {',
    '  @keyframes fbIn { from { transform: translateY(-100%); opacity: 0; } to { transform: none; opacity: 1; } }\n'
    '  @keyframes fbOut { from { transform: none; opacity: 1; } to { transform: translateY(-100%); opacity: 0; } }\n'
    '  @keyframes fbMarquee { from { transform: translateX(287px); } to { transform: translateX(-100%); } }\n'
    '  @keyframes fbCallPop { 0% { transform: scale(.4); opacity: 0; } 18% { transform: scale(1.15); opacity: 1; } 30%, 82% { transform: scale(1); opacity: 1; } 100% { transform: scale(1); opacity: 0; } }\n'
    '  @keyframes fbBuildL { 0% { transform: scaleX(0); opacity: 0; } 13% { opacity: 1; } 100% { transform: scaleX(1); opacity: 1; } }\n'
    '  @keyframes fbBeat { 0%, 100% { transform: scale(1); } 35% { transform: scale(.7); } 65% { transform: scale(1.12); } }\n'
    '  @keyframes fbFlash { from { background-position: -160px 0; } to { background-position: 420px 0; } }\n'
    '  @keyframes fbWinCrest { 0% { transform: scale(.3); opacity: 0; } 100% { transform: none; opacity: 1; } }\n'
    '  @keyframes fbWinMedal { 0% { transform: translateY(-30px) scale(.4); opacity: 0; } 100% { transform: none; opacity: 1; } }\n'
    '  @keyframes fbRowIn { from { opacity: 0; transform: translateY(12px); } to { opacity: 1; transform: none; } }\n'
    '  .fb-gift:active svg { transform: scale(.9); }\n'
    '  @keyframes fzPushIn {')

LOGIC = '''  // Fan Battle (from the shell)
  fbOnNow = () => !!this.state.fbPhase && this.state.screen === "fanzone";
  startBattle = () => {
    if (this.state.screen !== "fanzone") return;
    this.stopBattle(true);
    const steps = [["entry", 600], ["text", 5600], ["ready", 1000], ["set", 1000], ["go", 1000], ["build", 2000], ["battle", 20000], ["finish", 1500], ["winner", 4800], ["out", 450]];
    this.setState({ fbScore: { home: 1000, away: 1000 }, fbClockS: 20, fbPulse: null, fbFlash: null });
    let t = 0;
    this._fbT = [];
    steps.forEach(([phase, ms]) => {
      this._fbT.push(setTimeout(() => {
        this.setState({ fbPhase: phase });
        if (phase === "battle") {
          this._fbClock = setInterval(() => this.setState(s => ({ fbClockS: Math.max(0, (s.fbClockS || 0) - 1) })), 1000);
          const others = () => {
            const amts = [5, 5, 5, 10, 10, 10, 50, 50, 100, 500];
            const a = amts[Math.floor(Math.random() * amts.length)];
            const side = Math.random() < .5 ? "home" : "away";
            this.setState(s => ({ fbScore: { ...s.fbScore, [side]: (s.fbScore[side] || 0) + a * (5 + Math.floor(Math.random() * 20)) } }));
            this._fbOther = setTimeout(others, 350 + Math.random() * 450);
          };
          others();
        }
        if (phase === "finish") { clearInterval(this._fbClock); clearTimeout(this._fbOther); }
      }, t));
      t += ms;
    });
    this._fbT.push(setTimeout(() => this.setState({ fbPhase: null }), t));
  };
  stopBattle = (silent) => {
    (this._fbT || []).forEach(clearTimeout); clearInterval(this._fbClock); clearTimeout(this._fbOther); clearTimeout(this._fbPulseT);
    if (!silent) this.setState({ fbPhase: null });
  };
  sendGift = (amount) => {
    const s = this.state;
    if (s.fbPhase !== "battle") return;
    const team = s.fzTeam === "bayern" ? "home" : (s.fzTeam === "bvb" ? "away" : null);
    if (!team) { this.setState({ fzChoose: true }); return; }
    clearTimeout(this._fbPulseT);
    this.setState(st => ({ fbScore: { ...st.fbScore, [team]: (st.fbScore[team] || 0) + amount * 20 }, fbPulse: team, fbFlash: team, fbPulseN: (st.fbPulseN || 0) + 1 }));
    this._fbPulseT = setTimeout(() => this.setState({ fbPulse: null, fbFlash: null }), 650);
  };
  fbVals() {
    const s = this.state;
    const ph = s.screen === "fanzone" ? s.fbPhase : null;
    const sc = s.fbScore || { home: 0, away: 0 };
    const total = sc.home + sc.away;
    const homeShare = ph === "battle" || ph === "finish" ? (total ? Math.min(68, Math.max(32, sc.home / total * 100)) : 50) : 50;
    const fmt = (n) => Number(n).toLocaleString("en-US");
    const winHome = sc.home >= sc.away;
    const team = s.fzTeam === "bayern" ? "home" : (s.fzTeam === "bvb" ? "away" : null);
    const beat = (side) => (s.fbPulse === side ? "animation:fbBeat .55s ease both;" : "");
    const flash = (side) => (s.fbFlash === side ? "background:linear-gradient(100deg,rgba(255,255,255,0) 0,rgba(255,255,255,.55) 50%,rgba(255,255,255,0) 100%) no-repeat;background-size:160px 100%;animation:fbFlash .6s ease-out both;" : "");
    const bars = ph === "build" || ph === "battle" || ph === "finish";
    return {
      fbOn: !!ph, fbStripAnim: ph === "out" ? "animation:fbOut .45s ease both;" : (ph === "entry" ? "animation:fbIn .5s cubic-bezier(.22,1,.36,1) both;" : ""),
      fbBars: bars && ph !== "finish", fbBuildL: ph === "build" ? "animation:fbBuildL 2s cubic-bezier(.4,0,.2,1) both;" : "", fbBuildR: ph === "build" ? "animation:fbBuildL 2s cubic-bezier(.4,0,.2,1) both;" : "",
      fbHomePct: homeShare.toFixed(1), fbAwayPct: (100 - homeShare).toFixed(1),
      fbHomeColor: "#DC052D", fbAwayColor: "#FDE100", fbAwayText: "#080E12",
      fbScores: ph === "battle", fbHomeScore: fmt(sc.home), fbAwayScore: fmt(sc.away),
      fbClock: "00:" + String(s.fbClockS != null ? s.fbClockS : 20).padStart(2, "0"),
      fbMarquee: ph === "text", fbMarqueeS: 5.4, fbWinLine: ph === "finish" || ph === "winner",
      fbMarqueeText: "Fans Battle! Send Gifts to Cheer Your Team!",
      fbCallReady: ph === "ready", fbCallSet: ph === "set", fbCallGo: ph === "go",
      fbWin: ph === "winner", fbWinName: winHome ? "Bayern München" : "Dortmund", fbWinCrest: winHome ? "assets/vec/tiles/img-logo-bayern.svg" : "assets/poll/logo-bvb.png",
      fbBeatHome: beat("home"), fbBeatAway: beat("away"), fbFlashHome: flash("home"), fbFlashAway: flash("away"),
      fbGifts: ph === "battle", fbGiftColor: team === "away" ? "yellow" : "red",
      fbG1: team === "away" ? "#FDE100" : (team === "home" ? "#DC052D" : "#6D7377"), fbG2: team === "away" ? "#080E12" : "#FFFFFF", fbG3: "#080E12",
      fbGift5: () => this.sendGift(5), fbGift10: () => this.sendGift(10), fbGift50: () => this.sendGift(50), fbGift100: () => this.sendGift(100), fbGift500: () => this.sendGift(500),
    };
  }
  openFanZoneOver = (e) => {'''
rep('  openFanZoneOver = (e) => {', LOGIC)
rep('      ...this.gzVals(),', '      ...this.gzVals(),\n      ...this.fbVals(),')

# the shell starts / stops it and hears whether it runs
rep('      if (d && d.fz === "pin")', '      if (d && d.fz === "battle") { if (d.on) this.startBattle(); else this.stopBattle(); return; }\n      if (d && d.fz === "pin")')
rep('+ "|" + (s.pinOn ? "pin" : "-");', '+ "|" + (s.pinOn ? "pin" : "-") + "|" + (s.fbPhase ? "battle" : "-");')
rep('pin: !!s.pinOn }, "*");', 'pin: !!s.pinOn, battle: !!s.fbPhase }, "*");')
rep('  goHome = () => { this.pollEnd(true);', '  goHome = () => { this.pollEnd(true); if (this.state.fbPhase) this.stopBattle();')

# the pinned image and the poll sit under the battle strip while it shows
rep('          <div style="position:absolute;left:0;right:0;top:48px;z-index:5;background:#242D33;',
    '          <div style="position:absolute;left:0;right:0;top:{{ pinTopPx }}px;z-index:5;transition:top .3s ease;background:#242D33;')
rep('    return { pollTop: on ? (s.pinExpanded ? 48 + 289 : 48 + 64) : 48, pinOn: on,',
    '    const fbH = s.fbPhase && s.screen === "fanzone" ? 40 : 0;\n'
    '    return { pinTopPx: 48 + fbH, pollTop: fbH + (on ? (s.pinExpanded ? 48 + 289 : 48 + 64) : 48), pinOn: on,')

open(PATH, 'w', encoding='utf-8').write(src)
print('ok')
