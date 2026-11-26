"""Live updates (Figma FanZone 80-20 38:188098): a red card alert takes over the chat, then drops into the chat as a message and scrolls up with the rest."""
import sys
p = sys.argv[1]; s = open(p).read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:80])
    s = s.replace(a, b)

JERSEY = '''<svg class="lu-jersey" width="40" height="33" viewBox="0 0 42 34" fill="none" aria-hidden="true"><path d="M14.1611 0.5C14.1611 0.5 18.1152 1.5 20.6611 1.5C23.207 1.5 27.1611 0.5 27.1611 0.5L26.6611 7H14.6611L14.1611 0.5Z" fill="white" fill-opacity="0.5"/><path d="M26.0778 0.412598C25.5825 0.412598 23.5778 4.1251 20.6611 4.9501C17.3278 3.7126 15.7417 0.412597 15.2445 0.412598C14.8502 0.412598 10.5123 1.65507 8.7325 2.16968C8.23547 2.3134 7.78758 2.58362 7.42658 2.95425L0.817572 9.73949C0.724802 9.83473 0.705789 9.97968 0.770855 10.0956L2.74447 13.6126L5.66113 15.6751L10.461 11.1505C10.6541 10.9684 10.9714 11.0995 10.9669 11.365C10.9093 14.7934 10.6611 29.6711 10.6611 31.3501C10.6611 31.9258 21.0778 33.4126 21.0778 33.4126L28.9945 32.1751C28.9945 32.1751 30.6611 31.9258 30.6611 31.3501C30.6611 30.7895 30.359 19.9793 30.3431 11.3591C30.3427 11.0961 30.6568 10.9613 30.8482 11.1416L35.6611 15.6751L38.5778 13.6126L40.6611 9.9001L33.901 2.96332C33.536 2.58878 33.0823 2.31695 32.5792 2.17413C30.7678 1.65992 26.3461 0.412598 26.0778 0.412598Z" fill="#CE1141"/><path d="M10.8411 19L11.8286 19.9447C13.3346 21.0213 14.1739 22.4481 14.1739 23.9312C14.1737 25.3796 14.9741 26.7755 16.4175 27.844L16.8166 28.1385C18.2603 29.2069 19.0611 30.6028 19.0612 32.0513L19.1611 33.5L14.3881 32.1493L11.0194 31.1105C10.8071 31.045 10.6634 30.8473 10.6668 30.6252L10.8411 19Z" fill="black" fill-opacity="0.1"/><path d="M26.1611 0.5C26.1611 0.5 22.3534 5 20.6611 5C18.9688 5 15.1611 0.5 15.1611 0.5" stroke-linecap="round" stroke="white"/><path d="M18.2716 10.1839V17.5519C18.2716 17.6959 18.2436 17.7919 18.1876 17.8399C18.1396 17.8799 18.0396 17.8999 17.8876 17.8999H17.2276C17.0756 17.8999 16.9716 17.8799 16.9156 17.8399C16.8676 17.7919 16.8436 17.6959 16.8436 17.5519V11.1319H15.6196C15.4756 11.1319 15.3796 11.1079 15.3316 11.0599C15.2916 11.0039 15.2716 10.8999 15.2716 10.7479V10.2199C15.2716 10.0679 15.2916 9.9679 15.3316 9.9199C15.3796 9.8639 15.4756 9.8359 15.6196 9.8359H17.8876C18.0396 9.8359 18.1396 9.8599 18.1876 9.9079C18.2436 9.9479 18.2716 10.0399 18.2716 10.1839ZM22.881 18.0679C21.553 18.0679 20.665 17.5319 20.217 16.4599C20.121 16.2359 20.053 15.9919 20.013 15.7279C19.973 15.4639 19.953 15.1239 19.953 14.7079V13.1479C19.953 12.7239 19.973 12.3759 20.013 12.1039C20.053 11.8239 20.121 11.5679 20.217 11.3359C20.665 10.2239 21.553 9.6679 22.881 9.6679C24.209 9.6679 25.097 10.2039 25.545 11.2759C25.641 11.4999 25.709 11.7439 25.749 12.0079C25.789 12.2719 25.809 12.6119 25.809 13.0279V14.5879C25.809 15.0119 25.789 15.3639 25.749 15.6439C25.709 15.9159 25.641 16.1679 25.545 16.3999C25.097 17.5119 24.209 18.0679 22.881 18.0679ZM22.881 10.9999C22.361 10.9999 21.993 11.1479 21.777 11.4439C21.569 11.7399 21.465 12.2519 21.465 12.9799V14.7559C21.465 15.4919 21.569 16.0079 21.777 16.3039C21.985 16.5919 22.353 16.7359 22.881 16.7359C23.409 16.7359 23.777 16.5919 23.985 16.3039C24.193 16.0079 24.297 15.4919 24.297 14.7559V12.9799C24.297 12.2519 24.189 11.7399 23.973 11.4439C23.765 11.1479 23.401 10.9999 22.881 10.9999Z" fill="#F9FAFA"/><path d="M35.1611 16C39.4098 14.577 41.1611 10 41.1611 10" stroke-linecap="round" stroke="white"/><path d="M0.500186 9.99996C1.79007 14.0995 5.82324 15.6951 5.82324 15.6951" stroke-linecap="round" stroke="white"/></svg>'''

