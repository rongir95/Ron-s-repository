#!/usr/bin/env python3
"""FanZone quiz, started from the prototype shell like the poll (FanZone DS, file NIgPxOlNU4U3sWMRdoE4Qh).

  10..6  toast under the FanZone header (node 12930:53666 "Alert updated"): 359x72, radius 24, olive-yellow
         glass, a 40px countdown ring and "New quiz coming up / Your chance to win!"
  5..1   the countdown takes over the panel (node 12930:51084): 200px ring (track #3D4549, indicator #F7FF1A,
         16px), big yellow number, confetti, "New quiz is starting / Your chance to win!", close X
  quiz   (node 12930:52000, approximate for now): "Answer 3 questions" + 60s timer, question, progress bar,
         four answers, pager. Three questions about Bayern / Dortmund; a pick moves to the next question.
  result (node 12930:52826): title by score, "You got 3/3", time, "Moving to leaderboard" bar (3s), then the
         leaderboard opens with its loading state and your score.

All graphics are vector: rings and confetti are SVG/CSS, the trophy is the SVG from Figma (assets/quiz/).
The party emoji on the result screen is a bitmap (lottie) in Figma, so the vector gold trophy stands in for it.
The big numbers use DAZN Trim in Figma, which the prototype doesn't have: DAZN Oscine, condensed.

Run after fanzone-leaderboard.py:  python3 tools/fanzone-quiz.py FanZone.dc.html
"""
import json, random, sys

PATH = sys.argv[1]
src = open(PATH, encoding='utf-8').read()

def rep(old, new, count=1):
    global src
    n = src.count(old)
    if n != count:
        raise SystemExit(f'expected {count} occurrence(s), found {n}: {old[:100]!r}')
    src = src.replace(old, new)

FONT = "font-family:'DAZN Oscine',sans-serif;"
TRIM = "display:inline-block;font-weight:800;transform:scaleX(.8);transform-origin:center;"
YEL = '#F7FF1A'
CLOSE = ('<button onClick="{{ closeQuiz }}" aria-label="Close quiz" title="Close" style="position:absolute;right:12px;top:8px;z-index:3;width:31px;height:32px;border:0;padding:0;border-radius:32px;'
         'background:rgba(61,69,73,.6);display:flex;align-items:center;justify-content:center;cursor:pointer;">'
         '<svg width="14" height="14" viewBox="0 0 14 14" fill="none" aria-hidden="true"><path d="M1.5 1.5l11 11M12.5 1.5l-11 11" stroke="#F9FAFA" stroke-width="1.8" stroke-linecap="round"/></svg></button>')

# confetti: small vector pieces around the ring (fixed seed, so every build is the same)
rnd = random.Random(7)
COLORS = ['#E8175D', '#FFFA00', '#8E2DE2', '#4FC3F7', '#FF7A00', '#2ECC71', '#F9FAFA']
pieces = []
for i in range(34):
    x, y = rnd.uniform(14, 361), rnd.uniform(10, 360)
    if 70 < x < 305 and 60 < y < 310 and rnd.random() < .85:
        continue  # keep the ring itself clear
    c = rnd.choice(COLORS)
    kind = rnd.choice(['rect', 'rect', 'dot', 'curl'])
    rot, d, dur = rnd.randint(0, 359), rnd.uniform(0, 2), rnd.uniform(2.2, 3.6)
    if kind == 'rect':
        shape = f'<span style="display:block;width:{rnd.choice([5,6,8])}px;height:{rnd.choice([9,11,13])}px;border-radius:1.5px;background:{c};"></span>'
    elif kind == 'dot':
        s = rnd.choice([4, 5, 7])
        shape = f'<span style="display:block;width:{s}px;height:{s}px;border-radius:50%;background:{c};"></span>'
    else:
        shape = f'<svg width="22" height="16" viewBox="0 0 22 16" fill="none" style="display:block;"><path d="M2 12c3-8 6 4 9-4s6 2 9-5" stroke="{c}" stroke-width="3" stroke-linecap="round"/></svg>'
    pieces.append(f'<span style="position:absolute;left:{x:.0f}px;top:{y:.0f}px;transform:rotate({rot}deg);animation:qzConf {dur:.1f}s ease-in-out {d:.1f}s infinite alternate;">{shape}</span>')
