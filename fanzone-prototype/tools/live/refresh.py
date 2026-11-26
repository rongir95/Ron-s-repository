#!/usr/bin/env python3
"""Patch for the live index.html (after load-seq.py):
 - Each feature page has a refresh button next to its page count: it restarts that page's phones only.
 - The side panel has a general refresh button next to the FanZone title: it reloads everything.
 - The line under the FanZone title ("Interactive prototype: ...") is removed.
   python3 tools/live/refresh.py index.html"""
import sys
p = sys.argv[1]; s = open(p, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    if s.count(a) != n: raise SystemExit('expected %d: %s' % (n, a[:90]))
    s = s.replace(a, b)
ICON = '<svg width="14" height="14" viewBox="0 0 16 16" fill="none" aria-hidden="true" style="display:block;"><path d="M13.5 8a5.5 5.5 0 1 1-1.61-3.89M13.5 2.5v3h-3" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>'
rep('''      <p>Interactive prototype: Home, the match page with Comments &amp; Replies, the Fan Card and FanZone live chat.</p>\n''', '')
rep('''<span class="fp-count" id="fpCount"></span>''',
    '''<span class="fp-countrow"><span class="fp-count" id="fpCount"></span><button type="button" class="fp-refresh" id="fpRefresh" aria-label="Restart this page" title="Restart this page">''' + ICON + '''</button></span>''')
rep('''FanZone<button type="button" class="panel-btn" id="panelClose"''',
    '''FanZone<button type="button" class="all-refresh" id="allRefresh" aria-label="Reload everything" title="Reload everything">''' + ICON.replace('width="14" height="14"', 'width="16" height="16"') + '''</button><button type="button" class="panel-btn" id="panelClose"''')
rep('''  .panel-btn { display: none; }''', '''  .panel-btn { display: none; }
  .fp-countrow { display: inline-flex; align-items: center; justify-content: center; gap: 8px; }
  .fp-refresh { display: inline-flex; align-items: center; justify-content: center; width: 24px; height: 24px; padding: 0; border: 1px solid var(--line-strong); border-radius: 50%; background: var(--surface); color: var(--muted); cursor: pointer; }
  .fp-refresh:hover, .fp-refresh:focus-visible { color: var(--text); background: var(--raise); }
  .all-refresh { margin-left: auto; display: flex; align-items: center; justify-content: center; width: 32px; height: 32px; padding: 0; border: 1px solid var(--line-strong); border-radius: 10px; background: var(--surface); color: var(--text); cursor: pointer; flex: none; }
  .all-refresh:hover, .all-refresh:focus-visible { background: var(--raise); }
  .brand h1 .all-refresh + .panel-btn { margin-left: 8px; }''')
rep('''  document.getElementById("fpPrev").addEventListener("click",''', '''  // restart this page's phones / reload everything
  document.getElementById("fpRefresh").addEventListener("click", function () {
    var id = settings.feature, el = setFor(id); if (el) el.remove();
    setOrder = setOrder.filter(function (x) { return x !== id; });
    shownFeature = null; fpDir = 0; paintPages();
  });
  document.getElementById("allRefresh").addEventListener("click", function () { location.reload(); });
  document.getElementById("fpPrev").addEventListener("click",''')
open(p, 'w', encoding='utf-8').write(s); print('ok')
