"""FanZone focus mode (Figma 23:97199): a toggle in the header shows only the host's messages; a tooltip introduces it."""
import sys
p = sys.argv[1]; s = open(p).read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:90])
    s = s.replace(a, b)

OFF = '<svg width="54" height="32" viewBox="0 0 54 32" fill="none" aria-hidden="true" style="display:block;"><path d="M0 16C0 7.16344 7.16344 0 16 0H38C46.8366 0 54 7.16344 54 16C54 24.8366 46.8366 32 38 32H16C7.16344 32 0 24.8366 0 16Z" fill="#F9FAFA" fill-opacity="0.12"/><path d="M2 16C2 8.26801 8.26801 2 16 2H24C31.732 2 38 8.26801 38 16C38 23.732 31.732 30 24 30H16C8.26801 30 2 23.732 2 16Z" fill="#080E12" fill-opacity="0.64"/><path d="M18.824 20.3574L19.947 23.1453C20.2994 24.0231 19.8742 25.0202 18.9971 25.3742C18.1193 25.7266 17.1223 25.3014 16.7682 24.4244L14.0703 17.7855" stroke-width="1.71458" stroke-linecap="round" stroke-linejoin="round" stroke="#F9FAFA"/><path d="M19.2145 10.9272H14.0708C12.177 10.9272 10.6416 12.4626 10.6416 14.3563C10.6416 16.2501 12.177 17.7855 14.0708 17.7855H19.2145C22.6436 17.7855 26.0728 21.2147 26.0728 21.2147V7.49805C26.0728 7.49805 22.6436 10.9272 19.2145 10.9272Z" stroke-width="1.71458" stroke-linecap="round" stroke-linejoin="round" stroke="#F9FAFA"/><path d="M27.7871 11.7845V16.9283C29.2076 16.9283 30.359 15.7769 30.359 14.3564C30.359 12.9359 29.2076 11.7845 27.7871 11.7845Z" fill="#F9FAFA"/></svg>'
ON = '<svg width="54" height="32" viewBox="0 0 54 32" fill="none" aria-hidden="true" style="display:block;"><path d="M0 16C0 7.16344 7.16344 0 16 0H38C46.8366 0 54 7.16344 54 16C54 24.8366 46.8366 32 38 32H16C7.16344 32 0 24.8366 0 16Z" fill="#F9FAFA" fill-opacity="0.12"/><path d="M16 16C16 8.26801 22.268 2 30 2H38C45.732 2 52 8.26801 52 16C52 23.732 45.732 30 38 30H30C22.268 30 16 23.732 16 16Z" fill="#FFFA00"/><path d="M33.947 23.1454L32.824 20.3575L29 20L30.7682 24.4245C31.1223 25.3015 32.1193 25.7267 32.9971 25.3744C33.8742 25.0203 34.2994 24.0233 33.947 23.1454Z" fill="#080E12" stroke-width="1.71458" stroke-linecap="round" stroke-linejoin="round" stroke="black"/><path d="M33.2135 10.9274H28.0698C26.176 10.9274 24.6406 12.4628 24.6406 14.3566C24.6406 16.2503 26.176 17.7857 28.0698 17.7857H33.2135C36.6427 17.7857 40.0718 21.2149 40.0718 21.2149V7.49829C40.0718 7.49829 36.6427 10.9274 33.2135 10.9274Z" fill="#080E12" stroke-width="1.71458" stroke-linecap="round" stroke-linejoin="round" stroke="black"/><path d="M41.7871 11.7847V16.9284C43.2076 16.9284 44.359 15.7771 44.359 14.3565C44.359 12.936 43.2076 11.7847 41.7871 11.7847Z" fill="black"/></svg>'
TOGGLE = ('<sc-if value="{{ focusAvail }}" hint-placeholder-val="{{ false }}"><button onClick="{{ toggleFocus }}" aria-label="Show top messages only" aria-pressed="{{ focusPressed }}" title="Show top messages only" style="width:54px;height:32px;border:0;padding:0;margin-right:8px;background:transparent;cursor:pointer;display:block;border-radius:16px;">'
          '<sc-if value="{{ focusOff }}" hint-placeholder-val="{{ true }}">' + OFF + '</sc-if><sc-if value="{{ focusOn }}" hint-placeholder-val="{{ false }}"><span style="display:block;animation:fzRxPop .3s cubic-bezier(.22,1.6,.36,1);">' + ON + '</span></sc-if></button></sc-if>\n            ')
a = '            <button onClick="{{ toggleLeaderboard }}" aria-label="Leaderboard"'
rep(a, TOGGLE + a, 2)

