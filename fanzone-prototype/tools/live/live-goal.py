"""Live updates: Goal flow (Figma 38:197736) next to the red card one. ?lu=goal picks it."""
import sys, re
p = sys.argv[1]; s = open(p).read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:90])
    s = s.replace(a, b)

BALL = ('<svg class="lu-ball" viewBox="0 0 64 64" aria-hidden="true"><defs><radialGradient id="luBallG" cx="38%" cy="32%" r="70%"><stop offset="0" stop-color="#fff"/><stop offset=".7" stop-color="#e9ecee"/><stop offset="1" stop-color="#b9bfc3"/></radialGradient><clipPath id="luBallC"><circle cx="32" cy="32" r="30"/></clipPath></defs>'
        '<circle cx="32" cy="32" r="30" fill="url(#luBallG)"/><g clip-path="url(#luBallC)" fill="#121a1f" stroke="#121a1f" stroke-width="1.6" stroke-linejoin="round">'
        '<polygon points="32,21 42.5,28.6 38.5,41 25.5,41 21.5,28.6"/><polygon points="32,-2 41,3 38,11 26,11 23,3"/><polygon points="60,22 68,28 64,38 56,36 54,27"/><polygon points="48,54 56,58 52,68 42,66 42,58"/><polygon points="16,54 22,58 22,66 12,68 8,58"/><polygon points="4,22 10,27 8,36 0,38 -4,28"/>'
        '<path d="M32 21V11M42.5 28.6L54 27M38.5 41L42 58M25.5 41L22 58M21.5 28.6L10 27" fill="none"/></g><circle cx="32" cy="32" r="30" fill="none" stroke="#0c161c" stroke-width="2"/></svg>')

def jersey(num):
    return ('<svg class="lu-jersey" width="40" height="33" viewBox="0 0 42 34" fill="none" aria-hidden="true"><path d="M14.1611 0.5C14.1611 0.5 18.1152 1.5 20.6611 1.5C23.207 1.5 27.1611 0.5 27.1611 0.5L26.6611 7H14.6611L14.1611 0.5Z" fill="white" fill-opacity="0.5"/>'
            '<path d="M26.0778 0.412598C25.5825 0.412598 23.5778 4.1251 20.6611 4.9501C17.3278 3.7126 15.7417 0.412597 15.2445 0.412598C14.8502 0.412598 10.5123 1.65507 8.7325 2.16968C8.23547 2.3134 7.78758 2.58362 7.42658 2.95425L0.817572 9.73949C0.724802 9.83473 0.705789 9.97968 0.770855 10.0956L2.74447 13.6126L5.66113 15.6751L10.461 11.1505C10.6541 10.9684 10.9714 11.0995 10.9669 11.365C10.9093 14.7934 10.6611 29.6711 10.6611 31.3501C10.6611 31.9258 21.0778 33.4126 21.0778 33.4126L28.9945 32.1751C28.9945 32.1751 30.6611 31.9258 30.6611 31.3501C30.6611 30.7895 30.359 19.9793 30.3431 11.3591C30.3427 11.0961 30.6568 10.9613 30.8482 11.1416L35.6611 15.6751L38.5778 13.6126L40.6611 9.9001L33.901 2.96332C33.536 2.58878 33.0823 2.31695 32.5792 2.17413C30.7678 1.65992 26.3461 0.412598 26.0778 0.412598Z" fill="#8B2346"/>'
            '<path d="M26.1611 0.5C26.1611 0.5 22.3534 5 20.6611 5C18.9688 5 15.1611 0.5 15.1611 0.5" stroke-linecap="round" stroke="white"/><path d="M35.1611 16C39.4098 14.577 41.1611 10 41.1611 10" stroke-linecap="round" stroke="white"/><path d="M0.500186 9.99996C1.79007 14.0995 5.82324 15.6951 5.82324 15.6951" stroke-linecap="round" stroke="white"/>'
            '<text x="20.7" y="18" text-anchor="middle" font-family="DAZN Oscine, sans-serif" font-weight="700" font-size="11" fill="#F9FAFA">' + num + '</text></svg>')

CHEV = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path fill-rule="evenodd" clip-rule="evenodd" d="M7.29289 10.7071L8.70711 9.29289L12 12.5858L15.2929 9.29289L16.7071 10.7071L12 15.4142L7.29289 10.7071Z" fill="#F9FAFA"/></svg>'
FIELD = ('<svg class="lu-field" viewBox="0 0 311 114" aria-label="Where the goal was scored"><rect x="1" y="1" width="309" height="112" rx="7" fill="rgba(249,250,250,.04)" stroke="rgba(249,250,250,.1)" stroke-width="2"/>'
         '<path d="M64 2V74H247V2" fill="none" stroke="rgba(249,250,250,.2)"/><path d="M115 2V24H196V2" fill="none" stroke="rgba(249,250,250,.2)"/><rect x="132" y="0" width="47" height="5" rx="2" fill="#4d5457"/>'
         '<path d="M131.5 74A24 24 0 0 0 179.5 74" fill="none" stroke="rgba(249,250,250,.2)"/><line class="lu-shot" x1="172" y1="84" x2="158" y2="5" stroke="#FFFA00" stroke-width="1.2" stroke-dasharray="3 3"/>'
         '<g transform="translate(164 76)"><circle cx="8" cy="8" r="7.5" fill="#fff" stroke="#0c161c"/><polygon points="8,4.5 11.3,6.9 10.1,10.8 5.9,10.8 4.7,6.9" fill="#0c161c"/></g></svg>')

