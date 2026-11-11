#!/usr/bin/env python3
"""The updated iOS keyboard everywhere the prototype shows one, per Figma "[Dev] Public Profile"
(file ZERpW2GRsRMrd1URSjoeRB, screen "Empty status field" node 6377:235075, Keyboard node 8003:175519).

  375 x 317, light glass panel (radius 27), keys 45px tall with radius 8.5 (#EDF4F9, glyphs #474E53),
  blue return key (#0088FF), emoji and mic below. Key positions are Figma's. Built in HTML and CSS
  (letters are text, symbols are SVGs from Figma in assets/icons/kb-*.svg), so it stays sharp at any zoom.

Two places use it: the status editor on the Fan Card (replaces the dark 291px keyboard; the sheet above
it moves up to match) and the Comments composer (replaces the dark keyboard; Return still sends).

Run after the other scripts:  python3 tools/ios-keyboard.py FanZone.dc.html
"""
import re, sys

PATH = sys.argv[1]
src = open(PATH, encoding='utf-8').read()

KB_H = 317

ROW1 = [(8.5 + i * 36.4, 'qwertyuiop'[i]) for i in range(10)]
ROW2 = [(28.5 + i * 36, 'asdfghjkl'[i]) for i in range(9)]
ROW3 = [(x, c) for x, c in zip([67.4, 102.5, 137.7, 172.8, 207.9, 243, 278.1], 'zxcvbnm')]

THEMES = {
    # light: Figma "[Dev] Public Profile" 8003:175519; dark: FanZone DS "Fanzone package = expanded" 12302:56502
    'light': dict(panel='background:rgba(206,213,220,.78);-webkit-backdrop-filter:blur(20px) saturate(1.4);backdrop-filter:blur(20px) saturate(1.4);box-shadow:0 0 0 .5px rgba(255,255,255,.35) inset;',
                  key='#EDF4F9', glyph='#474E53', ret='#0088FF', icons=''),
    'dark':  dict(panel='background:#232323;',
                  key='#474747', glyph='#EDEDED', ret='#474747', icons='filter:brightness(0) invert(.93);'),
}

KEY = ("position:absolute;top:{y}px;left:{x}px;width:{w}px;height:45px;border-radius:8.5px;background:{bg};"
       "display:flex;align-items:center;justify-content:center;box-sizing:border-box;cursor:pointer;")
FONT = "font-family:-apple-system,'SF Pro Text','SF Compact Text',system-ui,'Helvetica Neue',Arial,sans-serif;"

def keyboard(position_style, return_attr='', theme='light'):
    T = THEMES[theme]
    k = lambda x, y, w, bg=None: KEY.format(x=x, y=y, w=w, bg=bg or T['key'])
    glyph = FONT + f"font-size:25px;line-height:1;color:{T['glyph']};padding-bottom:5px;"
    icon = T['icons']
    keys = []
    for y, row, w in ((24, ROW1, 30.4), (80, ROW2, 30), (136, ROW3, 29.1)):
        for x, c in row:
            keys.append(f'<span data-k="{c}" class="kb-l" style="{k(x, y, w)}{glyph}">{c}</span>')
    keys.append(f'<span data-k="shift" class="kb-shift" style="{k(8.5, 136, 44.7)}"><img src="assets/icons/kb-shift.svg" alt="" width="24" height="20" style="display:block;pointer-events:none;{icon}"></span>')
    keys.append(f'<span data-k="del" style="{k(321.5, 136, 45)}"><img src="assets/icons/kb-delete.svg" alt="" width="24" height="20" style="display:block;pointer-events:none;{icon}"></span>')
    keys.append(f'<span data-k="abc" style="{k(8.5, 192, 91.7)}{FONT}font-size:18px;color:{T["glyph"]};">ABC</span>')
    keys.append(f'<span data-k="space" style="{k(106.2, 192, 162.3)}"></span>')
    ret_k = 'none' if return_attr else 'ret'
    keys.append(f'<span data-k="{ret_k}"{return_attr} style="{k(274.5, 192, 92, T["ret"])}"><img src="assets/icons/kb-return.svg" alt="" width="20" height="18" style="display:block;pointer-events:none;"></span>')
    keys.append(f'<img src="assets/icons/kb-emoji.svg" alt="" width="27" height="27" style="position:absolute;left:36px;top:264px;display:block;{icon}">')
    keys.append(f'<img src="assets/icons/kb-mic.svg" alt="" width="19" height="29" style="position:absolute;left:317px;top:263px;display:block;{icon}">')
    return (f'<div class="ios-kb" ref="{{{{ kbRef }}}}" aria-hidden="true" style="{position_style}height:{KB_H}px;border-radius:27px;overflow:hidden;{T["panel"]}'
            'user-select:none;-webkit-user-select:none;touch-action:manipulation;">'
            '<div style="position:relative;width:375px;height:317px;margin:0 auto;">' + ''.join(keys) + '</div></div>')