def card(cls):
    return ('<div class="lu-card ' + cls + '">'
      '<div class="lu-hd"><span class="lu-min">46’</span><span class="lu-ttl">Red card</span></div>'
      '<div class="lu-body"><div class="lu-pl">' + JERSEY + '<span class="lu-nm">Julian Alvarez</span><img src="assets/img/logo-atletico.png" alt="Atlético de Madrid" width="32" height="32"></div>'
      '<div class="lu-tx">Rodrygo comes off for Diaz</div></div></div>')

CSS = '''  /* Live updates (Figma 38:188098) */
  .lu-card { position: relative; z-index: 1; box-sizing: border-box; width: 100%; display: flex; flex-direction: column; gap: 12px; padding: 16px; border: 1px solid rgba(249,250,250,.2); border-radius: 10px; background: linear-gradient(203.7deg, rgba(206,17,65,.3) 0%, rgba(206,17,65,.3) 16.36%, rgba(206,17,65,0) 30.64%), #1B2326; font-family: 'DAZN Oscine', sans-serif; color: #F9FAFA; text-align: left; }
  .lu-card.lu-msg { padding: 8px 12px; background: linear-gradient(201.5deg, rgba(206,17,65,.3) 0%, rgba(206,17,65,.3) 16.36%, rgba(206,17,65,0) 30.64%), #1B2326; }
  .lu-hd { display: flex; align-items: center; gap: 8px; }
  .lu-min { padding: 2px 6px; border-radius: 12px; background: rgba(249,250,250,.12); font-weight: 700; font-size: 16px; line-height: normal; }
  .lu-ttl { font-weight: 700; font-size: 18px; line-height: 1.38; }
  .lu-body { display: flex; flex-direction: column; gap: 8px; }
  .lu-pl { display: flex; align-items: center; gap: 12px; height: 55px; box-sizing: border-box; padding: 8px 10px; border-radius: 12px; background: rgba(249,250,250,.04); }
  .lu-jersey { flex-shrink: 0; display: block; }
  .lu-nm { flex: 1; min-width: 0; font-weight: 700; font-size: 16px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .lu-pl img { flex-shrink: 0; display: block; width: 32px; height: 32px; object-fit: contain; }
  .lu-tx { font-size: 14px; line-height: 1.5; }
  .lu-art { position: absolute; border-radius: 9%/7%; background: linear-gradient(162deg, #FF5A4E 0%, #F21C1C 38%, #C80A12 100%); box-shadow: inset 0 0 0 1px rgba(255,255,255,.18), 0 18px 40px rgba(0,0,0,.45); pointer-events: none; overflow: hidden; }
  .lu-art::after { content: ""; position: absolute; inset: 0; background: linear-gradient(118deg, rgba(255,255,255,.38) 0%, rgba(255,255,255,.12) 34%, rgba(255,255,255,0) 35%); }
  .lu-over { position: absolute; left: 0; right: 0; top: 48px; bottom: 72px; z-index: 30; overflow: hidden; display: flex; flex-direction: column; justify-content: flex-end; padding: 8px 12px; box-sizing: border-box; background: linear-gradient(180deg, rgba(8,14,18,.64) 0%, #080E12 100%); animation: luFade .35s ease both; }
  .lu-over.lu-out { animation: luOut .4s ease forwards; }
  .lu-over .lu-card { animation: luUp .5s cubic-bezier(.2,.8,.2,1) .1s both; }
  .lu-over .lu-art { right: 34px; bottom: 120px; width: 132px; height: 182px; transform: rotate(16deg); animation: luArt .7s cubic-bezier(.2,.9,.25,1.15) .45s both; }
  .lu-row { position: relative; flex-shrink: 0; padding: 8px 12px; animation: fzMsgIn .45s cubic-bezier(.22,1,.36,1); overflow: hidden; }
  .lu-row .lu-art { z-index: 2; right: 26px; top: 0; width: 36px; height: 50px; transform: rotate(16deg); animation: luArtMini .5s cubic-bezier(.2,.9,.25,1.2) .15s both; }
  @keyframes luFade { from { opacity: 0; } to { opacity: 1; } }
  @keyframes luOut { from { opacity: 1; } to { opacity: 0; } }
  @keyframes luUp { from { opacity: 0; transform: translateY(24px) scale(.97); } to { opacity: 1; transform: none; } }
  @keyframes luArt { from { opacity: 0; transform: translate(220px, 40px) rotate(40deg); } to { opacity: 1; transform: rotate(16deg); } }
  @keyframes luArtMini { from { opacity: 0; transform: translate(20px, 14px) rotate(36deg); } to { opacity: 1; transform: rotate(16deg); } }
'''
rep('  @keyframes fzEbIn {', CSS + '  @keyframes fzEbIn {')