TIP = '''        <!-- focus mode tooltip (Figma 23:98112) -->
        <sc-if value="{{ focusTip }}" hint-placeholder-val="{{ false }}">
          <div role="status" style="position:absolute;left:0;right:0;top:48px;z-index:12;display:flex;flex-direction:column;align-items:flex-end;padding:4px 16px 18px;background:linear-gradient(180deg,#000,rgba(0,0,0,0));pointer-events:none;animation:fzFadeIn .25s ease;font-family:'DAZN Oscine',sans-serif;">
            <svg width="24" height="10" viewBox="0 0 24 10" aria-hidden="true" style="display:block;margin-right:98px;"><path d="M12 0L24 10H0Z" fill="#F0F2F2"/></svg>
            <div style="pointer-events:auto;display:flex;align-items:center;gap:24px;padding:16px;border-radius:8px;background:#F0F2F2;box-shadow:0 2px 4px rgba(17,24,39,.08);">
              <div style="display:flex;align-items:center;gap:8px;width:195px;">
                <span style="height:20px;padding:0 6px;border-radius:9999px;background:#FFFA00;display:inline-flex;align-items:center;font-weight:700;font-size:12px;letter-spacing:.12px;text-transform:uppercase;color:#060606;">New</span>
                <span style="font-weight:700;font-size:14px;line-height:1.5;color:#080E12;white-space:nowrap;">Show top messages only</span>
              </div>
              <button onClick="{{ closeFocusTip }}" aria-label="Close" style="width:24px;height:24px;border:0;padding:0;border-radius:9999px;background:rgba(8,14,18,.06);display:flex;align-items:center;justify-content:center;cursor:pointer;"><svg width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="M13.3333 3.79566L12.2046 2.66699L7.99996 6.87961L3.79529 2.66699L2.66663 3.79566L6.87924 8.00033L2.66663 12.205L3.79529 13.3337L7.99996 9.12104L12.2046 13.3337L13.3333 12.205L9.12068 8.00033L13.3333 3.79566Z" fill-rule="evenodd" clip-rule="evenodd" fill="#080E12"/></svg></button>
            </div>
          </div>
        </sc-if>
'''
rep('        <!-- Live updates (Figma 38:188098)', TIP + '        <!-- Live updates (Figma 38:188098)')

rep('      chatMessages: s.feed.map(m => {', '      chatMessages: (s.fzFocus ? s.feed.filter(m => m.host || m.mine) : s.feed).map(m => {')
rep('      luOver: !!this.state.luOver', '''      focusAvail: !!this.state.focusAvail, focusOn: !!this.state.fzFocus, focusOff: !this.state.fzFocus, focusPressed: this.state.fzFocus ? "true" : "false",
      focusTip: !!this.state.focusTip && this.state.screen === "fanzone" && !this.state.sheet,
      toggleFocus: () => this.setState(st => ({ fzFocus: !st.fzFocus, focusTip: false, atBottom: true })),
      closeFocusTip: () => this.setState({ focusTip: false }),
      luOver: !!this.state.luOver''')

rep('const CHAT_POOL = [', '''// focus mode: the host's messages (Figma 23:97199)
const FOCUS_HOST = ["The midfielders are also playing well. Their passes are accurate.", "Another good chance! Shoot!", "Start your game now!", "What a thrilling moment! Take your shot!", "The defense is focused. Bayern can't find a way through.", "Halftime is close: drop your prediction in the chat!"]
  .map(t => ({ name: "Misaki", host: true, text: t, avatar: "assets/pinned/host-avatar.svg" }));
const CHAT_POOL = [''')
rep('      const msg = { ...pick, id: "m" + (++this._feedId) };\n      this.setState(st => ({ feed: st.feed.concat(msg).slice(-40) }));\n    }, 2800);',
    '      if (this.state.focusAvail && this._feedId % 3 === 2) { this._hostI = ((this._hostI || 0) + 1) % FOCUS_HOST.length; pick = FOCUS_HOST[this._hostI]; }\n      const msg = { ...pick, id: "m" + (++this._feedId) };\n      this.setState(st => ({ feed: st.feed.concat(msg).slice(-40) }));\n    }, 2800);')

rep('"blocked", "liveupdate"].indexOf(q.get("moment"))', '"blocked", "liveupdate", "focus"].indexOf(q.get("moment"))')
rep('        else if (m === "liveupdate") this.luSoon(1800);\n', '        else if (m === "liveupdate") this.luSoon(1800);\n        else if (m === "focus") this.focusStart();\n')
rep('''      if (e.data && e.data.fz === "shown" && new URLSearchParams(location.search).get("moment") === "liveupdate")''',
    '''      if (e.data && e.data.fz === "shown" && new URLSearchParams(location.search).get("moment") === "focus") { this.focusStart(); return; }
      if (e.data && e.data.fz === "shown" && new URLSearchParams(location.search).get("moment") === "liveupdate")''')
rep('  luKind() {', '''  // focus mode: seed host messages among the chat, then show the tooltip on the toggle
  focusStart() {
    clearTimeout(this._focusT);
    this.setState(st => {
      const feed = st.feed.filter(m => !m.host).map((m, i, arr) => (arr.length - 1 - i) % 3 === 1 ? Object.assign({}, FOCUS_HOST[((arr.length - 1 - i) / 3 | 0) % FOCUS_HOST.length], { id: "fh" + i + "_" + Date.now() }) : m);
      return { focusAvail: true, fzFocus: false, focusTip: false, feed, atBottom: true };
    });
    this._focusT = setTimeout(() => { if (!this.state.fzFocus) this.setState({ focusTip: true }); }, 1400);
  }
  luKind() {''')
open(p, 'w').write(s); print("focus-mode ok")
