#!/usr/bin/env python3
"""Patch for the live index.html (after phone-loader.py):
 - Phones on a page load one after the other (Current first), not all at once: they share one thread, so
   together they all finished after ~3s; now the first shows after ~1s and the next follow.
 - The side list's first group is called "80-20" (was "Improvements"); Share moment moves into it.
   python3 tools/live/load-seq.py index.html"""
import sys
p = sys.argv[1]; s = open(p, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    if s.count(a) != n: raise SystemExit('expected %d: %s' % (n, a[:90]))
    s = s.replace(a, b)
rep('''" src="' + landSrc(ph.q) + '"''', '''" data-src="' + landSrc(ph.q) + '"''')
rep('''" src="' + phoneSrc(ph.q) + '"''', '''" data-src="' + phoneSrc(ph.q) + '"''')
rep('''      el.innerHTML = setHTML(f);
      row.appendChild(el);''', '''      el.innerHTML = setHTML(f);
      row.appendChild(el);
      startLoads(el);''')
rep('''      if (ok || Date.now() - t0 > 8000) { fr.classList.add("ready"); return; }''',
    '''      if (ok || Date.now() - t0 > 8000) { fr.classList.add("ready"); var set = fr.closest(".fp-set"); if (set) startLoads(set); return; }''')
rep('''  function setHTML(f) {''', '''  // start the next phone of a page that hasn't started loading yet
  function startLoads(el) {
    var nx = el.querySelector("iframe[data-src]"); if (!nx) return;
    nx.src = nx.getAttribute("data-src"); nx.removeAttribute("data-src");
  }
  function setHTML(f) {''')
rep('''var groups = [["imp", "Improvements"], ["new", "New"]];''', '''var groups = [["imp", "80-20"], ["new", "New"]];''')
rep('''{"id": "share", "name": "Share moment", "cat": "Activations", "kind": "new", "screens": 2}''',
    '''{"id": "share", "name": "Share moment", "cat": "Activations", "kind": "imp", "screens": 2}''')
open(p, 'w', encoding='utf-8').write(s); print('ok')
