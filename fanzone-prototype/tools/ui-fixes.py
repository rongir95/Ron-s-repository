#!/usr/bin/env python3
"""Small UI fixes.

  - Drawers pushed over the Fan Card (My Favorite, Followings, Avatars, ...): the card slides left and dims under
    them, and its team-colour gradient showed through the new drawer's rounded top-left corner. Once the push
    animation is over the card is hidden (it comes back at once when you go back).

  - Other fans' cards: "<name> and you have N interests in common" shows only the text (no avatars).

  - Fan Card scroll (Figma EyEm3J8Y3qrWV40vOPOkjV node 496:102108, "Half-height card"): the top strip with the
    team colour stays fixed in the drawer's background and the top strip shows the same slice of it, so the
    content scrolls under the strip without a seam (the colour used to scroll away with the content).

  - Fan Card reveal: after the loading skeleton the whole card appears at once (one short fade), instead of
    the avatar, name, team and rows coming in one after another.

  - Comments: every author's avatar and name opens their card (comments and replies), not just the four with a
    ready-made profile. Authors without one get a generated profile: Bayern or Dortmund fan, a status that fits
    the team, their picture or initial.

Run after the other scripts:  python3 tools/ui-fixes.py FanZone.dc.html
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

rep('''        ? "transform:translateX(-30%);filter:brightness(.55);pointer-events:none;"
        : "transform:translateX(0);filter:none;") + "transition:transform .32s cubic-bezier(.2,0,0,1), filter .32s ease;",''',
    '''        ? "transform:translateX(-30%);filter:brightness(.55);pointer-events:none;visibility:hidden;transition:transform .32s cubic-bezier(.2,0,0,1), filter .32s ease, visibility 0s linear .32s;"
        : "transform:translateX(0);filter:none;visibility:visible;transition:transform .32s cubic-bezier(.2,0,0,1), filter .32s ease, visibility 0s;"),''')

import re
m = re.search(r'(              <div style="display:flex;align-items:center;gap:6px;margin:0 16px 12px;">\n)                <span style="display:flex;flex-direction:row-reverse;align-items:center;flex-shrink:0;padding-left:8px;">\n.*?\n                </span>\n(                <span style="font-size:12px;line-height:1.52;color:#B3B9BB;min-width:0;"><strong style="color:#B3B9BB;font-weight:700;">\{\{ commonWho \}\}</strong>)', src, re.S)
if not m:
    raise SystemExit('common-interests avatars not found')
src = src[:m.start()] + m.group(1) + m.group(2) + src[m.end():]

# the team colour is painted on the scroller itself, so it stays put while the content scrolls, and the
# sticky top strip shows the same slice of it: the content slides under the strip without a seam
rep('''        <sc-if value="{{ cardReady }}" hint-placeholder-val="{{ true }}">
          <div class="fz-r-wash" style="position:absolute;left:0;right:0;top:0;height:350px;pointer-events:none;background:{{ cardWash }};"></div>
        </sc-if>
        <!-- Top - Sheet''', '''        <!-- Top - Sheet''')
rep('''overflow-x:hidden;overflow-y:auto;-webkit-overflow-scrolling:touch;background:#080E12;box-shadow:0 -1px 0 rgba(249,250,250,.2);{{ sheetAnimStyle }}''',
    '''overflow-x:hidden;overflow-y:auto;-webkit-overflow-scrolling:touch;background-color:#080E12;background-image:{{ cardWash }};background-size:100% 350px;background-repeat:no-repeat;background-position:top;background-attachment:scroll;box-shadow:0 -1px 0 rgba(249,250,250,.2);{{ sheetAnimStyle }}''')
import re as _re
m = _re.search(r'  \.fz-r-avatar \{ animation:.*?\n  \.fz-r-wash \{ animation:[^\n]*\n', src, _re.S)
if not m:
    raise SystemExit('card reveal animations not found')
src = src[:m.start()] + ('  @keyframes fzCardIn { from { opacity: 0; } to { opacity: 1; } }\n'
    '  @keyframes fzCardOut { from { opacity: 1; } to { opacity: 0; } }\n'
    '  .fz-r-wash { animation: fzCardIn .22s ease both; }\n') + src[m.end():]

rep("        avatarStyle: Object.assign(this.crAvFull(item.ai, isReply, item.mine ? 'assets/comments/avin.png' : item.img), (!isReply && (item.profileIdx!=null || item.mine)) ? { cursor:'pointer' } : {}),",
    "        avatarStyle: Object.assign(this.crAvFull(item.ai, isReply, item.mine ? 'assets/comments/avin.png' : item.img), { cursor:'pointer' }),")
rep("        authorStyle: { color:'#B3B9BB', fontSize:'13px', fontWeight:700, cursor: (!isReply && (item.profileIdx!=null || item.mine)) ? 'pointer' : 'default' },",
    "        authorStyle: { color:'#B3B9BB', fontSize:'13px', fontWeight:700, cursor:'pointer' },")
rep("        onProfile: (e)=>{ if(isReply) return; if(item.profileIdx!=null) this.openOtherProfile(item.profileIdx, e); else if(item.mine) this.openCardFromComments(e); },",
    "        onProfile: (e)=>{ if(item.mine) { this.openCardFromComments(e); return; } this.openOtherProfile(item.profileIdx!=null ? item.profileIdx : this.crProfileFor(item), e); },")
rep('  openOtherProfile = (i, e) => {', '''  // a Fan Card profile for any comment author (made once per name)
  crProfileFor = (item) => {
    const name = item.author || item.name || "Fan";
    let i = OTHER_PROFILES.findIndex(p => p.name === name);
    if (i >= 0) return i;
    let h = 0; for (let k = 0; k < name.length; k++) h = (h * 31 + name.charCodeAt(k)) >>> 0;
    const team = h % 2 ? "bayern" : "bvb";
    const img = item.img ? (item.img.indexOf("/") >= 0 ? item.img : "assets/avatars/" + item.img + ".png") : "";
    const F = ["barcelona", "realmadrid", "mancity", "chelsea", "juventus", "inter"];
    OTHER_PROFILES.push({ name, avatar: img, initial: img ? "" : name.charAt(0).toUpperCase(), second: "bundesliga", status: fanStatusFor(team, h), team,
      following: [F[h % F.length], F[(h >> 3) % F.length] === F[h % F.length] ? F[(h + 1) % F.length] : F[(h >> 3) % F.length]], more: 1 + (h % 5),
      interests: ["in_bundesliga", "in_football", "in_tennis", "in_nba"], watched: ["laliga", "ufc", "tennis"] });
    return OTHER_PROFILES.length - 1;
  };
  openOtherProfile = (i, e) => {''')

# The card content is mounted while the skeleton shows (so its images are loaded by the time it is
# ready); when loading ends the skeleton fades out and the whole card is there at once.
rep('''          <div style="height:24px;"></div>
        </div>
        </sc-if>
        </sc-if>
        <!-- Skeleton (Figma 496:102531), shown while the card loads -->
        <sc-if value="{{ cardLoading }}" hint-placeholder-val="{{ false }}">
          <div style="position:absolute;left:0;right:0;top:60px;height:720px;z-index:5;background:#080E12;pointer-events:none;">''',
'''          <div style="height:24px;"></div>
        </div>
        </sc-if>
        </sc-if>
        <!-- Skeleton (Figma 496:102531), shown while the card loads -->
        <sc-if value="{{ cardSk }}" hint-placeholder-val="{{ false }}">
          <div style="position:absolute;left:0;right:0;top:60px;height:720px;z-index:5;background:#080E12;pointer-events:none;{{ cardSkStyle }}">''')
n = src.count('<sc-if value="{{ cardReady }}" hint-placeholder-val="{{ true }}">')
if n != 2: raise SystemExit('cardReady blocks: %d' % n)
i = src.index('<sc-if value="{{ cardReady }}" hint-placeholder-val="{{ true }}">')
j = src.index('<sc-if value="{{ cardReady }}" hint-placeholder-val="{{ true }}">', i + 10)
src = src[:j] + '<sc-if value="{{ cardMounted }}" hint-placeholder-val="{{ true }}">' + src[j + len('<sc-if value="{{ cardReady }}" hint-placeholder-val="{{ true }}">'):]
rep('this._cardLoadT = setTimeout(() => this.setState({ cardLoading: false }), 1200);',
    'this._cardLoadT = setTimeout(() => { this.setState({ cardLoading: false, cardSkOut: true }); this._cardLoadT = setTimeout(() => this.setState({ cardSkOut: false }), 240); }, 1200);', 2)
rep('cardLoading: !!s.cardLoading, cardReady: !s.cardLoading,',
    'cardLoading: !!s.cardLoading, cardReady: !s.cardLoading, cardMounted: true, cardSk: !!s.cardLoading || !!s.cardSkOut, cardSkStyle: !s.cardLoading && s.cardSkOut ? "animation:fzCardOut .22s ease both;" : "",')

open(PATH, 'w', encoding='utf-8').write(src)
print('ok')