def gcard(cls, toggle):
    btn = ('<button type="button" onClick="{{ m.luToggle }}" aria-label="{{ m.luToggleLabel }}" class="lu-chev" style="transform:rotate({{ m.luChevRot }}deg);">' + CHEV + '</button>') if toggle else ('<span class="lu-chev">' + CHEV + '</span>')
    field = '<sc-if value="{{ m.luOpen }}" hint-placeholder-val="{{ false }}">' + FIELD + '</sc-if>' if toggle else ''
    return ('<div class="lu-card lu-msg lu-goal ' + cls + '"><div class="lu-hd"><span class="lu-min lu-min-g">53’</span><span class="lu-ttl">GOAL!</span></div>'
            '<div class="lu-body"><div class="lu-pl">' + jersey("9") + '<span class="lu-nm">9 Gabriel Jesus</span><img src="assets/img/logo-barcelona.png" alt="FC Barcelona" width="32" height="32"></div>'
            '<div class="lu-txr"><span class="lu-tx">Rodrygo comes off for Diaz</span>' + btn + '</div>' + field + '</div></div>')

CSS = '''  .lu-goal { background: linear-gradient(217deg, rgba(206,17,65,.3) 0%, rgba(206,17,65,.3) 16.36%, rgba(206,17,65,0) 30.64%), #1B2326; }
  .lu-min-g { background: rgba(206,17,65,.5); }
  .lu-txr { display: flex; align-items: center; gap: 10px; } .lu-txr .lu-tx { flex: 1; min-width: 0; }
  .lu-chev { all: unset; flex-shrink: 0; width: 24px; height: 24px; border-radius: 9999px; background: rgba(255,255,255,.2); display: flex; align-items: center; justify-content: center; cursor: pointer; transition: transform .25s ease; }
  .lu-field { display: block; width: 100%; height: auto; animation: luFieldIn .35s ease both; }
  .lu-shot { stroke-dashoffset: 0; animation: luShot 1s ease .2s both; }
  .lu-ball { position: absolute; pointer-events: none; display: block; filter: drop-shadow(0 12px 24px rgba(0,0,0,.45)); }
  .lu-over .lu-ball { right: 40px; bottom: 140px; width: 150px; height: 150px; animation: luBallIn .9s cubic-bezier(.2,.9,.25,1.1) .4s both; }
  .lu-row .lu-ball { z-index: 2; right: 18px; top: 0; width: 40px; height: 40px; animation: luBallMini .6s cubic-bezier(.2,.9,.25,1.2) .15s both; }
  @keyframes luBallIn { from { opacity: 0; transform: translate(180px,-160px) rotate(-240deg) scale(.6); } to { opacity: 1; transform: none; } }
  @keyframes luBallMini { from { opacity: 0; transform: translate(20px,-14px) rotate(-180deg); } to { opacity: 1; transform: none; } }
  @keyframes luFieldIn { from { opacity: 0; transform: translateY(-6px); } to { opacity: 1; transform: none; } }
  @keyframes luShot { from { stroke-dasharray: 0 200; } to { stroke-dasharray: 3 3; } }
'''
rep('  @keyframes luFade {', CSS + '  @keyframes luFade {')

# overlay: red or goal
i = s.index('          <div class="lu-over {{ luOutCls }}"'); j = s.index('\n', i)
red = s[i:j]
s = s[:i] + '          <sc-if value="{{ luRed }}" hint-placeholder-val="{{ true }}">' + red.strip() + '</sc-if>\n          <sc-if value="{{ luGoal }}" hint-placeholder-val="{{ false }}"><div class="lu-over {{ luOutCls }}" role="status" aria-label="Live update: goal">' + BALL + gcard('', False) + '</div></sc-if>' + s[j:]

# feed row for goals
a = '              <sc-if value="{{ m.notLu }}" hint-placeholder-val="{{ true }}">\n'
rep(a, '              <sc-if value="{{ m.luGoal }}" hint-placeholder-val="{{ false }}"><div class="lu-row">' + BALL + gcard('', True) + '</div></sc-if>\n' + a)

rep('        if (m.lu) return { id: m.id, lu: true, notLu: false };',
    '''        if (m.lu) { const g = m.kind === "goal"; return { id: m.id, lu: !g, luGoal: g, notLu: false, luOpen: !!m.open, luChevRot: m.open ? 180 : 0, luToggleLabel: m.open ? "Hide where it was scored" : "Show where it was scored",
          luToggle: () => this.setState(st => ({ feed: st.feed.map(x => x.id === m.id ? Object.assign({}, x, { open: !x.open }) : x) })) }; }''')
rep('      luOver: !!this.state.luOver && this.state.screen === "fanzone", luOutCls: this.state.luOut ? "lu-out" : "",',
    '      luOver: !!this.state.luOver && this.state.screen === "fanzone", luOutCls: this.state.luOut ? "lu-out" : "", luGoal: this.luKind() === "goal", luRed: this.luKind() !== "goal",')
rep('feed: st.feed.concat({ id: "lu" + Date.now(), lu: true }).slice(-40) }));',
    'feed: st.feed.concat({ id: "lu" + Date.now(), lu: true, kind: this.luKind() }).slice(-40) }));\n          if (this.luKind() === "goal") { const id = this.state.feed.length; clearTimeout(this._luT4); this._luT4 = setTimeout(() => this.setState(st => ({ feed: st.feed.map(x => x.lu && !x.opened ? Object.assign({}, x, { open: true, opened: true }) : x) })), 2600); }')
rep('  luReset() {', '  luKind() { return new URLSearchParams(location.search).get("lu") === "goal" ? "goal" : "red"; }\n  luReset() {')
open(p, 'w').write(s); print("live-goal ok")
