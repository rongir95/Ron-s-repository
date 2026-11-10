#!/usr/bin/env python3
"""Merge the 'Comments & Replies' prototype into the 'Personal Fan Card' prototype.

Input : Fan Card page (full app shell) + Comments & Replies page.
Output: one FanZone.dc.html where the match page's Comments drawer runs the
        full Comments & Replies experience, and the app reads prototype
        settings from the URL (?card=B&start=fanzone ...).
"""
import re, sys

FC_PATH, CR_PATH, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
fc = open(FC_PATH, encoding='utf-8').read()
cr = open(CR_PATH, encoding='utf-8').read()
cr_lines = cr.split('\n')

def must_replace(src, old, new, count=1):
    n = src.count(old)
    if n != count:
        raise SystemExit(f'expected {count} occurrence(s), found {n}: {old[:90]!r}')
    return src.replace(old, new)

# ---------------------------------------------------------------- renaming
STATE = ['comments', 'composerOpen', 'replyTo', 'mentionOn', 'composerText', 'pickerOpen',
         'pickerTarget', 'pickerPos', 'menuOpen', 'menuTarget', 'menuPos', 'menuLoading',
         'loadingReplies', 'loadingMore', 'toast', 'floaters', 'online', 'nextId']
METHODS = ['setPhoneRef', 'setFeedRef', 'setInputRef', 'setMentionRef', 'autosize',
           'onComposerScroll', 'fmt', 'agg', 'avFull', 'avInner', 'findComment', 'findAny',
           'onHeartDown', 'onHeartUp', 'toggleLike', 'openPickerAt', 'openCluster', 'closePicker',
           'pickReaction', 'measureText', 'toggleClamp', 'toggleReplies', 'hideReplies', 'loadMore',
           'openTopComposer', 'openReply', 'removeReplyTo', 'onComposerKeyDown', 'onComposerInput',
           'blurComposer', 'onBarClick', 'onSend', 'postNow', 'scrollToEl', 'retryPost',
           'onMenuDown', 'onMenuUp', 'openMenu', 'closeMenu', 'doDelete', 'doReport', 'showToast',
           'toggleOnline', 'capture', 'EMOJI', 'REACT', 'PROFANITY', 'ME', 'ringGrads', 'avatars',
           'floaterId', 'holdTimer', 'heldOpened', 'phoneEl', 'feedEl', 'inputEl', 'mentionEl',
           'menuTimer', 'menuHeld']
PRIVATE = ['_ovf', '_focusNext', '_lastBtn', '_lastMenuBtn', '_toastTimer', '_loadTimer',
           '_loadMoreTimer']
KEYS = ['feedStyle', 'offline', 'onToggleOnline', 'barVisible', 'hasReplyTo', 'replyingToName',
        'composerBoxStyle', 'showMention', 'mentionToken', 'composerPlaceholder', 'barText',
        'barTextStyle', 'sendEnabled', 'sendDisabled', 'pickerStyle', 'pickerItems',
        'menuPillStyle', 'menuShowDelete', 'menuShowReport', 'deleteLabel', 'toastOpen',
        'toastText', 'toastHasRetry', 'onRetry', 'toastStyle', 'toastTextStyle', 'skeletonRows']
ANIMS = ['popIn', 'toastIn', 'floatUp', 'shimmer', 'spin']

ren = {}
for w in STATE + METHODS + KEYS + ANIMS:
    ren[w] = 'cr' + w[0].upper() + w[1:]
for w in PRIVATE:
    ren[w] = '_cr' + w[1].upper() + w[2:]
ren_re = re.compile(r'(?<![A-Za-z0-9_$])(' + '|'.join(sorted(map(re.escape, ren), key=len, reverse=True)) + r')(?![A-Za-z0-9_$])')

def rename(text):
    return ren_re.sub(lambda m: ren[m.group(1)], text).replace('assets/crAvatars/', 'assets/avatars/')

def seg(a, b):
    """1-based inclusive line range of the C&R file."""
    return '\n'.join(cr_lines[a - 1:b])

# ---------------------------------------------------------------- template parts from C&R
feed = rename(seg(174, 305))
# avatar + author open the fan's card (Fan Card behaviour) when that fan has one
feed = must_replace(feed, '<div style="{{ c.avatarStyle }}">', '<div onClick="{{ c.onProfile }}" style="{{ c.avatarStyle }}">')
feed = must_replace(feed, '<span style="color:#B3B9BB;font-size:13px;font-weight:700;">{{ c.author }}</span>',
                    '<span onClick="{{ c.onProfile }}" style="{{ c.authorStyle }}">{{ c.author }}</span>')
assert 'comments-feed' not in feed or True

overlays = seg(319, 356) + '\n' + seg(358, 425)   # line 357 is a stray </sc-if> in the source
overlays = rename(overlays)
assert overlays.count('<sc-if') == overlays.count('</sc-if>'), 'unbalanced sc-if in overlays'

