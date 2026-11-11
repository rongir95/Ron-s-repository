#!/usr/bin/env python3
"""Report a message in FanZone (FanZone DS, file NIgPxOlNU4U3sWMRdoE4Qh).

  Long press another fan's message (node 12356:11041): the chat blurs, the message is shown in focus and a
  "Report" menu appears under it (red text + alert icon). Tap outside to close.
  Report (node 12356:11859): a drawer over FanZone, "Report <name>", five reasons (radio buttons) and a
  Report button that turns on once a reason is picked. Sending it closes the drawer and shows a thank-you toast.

Everything here is HTML/CSS/SVG (vector).

Run after the other scripts:  python3 tools/fanzone-report.py FanZone.dc.html
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

FONT = "font-family:'DAZN Oscine',sans-serif;"
RED = '#FD7777'

# ---------------------------------------------------------------- long press on a message
rep('              <div style="flex-shrink:0;display:flex;align-items:flex-start;gap:6px;padding:8px 0;animation:fzMsgIn .45s cubic-bezier(.22,1,.36,1);">',
    '              <div onPointerDown="{{ m.onPress }}" onPointerUp="{{ msgPressEnd }}" onPointerLeave="{{ msgPressEnd }}" onPointerCancel="{{ msgPressEnd }}" onContextMenu="{{ msgNoMenu }}" '
    'style="flex-shrink:0;display:flex;align-items:flex-start;gap:6px;padding:8px 0;animation:fzMsgIn .45s cubic-bezier(.22,1,.36,1);-webkit-touch-callout:none;-webkit-user-select:none;user-select:none;">')
rep('        return { ...m, ...fzAv, ring: t ? t.card : "#F2C400", onOpen: () => this.openUserCard(m) };',
    '        return { ...m, ...fzAv, ring: t ? t.card : "#F2C400", onOpen: () => this.openUserCard(m), onPress: (e) => this.msgPressStart(m, t ? t.card : "#F2C400", fzAv) };')
# my own messages can't be reported: no long press
rep('ring: myFav ? myFav.card : "linear-gradient(210deg,#8923A0 0%,#F1A322 38%,#FFFA00 100%)", onOpen: this.openCard };',
    'ring: myFav ? myFav.card : "linear-gradient(210deg,#8923A0 0%,#F1A322 38%,#FFFA00 100%)", onOpen: this.openCard, onPress: null };')

ALERT = (f'<svg width="20" height="20" viewBox="0 0 20 20" fill="none" aria-hidden="true" style="display:block;"><circle cx="10" cy="10" r="8" stroke="{RED}" stroke-width="1.6"/>'
         f'<path d="M10 5.8v5" stroke="{RED}" stroke-width="1.8" stroke-linecap="round"/><circle cx="10" cy="13.9" r="1.1" fill="{RED}"/></svg>')

FOCUS = '''        <!-- Message in focus + Report (FanZone DS 12356:11041) -->
        <sc-if value="{{ msgFocusOn }}" hint-placeholder-val="{{ false }}">
          <div onClick="{{ msgFocusClose }}" style="position:absolute;left:0;right:0;top:48px;bottom:0;z-index:9;background:rgba(12,22,28,.55);-webkit-backdrop-filter:blur(22px);backdrop-filter:blur(22px);animation:fzFadeIn .2s ease;''' + FONT + '''">
            <div style="position:absolute;left:12px;right:12px;top:170px;padding:10px 12px;border-radius:12px;background:rgba(61,69,73,.6);display:flex;gap:6px;align-items:flex-start;animation:fzRxPop .25s cubic-bezier(.22,1.3,.36,1);">
              <span style="width:24px;height:24px;border-radius:50%;flex-shrink:0;box-sizing:border-box;border:1.5px solid transparent;padding:1.5px;background:linear-gradient(#2E3639,#2E3639) padding-box,{{ msgFocusRing }} border-box;">
                <span style="display:flex;align-items:center;justify-content:center;width:18px;height:18px;border-radius:50%;overflow:hidden;background:#080E12;color:#F9FAFA;font-weight:700;font-size:11px;">
                  <sc-if value="{{ msgFocusHasImg }}" hint-placeholder-val="{{ true }}"><img src="{{ msgFocusAvatar }}" alt="" style="display:block;width:18px;height:18px;object-fit:cover;{{ msgFocusImgScale }}"></sc-if>
                  <sc-if value="{{ msgFocusNoImg }}" hint-placeholder-val="{{ false }}">{{ msgFocusInitial }}</sc-if>
                </span>
              </span>
              <span style="min-width:0;">
                <span style="display:block;font-weight:700;font-size:14px;line-height:24px;color:#F9FAFA;">{{ msgFocusName }}</span>
                <span style="display:block;margin-top:2px;font-size:16px;line-height:1.3;color:#CED0D2;">{{ msgFocusText }}</span>
              </span>
            </div>
            <button onClick="{{ openReport }}" style="position:absolute;left:112px;top:{{ msgMenuTop }}px;width:150px;height:44px;box-sizing:border-box;padding:0 14px 0 12px;border:0;border-radius:12px;background:#3C4348;display:flex;align-items:center;justify-content:space-between;cursor:pointer;''' + FONT + '''font-size:16px;color:''' + RED + ''';animation:fzRxPop .3s cubic-bezier(.22,1.3,.36,1);">Report''' + ALERT + '''</button>
          </div>
        </sc-if>
'''

REASONS = ["Offensive", "Harassments or abuse", "Violent or Harmful", "Spam", "Other"]
SHEET = '''        <!-- Report drawer (FanZone DS 12356:11859) -->
        <sc-if value="{{ reportOn }}" hint-placeholder-val="{{ false }}">
          <div role="dialog" aria-label="Report" style="position:absolute;left:0;right:0;top:0;bottom:0;z-index:12;border-radius:24px 24px 0 0;background:#1B2326;box-shadow:0 -1px 0 rgba(249,250,250,.2);animation:fzSlideUp .32s cubic-bezier(.22,1,.36,1);''' + FONT + '''">
            <span aria-hidden="true" style="position:absolute;left:50%;top:8px;transform:translateX(-50%);width:36px;height:4px;border-radius:9999px;background:#6D7377;"></span>
            <div style="height:56px;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:16px;color:#F9FAFA;padding-top:6px;box-sizing:border-box;">Report</div>
            <button onClick="{{ closeReport }}" aria-label="Close" title="Close" style="position:absolute;right:16px;top:16px;width:32px;height:32px;border:0;padding:0;border-radius:9999px;background:rgba(255,255,255,.2);display:flex;align-items:center;justify-content:center;cursor:pointer;"><svg width="20" height="20" viewBox="0 0 20 20" fill="none" style="display:block;"><path d="M5 5L15 15M15 5L5 15" stroke="#F9FAFA" stroke-width="1.6" stroke-linecap="round"></path></svg></button>
            <div style="padding:16px 16px 0;">
              <div style="font-weight:700;font-size:20px;line-height:26px;color:#F9FAFA;">Report {{ msgFocusName }}</div>
              <div style="margin-top:6px;font-size:14px;line-height:20px;color:#B3B9BB;">Your report is anonymous and can be seen only by DAZN moderators</div>
              <div role="radiogroup" aria-label="Reason" style="margin-top:22px;display:flex;flex-direction:column;">
                <sc-for list="{{ reportReasons }}" as="r" hint-placeholder-count="5">
                  <button role="radio" aria-checked="{{ r.checked }}" onClick="{{ r.pick }}" style="display:flex;align-items:center;gap:12px;height:45px;border:0;padding:0;background:transparent;cursor:pointer;''' + FONT + '''font-size:16px;color:{{ r.color }};text-align:left;">
                    <span style="width:20px;height:20px;border-radius:50%;box-sizing:border-box;border:2px solid {{ r.ring }};display:flex;align-items:center;justify-content:center;"><span style="width:10px;height:10px;border-radius:50%;background:#F9FAFA;{{ r.dot }}"></span></span>
                    {{ r.label }}
                  </button>
                </sc-for>
              </div>
            </div>
            <button onClick="{{ sendReport }}" style="position:absolute;left:16px;right:16px;bottom:24px;height:48px;border:0;border-radius:8px;''' + FONT + '''font-weight:700;font-size:16px;{{ reportBtnStyle }}">Report</button>
          </div>
        </sc-if>
        <sc-if value="{{ reportToast }}" hint-placeholder-val="{{ false }}">
          <div role="status" style="position:absolute;left:12px;right:12px;bottom:84px;z-index:11;padding:12px 14px;border-radius:12px;background:#F9FAFA;color:#080E12;display:flex;align-items:center;gap:10px;animation:fzPop .28s cubic-bezier(.22,1,.36,1);''' + FONT + '''font-size:15px;line-height:20px;">
            <svg width="20" height="20" viewBox="0 0 20 20" fill="none" aria-hidden="true" style="flex-shrink:0;display:block;"><circle cx="10" cy="10" r="9" fill="#080E12"/><path d="M6 10.3l2.6 2.6L14 7.4" stroke="#F9FAFA" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>
            Thanks for reporting. Our moderators will review it.
          </div>
        </sc-if>
'''
rep('        <!-- chat feed -->\n', FOCUS + SHEET + '        <!-- chat feed -->\n')

LOGIC = '''  // Long press a fan's message -> focus + Report; Report -> drawer (FanZone DS 12356:11041 / 12356:11859)
  msgPressStart = (m, ring, av) => {
    clearTimeout(this._msgT);
    this._msgT = setTimeout(() => this.setState({ msgFocus: { name: m.name, text: m.text || (m.gif ? "GIF" : "Sticker"), ring, avatar: m.avatar || "", hasImg: !!m.avatar, initial: av.initial, imgScale: av.imgScale } }), 450);
  };
  msgPressEnd = () => { clearTimeout(this._msgT); };
  msgNoMenu = (e) => { if (e && e.preventDefault) e.preventDefault(); };
  msgFocusClose = () => this.setState({ msgFocus: null });
  openReport = (e) => { if (e && e.stopPropagation) e.stopPropagation(); this.setState({ reportOn: true, reportReason: null }); };
  closeReport = () => this.setState({ reportOn: false, msgFocus: null });
  sendReport = () => {
    if (this.state.reportReason == null) return;
    clearTimeout(this._repT);
    this.setState({ reportOn: false, msgFocus: null, reportToast: true });
    this._repT = setTimeout(() => this.setState({ reportToast: false }), 2600);
  };
  reportVals() {
    const s = this.state;
    const f = s.screen === "fanzone" ? s.msgFocus : null;
    const textLen = f ? String(f.text).length : 0;
    return {
      msgFocusOn: !!f && !s.reportOn, msgFocusClose: this.msgFocusClose, msgPressEnd: this.msgPressEnd, msgNoMenu: this.msgNoMenu,
      msgFocusName: f ? f.name : "", msgFocusText: f ? f.text : "", msgFocusRing: f ? f.ring : "#F2C400",
      msgFocusAvatar: f ? f.avatar : "", msgFocusHasImg: !!(f && f.hasImg), msgFocusNoImg: !!(f && !f.hasImg),
      msgFocusInitial: f ? f.initial : "", msgFocusImgScale: f ? f.imgScale : "",
      msgMenuTop: 170 + 64 + Math.max(0, Math.ceil(textLen / 34) - 1) * 21 + 10,
      openReport: this.openReport, closeReport: this.closeReport, sendReport: this.sendReport,
      reportOn: !!s.reportOn && s.screen === "fanzone", reportToast: !!s.reportToast && s.screen === "fanzone",
      reportReasons: REPORT_REASONS.map((label, i) => { const on = s.reportReason === i; return { id: "r" + i, label, checked: on ? "true" : "false",
        color: on ? "#F9FAFA" : "#B3B9BB", ring: on ? "#F9FAFA" : "#B3B9BB", dot: on ? "" : "display:none;", pick: () => this.setState({ reportReason: i }) }; }),
      reportBtnStyle: s.reportReason != null ? "background:#F9FAFA;color:#080E12;cursor:pointer;" : "background:#CED0D2;color:#6D7377;cursor:default;",
    };
  }
  openFanZoneOver = (e) => {'''
rep('  openFanZoneOver = (e) => {', LOGIC)
rep('      ...this.gzVals(),', '      ...this.gzVals(),\n      ...this.reportVals(),')
rep('// FanZone chat: which team each fan supports', '// Report reasons (FanZone DS)\nconst REPORT_REASONS = ' + repr(REASONS).replace("'", '"') + ';\n// FanZone chat: which team each fan supports')

open(PATH, 'w', encoding='utf-8').write(src)
print('ok')
