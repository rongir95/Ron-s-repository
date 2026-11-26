#!/usr/bin/env python3
"""Patch for the live index.html (after row-rename.py): comments on the slides, through claude.ai's own comments
(the shell draws the pins, cards, replies and the list; publish with capabilities {comments: {customAnchors: true}}).
 - Each comment belongs to one slide and one thing on it: "slide/<feature>/title", ".../note" or ".../phone-<n>"
   (the phone under the Current / 80-20 / ... tag). Its pin shows only while that slide is shown; opening it from the
   comments list goes to its slide.
 - In comment mode, a click on a phone (or its tag), the title or the explanation line starts a comment there
   (phones get a click layer so the click doesn't go into the prototype). A Comment button in the bottom bar
   comments on the slide itself.
   python3 tools/live/slide-comments.py index.html"""
import sys
p = sys.argv[1]; s = open(p, encoding='utf-8').read()
def rep(a, b):
    global s
    if s.count(a) != 1: raise SystemExit('expected once: ' + a[:90])
    s = s.replace(a, b)
BTN = '''          <button type="button" class="fp-cbtn" id="fpComment" hidden aria-label="Comment on this slide" title="Comment on this slide"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 12a8 8 0 0 1-11.6 7.1L4 20l1-4.6A8 8 0 1 1 21 12Z"/></svg></button>
'''
rep('''          <button type="button" class="fp-step fp-next" id="fpNext"''', BTN + '''          <button type="button" class="fp-step fp-next" id="fpNext"''')
rep('''    fitPages();\n  }\n''', '''    fitPages();
    if (window.fzCommentsPlace) setTimeout(window.fzCommentsPlace, 60);
  }\n''')
JS = '''
  // ---------- comments on slides (claude.ai comments, page-anchored) ----------
  (function () {
    if (!window.claude || typeof window.claude.use !== "function") return;
    var ca = null, threads = [], cmode = false;
    var esc = function (t) { return String(t); };
    function feat(id) { return FEATURES.filter(function (x) { return x.id === id; })[0]; }
    function curSet() { return document.querySelector("#fpRow .fp-set:not([hidden])"); }
    function phoneLabel(set, i) { var col = set && set.querySelectorAll(".fp-col")[i]; var c = col && col.querySelector(".fp-chip"); return c ? c.textContent.trim() : "Phone " + (i + 1); }
    // the element an anchor points at, if it's on the slide being shown
    function elFor(anchor) {
      var m = /^slide\\/([^/]+)\\/(title|note|phone-(\\d+))$/.exec(anchor || ""); if (!m) return null;
      if (m[1] !== settings.feature || settings.view !== "pages") return null;
      var set = curSet(); if (!set) return null;
      if (m[2] === "title") { var f = feat(m[1]); return f && f.section ? set.querySelector(".fp-section h1") : document.getElementById("fpTitle"); }
      if (m[2] === "note") { var n = document.getElementById("fpNote"); return n && !n.hidden ? n : null; }
      var col = set.querySelectorAll(".fp-col")[+m[3]]; return col ? (col.querySelector(".fp-phone") || col) : null;
    }
    function pinAt(el) { var r = el.getBoundingClientRect(); return { x: r.right - 14 + scrollX, y: r.top + 14 + scrollY }; }
    function place() {
      if (!ca) return;
      var map = {};
      threads.forEach(function (t) { var el = elFor(t.anchor); map[t.id] = el ? pinAt(el) : null; });
      try { ca.placed(map); } catch (err) {}
    }
    window.fzCommentsPlace = place;
    window.addEventListener("resize", function () { setTimeout(place, 80); });
    // what a click in comment mode points at
    function targetOf(e) {
      var f = feat(settings.feature); if (!f || settings.view !== "pages") return null;
      var t = e.target, set = curSet();
      var col = t.closest && t.closest(".fp-col");
      if (col && set && set.contains(col)) { var i = [].indexOf.call(set.querySelectorAll(".fp-col"), col); return { anchor: "slide/" + f.id + "/phone-" + i, el: col.querySelector(".fp-phone") || col, label: f.name + " \\u00b7 " + phoneLabel(set, i) }; }
      if (t.closest && (t.closest("#fpTitle") || t.closest(".fp-section h1"))) return { anchor: "slide/" + f.id + "/title", el: t.closest("#fpTitle") || t.closest(".fp-section h1"), label: f.name };
      if (t.closest && t.closest("#fpNote")) return { anchor: "slide/" + f.id + "/note", el: document.getElementById("fpNote"), label: f.name + " \\u00b7 explanation" };
      return null;
    }
    document.addEventListener("click", function (e) {
      if (!ca || !cmode) return;
      var tg = targetOf(e); if (!tg) return;
      e.preventDefault(); e.stopPropagation();
      ca.compose(tg.anchor, tg.el, { label: tg.label.slice(0, 120) }).catch(function () {});
    }, true);
    var btn = document.getElementById("fpComment");
    btn.addEventListener("click", function () {
      var f = feat(settings.feature); if (!ca || !f) return;
      var el = f.section ? (curSet() && curSet().querySelector(".fp-section h1")) : document.getElementById("fpTitle");
      if (el) ca.compose("slide/" + f.id + "/title", el, { label: f.name.slice(0, 120) }).catch(function () {});
    });
    window.claude.use("comments").then(function (comments) {
      if (!comments || typeof comments.customAnchors !== "function") return;
      return comments.customAnchors({
        mode: function (on) { cmode = !!on; document.body.classList.toggle("fz-cmode", cmode); if (!on) { threads = []; } place(); },
        threads: function (list) { threads = list || []; place(); },
        reveal: function (id) {
          var t = threads.filter(function (x) { return x.id === id; })[0]; if (!t) return;
          var m = /^slide\\/([^/]+)\\//.exec(t.anchor); if (!m || !feat(m[1])) return;
          if (settings.view !== "pages") { settings.view = "pages"; }
          settings.feature = m[1]; try { localStorage.setItem(KEY, JSON.stringify(settings)); } catch (err) {}
          paintPages(); setTimeout(place, 120);
        }
      }).then(function (api) { ca = api; btn.hidden = false; place(); });
    }).catch(function () {});
  })();
'''
rep('''  paint();
  fit();
  load();''', JS + '''  paint();
  fit();
  load();''')
rep('''  .fp-foot { position: absolute;''', '''  .fp-navs.fp-bottom .fp-cbtn { display: inline-flex; align-items: center; justify-content: center; width: 32px; height: 32px; padding: 0; border: 0; border-radius: 10px; background: transparent; color: #c9ccd1; cursor: pointer; }
  .fp-navs.fp-bottom .fp-cbtn:hover { color: #fff; background: rgba(255, 255, 255, .1); }
  .fp-navs.fp-bottom .fp-cbtn[hidden] { display: none; }
  body.fz-cmode .fp-phone::after { content: ""; position: absolute; inset: 0; z-index: 4; cursor: crosshair; }
  body.fz-cmode .fp-top h2, body.fz-cmode .fp-note, body.fz-cmode .fp-section h1 { cursor: crosshair; }
  .fp-foot { position: absolute;''')
open(p, 'w', encoding='utf-8').write(s); print('ok')
