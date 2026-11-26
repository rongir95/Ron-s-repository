#!/usr/bin/env python3
"""Patch for FanZone.dc.html: Actions on messages, per Figma FanZone 80-20 90:104486. Long press a message: the
reactions bar (FanZone DS "Reactions tooltip", the same 6 reactions as the match page heart) sits 12px above the
focused message, Report under it. Picking a reaction closes the focus and the reaction shows under that message in chat
(tap it there to remove it).
   python3 tools/live/msg-reactions.py FanZone.dc.html"""
import sys
p = sys.argv[1]; s = open(p, encoding='utf-8').read()
def rep(a, b):
    global s
    if s.count(a) != 1: raise SystemExit('expected once: ' + a[:90])
    s = s.replace(a, b)
# 1) reactions bar in the focus overlay, 12px above the message (message top 170 -> bar top 106)
rep('''          <div onClick="{{ msgFocusClose }}" style="position:absolute;left:0;right:0;top:48px;bottom:0;z-index:9;background:rgba(12,22,28,.55);-webkit-backdrop-filter:blur(22px);backdrop-filter:blur(22px);animation:fzFadeIn .2s ease;font-family:'DAZN Oscine',sans-serif;">
''', '''          <div onClick="{{ msgFocusClose }}" style="position:absolute;left:0;right:0;top:48px;bottom:0;z-index:9;background:rgba(12,22,28,.55);-webkit-backdrop-filter:blur(22px);backdrop-filter:blur(22px);animation:fzFadeIn .2s ease;font-family:'DAZN Oscine',sans-serif;">
            <div role="menu" aria-label="React to this message" style="position:absolute;left:calc(50% - 140px);top:106px;width:280px;height:52px;box-sizing:border-box;border-radius:9999px;background:rgba(36,45,51,.92);border:1px solid rgba(249,250,250,.2);-webkit-backdrop-filter:blur(30px);backdrop-filter:blur(30px);animation:fzRxIn .22s cubic-bezier(.22,1,.36,1);transform-origin:50% 100%;">
              <sc-for list="{{ msgRxItems }}" as="r" hint-placeholder-count="6">
                <button role="menuitem" class="fz-rx" onClick="{{ r.pick }}" aria-label="{{ r.name }}" style="position:absolute;top:1px;left:{{ r.x }}px;width:48px;height:48px;border:0;padding:0;background:transparent;cursor:pointer;{{ r.on }}"><img src="{{ r.src }}" alt="" width="48" height="48" draggable="false" style="display:block;"></button>
              </sc-for>
            </div>
''')
# 2) the chosen reaction under the message in chat
rep('''                  <sc-if value="{{ m.sticker }}" hint-placeholder-val="{{ false }}">
                    <img src="{{ m.sticker }}" alt="Sticker" style="display:block;margin-top:6px;width:100px;height:100px;object-fit:cover;">
                  </sc-if>
                </div>''', '''                  <sc-if value="{{ m.sticker }}" hint-placeholder-val="{{ false }}">
                    <img src="{{ m.sticker }}" alt="Sticker" style="display:block;margin-top:6px;width:100px;height:100px;object-fit:cover;">
                  </sc-if>
                  <sc-if value="{{ m.rxOn }}" hint-placeholder-val="{{ false }}">
                    <button type="button" onClick="{{ m.rxRemove }}" onPointerDown="{{ msgStop }}" aria-label="{{ m.rxLabel }}" title="Remove your reaction" style="margin-top:6px;height:28px;box-sizing:border-box;padding:0 10px 0 4px;border-radius:9999px;border:1px solid rgba(255,250,0,.5);background:rgba(255,250,0,.12);display:inline-flex;align-items:center;gap:4px;cursor:pointer;font-family:'DAZN Oscine',sans-serif;font-size:12px;font-weight:700;color:#FFFA00;animation:fzRxPop .3s cubic-bezier(.22,1.3,.36,1);"><img src="{{ m.rxSrc }}" alt="" width="22" height="22" draggable="false" style="display:block;">1</button>
                  </sc-if>
                </div>''')
# 3) state: remember which message was pressed; per-message reactions
rep('''    this._msgT = setTimeout(() => this.setState({ msgFocus: { name: m.name,''',
    '''    this._msgT = setTimeout(() => this.setState({ msgFocus: { id: m.id, name: m.name,''')
rep('''  msgFocusClose = () => this.setState({ msgFocus: null });''',
    '''  msgFocusClose = () => this.setState({ msgFocus: null });
  msgStop = (e) => { if (e && e.stopPropagation) e.stopPropagation(); };
  setMsgRx = (id, rx) => this.setState(st => { const r = Object.assign({}, st.msgRx || {}); if (rx) r[id] = rx; else delete r[id]; return { msgRx: r, msgFocus: null }; });''')
rep('''      msgFocusName: f ? f.name : "",''',
    '''      msgRxItems: [["like", "Like"], ["happy", "Happy"], ["cheer", "Cheering"], ["wow", "Mind blown"], ["angry", "Angry"], ["sad", "Sad"]].map(([id, name], i) => ({ id, name, x: 5 + i * 44, src: "assets/reactions/" + id + ".png",
        on: f && (s.msgRx || {})[f.id] === id ? "transform:scale(1.18);" : "",
        pick: (e) => { if (e && e.stopPropagation) e.stopPropagation(); if (f) this.setMsgRx(f.id, (s.msgRx || {})[f.id] === id ? null : id); } })),
      msgStop: this.msgStop,
      msgFocusName: f ? f.name : "",''')
rep('''        return { ...m, ...fzAv, notLu: true, text: this.lightText(m),''',
    '''        const rxId = (s.msgRx || {})[m.id];
        return { ...m, ...fzAv, notLu: true, rxOn: !!rxId, rxSrc: rxId ? "assets/reactions/" + rxId + ".png" : "", rxLabel: "Your reaction: " + (rxId || ""), rxRemove: (e) => { if (e && e.stopPropagation) e.stopPropagation(); this.setMsgRx(m.id, null); }, text: this.lightText(m),''')
open(p, 'w', encoding='utf-8').write(s); print('ok')
