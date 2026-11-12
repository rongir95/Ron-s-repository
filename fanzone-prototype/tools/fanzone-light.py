#!/usr/bin/env python3
"""FanZone Light: predefined messages only (FanZone DS, file NIgPxOlNU4U3sWMRdoE4Qh, section 12371:19963
"Tier 2/3 - Chat is disabled").

  - The shell's "FanZone Light" switch turns it on and off live (no reload).
  - The message bar has no text field: a 56px quick-message button (radius 24, "New" badge) opens the drawer,
    followed by the reactions and Change team.
  - The drawer gets a third tab, Quick message, first: title, subtitle and the predefined messages as chips
    (a short loading skeleton first). GIF and Sticker tabs work as before: GIFs and stickers can still be sent.
  - The chat shows only predefined messages (plus GIFs and stickers).

Vector: the quick-message icon is the SVG from Figma (assets/icons/quick-message.svg); chips are HTML/CSS.

Run after the other scripts:  python3 tools/fanzone-light.py FanZone.dc.html
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
QUICK = ["Goal! ⚽️", "What a save! 🔥", "Seriously, ref?! 🫵", "VAR again?! 😒", "Let's go! 🤘",
         "That's never a penalty! 🙈", "What a comeback! 🚀", "We needed that goal! 🙌", "He's a magician! 🪄",
         "About time! 👏", "Sub him off! 😤", "Keep pressing! 💪", "I can't take it anymore! 😩",
         "So close! 😱", "That's how it's done! 💪", "Mia san mia! ❤️", "Echte Liebe! 💛🖤"]

# ---------------------------------------------------------------- setting: URL + live message
rep('    if (q.get("sponsor") === "1") o.fzSponsor = true;', '    if (q.get("sponsor") === "1") o.fzSponsor = true;\n    if (q.get("light") === "1") o.fzLight = true;')
rep('      if (d && d.fz === "sponsor") { this.setState({ fzSponsorLive: !!d.on }); return; }',
    '      if (d && d.fz === "sponsor") { this.setState({ fzSponsorLive: !!d.on }); return; }\n'
    '      if (d && d.fz === "light") { this.setState({ fzLightLive: !!d.on, fzTyping: false, gzOpen: false }); return; }')

# ---------------------------------------------------------------- message bar
QUICK_BTN = ('            <sc-if value="{{ fzLight }}" hint-placeholder-val="{{ false }}">\n'
             '              <button onClick="{{ openQuick }}" aria-label="Quick messages" style="position:relative;flex-shrink:0;width:56px;height:56px;box-sizing:border-box;border:1px solid rgba(255,255,255,.1);border-radius:24px;background:#242D33;display:flex;align-items:center;justify-content:center;cursor:pointer;">'
             '<img src="assets/icons/quick-message.svg" alt="" width="24" height="24" style="display:block;">'
             '<span style="position:absolute;left:31px;top:-4px;padding:4px 5px;border-radius:9999px;background:#FFFA00;' + FONT + 'font-weight:700;font-size:12px;line-height:9px;color:#080E12;text-transform:uppercase;">New</span></button>\n'
             '            </sc-if>\n')
rep('            <!-- entry point: your avatar (B + avatar in gradient ring) -->\n', QUICK_BTN + '            <!-- entry point: your avatar (B + avatar in gradient ring) -->\n')
# your avatar and the Message field exist only in regular FanZone
i = src.index('            <!-- entry point: your avatar (B + avatar in gradient ring) -->\n')
j = src.index('            <sc-if value="{{ fzTyping }}" hint-placeholder-val="{{ false }}">\n              <button onPointerDown="{{ kbKeep }}"', i)
src = src[:i] + '            <sc-if value="{{ fzRegular }}" hint-placeholder-val="{{ true }}">\n' + src[i:j] + '            </sc-if>\n' + src[j:]
rep('      fzBarX: s.fzTyping ? 0 : (s.fzBar2 ? -245 : 0),', '      fzBarX: (s.fzTyping || this.isLight()) ? 0 : (s.fzBar2 ? -245 : 0),')

# ---------------------------------------------------------------- drawer: Quick message tab
rep('<div role="tablist" aria-label="GIF or sticker" style="width:153px;', '<div role="tablist" aria-label="GIF or sticker" style="width:{{ gzTabsW }}px;')
rep('<button class="gz-tab" role="tab" aria-selected="{{ gzGifSel }}" aria-label="GIFs" onClick="{{ gzPickGif }}" style="width:72px;',
    '<sc-if value="{{ fzLight }}" hint-placeholder-val="{{ false }}"><button class="gz-tab" role="tab" aria-selected="{{ gzQuickSel }}" aria-label="Quick messages" onClick="{{ gzPickQuick }}" style="width:{{ gzTabW }}px;height:32px;border:0;padding:0;border-radius:6px;cursor:pointer;display:flex;align-items:center;justify-content:center;background:{{ gzQuickTabBg }};"><img src="assets/icons/quick-message.svg" alt="" width="24" height="24" style="display:block;"></button></sc-if>'
    '<button class="gz-tab" role="tab" aria-selected="{{ gzGifSel }}" aria-label="GIFs" onClick="{{ gzPickGif }}" style="width:{{ gzTabW }}px;')
rep('<button class="gz-tab" role="tab" aria-selected="{{ gzStickerSel }}" aria-label="Stickers" onClick="{{ gzPickSticker }}" style="width:72px;',
    '<button class="gz-tab" role="tab" aria-selected="{{ gzStickerSel }}" aria-label="Stickers" onClick="{{ gzPickSticker }}" style="width:{{ gzTabW }}px;')
rep('          <div style="flex-shrink:0;height:72px;box-sizing:border-box;padding:12px 16px;">',
    '          <div style="flex-shrink:0;height:72px;box-sizing:border-box;padding:12px 16px;{{ gzSearchDisplay }}">')

SK_W = [44, 72, 96, 84, 54, 82, 150, 70, 100, 76, 74, 100]
SKEL = ''.join(f'<span style="display:block;width:{w}px;height:32px;border-radius:8px;background:#2A3439;animation:fzSkel 1.1s ease-in-out infinite alternate;"></span>' for w in SK_W)
QUICK_PANEL = '''            <sc-if value="{{ gzShowQuick }}" hint-placeholder-val="{{ false }}">
              <div style="padding:8px 0 24px;text-align:center;''' + FONT + '''">
                <div style="font-weight:700;font-size:16px;line-height:25px;color:#F9FAFA;">Quick message</div>
                <div style="margin-top:4px;font-size:14px;line-height:20px;color:#B3B9BB;">Share your voice on every play with quick messages.</div>
                <div style="margin-top:24px;display:flex;flex-wrap:wrap;justify-content:center;gap:12px;">
                  <sc-if value="{{ gzQuickLoading }}" hint-placeholder-val="{{ false }}">''' + SKEL + '''</sc-if>
                  <sc-if value="{{ gzQuickReady }}" hint-placeholder-val="{{ true }}">
                    <sc-for list="{{ gzQuickItems }}" as="c" hint-placeholder-count="8">
                      <button class="gz-chip" onClick="{{ c.send }}" style="position:relative;height:32px;box-sizing:border-box;padding:2px 8px;border:0;border-radius:8px;background:#242D33;cursor:pointer;''' + FONT + '''font-size:12px;color:#F9FAFA;white-space:nowrap;">{{ c.text }}<span aria-hidden="true" style="position:absolute;left:4px;bottom:-3px;width:9px;height:9px;border-radius:2px;background:#242D33;transform:skewX(-35deg);"></span></button>
                    </sc-for>
                  </sc-if>
                </div>
              </div>
            </sc-if>
'''
rep('            <sc-if value="{{ gzShowGifs }}" hint-placeholder-val="{{ true }}">', QUICK_PANEL + '            <sc-if value="{{ gzShowGifs }}" hint-placeholder-val="{{ true }}">')
rep('  @keyframes fzPushIn {', '  @keyframes fzSkel { from { opacity: .55; } to { opacity: 1; } }\n  .gz-chip:hover { background: #2E383E !important; }\n  @keyframes fzPushIn {')

# ---------------------------------------------------------------- chat: predefined messages only
rep('return { ...m, ...fzAv, ring: t ? t.card : "#F2C400",', 'return { ...m, ...fzAv, text: this.lightText(m), ring: t ? t.card : "#F2C400",')

LOGIC = '''  // FanZone Light (predefined messages only)
  isLight = () => (this.state.fzLightLive != null ? this.state.fzLightLive : this.P.fzLight === true);
  lightText = (m) => {
    if (!this.isLight() || !m.text) return m.text;
    let h = 0; const k = String(m.id || m.name || "");
    for (let i = 0; i < k.length; i++) h = (h * 31 + k.charCodeAt(i)) >>> 0;
    return FZ_QUICK[h % FZ_QUICK.length];
  };
  openQuick = (e) => {
    if (e && e.stopPropagation) e.stopPropagation();
    clearTimeout(this._qmT);
    this.setState({ gzOpen: true, gzTab: "quick", gzExpanded: false, gzQuery: "", gzLoading: false, gzQuickLoading: true, showFtue: false });
    this._qmT = setTimeout(() => this.setState({ gzQuickLoading: false }), 800);
  };
  sendQuick = (text) => {
    const s = this.state;
    const av = s.avatar && AV_MAP[s.avatar] && AV_MAP[s.avatar].src ? AV_MAP[s.avatar].src : "";
    const msg = { id: "me" + Date.now(), name: s.nickname || "Charlie", avatar: av, text, mine: true };
    this.setState(st => ({ feed: st.feed.concat(msg).slice(-40), atBottom: true, gzOpen: false, gzExpanded: false }));
  };
  lightVals() {
    const s = this.state;
    const light = this.isLight();
    const tab = s.gzTab || "gif";
    const quick = light && tab === "quick";
    return {
      fzLight: light, fzRegular: !light, openQuick: this.openQuick,
      gzTabsW: light ? 343 : 153, gzTabW: light ? 111 : 72,
      gzQuickSel: quick ? "true" : "false", gzQuickTabBg: quick ? "#3D4549" : "transparent",
      gzPickQuick: () => { this.setState({ gzTab: "quick", gzQuickLoading: false }); },
      gzSearchDisplay: quick ? "display:none;" : "",
      gzShowQuick: quick, gzQuickLoading: quick && !!s.gzQuickLoading, gzQuickReady: quick && !s.gzQuickLoading,
      gzQuickItems: FZ_QUICK.map((t, i) => ({ id: "q" + i, text: t, send: () => this.sendQuick(t) })),
    };
  }
  openFanZoneOver = (e) => {'''
rep('  openFanZoneOver = (e) => {', LOGIC)
# after gzVals so the GIF tab defaults stay, and the light values win where they overlap
rep('      ...this.gzVals(),', '      ...this.gzVals(),\n      ...this.lightVals(),')
rep('// FanZone chat: which team each fan supports', '// FanZone Light: predefined messages\nconst FZ_QUICK = ' + json.dumps(QUICK, ensure_ascii=False) + ';\n// FanZone chat: which team each fan supports')
# leaving Light while on the Quick tab: back to GIFs
rep('    const tab = s.gzTab || "gif";\n    const searched', '    const tab = (s.gzTab === "quick" && !this.isLight()) ? "gif" : (s.gzTab || "gif");\n    const searched')

open(PATH, 'w', encoding='utf-8').write(src)
print('ok')