OVER = ('        <!-- Live updates (Figma 38:188098): the event takes over the chat for a few seconds -->\n'
        '        <sc-if value="{{ luOver }}" hint-placeholder-val="{{ false }}">\n'
        '          <div class="lu-over {{ luOutCls }}" role="status" aria-label="Live update">' + '<span class="lu-art" aria-hidden="true"></span>' + card('') + '</div>\n'
        '        </sc-if>\n')
rep('        <!-- chat feed -->\n', OVER + '        <!-- chat feed -->\n')

# chat feed: live update cards sit in the feed like messages
a = '            <sc-for list="{{ chatMessages }}" as="m" key="m.id" hint-placeholder-count="4">\n'
i = s.index(a); j = s.index('            </sc-for>\n', i)
s = s[:i] + a + '              <sc-if value="{{ m.lu }}" hint-placeholder-val="{{ false }}"><div class="lu-row"><span class="lu-art" aria-hidden="true"></span>' + card('lu-msg') + '</div></sc-if>\n              <sc-if value="{{ m.notLu }}" hint-placeholder-val="{{ true }}">\n' + s[i+len(a):j] + '              </sc-if>\n' + s[j:]

rep('      chatMessages: s.feed.map(m => {\n        const p = this.synthProfile(m.name, m.avatar);',
    '      chatMessages: s.feed.map(m => {\n        if (m.lu) return { id: m.id, lu: true, notLu: false };\n        const p = this.synthProfile(m.name, m.avatar);')
rep('return { ...m, ...fzAv, ring: myFav ? myFav.card', 'return { ...m, ...fzAv, notLu: true, ring: myFav ? myFav.card')
rep('return { ...m, ...fzAv, text: this.lightText(m),', 'return { ...m, ...fzAv, notLu: true, text: this.lightText(m),')

rep('      ebOn: !!this.state.ebOn && this.state.screen === "fanzone",',
    '      luOver: !!this.state.luOver && this.state.screen === "fanzone", luOutCls: this.state.luOut ? "lu-out" : "",\n      ebOn: !!this.state.ebOn && this.state.screen === "fanzone",')

rep('''if (["quiz", "pin", "battle", "leaderboard", "team", "eb", "typing", "blocked"].indexOf(q.get("moment")) >= 0)''',
    '''if (["quiz", "pin", "battle", "leaderboard", "team", "eb", "typing", "blocked", "liveupdate"].indexOf(q.get("moment")) >= 0)''')
rep('        else if (m === "eb") this.ebSoon(4000);\n',
    '        else if (m === "eb") this.ebSoon(4000);\n        else if (m === "liveupdate") this.luSoon(1800);\n')
# restart each time the slide is shown
rep('''      if (!e.data || e.data.fz !== "shown" || new URLSearchParams(location.search).get("moment") !== "eb") return;''',
    '''      if (e.data && e.data.fz === "shown" && new URLSearchParams(location.search).get("moment") === "liveupdate") { this.luReset(); this.luSoon(1800); return; }
      if (!e.data || e.data.fz !== "shown" || new URLSearchParams(location.search).get("moment") !== "eb") return;''')

METHODS = '''  // Live updates: the event covers the chat, then drops into the feed as a card; it comes round again every so often
  luReset() {
    clearTimeout(this._luT); clearTimeout(this._luT2); clearTimeout(this._luT3);
    this.setState(st => ({ luOver: false, luOut: false, feed: st.feed.filter(m => !m.lu) }));
  }
  luSoon(ms) {
    clearTimeout(this._luT);
    this._luT = setTimeout(() => {
      if (this.state.screen !== "fanzone") { this.luSoon(1500); return; }
      this.setState(st => ({ luOver: true, luOut: false, feed: st.feed.filter(m => !m.lu) }));
      this._luT2 = setTimeout(() => {
        this.setState({ luOut: true });
        this._luT3 = setTimeout(() => {
          this.setState(st => ({ luOver: false, luOut: false, atBottom: true, feed: st.feed.concat({ id: "lu" + Date.now(), lu: true }).slice(-40) }));
          this.luSoon(16000);
        }, 380);
      }, 4200);
    }, ms);
  }
  // Engagement break: comes in after a delay and plays its video (muted, started from code)
'''
rep('  // Engagement break: comes in after a delay and plays its video (muted, started from code)\n', METHODS)
open(p, 'w').write(s); print("live-updates ok")
