#!/usr/bin/env python3
"""Fan Battle: a gift you send plays big in the middle of the chat
(Fan Battle file QRYQoParO5SQY1djfuBnB5, screen 4935:36015, "Animation gifts" set 6482:109451).

  - The 375x375 animation sits at the top of the chat, under the battle strip, over the messages.
    Taps do not go to it; you can keep sending gifts.
  - Each tap restarts it with the new gift. It plays for about 2.4s and then fades out.
  - Source: assets/gifts/anim/{red|yellow}-{finger|flag|horn|drum|fireworks}.gif when that file exists
    (the Figma animations are animated GIFs). Until then it plays the DS gift image with a CSS animation:
    a team-colour circle grows behind it, the gift pops in, does its move (finger pumps, flag waves,
    horn shakes, drum beats, fireworks burst) and floats away.

Run after fanzone-battle.py:  python3 tools/fanzone-gift-anim.py FanZone.dc.html
"""
import os, sys

PATH = sys.argv[1]
src = open(PATH, encoding='utf-8').read()
HERE = os.path.dirname(os.path.abspath(PATH))

def rep(old, new, count=1):
    global src
    n = src.count(old)
    if n != count:
        raise SystemExit(f'expected {count} occurrence(s), found {n}: {old[:100]!r}')
    src = src.replace(old, new)

KINDS = ['finger', 'flag', 'horn', 'drum', 'fireworks']
HAVE_GIF = sorted(f'{c}-{k}' for c in ('red', 'yellow') for k in KINDS
                  if os.path.exists(os.path.join(HERE, 'assets/gifts/anim', f'{c}-{k}.gif')))

SPARKS = ''.join(
    f'<span style="position:absolute;left:50%;top:50%;width:10px;height:10px;margin:-5px 0 0 -5px;border-radius:50%;'
    f'background:{{{{ ga.spark }}}};--a:{a}deg;animation:gaSpark 1.1s .35s ease-out both;"></span>'
    for a in range(0, 360, 30))

PANEL = '''        <!-- Fan Battle: the gift you sent plays big over the chat (Fan Battle 4935:36015) -->
        <sc-if value="{{ gaOn }}" hint-placeholder-val="{{ false }}">
          <div aria-hidden="true" style="position:absolute;left:0;top:{{ gaTop }}px;width:375px;height:375px;z-index:6;pointer-events:none;overflow:hidden;">
            <sc-for list="{{ gaList }}" as="ga" hint-placeholder-count="1">
              <div style="position:absolute;inset:0;animation:gaOut 2.4s linear both;">
                <sc-if value="{{ ga.gif }}" hint-placeholder-val="{{ false }}">
                  <img src="{{ ga.src }}" alt="" width="375" height="375" style="display:block;">
                </sc-if>
                <sc-if value="{{ ga.css }}" hint-placeholder-val="{{ true }}">
                  <span style="position:absolute;left:50%;top:50%;width:220px;height:220px;margin:-110px 0 0 -110px;border-radius:50%;background:{{ ga.circle }};animation:gaCircle 2.4s cubic-bezier(.22,1,.36,1) both;"></span>
                  <sc-if value="{{ ga.burst }}" hint-placeholder-val="{{ false }}">''' + SPARKS + '''</sc-if>
                  <span style="position:absolute;left:50%;top:50%;width:260px;height:223px;margin:-112px 0 0 -130px;animation:gaPop 2.4s cubic-bezier(.22,1,.36,1) both;">
                    <img src="{{ ga.src }}" alt="" width="260" height="223" draggable="false" style="display:block;transform-origin:50% 85%;filter:drop-shadow(0 10px 18px rgba(0,0,0,.45));{{ ga.move }}">
                  </span>
                </sc-if>
              </div>
            </sc-for>
          </div>
        </sc-if>
'''
rep('        <!-- chat feed -->\n', PANEL + '        <!-- chat feed -->\n')

