#!/usr/bin/env python3
"""Patch for the live FanZone.dc.html: the match page as the "Outside FanZone" screen of the feature pages
(Figma FanZone 80-20, a38ncus4fbwkPfnlFQIUPt 23:153607).
   fixture=1        the prototype opens on the match page with FanZone closed (no live event: FanZone doesn't
                    open by itself)
   slot=<name>      where the FanZone card sits, a placeholder for that feature (Poll, Quiz, ...): when there is
                    no live event this spot shows a feature instead of the FanZone button. Same place and width
                    as the card; 96px high like the FanZone block in Figma.
Without these keys nothing changes.
   python3 tools/live/fixture-slot.py FanZone.dc.html"""
import sys
p = sys.argv[1]; s = open(p, encoding='utf-8').read()
def rep(a, b):
    global s
    if s.count(a) != 1: raise SystemExit('expected once: ' + a[:90])
    s = s.replace(a, b)
rep('    if (q.get("reset") === "1") o.resetOnLoad = true;',
    '    if (q.get("reset") === "1") o.resetOnLoad = true;\n'
    '    if (q.get("fixture") === "1") o.startFixture = true;\n'
    '    if (q.get("slot")) o.fixtureSlot = String(q.get("slot")).slice(0, 60);')
rep('  componentDidMount() {\n',
    '  componentDidMount() {\n'
    '    // feature pages: open on the match page with FanZone closed (no live event)\n'
    '    if (this.P.startFixture) this.setState({ screen: "fixture", fzOver: false, fzEntrySeen: true, showHomeTip: false });\n')
old_start = '''          <sc-if value="{{ showFzEntry }}" hint-placeholder-val="{{ false }}">
            <div style="padding:16px 16px 4px;">
              <button class="fz-entry"'''
rep(old_start, '''          <sc-if value="{{ showFxSlot }}" hint-placeholder-val="{{ false }}">
            <div style="padding:16px 16px 4px;">
              <div role="note" aria-label="{{ fxSlotName }}: placeholder" style="width:343px;height:96px;box-sizing:border-box;border:1.5px dashed #3D4549;border-radius:18px;background:#0C161C;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:4px;font-family:'DAZN Oscine',sans-serif;text-align:center;padding:0 16px;">
                <span style="font-weight:700;font-size:14px;line-height:20px;color:#F9FAFA;">{{ fxSlotName }}</span>
                <span style="font-size:12px;line-height:16px;color:#8C959E;">Placeholder · shown here when there's no live event</span>
              </div>
            </div>
          </sc-if>
          <sc-if value="{{ showFzEntry }}" hint-placeholder-val="{{ false }}">
            <div style="padding:16px 16px 4px;">
              <button class="fz-entry"''')
rep('      showFzEntry: s.screen === "fixture" && !!s.fzEntrySeen,',
    '      showFzEntry: s.screen === "fixture" && !!s.fzEntrySeen && !this.P.fixtureSlot,\n'
    '      showFxSlot: s.screen === "fixture" && !!this.P.fixtureSlot, fxSlotName: this.P.fixtureSlot || "",')
open(p, 'w', encoding='utf-8').write(s); print('ok')