CONFETTI = '<div aria-hidden="true" style="position:absolute;left:0;top:8px;width:375px;height:375px;pointer-events:none;">' + ''.join(pieces) + '</div>'

TOAST = '''        <!-- Quiz coming up toast (FanZone DS 12930:53666) -->
        <sc-if value="{{ qzToast }}" hint-placeholder-val="{{ false }}">
          <div role="status" aria-live="polite" style="position:absolute;left:8px;right:8px;top:56px;z-index:6;height:72px;box-sizing:border-box;padding:12px 16px;border-radius:24px;border:2px solid rgba(249,250,250,.1);
            background:linear-gradient(100deg,rgba(247,255,26,.44) 0%,rgba(247,255,26,.15) 100%),rgba(36,45,51,.6);-webkit-backdrop-filter:blur(40px);backdrop-filter:blur(40px);
            display:flex;align-items:center;gap:4px;animation:qzToastIn .4s cubic-bezier(.22,1,.36,1);''' + FONT + '''">
            <span style="position:relative;width:48px;height:48px;flex-shrink:0;">
              <svg width="48" height="48" viewBox="0 0 48 48" aria-hidden="true" style="position:absolute;inset:0;display:block;transform:rotate(-90deg);">
                <circle cx="24" cy="24" r="20" fill="#0C161C"/>
                <circle cx="24" cy="24" r="18" fill="none" stroke="#3D4549" stroke-width="4"/>
                <circle cx="24" cy="24" r="18" fill="none" stroke="''' + YEL + '''" stroke-width="4" stroke-linecap="round" stroke-dasharray="113.1" style="animation:qzSweepS 1s linear infinite;"/>
              </svg>
              <span style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:20px;color:''' + YEL + ''';">{{ qzNum }}</span>
            </span>
            <span style="display:flex;flex-direction:column;gap:6px;min-width:0;">
              <span style="font-weight:700;font-size:16px;line-height:1;color:''' + YEL + ''';">New quiz coming up</span>
              <span style="font-weight:700;font-size:14px;line-height:1;color:#F9FAFA;">Your chance to win!</span>
            </span>
          </div>
        </sc-if>
'''

QUESTIONS = [
    {"q": "What is the Bayern v Dortmund fixture called?", "a": ["Der Klassiker", "Revierderby", "El Clásico", "Nordderby"], "c": 0},
    {"q": "Which stadium is Bayern München's home?", "a": ["Signal Iduna Park", "Allianz Arena", "Olympiastadion", "Volksparkstadion"], "c": 1},
    {"q": "What is Dortmund's famous south stand called?", "a": ["The Kop", "Südkurve", "Die Gelbe Wand", "Curva Sud"], "c": 2},
]

