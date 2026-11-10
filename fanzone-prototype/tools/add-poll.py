#!/usr/bin/env python3
"""Add the live Poll (from the landscape 'FanZone Prototype' canvas) to the portrait FanZone screen.

The poll card enters from under the stream and pushes the FanZone panel down. It is started
from the prototype shell (index.html) with a postMessage, and only while the FanZone screen is open.
Run after merge-prototypes.py:  python3 tools/add-poll.py FanZone.dc.html
"""
import sys

PATH = sys.argv[1]
src = open(PATH, encoding='utf-8').read()

def must_replace(s, old, new):
    n = s.count(old)
    if n != 1:
        raise SystemExit(f'expected 1 occurrence, found {n}: {old[:90]!r}')
    return s.replace(old, new)

# ---------------------------------------------------------------- CSS
src = must_replace(src, "  @keyframes fzPushIn {",
"""  /* Live poll (from the landscape FanZone prototype) */
  .fz-poll { animation: fzPollIn .6s cubic-bezier(.22,1,.36,1) both; transition: height .45s cubic-bezier(.22,1,.36,1); }
  .fz-poll.is-out { animation: fzPollOut .4s cubic-bezier(.4,0,1,1) both; }
  @keyframes fzPollIn { from { transform: translateY(-100%); } to { transform: none; } }
  @keyframes fzPollOut { from { transform: none; } to { transform: translateY(-100%); } }
  .fz-poll-me { animation: fzPollMe .5s cubic-bezier(.34,1.56,.64,1) .15s both; }
  @keyframes fzPollMe { 0% { opacity: 0; transform: scale(.3); } 100% { opacity: 1; transform: none; } }
  .fz-poll-opt { transition: border-color .2s ease, background-color .2s ease; }
  .fz-poll-opt:disabled { cursor: default; }
  @keyframes fzPushIn {""")

# ---------------------------------------------------------------- markup
src = must_replace(src,
    '      <!-- Match video -->\n      <div style="position:absolute;top:54px;left:0;right:0;height:211px;">',
    '      <!-- Match video -->\n      <div style="position:absolute;top:54px;left:0;right:0;height:211px;z-index:2;">')

