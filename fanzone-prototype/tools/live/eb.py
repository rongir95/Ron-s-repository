#!/usr/bin/env python3
"""Patch for the live FanZone.dc.html (after auto-moment.py): Engagement break (EB) per Figma FanZone 80-20
(a38ncus4fbwkPfnlFQIUPt 23:138381 "Fanzone package"): a full-bleed video takes over FanZone under its header
(the chat and the message bar) with a round dismiss button (31x32, #3D4549 at 60%, top right 8px).
   moment=eb   opens it (feature pages). The X closes it and FanZone is back.
The video file is assets/eb/eb.mp4 when it's there (Figma's video fill can't be downloaded from here); until then
the EB shows its first frame from Figma (assets/eb/eb-poster.png), which is also the video's poster.
   python3 tools/live/eb.py FanZone.dc.html"""
import os, sys
p = sys.argv[1]; s = open(p, encoding='utf-8').read()
here = os.path.dirname(os.path.abspath(p))
has_video = os.path.exists(os.path.join(here, 'assets/eb/eb.mp4'))
def rep(a, b):
    global s
    if s.count(a) != 1: raise SystemExit('expected once: ' + a[:90])
    s = s.replace(a, b)
media = ('<video src="assets/eb/eb.mp4" poster="assets/eb/eb-poster.png" autoplay="" muted="" loop="" playsinline="" '
         'style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;display:block;"></video>') if has_video else \
        '<img src="assets/eb/eb-poster.png" alt="" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;display:block;">'
rep('        <!-- chat feed -->\n', '''        <!-- Engagement break (Figma FanZone 80-20 23:138381): a video takes over FanZone under the header -->
        <sc-if value="{{ ebOn }}" hint-placeholder-val="{{ false }}">
          <div role="dialog" aria-label="Engagement break" style="position:absolute;left:0;right:0;top:48px;bottom:0;z-index:30;overflow:hidden;background:#080E12;animation:fzFadeIn .3s ease;">
            ''' + media + '''
            <button onClick="{{ ebClose }}" aria-label="Close" title="Close" style="position:absolute;right:8px;top:8px;width:31px;height:32px;border:0;padding:0;border-radius:16px;background:rgba(61,69,73,.6);display:flex;align-items:center;justify-content:center;cursor:pointer;"><svg width="31" height="32" viewBox="0 0 31 32" fill="none" aria-hidden="true" style="display:block;"><path d="M22.71 10.71L21.29 9.29004L16 14.59L10.71 9.29004L9.29004 10.71L14.59 16L9.29004 21.29L10.71 22.71L16 17.41L21.29 22.71L22.71 21.29L17.41 16L22.71 10.71V10.71Z" fill-rule="evenodd" clip-rule="evenodd" fill="#F9FAFA"/></svg></button>
          </div>
        </sc-if>
        <!-- chat feed -->
''')
rep('      ...this.gzVals(),', '      ...this.gzVals(),\n      ebOn: !!this.state.ebOn && this.state.screen === "fanzone", ebClose: () => this.setState({ ebOn: false }),')
rep('["quiz", "pin", "battle", "leaderboard", "team"].indexOf(q.get("moment"))', '["quiz", "pin", "battle", "leaderboard", "team", "eb"].indexOf(q.get("moment"))')
rep('        if (m === "leaderboard") this.openLeaderboard(false);', '        if (m === "leaderboard") this.openLeaderboard(false);\n        else if (m === "eb") this.setState({ ebOn: true });')
open(p, 'w', encoding='utf-8').write(s); print('ok', 'video' if has_video else 'poster')