FULL = '''        <!-- Quiz: countdown (12930:51084), questions (12930:52000), results (12930:52826) -->
        <sc-if value="{{ qzFull }}" hint-placeholder-val="{{ false }}">
          <div role="dialog" aria-label="Quiz" style="position:absolute;left:0;right:0;top:48px;bottom:0;z-index:8;overflow:hidden;background:linear-gradient(180deg,#141C20 0%,#0B1317 48%,#080E12 77%);animation:fzFadeIn .25s ease;''' + FONT + '''">
            <sc-if value="{{ qzCount }}" hint-placeholder-val="{{ false }}">
              ''' + CLOSE + '''
              ''' + CONFETTI + '''
              <div style="position:absolute;left:68px;top:71px;width:240px;height:240px;">
                <svg width="240" height="240" viewBox="0 0 240 240" aria-hidden="true" style="position:absolute;inset:0;display:block;transform:rotate(-90deg);">
                  <circle cx="120" cy="120" r="100" fill="#0C161C"/>
                  <circle cx="120" cy="120" r="92" fill="none" stroke="#3D4549" stroke-width="16"/>
                  <circle cx="120" cy="120" r="92" fill="none" stroke="''' + YEL + '''" stroke-width="16" stroke-linecap="round" stroke-dasharray="578.1" style="animation:qzSweepL 1s linear infinite;"/>
                </svg>
                <span style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font-size:128px;line-height:1;color:''' + YEL + ''';"><span style="''' + TRIM + '''animation:qzTick 1s ease-out infinite;">{{ qzNum }}</span></span>
              </div>
              <div style="position:absolute;left:16px;right:16px;top:373px;text-align:center;">
                <div style="font-weight:700;font-size:24px;line-height:28px;color:''' + YEL + ''';">New quiz is starting</div>
                <div style="margin-top:4px;font-weight:700;font-size:18px;line-height:24px;color:#F9FAFA;">Your chance to win!</div>
              </div>
            </sc-if>
            <sc-if value="{{ qzAsk }}" hint-placeholder-val="{{ false }}">
              <div style="position:relative;height:40px;background:#1B2326;display:flex;align-items:center;justify-content:center;gap:6px;font-weight:700;font-size:16px;color:#F9FAFA;">
                <span>Answer 3 questions</span><span style="color:''' + YEL + ''';font-variant-numeric:tabular-nums;">{{ qzClock }}</span>
                <button onClick="{{ closeQuiz }}" aria-label="Close quiz" style="position:absolute;right:12px;top:8px;width:24px;height:24px;border:0;padding:0;background:transparent;cursor:pointer;"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" aria-hidden="true" style="display:block;"><path d="M6 6l12 12M18 6L6 18" stroke="#F9FAFA" stroke-width="2" stroke-linecap="round"/></svg></button>
              </div>
              <div style="padding:16px 16px 0;">
                <div style="text-align:center;font-weight:700;font-size:16px;line-height:22px;color:#F9FAFA;">{{ qzQuestion }}</div>
                <div style="margin-top:12px;height:4px;border-radius:2px;background:#3D4549;overflow:hidden;"><span style="display:block;height:100%;width:{{ qzBar }}%;background:''' + YEL + ''';transition:width .4s ease;"></span></div>
                <div style="margin-top:8px;display:flex;flex-direction:column;gap:10px;">
                  <sc-for list="{{ qzAnswers }}" as="a" hint-placeholder-count="4">
                    <button onClick="{{ a.pick }}" style="height:70px;border-radius:8px;cursor:pointer;box-sizing:border-box;''' + FONT + '''font-weight:700;font-size:18px;letter-spacing:.02em;text-transform:uppercase;transition:all .2s ease;{{ a.style }}">{{ a.text }}</button>
                  </sc-for>
                </div>
                <div style="margin-top:14px;display:flex;justify-content:center;">
                  <span style="display:flex;gap:6px;padding:3px 8px;border-radius:6px;background:#3D4549;font-weight:700;font-size:14px;">
                    <sc-for list="{{ qzPager }}" as="p" hint-placeholder-count="3"><span style="color:{{ p.color }};">{{ p.n }}</span></sc-for>
                  </span>
                </div>
              </div>
            </sc-if>
            <sc-if value="{{ qzResult }}" hint-placeholder-val="{{ false }}">
              ''' + CLOSE + '''
              <div style="position:absolute;left:0;right:0;top:24px;display:flex;flex-direction:column;align-items:center;">
                <img src="assets/quiz/trophy.svg" alt="" width="84" height="84" style="display:block;animation:fzRxPop .5s cubic-bezier(.22,1.6,.36,1);">
                <div style="margin-top:12px;font-size:24px;line-height:28px;color:#F9FAFA;"><span style="''' + TRIM + '''">{{ qzTitle }}</span></div>
                <div style="margin-top:32px;font-size:20px;line-height:24px;color:#CED0D2;"><span style="''' + TRIM + '''">You got</span></div>
                <div style="margin-top:4px;font-size:118px;line-height:1;"><span style="''' + TRIM + '''"><span style="color:#5ADC8C;">{{ qzGood }}</span><span style="color:#F9FAFA;">/3</span></span></div>
                <div style="margin-top:6px;font-size:20px;line-height:24px;color:#F9FAFA;"><span style="''' + TRIM + '''">IN {{ qzTime }}</span></div>
              </div>
              <div style="position:absolute;left:0;right:0;bottom:46px;display:flex;flex-direction:column;align-items:center;gap:8px;">
                <span style="display:flex;align-items:center;gap:8px;font-size:16px;color:#F9FAFA;"><img src="assets/quiz/trophy.svg" alt="" width="24" height="24" style="display:block;">Moving to leaderboard</span>
                <span style="width:240px;height:12px;box-sizing:border-box;padding:2px;border-radius:6px;background:#576065;"><span style="display:block;height:8px;border-radius:4px;background:''' + YEL + ''';animation:qzLoad 3s linear forwards;"></span></span>
              </div>
            </sc-if>
          </div>
        </sc-if>
'''
rep('        <!-- chat feed -->\n', TOAST + FULL + '        <!-- chat feed -->\n')