POLL = r'''      <!-- ===================== LIVE POLL (from the landscape FanZone prototype): enters under the stream ===================== -->
      <sc-if value="{{ pollMounted }}" hint-placeholder-val="{{ false }}">
        <section class="fz-poll {{ pollCls }}" aria-label="Poll" style="position:absolute;left:0;right:0;top:265px;z-index:1;height:{{ pollH }}px;background:#1B232B;border-radius:0 0 14px 14px;box-shadow:0 10px 24px rgba(0,0,0,.45);overflow:hidden;font-family:'DAZN Oscine',sans-serif;color:#F9FAFA;">
          <div style="height:46px;display:flex;align-items:center;justify-content:space-between;padding:0 16px;">
            <div style="display:flex;align-items:center;gap:10px;">
              <svg width="24" height="24" viewBox="0 0 100 100" fill="none" aria-hidden="true"><path d="M64.2857 20.8332C64.2857 18.532 62.6867 16.6665 60.7143 16.6665H26.7857C25.7995 16.6665 25 17.5992 25 18.7498V31.2498C25 32.4004 25.7995 33.3332 26.7857 33.3332H60.7143C62.6867 33.3332 64.2857 31.4677 64.2857 29.1665V20.8332Z" fill="#F9FAFA"></path><path d="M75 45.8332C75 43.532 73.401 41.6665 71.4286 41.6665H26.7857C25.7995 41.6665 25 42.5992 25 43.7498V56.2498C25 57.4004 25.7995 58.3332 26.7857 58.3332H71.4286C73.401 58.3332 75 56.4677 75 54.1665V45.8332Z" fill="#F9FAFA"></path><path d="M46.4286 70.8332C46.4286 68.532 44.8296 66.6665 42.8571 66.6665H26.7857C25.7995 66.6665 25 67.5992 25 68.7498V81.2498C25 82.4004 25.7995 83.3332 26.7857 83.3332H42.8571C44.8296 83.3332 46.4286 81.4677 46.4286 79.1665V70.8332Z" fill="#F9FAFA"></path></svg>
              <span style="font-size:16px;font-weight:400;">Poll</span>
            </div>
            <img src="assets/poll/sponsor-heineken.png" alt="Heineken" style="width:98px;height:28px;display:block;">
          </div>
          <div style="height:3px;background:#3A434C;position:relative;">
            <div style="position:absolute;left:0;top:0;bottom:0;width:{{ pollTimerPct }}%;background:#FFF200;transition:width 1s linear;"></div>
          </div>
          <div style="height:58px;box-sizing:border-box;display:flex;align-items:center;justify-content:space-between;gap:12px;padding:8px 12px 8px 16px;">
            <div style="display:flex;flex-direction:column;gap:2px;min-width:0;">
              <span style="font-size:12px;color:#8C959E;letter-spacing:.2px;">Bundesliga</span>
              <h2 style="margin:0;font-size:16px;font-weight:400;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;min-width:0;">Who wins the league title?</h2>
            </div>
            <button onClick="{{ pollToggleCollapse }}" aria-label="{{ pollCollapseLabel }}" style="width:44px;height:44px;flex-shrink:0;border:0;padding:0;border-radius:50%;background:transparent;display:flex;align-items:center;justify-content:center;cursor:pointer;">
              <svg width="28" height="28" viewBox="0 0 17.408 17.408" fill="none" aria-hidden="true" style="transform:rotate({{ pollChevronRot }}deg);transition:transform .25s ease;"><path d="M0 8.704C0 3.89691 3.89691 0 8.704 0V0C13.5111 0 17.408 3.89691 17.408 8.704V8.704C17.408 13.5111 13.5111 17.408 8.704 17.408V17.408C3.89691 17.408 0 13.5111 0 8.704V8.704Z" fill="#F9FAFA" fill-opacity="0.12"></path><path d="M8.73828 5.74889L13.7383 10.7489L12.2361 12.2511L8.73828 8.75332L5.24049 12.2511L3.73828 10.7489L8.73828 5.74889Z" fill-rule="evenodd" clip-rule="evenodd" fill="#F9FAFA"></path></svg>
            </button>
          </div>
          <div style="display:flex;flex-direction:column;gap:8px;padding:0 16px 12px;">
            <sc-for list="{{ pollOptions }}" as="o" hint-placeholder-count="3">
              <button class="fz-poll-opt" onClick="{{ o.pick }}" disabled="{{ pollVoted }}" style="position:relative;height:50px;border-radius:12px;border:2px solid {{ o.border }};background:{{ o.bg }};padding:0 14px 0 7px;display:flex;align-items:center;gap:12px;overflow:hidden;text-align:left;box-sizing:border-box;width:100%;cursor:pointer;font-family:inherit;">
                <span style="position:absolute;left:0;top:0;bottom:0;width:{{ o.fillPct }}%;background:{{ o.fill }};transition:width .8s ease;"></span>
                <span style="position:relative;width:36px;height:36px;flex-shrink:0;border-radius:50%;background:{{ o.ring }};display:flex;align-items:center;justify-content:center;">
                  <img src="{{ o.logo }}" alt="" style="width:26px;height:26px;object-fit:contain;display:block;">
                </span>
                <span style="position:relative;flex:1;min-width:0;font-size:15px;font-weight:400;color:{{ o.text }};white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">{{ o.name }}</span>
                <span style="position:relative;flex-shrink:0;display:flex;align-items:center;gap:6px;">
                  <sc-if value="{{ o.mine }}" hint-placeholder-val="{{ false }}">
                    <img class="fz-poll-me" src="assets/poll/your-vote.png" alt="Your vote" style="width:22px;height:22px;flex-shrink:0;display:block;">
                  </sc-if>
                  <sc-if value="{{ pollVoted }}" hint-placeholder-val="{{ false }}">
                    <span style="font-size:15px;font-weight:700;color:{{ o.text }};">{{ o.pct }}%</span>
                  </sc-if>
                </span>
              </button>
            </sc-for>
          </div>
          <div style="display:flex;align-items:center;gap:10px;padding:0 16px 12px;">
            <div style="display:flex;padding-left:8px;">
              <img src="assets/poll/voter1.png" alt="" style="width:24px;height:24px;margin-left:-8px;border-radius:50%;border:2px solid #1B232B;display:block;">
              <img src="assets/poll/voter2.png" alt="" style="width:24px;height:24px;margin-left:-8px;border-radius:50%;border:2px solid #1B232B;display:block;">
              <img src="assets/poll/voter3.png" alt="" style="width:24px;height:24px;margin-left:-8px;border-radius:50%;border:2px solid #1B232B;display:block;">
            </div>
            <span style="font-size:13px;color:#8C959E;">{{ pollVotesLabel }} fans voted</span>
          </div>
        </section>
      </sc-if>
      <!-- FanZone panel -->
      <div style="position:absolute;left:0;right:0;bottom:0;top:{{ fzPanelTop }}px;transition:top .55s cubic-bezier(.22,1,.36,1);background:#080E12;'''