# ---------------------------------------------------------------- JS from C&R
ctor = seg(434, 591)          # constructor body after super(props)
methods = seg(594, 1046)      # class fields/methods incl. renderVals()
ctor, methods = rename(ctor), rename(methods)

# constructor -> crInit(), merged into the Fan Card state on first render
ctor = must_replace(ctor, "    this.state = {\n      view: 'fixture',\n", "    const crState = {\n")
ctor = must_replace(ctor, "      sheetIn:false,\n", "")
ctor = must_replace(ctor, "    this.crFloaterId = 0;", "    Object.assign(this.state, crState);\n    this.crFloaterId = 0;")
# the two fans who already commented in the Fan Card prototype keep their identity + card
ctor = ctor.replace("Scarlet82", "Futcrunch")
ctor = must_replace(ctor, "{ id:1, author:'Futcrunch', ai:0, time:'4d', img:'avatar1',",
                    "{ id:1, author:'Futcrunch', ai:0, time:'4d', img:'assets/comments/av0.png', profileIdx:0,")
ctor = must_replace(ctor, "{ id:2, author:'Adam173', ai:6, time:'4d', img:'avatar4',\n          text:'I\\u2019ve been nervous about this game since yesterday 😅',",
                    "{ id:2, author:'Mariana', ai:6, time:'4d', img:'assets/comments/av1.png', profileIdx:1,\n          text:'I\\u2019ve been kinda nervous about this game since yesterday 😅',")
ctor = must_replace(ctor, "replies: makeReplies('Adam173', 6, 9300)", "replies: makeReplies('Mariana', 6, 9300)")
ctor = must_replace(ctor, "        { id:3, author:'Demian990',",
    "        { id:101, author:'Sandra45', ai:2, time:'5d', profileIdx:2,\n"
    "          text:'Here for the chaos, staying for the goals ⚽',\n"
    "          base:{ like:2 }, my:null, mine:false,\n"
    "          replies:[], totalReplies:0, repliesExpanded:false, loaded:0, textExpanded:false },\n"
    "        { id:102, author:'MisterFotball12', ai:3, time:'5d', img:'assets/comments/av3.png', profileIdx:3,\n"
    "          text:'Tough loss but I\\u2019m honestly proud of the team',\n"
    "          base:{}, my:null, mine:false,\n"
    "          replies: makeReplies('MisterFotball12', 3, 9050), totalReplies:3, repliesExpanded:false, loaded:0, textExpanded:false },\n"
    "        { id:3, author:'Demian990',")
crinit = "  crInit() {\n    this._crReady = true;\n" + ctor + "\n  }\n"

# drop C&R's own sheet open/close + sheet ref (the Fan Card drawer owns those)
start = methods.index('  setSheetRef = (el)=>{')
end = methods.index('  crSetFeedRef = ')
methods = methods[:start] + methods[end:]
start = methods.index('  // ----- view nav -----')
end = methods.index('  // ----- reactions -----')
methods = methods[:start] + methods[end:]
# avatars: allow full asset paths; "me" uses the Fan Card user's avatar
methods = must_replace(methods, "backgroundImage:'url(assets/avatars/'+img+'.png)'",
                       "backgroundImage:'url('+(img.indexOf('/')>=0 ? img : 'assets/avatars/'+img+'.png')+')'")
methods = must_replace(methods, "avatarStyle: this.crAvFull(item.ai, isReply, item.mine ? 'me' : item.img),",
    "avatarStyle: Object.assign(this.crAvFull(item.ai, isReply, item.mine ? 'assets/comments/avin.png' : item.img), (!isReply && (item.profileIdx!=null || item.mine)) ? { cursor:'pointer' } : {}),\n"
    "        authorStyle: { color:'#B3B9BB', fontSize:'13px', fontWeight:700, cursor: (!isReply && (item.profileIdx!=null || item.mine)) ? 'pointer' : 'default' },\n"
    "        onProfile: (e)=>{ if(isReply) return; if(item.profileIdx!=null) this.openOtherProfile(item.profileIdx, e); else if(item.mine) this.openCardFromComments(e); },")