rep('  @keyframes fzPushIn {',
    '  @keyframes qzToastIn { from { opacity: 0; transform: translateY(-14px); } to { opacity: 1; transform: none; } }\n'
    '  @keyframes qzSweepS { from { stroke-dashoffset: 0; } to { stroke-dashoffset: 113.1; } }\n'
    '  @keyframes qzSweepL { from { stroke-dashoffset: 0; } to { stroke-dashoffset: 578.1; } }\n'
    '  @keyframes qzTick { 0% { opacity: .2; transform: scaleX(.8) scale(1.25); } 25% { opacity: 1; transform: scaleX(.8) scale(1); } 100% { transform: scaleX(.8) scale(1); } }\n'
    '  @keyframes qzConf { from { translate: 0 0; } to { translate: 4px 10px; rotate: 35deg; } }\n'
    '  @keyframes qzLoad { from { width: 4px; } to { width: 100%; } }\n'
    '  @keyframes fzPushIn {')

LOGIC = '''  // Quiz (started from the shell): toast 10..6, countdown 5..1, three questions, result, leaderboard
  startQuiz = () => {
    if (this.state.screen !== "fanzone") return;
    this.clearQuiz();
    this.setState({ qzPhase: "toast", qzLeft: 10, lbOpen: false, fzTyping: false });
    this._qzTick = setInterval(() => {
      const left = (this.state.qzLeft || 0) - 1;
      if (left <= 0) {
        clearInterval(this._qzTick);
        this.setState({ qzPhase: "ask", qzQ: 0, qzPick: null, qzGoodN: 0, qzClockS: 60, qzT0: Date.now() });
        this._qzClock = setInterval(() => this.setState(s => ({ qzClockS: Math.max(0, (s.qzClockS || 0) - 1) })), 1000);
        return;
      }
      this.setState({ qzLeft: left, qzPhase: left <= 5 ? "count" : "toast" });
    }, 1000);
  };
  clearQuiz = () => { clearInterval(this._qzTick); clearInterval(this._qzClock); clearTimeout(this._qzNext); clearTimeout(this._qzEnd); };
  closeQuiz = () => { this.clearQuiz(); this.setState({ qzPhase: null }); };
  pickQuiz = (i) => {
    const s = this.state;
    if (s.qzPick != null || s.qzPhase !== "ask") return;
    const good = (s.qzGoodN || 0) + (i === QZ[s.qzQ].c ? 1 : 0);
    this.setState({ qzPick: i, qzGoodN: good });
    this._qzNext = setTimeout(() => {
      if (s.qzQ < QZ.length - 1) { this.setState({ qzQ: s.qzQ + 1, qzPick: null }); return; }
      clearInterval(this._qzClock);
      this.setState({ qzPhase: "result", qzMs: Date.now() - (this.state.qzT0 || Date.now()) });
      this._qzEnd = setTimeout(() => {
        this.setState({ qzPhase: null, quizDone: true, quizScore: good, quizRank: good === 3 ? "11" : (good === 2 ? "86" : "1,204") });
        this.openLeaderboard(true);
      }, 3200);
    }, 650);
  };
  qzVals() {
    const s = this.state;
    const on = s.screen === "fanzone" ? s.qzPhase : null;
    const q = QZ[s.qzQ || 0];
    const two = (n) => String(Math.max(0, n)).padStart(2, "0");
    const ms = s.qzMs || 0, sec = Math.floor(ms / 1000);
    const good = s.qzGoodN || 0;
    return {
      qzToast: on === "toast", qzFull: on === "count" || on === "ask" || on === "result",
      qzCount: on === "count", qzAsk: on === "ask", qzResult: on === "result",
      qzNum: two(s.qzLeft || 0), closeQuiz: this.closeQuiz,
      qzClock: "00:" + two(s.qzClockS != null ? s.qzClockS : 60),
      qzQuestion: q.q, qzBar: Math.round(((s.qzQ || 0) + 1) / QZ.length * 100),
      qzAnswers: q.a.map((t, i) => {
        const picked = s.qzPick === i, other = s.qzPick != null && !picked;
        return { id: (s.qzQ || 0) + "-" + i, text: t, pick: () => this.pickQuiz(i),
          style: picked ? "border:2px solid #F7FF1A;background:rgba(255,255,255,.12);color:#F9FAFA;"
               : (other ? "border:2px solid transparent;background:rgba(255,255,255,.06);color:#6D7377;"
                        : "border:2px solid transparent;background:rgba(255,255,255,.1);color:#F9FAFA;") };
      }),
      qzPager: QZ.map((x, i) => ({ id: "p" + i, n: String(i + 1), color: i === (s.qzQ || 0) ? "#F9FAFA" : "#9EA2A4" })),
      qzTitle: good === 3 ? "A PERFECT GAME" : (good === 2 ? "GREAT GAME" : (good === 1 ? "GOOD TRY" : "BETTER LUCK NEXT TIME")),
      qzGood: String(good), qzTime: two(Math.floor(sec / 3600)) + ":" + two(Math.floor(sec / 60) % 60) + ":" + two(sec % 60),
    };
  }
  openFanZoneOver = (e) => {'''