src = must_replace(src,
    '      <!-- FanZone panel -->\n      <div style="position:absolute;left:0;right:0;bottom:0;top:273px;background:#080E12;',
    POLL)

# ---------------------------------------------------------------- logic
LOGIC = r'''
  // ===================== LIVE POLL (from the landscape FanZone prototype) =====================
  // The prototype shell starts / ends it with postMessage({ fz: "poll", on: true|false }); only while FanZone is open.
  pollStart() {
    if (this.state.screen !== "fanzone" || this.state.pollOn) return;
    this.pollClear();
    clearTimeout(this._pollOutT);
    this.setState({ pollOn: true, pollClosing: false, pollCollapsed: false, pollVote: null, pollCounts: { fcb: 610, bvb: 420, b04: 317 }, pollPcts: [46, 31, 23], pollTime: 100 });
    this._pollW = { fcb: 0.45, bvb: 0.33, b04: 0.22 };
    this._pollVotesT = setInterval(() => this.pollBumpVotes(), 1100);
    this._pollPctT = setInterval(() => this.pollShiftPcts(), 2000);
    // the yellow bar runs down in ~90 s, then the poll closes by itself
    this._pollClockT = setInterval(() => {
      const t = (this.state.pollTime ?? 100) - 100 / 90;
      if (t <= 0) this.pollEnd(); else this.setState({ pollTime: t });
    }, 1000);
  }
  pollEnd(instant) {
    this.pollClear();
    if (!this.state.pollOn) return;
    if (instant) { this.setState({ pollOn: false, pollClosing: false }); return; }
    this.setState({ pollClosing: true });
    clearTimeout(this._pollOutT);
    this._pollOutT = setTimeout(() => this.setState({ pollOn: false, pollClosing: false }), 420);
  }
  pollClear() { clearInterval(this._pollVotesT); clearInterval(this._pollPctT); clearInterval(this._pollClockT); }
  pollBumpVotes() {
    this.setState((st) => {
      const c = { ...(st.pollCounts || { fcb: 610, bvb: 420, b04: 317 }) };
      const w = this._pollW;
      for (const k of Object.keys(w)) w[k] = Math.min(0.7, Math.max(0.08, w[k] + (Math.random() - 0.5) * 0.12));
      const sum = w.fcb + w.bvb + w.b04;
      const weights = [["fcb", w.fcb / sum], ["bvb", w.bvb / sum], ["b04", w.b04 / sum]];
      const n = 12 + Math.floor(Math.random() * 30);
      let total = c.fcb + c.bvb + c.b04;
      for (let i = 0; i < n && total < 9999; i++, total++) {
        let r = Math.random(), k = "b04";
        for (const [id, wt] of weights) { if ((r -= wt) < 0) { k = id; break; } }
        c[k] += 1;
      }
      return { pollCounts: c };
    });
  }
  pollShiftPcts() {
    this.setState((st) => {
      const p = (st.pollPcts || [46, 31, 23]).slice();
      const from = Math.floor(Math.random() * 3);
      let to = Math.floor(Math.random() * 2); if (to >= from) to++;
      const amt = Math.min(3 + Math.floor(Math.random() * 5), p[from] - 10);
      if (amt <= 0) return null;
      p[from] -= amt; p[to] += amt;
      if (Math.max(...p) > 70) return null;
      return { pollPcts: p };
    });
  }
  pollVals() {
    const s = this.state;
    const on = !!s.pollOn && s.screen === "fanzone";
    const collapsed = !!s.pollCollapsed;
    const voted = !!s.pollVote;
    const H_OPEN = 46 + 3 + 58 + (3 * 50 + 2 * 8 + 12) + 36, H_SHUT = 46 + 3 + 58;
    const h = collapsed ? H_SHUT : H_OPEN;
    const counts = s.pollCounts || { fcb: 610, bvb: 420, b04: 317 };
    const total = (counts.fcb + counts.bvb + counts.b04) || 1;
    const pcts = s.pollPcts || [46, 31, 23];
    const raw = [
      { id: "fcb", name: "FC Bayern München", logo: "assets/poll/logo-fcb.png", ring: "rgba(220,5,45,0.28)" },
      { id: "bvb", name: "Borussia Dortmund", logo: "assets/poll/logo-bvb.png", ring: "rgba(253,225,0,0.22)" },
      { id: "b04", name: "Bayer 04 Leverkusen", logo: "assets/poll/logo-b04.png", ring: "rgba(255,255,255,0.12)" }
    ];
    // post the screen + poll state to the prototype shell so it can enable its Poll button
    const report = (s.screen === "fanzone" ? "fanzone" : "other") + "|" + (on && !s.pollClosing ? "on" : "off");
    if (report !== this._pollReport) {
      this._pollReport = report;
      setTimeout(() => { try { if (window.parent && window.parent !== window) window.parent.postMessage({ fz: "state", screen: s.screen, poll: on && !s.pollClosing }, "*"); } catch (e) {} }, 0);
    }
    return {
      pollMounted: on,
      pollCls: s.pollClosing ? "is-out" : "",
      pollH: h,
      fzPanelTop: on && !s.pollClosing ? 265 + h + 8 : 273,
      pollTimerPct: Math.max(0, Math.min(100, s.pollTime ?? 100)),
      pollToggleCollapse: () => this.setState({ pollCollapsed: !collapsed }),
      pollCollapseLabel: collapsed ? "Expand poll" : "Collapse poll",
      pollChevronRot: collapsed ? 180 : 0,
      pollVoted: voted,
      pollVotesLabel: (total / 1000).toFixed(1) + "K",
      pollOptions: raw.map((o, i) => {
        const sel = s.pollVote === o.id;
        return {
          ...o,
          pct: pcts[i],
          mine: sel,
          border: sel ? "#FFF200" : "rgba(255,255,255,0.07)",
          bg: sel ? "#C9C716" : "rgba(255,255,255,0.04)",
          fill: sel ? "#FFF200" : "rgba(255,255,255,0.09)",
          fillPct: voted ? pcts[i] : 0,
          text: sel ? "#0A1016" : "#FFFFFF",
          pick: () => this.setState((st) => {
            if (st.pollVote) return null;
            const c = { ...(st.pollCounts || { fcb: 610, bvb: 420, b04: 317 }) };
            if (c.fcb + c.bvb + c.b04 < 9999) c[o.id] += 1;
            return { pollVote: o.id, pollCounts: c };
          })
        };
      })
    };
  }
'''
src = must_replace(src, "  renderVals() {\n    if (!this._crReady) this.crInit();\n",
                   LOGIC + "  renderVals() {\n    if (!this._crReady) this.crInit();\n")
src = must_replace(src, "    return {\n      ...this.crVals(),", "    return {\n      ...this.crVals(),\n      ...this.pollVals(),")

# listen to the shell; stop on unmount; end the poll when FanZone closes
src = must_replace(src, "  componentDidMount() {\n",
"""  componentDidMount() {
    this._onShellMsg = (e) => {
      const d = e && e.data;
      if (!d || d.fz !== "poll") return;
      if (d.on) this.pollStart(); else this.pollEnd();
    };
    window.addEventListener("message", this._onShellMsg);
""")
src = must_replace(src, "  componentWillUnmount() { ",
                   "  componentWillUnmount() { window.removeEventListener(\"message\", this._onShellMsg); this.pollClear(); clearTimeout(this._pollOutT); ")
src = must_replace(src, "  goHome = () => { clearTimeout(this._ftueTimer);",
                   "  goHome = () => { this.pollEnd(true); clearTimeout(this._ftueTimer);")

open(PATH, 'w', encoding='utf-8').write(src)
print('ok')