# ---------------------------------------------------------------- status editor (Fan Card)
m = re.search(r'      <!-- iOS keyboard -->\n      <div style="position:absolute;left:0;right:0;bottom:0;height:291px;.*?\n      </div>\n(?=    </sc-if>\n\n    <!-- ===================== COMMENTS & REPLIES OVERLAYS)', src, re.S)
if not m:
    raise SystemExit('status keyboard not found')
src = src[:m.start()] + '      <!-- iOS keyboard (Figma 8003:175519) -->\n      ' + keyboard('position:absolute;left:0;right:0;bottom:0;z-index:25;') + '\n' + src[m.end():]
n = src.count('top:282px;bottom:291px;z-index:26;')
if n != 1:
    raise SystemExit(f'status sheet offset: {n}')
src = src.replace('top:282px;bottom:291px;z-index:26;', f'top:282px;bottom:{KB_H}px;z-index:26;')

# ---------------------------------------------------------------- Comments composer
m = re.search(r'      <!-- iOS keyboard \(decorative\) -->\n      <div style="background:#1a1c1e;padding-bottom:8px;">.*?\n        <div style="display:flex;justify-content:center;padding-top:8px;"><div style="width:134px;height:5px;border-radius:3px;background:#fff;"></div></div>\n      </div>\n', src, re.S)
if not m:
    raise SystemExit('composer keyboard not found')
src = (src[:m.start()] + '      <!-- iOS keyboard (Figma 8003:175519) -->\n      '
       + keyboard('position:relative;flex-shrink:0;', ' onClick="{{ crOnSend }}" title="Send"').replace('<span onClick', '<span onClick', 1)
       + '\n' + src[m.end():])

# ---------------------------------------------------------------- FanZone: typing state (FanZone DS 12302:56387)
# Focus the Message field: the dark keyboard comes up, the FanZone panel shrinks to the space above it,
# the field gets a light border (247px), reactions hide and a yellow send button appears.
m = re.search(r'\n      <div class="fz-fzpanel ', src)
if not m:
    raise SystemExit('FanZone panel not found')
src = (src[:m.start()] + '\n      <sc-if value="{{ fzTyping }}" hint-placeholder-val="{{ false }}">\n        '
       + '<div style="position:absolute;left:0;right:0;bottom:0;height:317px;z-index:40;pointer-events:auto;background:#0C161C;animation:kbUp .28s cubic-bezier(.22,1,.36,1);">'
       + keyboard('position:absolute;left:0;right:0;top:0;', theme='dark')
       + '</div>\n      </sc-if>' + src[m.start():])
def rep(old, new, count=1):
    global src
    n = src.count(old)
    if n != count:
        raise SystemExit(f'expected {count} occurrence(s), found {n}: {old[:100]!r}')
    src = src.replace(old, new)
rep('style="position:absolute;left:0;right:0;bottom:0;top:{{ fzPanelTop }}px;transform:{{ fzPanelTransform }};transition:top .55s cubic-bezier(.22,1,.36,1),',
    'style="position:absolute;left:0;right:0;bottom:{{ fzPanelBottom }}px;top:{{ fzPanelTop }}px;transform:{{ fzPanelTransform }};transition:top .55s cubic-bezier(.22,1,.36,1),bottom .28s cubic-bezier(.22,1,.36,1),')
