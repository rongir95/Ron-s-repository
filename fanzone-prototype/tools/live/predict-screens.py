"""screens.html: Standalone predictions. ?v=predict = Scores with Predict, drawer open, then predicted. ?v=predictfix = match page with the prediction card."""
import sys
p = sys.argv[1]; s = open(p).read()
CSS = '''
/* Standalone predictions (Figma 81:91507, 19393:15953) */
.sc .pred.rb { cursor: pointer; background: radial-gradient(70px 40px at 0% 0%, rgba(209,36,36,.5), rgba(126,18,37,.25) 50%, rgba(27,35,38,0) 100%), radial-gradient(64px 50px at 100% 100%, rgba(255,217,0,.4), rgba(141,126,19,.2) 50%, rgba(27,35,38,0) 100%), linear-gradient(rgba(249,250,250,.04), rgba(249,250,250,.04)), #1B2326; border: 1px solid rgba(249,250,250,.1); border-top-color: rgba(249,250,250,.2); }
.pq-scrim { position: absolute; inset: 0; z-index: 10; background: rgba(8,14,18,.64); animation: pqFade .25s ease both; }
.pq-scrim[hidden] { display: none; }
.pq-sheet { position: absolute; left: 0; right: 0; bottom: 0; border-radius: 12px 12px 0 0; box-shadow: 0 -1px 0 rgba(255,255,255,.2); overflow: hidden; font-family: "DAZN Oscine", sans-serif; color: #F9FAFA; animation: pqUp .4s cubic-bezier(.2,.8,.2,1) both; padding-bottom: 34px;
  background: radial-gradient(120px 190px at 0% 50%, rgba(224,0,36,.5) 0%, rgba(175,9,37,.37) 25%, rgba(126,18,37,.25) 50%, rgba(27,35,38,0) 100%), radial-gradient(110px 230px at 100% 50%, var(--pq-r, rgba(255,217,0,.5)) 0%, var(--pq-r2, rgba(141,126,19,.25)) 50%, rgba(27,35,38,0) 100%), linear-gradient(rgba(249,250,250,.04), rgba(249,250,250,.04)), #0C161C; }
.pq-sheet.red { --pq-r: rgba(224,0,36,.5); --pq-r2: rgba(126,18,37,.25); }
.pq-top { position: relative; height: 60px; border-bottom: 1px solid rgba(255,255,255,.1); }
.pq-grab { position: absolute; left: 50%; top: 5px; width: 36px; height: 5px; margin-left: -18px; border-radius: 3px; background: rgba(249,250,250,.3); }
.pq-ttl { position: absolute; left: 16px; top: 21px; display: flex; align-items: center; gap: 4px; font-weight: 700; font-size: 15.6px; letter-spacing: .16px; }
.pq-ttl img { width: 24px; height: 24px; display: block; }
.pq-x { all: unset; position: absolute; right: 16px; top: 17px; width: 32px; height: 32px; border-radius: 50%; background: rgba(255,255,255,.2); display: flex; align-items: center; justify-content: center; cursor: pointer; }
.pq-body { padding: 12px 16px 0; }
.pq-eb { display: flex; align-items: center; justify-content: space-between; padding: 8px 0; }
.pq-eb small { display: block; font-size: 12px; color: #C5C7CA; letter-spacing: .12px; }
.pq-eb b { display: block; font-size: 16px; margin-top: 2px; }
.pq-lbl { min-height: 20px; box-sizing: border-box; padding: 4px 6px; border-radius: 8px; font-weight: 700; font-size: 12px; line-height: 1; text-transform: uppercase; background: #6EDB98; color: #080E12; border: 1px solid #6EDB98; }
.pq-lbl.out { background: transparent; color: #6EDB98; }
.pq-opts { display: flex; gap: 8px; padding: 24px 0; }
.pq-opt { all: unset; box-sizing: border-box; flex: 1; height: 88px; border-radius: 8px; background: rgba(249,250,250,.12); display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 8px; cursor: pointer; font-weight: 700; font-size: 14px; color: #C5C7CA; transition: background .2s ease, flex .35s ease; }
.pq-opt:hover { background: rgba(249,250,250,.18); }
.pq-opt img { width: 40px; height: 40px; object-fit: contain; display: block; }
.pq-opt.draw { flex: 0 0 48px; }
.pq-cta { all: unset; box-sizing: border-box; width: 100%; height: 40px; border-radius: 8px; background: #F9FAFA; color: #080E12; display: flex; align-items: center; justify-content: center; gap: 8px; font-weight: 700; font-size: 14px; letter-spacing: .14px; cursor: pointer; margin-bottom: 12px; }
.pq-fans { display: flex; align-items: center; gap: 6px; height: 24px; font-size: 12px; color: #C5C7CA; }
.pq-fans span { display: flex; } .pq-fans img { width: 16px; height: 16px; border-radius: 50%; margin-right: -8px; display: block; } .pq-fans img:last-child { margin-right: 0; }
@keyframes pqFade { from { opacity: 0; } to { opacity: 1; } }
@keyframes pqUp { from { transform: translateY(100%); } to { transform: none; } }
/* match page */
.fx { font-family: "DAZN Oscine", sans-serif; color: #F9FAFA; }
.fx .body { position: absolute; left: 0; right: 0; top: 274px; bottom: 0; overflow-y: auto; scrollbar-width: none; }
.fx .body::-webkit-scrollbar { display: none; }
.fx .comp { display: flex; align-items: center; gap: 16px; padding: 12px 16px; border-bottom: 1px solid rgba(255,255,255,.2); }
.fx .comp .l { flex: 1; display: flex; align-items: center; gap: 8px; font-weight: 700; font-size: 14px; color: #B3B9BB; }
.fx .comp .l span { width: 32px; height: 32px; border-radius: 50%; background: #F9FAFA; display: flex; align-items: center; justify-content: center; }
.fx .comp .l img { width: 24px; height: 24px; display: block; }
.fx .pill { height: 32px; padding: 0 12px; border-radius: 9999px; background: #242D33; display: inline-flex; align-items: center; gap: 6px; font-weight: 700; font-size: 12px; letter-spacing: .12px; box-sizing: border-box; flex: none; }
.fx .comp .pill { font-size: 14px; }
.fx .meta { padding: 8px 16px; }
.fx .meta h1 { margin: 0; font-size: 20px; line-height: 1.32; font-weight: 700; }
.fx .meta p { margin: 4px 0 0; font-size: 14px; line-height: 1.5; color: #B3B9BB; }
.fx .acts { display: flex; gap: 8px; padding: 6px 0 6px 16px; overflow: hidden; }
.fx .acts img { width: 24px; height: 24px; display: block; }
.fx .pc { margin: 18px 16px 0; border: 1px solid rgba(255,255,255,.2); border-radius: 12px; overflow: hidden;
  background: radial-gradient(103px 109px at 0% 50%, rgba(224,0,36,.5) 0%, rgba(175,9,37,.37) 25%, rgba(126,18,37,.25) 50%, rgba(27,35,38,0) 100%), radial-gradient(95px 134px at 100% 50%, rgba(255,217,0,.5) 0%, rgba(198,172,10,.37) 25%, rgba(141,126,19,.25) 50%, rgba(84,81,29,.12) 75%, rgba(27,35,38,0) 100%), linear-gradient(rgba(249,250,250,.04), rgba(249,250,250,.04)); }
.fx .pc .pq-eb { padding: 8px 12px; }
.fx .pc .pq-opts { padding: 12px; gap: 8px; }
.fx .pc .pq-opt { height: 58px; gap: 6px; }
.fx .pc .pq-opt img { width: 24px; height: 24px; }
.fx .pc .pq-opt.draw { flex: 0 0 48px; }
.fx .pc .pq-opt.mine { box-shadow: inset 0 0 0 1.5px #F9FAFA; color: #F9FAFA; }
.fx .pc .pq-opt .pct { font-size: 12px; font-weight: 700; color: #F9FAFA; display: none; }
.fx .pc.done .pq-opt .pct { display: block; }
.fx .pc.done .pq-opt { cursor: default; gap: 3px; }
.fx .pc .ft { border-top: 1px solid rgba(249,250,250,.1); padding: 8px 12px; }
.fx .tabs { display: flex; margin-top: 26px; padding-left: 16px; border-bottom: 1px solid #3D4549; white-space: nowrap; }
.fx .tabs span { height: 40px; padding: 0 16px; display: flex; align-items: center; font-weight: 700; font-size: 14px; color: #B3B9BB; }
.fx .tabs span.on { color: #F9FAFA; box-shadow: inset 0 -2px 0 #FFFA00; }
.fx .rail h2 { margin: 0; padding: 16px; font-size: 20px; line-height: 1.32; }
.fx .tiles { display: flex; gap: 16px; padding: 0 16px 24px; }
.fx .tl { width: 284px; flex: none; }
.fx .tl .cr { position: relative; height: 160px; border-radius: 10px; overflow: hidden; display: flex; }
.fx .tl .cr i { flex: 1; display: flex; align-items: center; justify-content: center; }
.fx .tl .cr i img { width: 68px; height: 68px; object-fit: contain; }
.fx .tl .cr em { position: absolute; left: 11px; top: 11px; height: 16px; padding: 0 7px; border-radius: 4px; background: rgba(255,255,255,.88); color: #242D33; font-style: normal; font-weight: 700; font-size: 11px; display: flex; align-items: center; }
.fx .tl b { display: block; margin-top: 12px; font-size: 16px; line-height: 20px; }
.fx .tl small { display: block; font-size: 14px; line-height: 20px; color: #CED0D2; }
'''
s = s.replace('</style></head>', CSS + '</style></head>', 1)