rep('  openFanZoneOver = (e) => {', LOGIC)
rep('      ...this.gzVals(),', '      ...this.gzVals(),\n      ...this.qzVals(),')
rep('// FanZone chat: which team each fan supports', '// Quiz questions\nconst QZ = ' + json.dumps(QUESTIONS, ensure_ascii=False) + ';\n// FanZone chat: which team each fan supports')

# the shell starts / ends it, like the poll; the app reports whether a quiz is running
rep('      if (!d || d.fz !== "poll") return;',
    '      if (d && d.fz === "quiz") { if (d.on) this.startQuiz(); else this.closeQuiz(); return; }\n      if (!d || d.fz !== "poll") return;')
rep('const report = (s.screen === "fanzone" ? "fanzone" : "other") + "|" + (on && !s.pollClosing ? "on" : "off");',
    'const report = (s.screen === "fanzone" ? "fanzone" : "other") + "|" + (on && !s.pollClosing ? "on" : "off") + "|" + (s.qzPhase ? "quiz" : "-");')
rep('poll: on && !s.pollClosing }, "*");', 'poll: on && !s.pollClosing, quiz: !!s.qzPhase }, "*");')
# leaving FanZone ends it
rep('  goHome = () => { this.pollEnd(true);', '  goHome = () => { this.pollEnd(true); if (this.state.qzPhase) this.closeQuiz();')

open(PATH, 'w', encoding='utf-8').write(src)
print('ok')