rep('<input class="fz-msg-input" type="text" value="{{ fzDraft }}" onInput="{{ onFzDraft }}" onKeyDown="{{ onFzKey }}"',
    '<input class="fz-msg-input" type="text" value="{{ fzDraft }}" onInput="{{ onFzDraft }}" onKeyDown="{{ onFzKey }}" onFocus="{{ fzTypeOn }}" onBlur="{{ fzTypeOff }}" inputmode="none"')
rep('<div class="fz-fzpanel {{ fzPanelCls }}"', '<div class="fz-fzpanel {{ fzPanelCls }} {{ fzTypingCls }}"')
rep('<textarea ref="{{ statusInputRef }}"', '<textarea inputmode="none" ref="{{ statusInputRef }}"')
rep('<textarea ref="{{ crSetInputRef }}"', '<textarea inputmode="none" ref="{{ crSetInputRef }}"')
rep('height:57px;background:#242D33;border:1px solid #3D4549;border-radius:24px;', 'height:57px;background:#242D33;border:1px solid {{ fzMsgBorder }};border-radius:24px;')
rep('<sc-if value="{{ fzHasDraft }}" hint-placeholder-val="{{ false }}">\n                <button onClick="{{ sendFzMessage }}"',
    '<sc-if value="{{ fzInlineSend }}" hint-placeholder-val="{{ false }}">\n                <button onClick="{{ sendFzMessage }}"')
rep('            <!-- reactions -->\n            <div style="display:flex;align-items:center;gap:8px;flex-shrink:0;height:48px;padding-right:12px;">',
    '            <sc-if value="{{ fzTyping }}" hint-placeholder-val="{{ false }}">\n'
    '              <button onPointerDown="{{ kbKeep }}" onMouseDown="{{ kbKeep }}" onClick="{{ sendFzMessage }}" aria-label="Send message" style="flex-shrink:0;margin-left:4px;width:32px;height:32px;border:0;padding:0;border-radius:999px;background:#FFFA00;display:flex;align-items:center;justify-content:center;cursor:pointer;">'
    '<svg width="14" height="16" viewBox="0 0 14 16" fill="none" aria-hidden="true" style="display:block;"><path d="M1.6 1.1 13 7.3a.8.8 0 0 1 0 1.4L1.6 14.9a.8.8 0 0 1-1.1-1l2-5.2a1 1 0 0 0 0-.7l-2-5.1a.8.8 0 0 1 1.1-1.8z" fill="#080E12"/></svg></button>\n'
    '            </sc-if>\n'
    '            <!-- reactions -->\n            <div style="display:flex;align-items:center;gap:8px;flex-shrink:0;height:48px;padding-right:12px;{{ fzRxDisplay }}">')
rep("      fzBarX: s.fzBar2 ? -245 : 0,\n      fzInputW: s.fzBar2 ? 280 : 240,",
    "      fzBarX: s.fzTyping ? 0 : (s.fzBar2 ? -245 : 0),\n      fzInputW: s.fzTyping ? 247 : (s.fzBar2 ? 280 : 240),\n"
    "      fzTyping: !!s.fzTyping && s.screen === \"fanzone\", fzPanelBottom: (s.fzTyping && s.screen === \"fanzone\") ? 317 : 0,\n"
    "      fzMsgBorder: s.fzTyping ? \"rgba(255,255,255,.3)\" : \"#3D4549\", fzTypingCls: s.fzTyping ? \"fz-typing\" : \"\", fzRxDisplay: s.fzTyping ? \"display:none;\" : \"\",\n"
    "      fzInlineSend: !!s.fzHasDraft && !s.fzTyping, fzTypeOn: this.fzTypeOn, fzTypeOff: this.fzTypeOff, kbKeep: this.kbKeep, kbRef: this.kbRef,")