# my posts are signed with the Fan Card nickname
methods = methods.replace("author:this.crME,", "author:(this.state.nickname||'Charlie'),")
assert 'this.crME' not in methods.replace("this.crME = ", ""), 'unreplaced ME'
# renderVals -> crVals, without the C&R-only view keys
methods = must_replace(methods, '  renderVals(){', '  crVals(){')
methods, n = re.subn(r"^      (isFixture|isComments|showFixtureLayer|sheetTransform|openComments|setSheetRef):.*\n", "", methods, flags=re.M)
assert n == 6, n
# reset transient comment state when the drawer closes (was C&R's closeComments)
crreset = """  crReset(){
    clearTimeout(this._crLoadTimer); clearTimeout(this._crLoadMoreTimer); clearTimeout(this._crToastTimer);
    this.setState(s=>({
      crComposerOpen:false, crReplyTo:null, crMentionOn:false, crComposerText:'',
      crPickerOpen:false, crPickerTarget:null, crMenuOpen:false, crMenuTarget:null, crMenuLoading:false,
      crLoadingReplies:null, crLoadingMore:null, crToast:null,
      crComments: (s.crComments||[]).map(c=> (c.repliesExpanded || c.loaded) ? { ...c, repliesExpanded:false, loaded:0 } : c)
    }));
    if(this.crFeedEl) this.crFeedEl.scrollTop = 0;
  }
"""
cr_js = "\n  // ===================== COMMENTS & REPLIES (merged from the Replies prototype) =====================\n" + crinit + crreset + methods + "\n"

# ---------------------------------------------------------------- patch the Fan Card page
out = fc

# 1) keyframes used by the merged comments
out = must_replace(out, "  @keyframes fzPushIn {",
    "  /* Comments & Replies */\n"
    "  @keyframes crPopIn { from { transform: scale(0.7) translateY(8px); opacity: 0; } to { transform: scale(1) translateY(0); opacity: 1; } }\n"
    "  @keyframes crToastIn { from { transform: translateY(14px); opacity: 0; } to { transform: translateY(0); opacity: 1; } }\n"
    "  @keyframes crFloatUp { 0% { transform: translateY(0) scale(0.6); opacity: 0; } 20% { opacity: 1; transform: translateY(-10px) scale(1.2); } 100% { transform: translateY(-120px) scale(1); opacity: 0; } }\n"
    "  @keyframes crShimmer { 0% { background-position: 100% 0; } 100% { background-position: -100% 0; } }\n"
    "  @keyframes crSpin { to { transform: rotate(360deg); } }\n"
    "  #crComments-feed::-webkit-scrollbar { display: none; }\n"
    "  #crComments-feed { scrollbar-width: none; }\n"
    "  /* embedded in the FanZone prototype shell: the shell draws the device frame */\n"
    "  html.fz-embed, html.fz-embed body { background: #000 !important; overflow: hidden; }\n"
    "  html.fz-embed .fz-stage { min-height: 0 !important; padding: 0 !important; display: block !important; background: #000 !important; }\n"
    "  html.fz-embed .fz-phone { border-radius: 0 !important; box-shadow: none !important; }\n"
    "  @keyframes fzPushIn {")
out = must_replace(out, "<script>\n(function(){\n  // Standalone-bundle asset resolver.",
    "<script>\n(function(){ try { if (/[?#&]embed=1/.test(location.search + location.hash)) document.documentElement.classList.add('fz-embed'); } catch (e) {} })();\n</script>\n"
    "<script>\n(function(){\n  // Standalone-bundle asset resolver.")

# 2) stage + phone hooks
out = must_replace(out, '<div style="min-height:100vh;display:flex;align-items:center;justify-content:center;padding:24px;background:radial-gradient(120% 120% at 50% 0%, #17171c 0%, #0a0a0c 60%);">',
    '<div class="fz-stage" style="min-height:100vh;display:flex;align-items:center;justify-content:center;padding:24px;background:radial-gradient(120% 120% at 50% 0%, #17171c 0%, #0a0a0c 60%);">')
out = must_replace(out, 'overflow:hidden;" data-fz-root="1">', 'overflow:hidden;" class="fz-phone" ref="{{ crSetPhoneRef }}" data-fz-root="1">')

# 3) the Comments drawer body: replace the static feed + input with the live one
a = out.index('            <!-- Messages (scrollable) -->')
b = out.index('            <!-- home indicator -->', a)
new_body = (
    '            <!-- Comments & Replies feed (merged from the Replies prototype) -->\n'
    '            <div style="position:absolute;left:0;right:0;top:48px;height:380px;display:flex;flex-direction:column;">\n'
    + feed.replace('<div id="crComments-feed" ref="{{ crSetFeedRef }}" style="{{ crFeedStyle }}">',
                   '<div id="crComments-feed" ref="{{ crSetFeedRef }}" style="{{ crFeedStyle }}">', 1) + '\n'
    '            </div>\n'
    '            <!-- Comments input: my avatar opens My Card, the field opens the composer -->\n'
    '            <div style="position:absolute;left:0;right:0;top:428px;height:68px;box-sizing:border-box;padding:12px 16px;display:flex;align-items:center;gap:12px;background:#0C161C;border-top:1px solid rgba(36,45,51,0.6);">\n'
    '              <button onClick="{{ openCardFromComments }}" title="Open My Card" style="flex-shrink:0;width:40px;height:40px;border:0;padding:0;background:transparent;border-radius:50%;cursor:pointer;"><img src="assets/comments/avin.png" alt="My card" width="40" height="40" style="display:block;border-radius:50%;"></button>\n'
    '              <button onClick="{{ crOnBarClick }}" style="flex:1;min-width:0;height:44px;box-sizing:border-box;padding:0 12px;border:0;border-radius:16px;background:rgba(249,250,250,.12);display:flex;align-items:center;font-family:\'DAZN Oscine\',sans-serif;cursor:text;text-align:left;"><span style="{{ crBarTextStyle }}">{{ crBarText }}</span></button>\n'
    '            </div>\n')