rep('  @keyframes fzPushIn {',
    '  @keyframes gaOut { 0%, 86% { opacity: 1; } 100% { opacity: 0; } }\n'
    '  @keyframes gaCircle { 0% { transform: scale(0); opacity: 0; } 18% { transform: scale(1.05); opacity: .9; } 30%, 78% { transform: scale(1); opacity: .9; } 100% { transform: scale(1.25); opacity: 0; } }\n'
    '  @keyframes gaPop { 0% { transform: translateY(70px) scale(.2); opacity: 0; } 16% { transform: translateY(-6px) scale(1.12); opacity: 1; } 26%, 80% { transform: none; opacity: 1; } 100% { transform: translateY(-70px) scale(.9); opacity: 0; } }\n'
    '  @keyframes gaPump { 0%, 22%, 82%, 100% { transform: none; } 34%, 54%, 74% { transform: translateY(-26px) rotate(-6deg); } 44%, 64% { transform: translateY(4px); } }\n'
    '  @keyframes gaWave { 0%, 22%, 84%, 100% { transform: none; } 34% { transform: rotate(-14deg); } 46% { transform: rotate(12deg); } 58% { transform: rotate(-12deg); } 70% { transform: rotate(10deg); } }\n'
    '  @keyframes gaShake { 0%, 22%, 82%, 100% { transform: none; } 28%, 40%, 52%, 64%, 76% { transform: translateX(-9px) rotate(-5deg) scale(1.04); } 34%, 46%, 58%, 70% { transform: translateX(9px) rotate(5deg) scale(1.04); } }\n'
    '  @keyframes gaBeat { 0%, 22%, 84%, 100% { transform: none; } 30%, 44%, 58%, 72% { transform: scale(.86, .9); } 37%, 51%, 65%, 79% { transform: scale(1.1); } }\n'
    '  @keyframes gaLaunch { 0%, 22%, 84%, 100% { transform: none; } 32% { transform: translateY(8px) scale(1.05, .92); } 42%, 70% { transform: translateY(-14px) rotate(3deg); } 56% { transform: translateY(-18px) rotate(-3deg); } }\n'
    '  @keyframes gaSpark { 0% { transform: rotate(var(--a)) translateY(0) scale(.4); opacity: 0; } 15% { opacity: 1; } 100% { transform: rotate(var(--a)) translateY(-150px) scale(1); opacity: 0; } }\n'
    '  @keyframes fzPushIn {')

LOGIC = '''  // Fan Battle: play the gift you sent over the chat
  playGiftAnim(kind) {
    const color = this.state.fzTeam === "bvb" ? "yellow" : "red";
    clearTimeout(this._gaT);
    const n = (this._gaN = (this._gaN || 0) + 1);
    // unmount first so a second tap starts the animation again
    this.setState({ gaAnim: null }, () => requestAnimationFrame(() => this.setState({ gaAnim: { kind, color, n } })));
    this._gaT = setTimeout(() => this.setState({ gaAnim: null }), 2450);
  }
  gaVals() {
    const s = this.state, a = s.screen === "fanzone" && s.fbPhase === "battle" ? s.gaAnim : null;
    if (!a) return { gaOn: false, gaList: [], gaTop: 40 };
    const gif = GIFT_ANIM_GIFS.includes(a.color + "-" + a.kind);
    const move = { finger: "gaPump", flag: "gaWave", horn: "gaShake", drum: "gaBeat", fireworks: "gaLaunch" }[a.kind];
    return {
      gaOn: true, gaTop: 40,
      // a new list item per tap, so the animation starts again from the top
      gaList: [{ key: a.n, gif, css: !gif,
        src: gif ? "assets/gifts/anim/" + a.color + "-" + a.kind + ".gif?n=" + a.n : "assets/gifts/" + a.color + "-" + a.kind + ".png",
        circle: a.color === "yellow" ? "rgba(253,225,0,.55)" : "rgba(220,5,45,.6)",
        spark: a.color === "yellow" ? "#FDE100" : "#FF4D5E", burst: a.kind === "fireworks",
        move: "animation:" + move + " 2.4s ease-in-out both;" }],
    };
  }
  openFanZoneOver = (e) => {'''
rep('  openFanZoneOver = (e) => {', LOGIC)
rep('      ...this.gzVals(),', '      ...this.gzVals(),\n      ...this.gaVals(),')
rep('// FanZone chat: which team each fan supports',
    '// Fan Battle gift animations available as GIFs (assets/gifts/anim/)\nconst GIFT_ANIM_GIFS = ' + repr(HAVE_GIF).replace("'", '"') + ';\n// FanZone chat: which team each fan supports')

# sending a gift plays it
rep('    this._fbPulseT = setTimeout(() => this.setState({ fbPulse: null, fbFlash: null }), 650);\n  };',
    '    this._fbPulseT = setTimeout(() => this.setState({ fbPulse: null, fbFlash: null }), 650);\n'
    '    this.playGiftAnim({ 5: "finger", 10: "flag", 50: "horn", 100: "drum", 500: "fireworks" }[amount] || "flag");\n  };')

open(PATH, 'w', encoding='utf-8').write(src)
print('ok', 'gifs:', HAVE_GIF)