LOGIC = r"""  // FanZone typing state: focus the Message field -> keyboard up, panel above it
  fzTypeOn = () => { clearTimeout(this._fzTypeT); if (!this.state.fzTyping) this.setState({ fzTyping: true, fzBar2: false }); };
  fzTypeOff = () => {
    clearTimeout(this._fzTypeT);
    this._fzTypeT = setTimeout(() => {
      const a = document.activeElement;
      if (!(a && a.classList && a.classList.contains("fz-msg-input"))) this.setState({ fzTyping: false });
    }, 120);
  };
  kbKeep = (e) => { if (e && e.preventDefault) e.preventDefault(); };
  // the on-screen iOS keyboard types into the field you are in
  kbRef = (el) => {
    if (!el || el._kb) return;
    el._kb = true;
    if (!window.__kbTrack) {
      window.__kbTrack = true;
      document.addEventListener("focusin", (e) => { const t = e.target; if (t && (t.tagName === "INPUT" || t.tagName === "TEXTAREA")) window.__kbTarget = t; });
    }
    const field = () => {
      let t = document.activeElement;
      if (t && (t.tagName === "INPUT" || t.tagName === "TEXTAREA")) return t;
      t = window.__kbTarget;
      if (t && t.isConnected && t.offsetParent) return t;
      const all = Array.from(document.querySelectorAll("textarea, input[type=text], input:not([type])")).filter(x => x.offsetParent);
      return all[all.length - 1] || null;
    };
    el.addEventListener("mousedown", (e) => { const k = e.target.closest && e.target.closest("[data-k]"); if (!k || k.getAttribute("data-k") !== "none") e.preventDefault(); });
    el.addEventListener("pointerdown", (e) => {
      const k = e.target.closest && e.target.closest("[data-k]");
      if (!k) { e.preventDefault(); return; }
      const key = k.getAttribute("data-k");
      if (key === "none") return;              // a key with its own click (Comments: Return sends)
      e.preventDefault();                       // keep the field focused
      k.style.filter = "brightness(.82)"; setTimeout(() => { k.style.filter = ""; }, 110);
      const t = field();
      if (!t) return;
      if (key === "shift") { el.classList.toggle("kb-up"); return; }
      if (key === "abc") return;
      t.focus();
      if (key === "ret") { t.dispatchEvent(new KeyboardEvent("keydown", { key: "Enter", code: "Enter", keyCode: 13, which: 13, bubbles: true, cancelable: true })); return; }
      const v = t.value || "";
      let a = typeof t.selectionStart === "number" ? t.selectionStart : v.length;
      let b = typeof t.selectionEnd === "number" ? t.selectionEnd : v.length;
      let nv, pos;
      if (key === "del") {
        if (a === b && a > 0) a -= 1;
        nv = v.slice(0, a) + v.slice(b); pos = a;
      } else {
        let ch = key === "space" ? " " : key;
        if (el.classList.contains("kb-up") || (v.slice(0, a).trim() === "" && ch !== " ")) { ch = ch.toUpperCase(); el.classList.remove("kb-up"); }
        const max = t.maxLength > 0 ? t.maxLength : 100000;
        if (v.length - (b - a) + ch.length > max) return;
        nv = v.slice(0, a) + ch + v.slice(b); pos = a + ch.length;
      }
      const proto = t.tagName === "TEXTAREA" ? HTMLTextAreaElement.prototype : HTMLInputElement.prototype;
      Object.getOwnPropertyDescriptor(proto, "value").set.call(t, nv);
      t.dispatchEvent(new Event("input", { bubbles: true }));
      try { t.setSelectionRange(pos, pos); } catch (err) {}
    });
  };
  openFanZoneOver = (e) => {"""
rep('  openFanZoneOver = (e) => {', LOGIC)
rep('  @keyframes fzPushIn {', '  @keyframes kbUp { from { transform: translateY(100%); } to { transform: none; } }\n  .ios-kb.kb-up .kb-l { text-transform: uppercase; }\n  .fz-fzpanel.fz-typing { padding-bottom: 0 !important; }\n  .fz-fzpanel.fz-typing::after { display: none; }\n  .ios-kb.kb-up .kb-shift img { opacity: .55; }\n  @keyframes fzPushIn {')

# the keyboard's rounded corners show the composer's own background, not the comments behind it
old = '<div style="position:absolute;left:0;right:0;bottom:0;z-index:45;display:flex;flex-direction:column;">'
if src.count(old) != 1:
    raise SystemExit('composer wrapper not found')
src = src.replace(old, '<div style="position:absolute;left:0;right:0;bottom:0;z-index:45;display:flex;flex-direction:column;background:#0c161c;">')

open(PATH, 'w', encoding='utf-8').write(src)
print('ok')