out = out[:a] + new_body + out[b:]

# 4) overlays (reaction picker, floaters, delete/report pill, toast, composer + keyboard) at phone level
out = must_replace(out, "\n  </div>\n</div>\n</x-dc>",
    "\n    <!-- ===================== COMMENTS & REPLIES OVERLAYS ===================== -->\n" + overlays + "\n\n  </div>\n</div>\n</x-dc>")

# 5) No-Internet simulation: tap the status bar on the match page
out = must_replace(out,
    '<div style="position:absolute;left:0;right:0;top:0;height:62px;background:#080E12;z-index:2;"><img src="assets/icons/status-941.svg" alt="" width="375" height="62" style="display:block;"></div>',
    '<div onClick="{{ crOnToggleOnline }}" title="Tap to simulate No Internet" style="position:absolute;left:0;right:0;top:0;height:62px;background:#080E12;z-index:2;cursor:pointer;"><img src="assets/icons/status-941.svg" alt="" width="375" height="62" style="display:block;">'
    '<sc-if value="{{ crOffline }}" hint-placeholder-val="{{ false }}"><span style="position:absolute;right:108px;top:22px;font-size:11px;font-weight:700;color:#ff6b6b;border:1px solid #ff6b6b;border-radius:5px;padding:1px 5px;background:#080E12;">No Internet</span></sc-if></div>')

# 6) JS: settings from the URL, wiring, comments engine
out = must_replace(out, "class Component extends DCLogic {\n  constructor(props) {",
"""// Prototype settings passed by the FanZone shell in the page URL (override the Tweaks defaults)
const FZ_URL_PROPS = (function () {
  const o = {};
  try {
    const q = new URLSearchParams((location.search || "").replace(/^\\?/, "") + "&" + (location.hash || "").replace(/^#/, ""));
    if (q.get("start")) o.startScreen = q.get("start") === "fanzone" ? "FanZone" : "Home";
    const card = (q.get("card") || "").toUpperCase();
    if (card === "A") o.myCardOption = "A · Current (Figma)";
    if (card === "B") o.myCardOption = "B · Spotlight";
    if (card === "C") o.myCardOption = "C · Compact + grid";
    if (q.get("selfcard") === "0") o.selfCard = false;
    if (q.get("following") === "0") o.showFollowing = false;
    if (q.get("profile") === "full") o.startState = "Full profile";
    if (q.get("profile") === "empty") o.startState = "Empty profile";
    if (q.get("reset") === "1") o.resetOnLoad = true;
  } catch (e) {}
  return o;
})();
class Component extends DCLogic {
  get P() { return Object.assign({}, this.props, FZ_URL_PROPS); }
  constructor(props) {""")
script_start = out.index('class Component extends DCLogic {')
head, body = out[:script_start], out[script_start:]
body = body.replace('this.props.', 'this.P.')
out = head + body
out = must_replace(out, "  closeComments = () => {\n    if (!this.state.commentsOpen) return;\n",
                   "  closeComments = () => {\n    if (!this.state.commentsOpen) return;\n    this.crReset();\n")
out = must_replace(out, "      showFollowingSection: true,", "      showFollowingSection: (this.P.showFollowing !== false) || !isMe,")
out = must_replace(out, "  renderVals() {\n", "  renderVals() {\n    if (!this._crReady) this.crInit();\n")
rv = out.index("  renderVals() {\n")
rt = out.index("\n    return {\n", rv)
out = out[:rt] + "\n    return {\n      ...this.crVals()," + out[rt + len("\n    return {"):]
# insert the comments engine before renderVals
out = must_replace(out, "  renderVals() {\n", cr_js + "  renderVals() {\n")
# componentWillUnmount: clear our timers too
out = must_replace(out, "  componentWillUnmount() { clearTimeout(this._introT);",
                   "  componentWillUnmount() { clearTimeout(this._crLoadTimer); clearTimeout(this._crLoadMoreTimer); clearTimeout(this._crToastTimer); clearTimeout(this._introT);")
out = out.replace('<title>', '<title>', 1)
open(OUT, 'w', encoding='utf-8').write(out)
print('ok', len(out))
