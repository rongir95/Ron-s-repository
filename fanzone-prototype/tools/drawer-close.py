#!/usr/bin/env python3
"""Every drawer closes with the same slide-down as the Comments drawer (fzSlideDown .28s); its dim backdrop fades out.

Drawers that used to vanish at once: GIFs & stickers (and the quick-message tab in FanZone Light), Report,
Who reacted, Update status and the small Edit My Favorite sheet. (The Fan Card and the pushed profile
sheets already slide down.)

How: closing a drawer sets dzClosing to its key; the drawer carries data-dz-closing="1" while it plays,
and the real close runs after 280ms.

Run after the other scripts:  python3 tools/drawer-close.py FanZone.dc.html
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

rep('  @keyframes fzPushIn {',
    '  [data-dz-closing="1"] { animation: fzSlideDown .28s cubic-bezier(.4,0,1,1) forwards !important; pointer-events: none !important; }\n'
    '  [data-dz-bd="1"] { animation: fzFadeOut .28s ease forwards !important; pointer-events: none !important; }\n'
    '  @keyframes fzPushIn {')

# drawers (and backdrops) get the closing flag
rep('<div class="gz-sheet" role="dialog" aria-label="GIFs and stickers" style="',
    '<div class="gz-sheet" data-dz-closing="{{ dzGz }}" role="dialog" aria-label="GIFs and stickers" style="')
rep('<div role="dialog" aria-label="Report" style="',
    '<div role="dialog" aria-label="Report" data-dz-closing="{{ dzReport }}" style="')
rep('''      <div onClick="{{ closeEditFav }}" style="position:absolute;inset:0;z-index:29;''',
    '''      <div onClick="{{ closeEditFav }}" data-dz-bd="{{ dzEditFav }}" style="position:absolute;inset:0;z-index:29;''')
rep('''      <div style="position:absolute;left:0;right:0;bottom:0;z-index:30;background:#1B2326;border-radius:24px 24px 0 0;padding:0 0 28px;animation:fzSlideUp''',
    '''      <div data-dz-closing="{{ dzEditFav }}" style="position:absolute;left:0;right:0;bottom:0;z-index:30;background:#1B2326;border-radius:24px 24px 0 0;padding:0 0 28px;animation:fzSlideUp''')
rep('''      <div style="position:absolute;left:0;right:0;top:282px;bottom:317px;z-index:26;''',
    '''      <div data-dz-closing="{{ dzStatus }}" style="position:absolute;left:0;right:0;top:282px;bottom:317px;z-index:26;''')
rep('''      <div onClick="{{ closeRxList }}" style="position:absolute;inset:0;z-index:40;''',
    '''      <div onClick="{{ closeRxList }}" data-dz-bd="{{ dzRx }}" style="position:absolute;inset:0;z-index:40;''')
rep('''      <div role="dialog" aria-label="Reactions" style="''',
    '''      <div role="dialog" aria-label="Reactions" data-dz-closing="{{ dzRx }}" style="''')

# the close handlers play the slide-down first
rep('  closeGiphy = () => { clearTimeout(this._gzT); this.setState({ gzOpen: false, gzExpanded: false, gzQuery: "", gzLoading: false }); };',
    '  closeGiphy = () => this.dismissDrawer("gz", () => { clearTimeout(this._gzT); this.setState({ gzOpen: false, gzExpanded: false, gzQuery: "", gzLoading: false }); });')
rep('closeReport = () => this.setState({ reportOn: false, msgFocus: null });',
    'closeReport = () => this.dismissDrawer("report", () => this.setState({ reportOn: false, msgFocus: null }));')
rep('  closeEditFav = () => this.setState({ editFavOpen: false });',
    '  closeEditFav = () => this.dismissDrawer("editFav", () => this.setState({ editFavOpen: false }));')
rep('  closeStatus = () => this.setState({ sheet: "card" });',
    '  closeStatus = () => this.dismissDrawer("status", () => this.setState({ sheet: "card" }));')
rep('  closeRxList = () => { clearTimeout(this._rxlT); this.setState({ rxList: false }); };',
    '  closeRxList = () => this.dismissDrawer("rx", () => { clearTimeout(this._rxlT); this.setState({ rxList: false }); });')

LOGIC = '''  // Drawers close with the Comments slide-down (fzSlideDown .28s), then really close
  dismissDrawer(key, done) {
    if (this.state.dzClosing === key) return;
    clearTimeout(this._dzT);
    this.setState({ dzClosing: key });
    this._dzT = setTimeout(() => { this.setState({ dzClosing: null }); done(); }, 280);
  }
  openFanZoneOver = (e) => {'''
rep('  openFanZoneOver = (e) => {', LOGIC)
rep('      ...this.gzVals(),',
    '      ...this.gzVals(),\n'
    '      dzGz: this.state.dzClosing === "gz" ? "1" : "0", dzReport: this.state.dzClosing === "report" ? "1" : "0",\n'
    '      dzEditFav: this.state.dzClosing === "editFav" ? "1" : "0", dzStatus: this.state.dzClosing === "status" ? "1" : "0",\n'
    '      dzRx: this.state.dzClosing === "rx" ? "1" : "0",')

open(PATH, 'w', encoding='utf-8').write(src)
print('ok')
