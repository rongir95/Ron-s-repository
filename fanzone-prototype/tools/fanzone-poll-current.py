#!/usr/bin/env python3
"""FanZone: a second poll type, "Current poll", next to the existing one (now called "Poll V2").
The prototype shell picks which one Start poll runs: postMessage({ fz: "poll", on: true, kind: "current" | "v2" }).

Current poll per FanZone DS (file NIgPxOlNU4U3sWMRdoE4Qh):
  12930:48147  collapsed (tap the header or the question): header (NEW POLL label, segmented timer, chevron) and the question
  12930:48834  open (how it arrives): three answers, each with an outlined check
  12930:49542  voted: your answer gets a yellow check and a lighter row; every answer shows its % and bar
  12930:50235  finished: POLL FINISHED label, your answer row turns yellow

  - The timer is 58 segments that run down over 30s: yellow, then orange, then red-orange with the
    seconds left (from 10s). The last filled segments fade (80%, 60%), the empty ones are 20%.
  - Tap the header or the question to open / collapse it.
  - When time runs out it shows the finished state for 6s and then slides away.
  - The percentages keep moving while it is live (the same live numbers as Poll V2).
  - It sits under the pinned image like Poll V2 does.

Icons are vectors from Figma (the check circles and the chevron are inline SVG).

Run after the other scripts:  python3 tools/fanzone-poll-current.py FanZone.dc.html
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
CHECK = 'M21.4893 11L13.622 18.7333L9.93733 15.0867L9 16.0347L13.1513 20.144C13.2761 20.2671 13.4444 20.3362 13.6197 20.3362C13.795 20.3362 13.9632 20.2671 14.088 20.144L22.4213 11.9493L21.4893 11Z'
V_OPEN = (f'<svg width="32" height="32" viewBox="0 0 32 32" fill="none" aria-hidden="true" style="display:block;"><circle cx="16" cy="16" r="15.5" stroke="#6D7377"/>'
          f'<path d="{CHECK}" fill="#6D7377"/></svg>')
V_MINE = (f'<svg width="32" height="32" viewBox="0 0 32 32" fill="none" aria-hidden="true" style="display:block;"><circle cx="16" cy="16" r="15.5" fill="#F7FF1A" stroke="#4F595F"/>'
          f'<path d="{CHECK}" fill="#4F595F"/></svg>')
V_DONE = (f'<svg width="32" height="32" viewBox="0 0 32 32" fill="none" aria-hidden="true" style="display:block;"><circle cx="16" cy="16" r="15.5" stroke="#4F595F"/>'
          f'<path d="{CHECK}" fill="#4F595F"/></svg>')
CHEV = ('<svg width="24" height="24" viewBox="0 0 24 24" fill="none" aria-hidden="true" style="display:block;transform:rotate({{ cpChevRot }}deg);transition:transform .25s ease;">'
        '<path fill-rule="evenodd" clip-rule="evenodd" d="M16.7071 13.2929L15.2929 14.7072L12 11.4143L8.70709 14.7072L7.29288 13.2929L12 8.58583L16.7071 13.2929Z" fill="#F9FAFA"/></svg>')

PANEL = '''        <!-- Current poll (FanZone DS 12930:48147 / 48834 / 49542 / 50235) -->
        <sc-if value="{{ cpOn }}" hint-placeholder-val="{{ false }}">
          <div style="position:absolute;left:0;right:0;top:{{ pollTop }}px;z-index:2;height:{{ cpH }}px;overflow:hidden;pointer-events:none;transition:opacity .25s ease,top .3s cubic-bezier(.22,1,.36,1),height .4s cubic-bezier(.22,1,.36,1);{{ fzPollWrapStyle }}">
          <section class="fz-poll {{ pollCls }}" aria-label="Poll" style="position:relative;pointer-events:auto;box-sizing:border-box;padding:0 16px 8px;background:#0C161C;''' + FONT + '''color:#F9FAFA;">
            <div style="background:#242D33;border-radius:0 0 6px 6px;overflow:hidden;display:flex;flex-direction:column;gap:12px;padding-bottom:12px;">
              <button onClick="{{ cpToggle }}" aria-label="{{ cpToggleLabel }}" style="display:flex;align-items:center;gap:8px;height:48px;width:100%;box-sizing:border-box;padding:0 12px;border:0;border-bottom:1px solid rgba(158,162,164,.2);background:#242D33;cursor:pointer;''' + FONT + '''">
                <span style="flex-shrink:0;height:18px;box-sizing:border-box;padding:1px 6px;border-radius:2px;background:{{ cpLabelBg }};display:flex;align-items:center;font-weight:700;font-size:12px;line-height:16px;text-transform:uppercase;color:{{ cpLabelColor }};white-space:nowrap;">{{ cpLabel }}</span>
                <span style="position:relative;flex:1;min-width:0;height:18px;display:flex;border-radius:2px;overflow:hidden;">
                  <sc-for list="{{ cpSegs }}" as="g" hint-placeholder-count="58">
                    <span style="flex:1;height:18px;background:{{ g }};"></span>
                  </sc-for>
                  <sc-if value="{{ cpShowSecs }}" hint-placeholder-val="{{ false }}">
                    <span style="position:absolute;right:2.58%;top:1px;font-weight:800;font-size:14px;line-height:16px;color:#F9FAFA;">{{ cpSecs }}</span>
                  </sc-if>
                </span>
                <span style="flex-shrink:0;width:24px;height:24px;">''' + CHEV + '''</span>
              </button>
              <div style="display:flex;flex-direction:column;gap:12px;padding:0 12px;">
                <div onClick="{{ cpToggle }}" style="font-weight:700;font-size:18px;line-height:1.38;color:#F9FAFA;cursor:pointer;">Vote for the official MOTM</div>
                <sc-if value="{{ cpOpen }}" hint-placeholder-val="{{ true }}">
                <div style="display:flex;flex-direction:column;gap:8px;">
                  <sc-for list="{{ cpOptions }}" as="o" hint-placeholder-count="3">
                    <button onClick="{{ o.pick }}" disabled="{{ cpLocked }}" aria-label="{{ o.name }}" style="display:flex;align-items:center;gap:10px;height:48px;width:100%;box-sizing:border-box;padding:0 12px;border:0;border-radius:4px;background:{{ o.bg }};cursor:pointer;text-align:left;transition:background-color .25s ease;''' + FONT + '''">
                      <span style="flex-shrink:0;width:32px;height:32px;">
                        <sc-if value="{{ o.vOpen }}" hint-placeholder-val="{{ true }}">''' + V_OPEN + '''</sc-if>
                        <sc-if value="{{ o.vMine }}" hint-placeholder-val="{{ false }}"><span style="display:block;animation:fzRxPop .3s cubic-bezier(.22,1.6,.36,1);">''' + V_MINE + '''</span></sc-if>
                        <sc-if value="{{ o.vDone }}" hint-placeholder-val="{{ false }}">''' + V_DONE + '''</sc-if>
                      </span>
                      <span style="flex:1;min-width:0;display:flex;flex-direction:column;gap:6px;">
                        <span style="display:flex;justify-content:space-between;font-size:16px;line-height:1.55;color:{{ o.text }};white-space:nowrap;">
                          <span>{{ o.name }}</span>
                          <sc-if value="{{ cpVoted }}" hint-placeholder-val="{{ false }}"><span>{{ o.pct }}%</span></sc-if>
                        </span>
                        <sc-if value="{{ cpVoted }}" hint-placeholder-val="{{ false }}">
                          <span style="position:relative;display:block;height:6px;border-radius:99px;background:#576065;">
                            <span style="position:absolute;left:.39%;top:1px;bottom:1px;width:{{ o.pct }}%;border-radius:99px;background:#F7FF1A;transition:width .8s ease;"></span>
                          </span>
                        </sc-if>
                      </span>
                    </button>
                  </sc-for>
                </div>
                </sc-if>
              </div>
            </div>
          </section>
          </div>
        </sc-if>
'''
rep('        <!-- chat feed -->\n', PANEL + '        <!-- chat feed -->\n')

LOGIC = '''  // Current poll (FanZone DS); Poll V2 is the other kind
  cpVals() {
    const s = this.state;
    const on = !!s.pollOn && s.screen === "fanzone" && s.pollKind === "current";
    if (!on) return { cpOn: false, cpOptions: [], cpSegs: [] };
    const collapsed = !!s.pollCollapsed && !s.cpFinished;
    const voted = !!s.pollVote || !!s.cpFinished;
    const frac = Math.max(0, Math.min(1, (s.pollTime ?? 100) / 100));
    const secs = Math.ceil(frac * 30);
    const col = frac > 0.5 ? "247,255,26" : (frac > 1 / 3 ? "255,156,26" : "255,108,26");
    const N = 58, filled = s.cpFinished ? 0 : Math.ceil(frac * N);
    const segs = [];
    for (let i = 0; i < N; i++) {
      const fromEnd = filled - 1 - i; // 0 = the last filled segment
      const a = i >= filled ? 0.2 : (fromEnd < 2 ? 0.6 : (fromEnd < 4 ? 0.8 : 1));
      segs.push("rgba(" + col + "," + a + ")");
    }
    const pcts = s.pollPcts || [46, 31, 23];
    const P = [["kimmich", "Joshua Kimmich"], ["olise", "Michael Olise"], ["kane", "Harry Kane"]];
    return {
      cpOn: true,
      cpH: collapsed ? 105 : 277, cpOpen: !collapsed,
      cpToggle: () => { if (!this.state.cpFinished) this.setState({ pollCollapsed: !collapsed }); },
      cpToggleLabel: collapsed ? "Open the poll" : "Collapse the poll",
      cpChevRot: collapsed ? 180 : 0,
      cpLabel: s.cpFinished ? "Poll finished" : "New poll",
      cpLabelBg: s.cpFinished ? "#CED0D2" : "#3D4549", cpLabelColor: s.cpFinished ? "#0C161C" : "#F7FF1A",
      cpSegs: segs, cpShowSecs: !s.cpFinished && secs <= 10, cpSecs: String(secs),
      cpVoted: voted, cpLocked: voted,
      cpOptions: P.map(([id, name], i) => {
        const mine = s.pollVote === id;
        return { id, name, pct: pcts[i],
          bg: mine ? (s.cpFinished ? "#F7FF1A" : "#4F595F") : "#3D4549",
          text: mine && s.cpFinished ? "#242D33" : "#F9FAFA",
          vOpen: !voted, vMine: mine && !s.cpFinished, vDone: mine && !!s.cpFinished,
          pick: () => this.setState(st => (st.pollVote || st.cpFinished ? null : { pollVote: id })) };
      }),
    };
  }
  openFanZoneOver = (e) => {'''
rep('  openFanZoneOver = (e) => {', LOGIC)
rep('      ...this.gzVals(),', '      ...this.gzVals(),\n      ...this.cpVals(),')

# Poll V2 shows only for its own kind
rep('      pollMounted: on,', '      pollMounted: on && s.pollKind !== "current",')

# the shell says which kind to start
rep('      if (d.on) { if (this.state.pinExpanded) this.setState({ pinExpanded: false }); this.pollStart(); } else this.pollEnd();',
    '      if (d.on) { this._pollKind = d.kind === "current" ? "current" : "v2"; if (this.state.pinExpanded) this.setState({ pinExpanded: false }); this.pollStart(); } else this.pollEnd();')
rep('    this.setState({ pollOn: true, pollClosing: false, pollCollapsed: false, pollVote: null,',
    '    clearTimeout(this._cpFinT);\n    this.setState({ pollOn: true, pollClosing: false, pollCollapsed: false, pollKind: this._pollKind || "v2", cpFinished: false, pollVote: null,')
# Current poll: 30s, then the finished state for 6s
rep('''      const t = (this.state.pollTime ?? 100) - 100 / 90;
      if (t <= 0) this.pollEnd(); else this.setState({ pollTime: t });''',
    '''      const cur = this.state.pollKind === "current";
      const t = (this.state.pollTime ?? 100) - 100 / (cur ? 30 : 90);
      if (t <= 0 && cur) { this.pollClear(); this.setState({ pollTime: 0, cpFinished: true, pollCollapsed: false }); this._cpFinT = setTimeout(() => this.pollEnd(), 6000); }
      else if (t <= 0) this.pollEnd(); else this.setState({ pollTime: t });''')
rep('    this._pollOutT = setTimeout(() => this.setState({ pollOn: false, pollClosing: false }), 420);',
    '    clearTimeout(this._cpFinT);\n    this._pollOutT = setTimeout(() => this.setState({ pollOn: false, pollClosing: false, cpFinished: false }), 420);')

open(PATH, 'w', encoding='utf-8').write(src)
print('ok')