X = '<svg width="20" height="20" viewBox="0 0 20 20" fill="none" aria-hidden="true"><path d="M15.5 5.5L14.5 4.5L10 9L5.5 4.5L4.5 5.5L9 10L4.5 14.5L5.5 15.5L10 11L14.5 15.5L15.5 14.5L11 10L15.5 5.5Z" fill="#F9FAFA"/></svg>'
SHEET = ('<div class="pq-scrim" id="pqScrim" hidden><div class="pq-sheet" id="pqSheet" role="dialog" aria-label="Predict"><div class="pq-top"><span class="pq-grab"></span><div class="pq-ttl"><img src="assets/scores/predict.svg" alt="">Predict</div>'
         '<button class="pq-x" id="pqX" type="button" aria-label="Close">' + X + '</button></div><div class="pq-body" id="pqBody"></div></div></div>')
FANS = '<div class="pq-fans"><span><img src="assets/scores/fan1.png" alt=""><img src="assets/scores/fan2.png" alt=""><img src="assets/scores/fan3.png" alt=""></span>5.7K fans predicted</div>'

FIX = ('''<div class="scr fx" id="predictfix" data-fz-root="1" hidden>
  <img class="status" src="assets/img/status-bar.svg" alt="">
  <video class="video" src="assets/video/fixture-bayern-bvb-lite.mp4" autoplay muted loop playsinline preload="auto"></video>
  <div class="body">
    <div class="comp"><div class="l"><span><img src="assets/vec/bundesliga.svg" alt=""></span>Bundesliga</div><span class="pill">Following</span></div>
    <div class="meta"><h1>FC Bayern München - Borussia Dortmund</h1><p>Follow Bundesliga live on DAZN.</p></div>
    <div class="acts"><span class="pill"><img src="assets/icons/like-outline.svg" alt="">2.1K</span><span class="pill"><img src="assets/icons/comment.svg" alt="">3.4K</span><span class="pill"><img src="assets/icons/share.svg" alt="">Share</span><span class="pill" style="width:48px;justify-content:center;padding:0"><img src="assets/icons/reminder.svg" alt=""></span></div>
    <div class="pc" id="pfCard"><div class="pq-eb"><div><small>Bundesliga · Matchday 5 · Prediction</small><b>Who will win?</b></div><span class="pq-lbl" id="pfLbl">Open</span></div>
      <div class="pq-opts" id="pfOpts"><button type="button" class="pq-opt" data-k="0"><img src="assets/vec/bayern.svg" alt=""><span>Bayern</span><span class="pct">58%</span></button><button type="button" class="pq-opt draw" data-k="1" aria-label="Draw">''' + X.replace('width="20" height="20"', 'width="16" height="16"') + '''<span class="pct">14%</span></button><button type="button" class="pq-opt" data-k="2"><img src="assets/poll/logo-bvb.png" alt=""><span>Dortmund</span><span class="pct">28%</span></button></div>
      <div class="ft">''' + FANS + '''</div></div>
    <div class="tabs"><span class="on">Related</span><span>Stats</span><span>Lineups</span><span>Live updates</span><span>Formations</span></div>
    <div class="rail"><h2>Live and Coming Up</h2><div class="tiles">
      <div class="tl"><div class="cr"><i style="background:#DC052D"><img src="assets/vec/bayern.svg" alt=""></i><i style="background:#FDE100"><img src="assets/poll/logo-bvb.png" alt=""></i><em>14 SEP</em></div><b>FC Bayern München vs Borussia Dortmund</b><small>Bundesliga</small></div>
      <div class="tl"><div class="cr"><i style="background:#1D9053"><img src="assets/scores/hamburg.png" alt=""></i><i style="background:#1A171B"><img src="assets/scores/hoffenheim.png" alt=""></i><em>14 SEP</em></div><b>Hamburg vs Hoffenheim</b><small>Bundesliga</small></div>
    </div></div>
  </div>
  <div class="home-ind"></div>
</div>
''')
s = s.replace('<script>\n(function () {\n  var v = new URLSearchParams', FIX + '<script>\n(function () {\n  var v = new URLSearchParams', 1)
# the scores screen also serves ?v=predict
s = s.replace('  <div class="nav"><div><img src="assets/icons/nav-home.svg"', '  ' + SHEET + '\n  <div class="nav"><div><img src="assets/icons/nav-home.svg"', 1)
JS = r'''
<script>
(function () {
  var v = new URLSearchParams(location.search).get("v");
  var $ = function (id) { return document.getElementById(id); };
  var FANS = ''' + repr(FANS) + r''';
  if (v === "predict") {
    var el = $("scores"); el.hidden = false;
    var v1 = el.querySelector("video"); if (v1) v1.pause();
    // the live match gets a prediction instead of the FanZone strip
    var st = el.querySelector(".card .strip");
    var pr = document.createElement("div"); pr.className = "pred rb"; pr.setAttribute("role", "button"); pr.innerHTML = "Who will score first?<span>Predict</span>";
    st.parentNode.replaceChild(pr, st);
    var scrim = $("pqScrim"), sheet = $("pqSheet"), body = $("pqBody");
    function eb(lbl, out) { return '<div class="pq-eb"><div><small>Bundesliga · Matchday 5 · Prediction</small><b>Who will score first?</b></div><span class="pq-lbl' + (out ? ' out' : '') + '">' + lbl + '</span></div>'; }
    var T = [["Bayern", "assets/vec/bayern.svg"], ["Dortmund", "assets/poll/logo-bvb.png"]];
    function open() {
      sheet.className = "pq-sheet";
      body.innerHTML = eb("Open") + '<div class="pq-opts"><button type="button" class="pq-opt" data-k="0"><img src="' + T[0][1] + '" alt="">Bayern</button><button type="button" class="pq-opt draw" data-k="x" aria-label="No goal"><svg width="16" height="16" viewBox="0 0 20 20" fill="none" aria-hidden="true"><path d="M15.5 5.5L14.5 4.5L10 9L5.5 4.5L4.5 5.5L9 10L4.5 14.5L5.5 15.5L10 11L14.5 15.5L15.5 14.5L11 10L15.5 5.5Z" fill="#F9FAFA"/></svg></button><button type="button" class="pq-opt" data-k="1"><img src="' + T[1][1] + '" alt="">Dortmund</button></div>' + FANS;
      scrim.hidden = false; sheet.style.animation = "none"; void sheet.offsetWidth; sheet.style.animation = "";
      [].forEach.call(body.querySelectorAll(".pq-opt"), function (b) { b.addEventListener("click", function () { pick(b.dataset.k); }); });
    }
    function pick(k) {
      var t = k === "x" ? ["No goal", null] : T[+k];
      sheet.className = "pq-sheet" + (k === "0" ? " red" : "");
      body.innerHTML = eb("Predicted", true) + '<div class="pq-opts"><div class="pq-opt" style="cursor:default">' + (t[1] ? '<img src="' + t[1] + '" alt="">' : '') + t[0] + '</div></div><button type="button" class="pq-cta">View all Match-day 5 predictions<svg width="24" height="24" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M9.7 17.3L8.3 15.9L12.2 12L8.3 8.1L9.7 6.7L15 12L9.7 17.3Z" fill="#080E12"/></svg></button>' + FANS;
      pr.innerHTML = "Who will score first?<span>Predicted</span>";
    }
    pr.addEventListener("click", open);
    $("pqX").addEventListener("click", function () { scrim.hidden = true; });
    scrim.addEventListener("click", function (e) { if (e.target === scrim) scrim.hidden = true; });
    window.addEventListener("message", function (e) { if (e.data && e.data.fz === "shown") { scrim.hidden = true; pr.innerHTML = "Who will score first?<span>Predict</span>"; } });
  }
  if (v === "predictfix") {
    var card = $("pfCard");
    [].forEach.call(card.querySelectorAll(".pq-opt"), function (b) { b.addEventListener("click", function () {
      if (card.classList.contains("done")) return;
      card.classList.add("done"); b.classList.add("mine"); var l = $("pfLbl"); l.textContent = "Predicted"; l.classList.add("out");
    }); });
    window.addEventListener("message", function (e) { if (e.data && e.data.fz === "shown") { card.classList.remove("done"); [].forEach.call(card.querySelectorAll(".mine"), function (m) { m.classList.remove("mine"); }); var l = $("pfLbl"); l.textContent = "Open"; l.classList.remove("out"); } });
  }
})();
</script>
'''
s = s.replace('</body></html>', JS + '</body></html>', 1)
open(p, 'w').write(s); print("predict-screens ok")
# (applied after the first run) ?v=predict shows the scores screen
s = open(p).read()
a = '  var el = document.getElementById(v) || document.getElementById("browser");'
if a in s:
    open(p, 'w').write(s.replace(a, '  var el = document.getElementById(v === "predict" ? "scores" : v) || document.getElementById("browser");'))
