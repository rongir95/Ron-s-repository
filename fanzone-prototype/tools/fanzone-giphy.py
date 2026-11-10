#!/usr/bin/env python3
"""GIFs and stickers in FanZone, per the Figma "Giphy - Stickers - Dev" (file vyXEcIzwOA5N0iLEQ4fL03, page 2004:28, iOS flow).

  Tap the sticker icon in the Message field  -> the GIF drawer opens over FanZone (Default view)
  GIF / Sticker segmented control             -> switches the grid (2-column masonry / 3-column stickers)
  Tap the search field                        -> the drawer expands to full height (search field in focus)
  Typing                                      -> skeleton for a moment, then results (any text brings results)
  Tap a GIF or sticker                        -> it is posted to the chat as my message; the drawer closes
  X                                           -> closes the drawer

The GIFs are still frames (the Figma's animated files are up to 10 MB and could not be brought in from Figma);
GIFs and stickers were rendered from the Figma at 2x into assets/gif/ and assets/stickers/.
Sheet: #1B2326, 24px top corners (all drawers), handle 44x4 #CED0D2, close 24px #3D4549 circle.
Segmented control 153x40, border #3D4549, radius 9, states 72x32 radius 6 (selected #3D4549).
Search field 343x48, border #6D7377, radius 8, placeholder #6D7377 16px.

Run after fanzone-bar.py:  python3 tools/fanzone-giphy.py FanZone.dc.html
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

G = 'assets/gif/'
S = 'assets/stickers/'
DATA = {
    # GIF columns (src, display height at 168px wide) — order and heights from the Figma frames
    "gifDefault": [[[G+'g01.jpg', 166], [G+'g03.jpg', 166], [G+'g07.jpg', 125], [G+'g06.jpg', 166]],
                   [[G+'g02.jpg', 165], [G+'g04.jpg', 124], [G+'g08.jpg', 163], [G+'g05.jpg', 121]]],
    "gifResult":  [[[G+'g05.jpg', 124], [G+'g06.jpg', 166], [G+'g07.jpg', 125], [G+'g03.jpg', 166]],
                   [[G+'g02.jpg', 165], [G+'g08.jpg', 163], [G+'g09.jpg', 166], [G+'g04.jpg', 121], [G+'g01.jpg', 166]]],
    "stickerDefault": [S+'s%02d.png' % i for i in (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 15, 13, 14, 16, 8, 17)],
    "stickerResult":  [S+'s%02d.png' % i for i in (10, 13, 14, 15, 3, 12, 16, 17, 18, 10, 11, 12, 15, 13, 14, 16, 8, 17)],
}

# ---------------------------------------------------------------- CSS
rep("  @keyframes fzPushIn {",
"""  /* GIF & sticker drawer */
  .gz-sheet { transition: top .35s cubic-bezier(.22,1,.36,1); animation: fzSlideUp .34s cubic-bezier(.22,1,.36,1); }
  .gz-scroll::-webkit-scrollbar { width: 0; height: 0; }
  .gz-scroll { scrollbar-width: none; }
  .gz-item { border: 0; padding: 0; background: transparent; cursor: pointer; display: block; }
  .gz-item:focus-visible, .gz-tab:focus-visible { outline: 2px solid #F9FAFA; outline-offset: 2px; }
  .gz-search::placeholder { color: #6D7377; opacity: 1; }
  .gz-sk { background: linear-gradient(90deg, #283035 0%, #283035 35%, #333C41 50%, #283035 65%, #283035 100%); background-size: 300% 100%; animation: fzShim 1.4s cubic-bezier(.4,0,.6,1) infinite; }
  @keyframes fzPushIn {""")

# ---------------------------------------------------------------- the sticker icon in the Message field opens the drawer
rep('              <img src="assets/icons/face-sticker.svg" alt="" width="24" height="24" style="display:block;flex-shrink:0;{{ fzStickerStyle }}">',
    '              <button onClick="{{ openGiphy }}" aria-label="GIFs and stickers" style="flex-shrink:0;border:0;padding:0;background:transparent;cursor:pointer;{{ fzStickerStyle }}"><img src="assets/icons/face-sticker.svg" alt="" width="24" height="24" style="display:block;"></button>')

# ---------------------------------------------------------------- chat: GIF / sticker messages
rep('                  <div style="font-size:16px;font-weight:400;color:#B3B9BB;line-height:1.3;margin-top:4px;">{{ m.text }}</div>',
    '                  <sc-if value="{{ m.text }}" hint-placeholder-val="{{ true }}">\n'
    '                    <div style="font-size:16px;font-weight:400;color:#B3B9BB;line-height:1.3;margin-top:4px;">{{ m.text }}</div>\n'
    '                  </sc-if>\n'
    '                  <sc-if value="{{ m.gif }}" hint-placeholder-val="{{ false }}">\n'
    '                    <img src="{{ m.gif }}" alt="GIF" style="display:block;margin-top:6px;width:144px;height:144px;object-fit:cover;border-radius:8px;border:1px solid rgba(249,250,250,.2);box-sizing:border-box;">\n'
    '                  </sc-if>\n'
    '                  <sc-if value="{{ m.sticker }}" hint-placeholder-val="{{ false }}">\n'
    '                    <img src="{{ m.sticker }}" alt="Sticker" style="display:block;margin-top:6px;width:144px;height:144px;object-fit:contain;">\n'
    '                  </sc-if>')

# ---------------------------------------------------------------- the drawer (inside the FanZone base, over its panel)
SHEET = r'''      <!-- ===================== GIF & STICKER DRAWER (Figma "Giphy - Stickers - Dev") ===================== -->
      <sc-if value="{{ gzOpen }}" hint-placeholder-val="{{ false }}">
        <div class="gz-sheet" role="dialog" aria-label="GIFs and stickers" style="position:absolute;left:0;right:0;bottom:0;top:{{ gzTop }}px;z-index:5;pointer-events:auto;background:#1B2326;border-radius:24px 24px 0 0;box-shadow:0 -1px 0 rgba(249,250,250,.2);display:flex;flex-direction:column;overflow:hidden;font-family:'DAZN Oscine',sans-serif;color:#F9FAFA;">
          <!-- sheet header: handle + close -->
          <div style="position:relative;flex-shrink:0;height:48px;">
            <span aria-hidden="true" style="position:absolute;left:50%;top:12px;transform:translateX(-50%);width:44px;height:4px;border-radius:9999px;background:#CED0D2;"></span>
            <button onClick="{{ closeGiphy }}" aria-label="Close" style="position:absolute;right:12px;top:12px;width:24px;height:24px;border:0;padding:0;border-radius:50%;background:#3D4549;display:flex;align-items:center;justify-content:center;cursor:pointer;"><img src="assets/icons/fz-close.svg" alt="" width="16" height="16" style="display:block;"></button>
          </div>
          <!-- GIF / Sticker -->
          <div style="flex-shrink:0;height:56px;box-sizing:border-box;padding:8px 16px;display:flex;justify-content:center;">
            <div role="tablist" aria-label="GIF or sticker" style="width:153px;height:40px;box-sizing:border-box;padding:3px 4px;border:1px solid #3D4549;border-radius:9px;background:#1B2326;display:flex;align-items:center;">
              <button class="gz-tab" role="tab" aria-selected="{{ gzGifSel }}" aria-label="GIFs" onClick="{{ gzPickGif }}" style="width:72px;height:32px;border:0;padding:0;border-radius:6px;cursor:pointer;display:flex;align-items:center;justify-content:center;background:{{ gzGifTabBg }};"><img src="assets/icons/gz-tab-gif.svg" alt="" width="24" height="24" style="display:block;"></button>
              <button class="gz-tab" role="tab" aria-selected="{{ gzStickerSel }}" aria-label="Stickers" onClick="{{ gzPickSticker }}" style="width:72px;height:32px;border:0;padding:0;border-radius:6px;cursor:pointer;display:flex;align-items:center;justify-content:center;background:{{ gzStickerTabBg }};"><img src="assets/icons/gz-tab-sticker.svg" alt="" width="24" height="24" style="display:block;"></button>
            </div>
          </div>
          <!-- search -->
          <div style="flex-shrink:0;height:72px;box-sizing:border-box;padding:12px 16px;">
            <label style="height:48px;box-sizing:border-box;padding:12px;border:1px solid {{ gzFieldBorder }};border-radius:8px;display:flex;align-items:center;gap:8px;cursor:text;">
              <img src="assets/icons/gz-search.svg" alt="" width="24" height="24" style="display:block;flex-shrink:0;">
              <input class="gz-search" type="text" value="{{ gzQuery }}" onInput="{{ gzOnInput }}" onFocus="{{ gzOnFocus }}" onKeyDown="{{ gzOnKey }}" placeholder="{{ gzPlaceholder }}" aria-label="{{ gzPlaceholder }}" autocomplete="off" enterkeyhint="search" style="flex:1;min-width:0;border:0;outline:0;background:transparent;color:#F9FAFA;font-family:inherit;font-size:16px;line-height:24px;padding:0;margin:0;">
              <sc-if value="{{ gzHasQuery }}" hint-placeholder-val="{{ false }}">
                <button onClick="{{ gzClear }}" aria-label="Clear search" style="flex-shrink:0;width:24px;height:24px;border:0;padding:0;background:transparent;cursor:pointer;display:block;"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" aria-hidden="true"><circle cx="12" cy="12" r="8.5" stroke="#B3B9BB" stroke-width="1.6"></circle><path d="M9.2 9.2l5.6 5.6M14.8 9.2l-5.6 5.6" stroke="#B3B9BB" stroke-width="1.6" stroke-linecap="round"></path></svg></button>
              </sc-if>
            </label>
          </div>
          <!-- grid -->
          <div class="gz-scroll" style="flex:1;min-height:0;overflow-y:auto;margin-top:8px;padding:0 16px 24px;">
            <sc-if value="{{ gzLoading }}" hint-placeholder-val="{{ false }}">
              <div style="display:flex;gap:8px;">
                <div style="width:168px;display:flex;flex-direction:column;gap:8px;"><span class="gz-sk" style="display:block;height:124px;"></span><span class="gz-sk" style="display:block;height:166px;"></span><span class="gz-sk" style="display:block;height:124px;"></span></div>
                <div style="width:168px;display:flex;flex-direction:column;gap:8px;"><span class="gz-sk" style="display:block;height:166px;"></span><span class="gz-sk" style="display:block;height:124px;"></span><span class="gz-sk" style="display:block;height:166px;"></span></div>
              </div>
            </sc-if>
            <sc-if value="{{ gzShowGifs }}" hint-placeholder-val="{{ true }}">
              <div style="display:flex;gap:8px;align-items:flex-start;">
                <sc-for list="{{ gzGifCols }}" as="col" hint-placeholder-count="2">
                  <div style="width:168px;display:flex;flex-direction:column;gap:8px;">
                    <sc-for list="{{ col.items }}" as="g" hint-placeholder-count="4">
                      <button class="gz-item" onClick="{{ g.send }}" aria-label="Send this GIF"><img src="{{ g.src }}" alt="" draggable="false" style="display:block;width:168px;height:{{ g.h }}px;object-fit:cover;"></button>
                    </sc-for>
                  </div>
                </sc-for>
              </div>
            </sc-if>
            <sc-if value="{{ gzShowStickers }}" hint-placeholder-val="{{ false }}">
              <div style="display:grid;grid-template-columns:repeat(3, 85px);justify-content:space-between;row-gap:8px;">
                <sc-for list="{{ gzStickers }}" as="st" hint-placeholder-count="9">
                  <button class="gz-item" onClick="{{ st.send }}" aria-label="Send this sticker"><img src="{{ st.src }}" alt="" draggable="false" style="display:block;width:85px;height:85px;object-fit:contain;"></button>
                </sc-for>
              </div>
            </sc-if>
          </div>
        </div>
      </sc-if>
'''
rep('      <!-- FanZone panel -->\n', SHEET + '      <!-- FanZone panel -->\n')

# ---------------------------------------------------------------- data + logic
rep('// FanZone chat: which team each fan supports',
    '// GIFs & stickers (Figma "Giphy - Stickers - Dev")\nconst GZ = ' + json.dumps(DATA) + ';\n// FanZone chat: which team each fan supports')
rep('  openFanZoneOver = (e) => {',
'''  openGiphy = (e) => { if (e && e.stopPropagation) e.stopPropagation(); clearTimeout(this._gzT); this.setState({ gzOpen: true, gzTab: this.state.gzTab || "gif", gzExpanded: false, gzQuery: "", gzLoading: false, showFtue: false }); };
  closeGiphy = () => { clearTimeout(this._gzT); this.setState({ gzOpen: false, gzExpanded: false, gzQuery: "", gzLoading: false }); };
  gzSetTab = (tab) => { clearTimeout(this._gzT); const q = this.state.gzQuery || ""; this.setState({ gzTab: tab, gzLoading: !!q.trim() }); if (q.trim()) this._gzT = setTimeout(() => this.setState({ gzLoading: false }), 700); };
  gzOnFocus = () => { if (!this.state.gzExpanded) this.setState({ gzExpanded: true }); };
  gzOnInput = (e) => {
    const q = String((e && e.target && e.target.value) || "").slice(0, 60);
    clearTimeout(this._gzT);
    this.setState({ gzQuery: q, gzLoading: !!q.trim(), gzExpanded: true });
    if (q.trim()) this._gzT = setTimeout(() => this.setState({ gzLoading: false }), 700);
  };
  gzOnKey = (e) => { if (e && e.key === "Enter") { e.preventDefault(); try { e.target.blur(); } catch (err) {} } if (e && e.key === "Escape") this.closeGiphy(); };
  gzClear = (e) => { if (e && e.preventDefault) e.preventDefault(); clearTimeout(this._gzT); this.setState({ gzQuery: "", gzLoading: false }); };
  gzSend = (kind, src) => {
    const s = this.state;
    const av = s.avatar && AV_MAP[s.avatar] && AV_MAP[s.avatar].src ? AV_MAP[s.avatar].src : "";
    const msg = { id: "me" + Date.now(), name: s.nickname || "Charlie", avatar: av, text: "", mine: true };
    msg[kind] = src;
    clearTimeout(this._gzT);
    this.setState(st => ({ feed: st.feed.concat(msg).slice(-40), atBottom: true, gzOpen: false, gzExpanded: false, gzQuery: "", gzLoading: false }));
  };
  gzVals() {
    const s = this.state;
    const tab = s.gzTab || "gif";
    const searched = !!(s.gzQuery || "").trim();
    const loading = !!s.gzLoading;
    const cols = (searched ? GZ.gifResult : GZ.gifDefault).map((col, ci) => ({ id: "c" + ci, items: col.map(([src, h], i) => ({ id: ci + "-" + i, src, h, send: () => this.gzSend("gif", src) })) }));
    const stickers = (searched ? GZ.stickerResult : GZ.stickerDefault).map((src, i) => ({ id: "s" + i, src, send: () => this.gzSend("sticker", src) }));
    const base = s.fzOver ? 282 : 273;
    return {
      gzOpen: !!s.gzOpen && s.screen === "fanzone",
      gzTop: s.gzExpanded ? (s.fzOver ? 62 : 54) : base,
      openGiphy: this.openGiphy, closeGiphy: this.closeGiphy,
      gzGifSel: tab === "gif" ? "true" : "false", gzStickerSel: tab === "sticker" ? "true" : "false",
      gzGifTabBg: tab === "gif" ? "#3D4549" : "transparent", gzStickerTabBg: tab === "sticker" ? "#3D4549" : "transparent",
      gzPickGif: () => this.gzSetTab("gif"), gzPickSticker: () => this.gzSetTab("sticker"),
      gzPlaceholder: tab === "gif" ? "Search GIFs" : "Search stickers",
      gzQuery: s.gzQuery || "", gzHasQuery: searched,
      gzFieldBorder: s.gzExpanded ? "#CED0D2" : "#6D7377",
      gzOnInput: this.gzOnInput, gzOnFocus: this.gzOnFocus, gzOnKey: this.gzOnKey, gzClear: this.gzClear,
      gzLoading: loading,
      gzShowGifs: tab === "gif" && !loading, gzShowStickers: tab === "sticker" && !loading,
      gzGifCols: cols, gzStickers: stickers,
    };
  }
  openFanZoneOver = (e) => {''')
rep("    return {\n      ...this.crVals(),", "    return {\n      ...this.crVals(),\n      ...this.gzVals(),")
# leaving FanZone closes the drawer
rep('  goHome = () => { this.pollEnd(true);', '  goHome = () => { this.pollEnd(true); clearTimeout(this._gzT); if (this.state.gzOpen) this.setState({ gzOpen: false, gzExpanded: false, gzQuery: "" });')
rep('  componentWillUnmount() { ', '  componentWillUnmount() { clearTimeout(this._gzT); ')

open(PATH, 'w', encoding='utf-8').write(src)
print('ok')
