"""Landscape Current screens (Figma FanZone 80-20): Poll 56:212822, Fan battle 56:212675, Pinned image 56:212838, Share moment 56:212901."""
import sys, re
p = sys.argv[1]; s = open(p).read()
SHARE = re.search(r'<svg class="btn-icon".*?</svg>', s).group(0).replace('class="btn-icon"', 'class="lc-ic16"')
X = '<svg width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="M13.3333 3.79566L12.2046 2.66699L7.99996 6.87961L3.79529 2.66699L2.66663 3.79566L6.87924 8.00033L2.66663 12.205L3.79529 13.3337L7.99996 9.12104L12.2046 13.3337L13.3333 12.205L9.12068 8.00033L13.3333 3.79566Z" fill-rule="evenodd" clip-rule="evenodd" fill="#F9FAFA"/></svg>'
POLLIC = '<svg width="32" height="32" viewBox="0 0 32 32" fill="none" aria-hidden="true"><rect width="32" height="32" rx="12.8" fill="#FFFA00"/><path d="M20.5714 6.66634C20.5714 5.92996 20.0598 5.33301 19.4286 5.33301H8.57143C8.25584 5.33301 8 5.63148 8 5.99967V9.99967C8 10.3679 8.25584 10.6663 8.57143 10.6663H19.4286C20.0598 10.6663 20.5714 10.0694 20.5714 9.33301V6.66634Z" fill="#0C161C"/><path d="M24 14.6663C24 13.93 23.4883 13.333 22.8571 13.333H8.57143C8.25584 13.333 8 13.6315 8 13.9997V17.9997C8 18.3679 8.25584 18.6663 8.57143 18.6663H22.8571C23.4883 18.6663 24 18.0694 24 17.333V14.6663Z" fill="#0C161C"/><path d="M14.8571 22.6663C14.8571 21.93 14.3455 21.333 13.7143 21.333H8.57143C8.25584 21.333 8 21.6315 8 21.9997V25.9997C8 26.3679 8.25584 26.6663 8.57143 26.6663H13.7143C14.3455 26.6663 14.8571 26.0694 14.8571 25.333V22.6663Z" fill="#0C161C"/></svg>'
SHAREIC = '<svg width="32" height="32" viewBox="0 0 32 32" fill="none" aria-hidden="true"><rect width="32" height="32" rx="12.8" fill="#FFFA00"/><path d="M26.4078 11.372L18.5922 5.46509C18.1646 5.14204 17.5536 5.44833 17.5536 5.98593V8.40514C17.5536 8.55021 17.4491 8.67425 17.3067 8.69772C10.4715 9.82961 5.33325 14.6799 5.33325 20.4917C5.33325 22.7004 6.07535 24.77 7.37059 26.5495C7.55558 26.8037 7.94933 26.6071 7.86156 26.3039C7.68175 25.6822 7.58727 25.037 7.58727 24.3753C7.58727 20.0127 11.7003 16.3616 17.2107 15.433C17.3902 15.4028 17.5536 15.543 17.5536 15.7259V17.7989C17.5536 18.3362 18.1646 18.6427 18.5922 18.3197L26.4078 12.4128C26.7528 12.1522 26.7528 11.632 26.4078 11.3714V11.372Z" fill="#0C161C"/></svg>'
SWITCH = '<svg width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="M10.9167 11.7119C13.1717 11.7118 14.9996 10.05 14.9998 8C14.9998 5.97541 13.217 4.33077 11.0007 4.29004V3.24121C11.0007 3.03743 10.7027 2.92518 10.5056 3.05469L8.11011 4.63184C7.96366 4.72829 7.9636 4.90749 8.11011 5.00391L10.5056 6.58008C10.7026 6.70961 11.0006 6.59824 11.0007 6.39453V5.35254C12.5726 5.39305 13.8337 6.56121 13.8337 8C13.8336 9.46424 12.5274 10.6513 10.9167 10.6514H9.58374C9.26158 10.6514 8.99976 10.8888 8.99976 11.1816C8.99978 11.4745 9.26159 11.7119 9.58374 11.7119H10.9167ZM4.99976 12.7588C4.99976 12.9626 5.29779 13.0749 5.49487 12.9453L7.89038 11.3682C8.03674 11.2717 8.03679 11.0925 7.89038 10.9961L5.49487 9.41992C5.29783 9.29024 4.99987 9.4017 4.99976 9.60547V10.6475C3.42755 10.6073 2.16675 9.43901 2.16675 8C2.16687 6.53582 3.47221 5.34882 5.08276 5.34863H6.49976C6.82187 5.34858 7.08276 5.1112 7.08276 4.81836C7.08275 4.52553 6.82186 4.28814 6.49976 4.28809H5.08276C2.82788 4.28828 0.999881 5.95006 0.999756 8C0.99976 10.0248 2.78313 11.6696 4.99976 11.71V12.7588Z" fill="#F9FAFA"/></svg>'

CSS = '''
/* Landscape Current screens */
.lc { position: absolute; font-family: "DAZN Oscine", system-ui, sans-serif; -webkit-font-smoothing: antialiased; color: #f9fafa; }
.lc[hidden] { display: none; }
.lc-x { all: unset; position: absolute; width: 24px; height: 24px; box-sizing: border-box; border-radius: 9999px; background: rgba(8,14,18,.64); border: 1px solid rgba(249,250,250,.2); display: flex; align-items: center; justify-content: center; cursor: pointer; }
.lc-ic16 { width: 16px; height: 16px; display: block; flex: none; }
.lc-in { animation: lcIn .45s cubic-bezier(.2,.8,.2,1) both; transform-origin: 100% 100%; }
@keyframes lcIn { from { opacity: 0; transform: translateY(12px) scale(.96); } to { opacity: 1; transform: none; } }
/* poll */
.lp { right: 98px; bottom: 28px; width: 204px; display: flex; flex-direction: column; gap: 8px; }
.lp .lc-x { right: 0; top: -32px; }
.lp-q { position: relative; overflow: hidden; display: flex; align-items: center; gap: 8px; padding: 8px; border-radius: 12px; background: rgba(0,0,0,.8); backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); border: 1px solid rgba(249,250,250,.1); }
.lp-bar { position: absolute; left: 0; top: 0; bottom: 0; width: 100%; background: rgba(247,255,26,.5); border-right: 2px solid #f7ff1a; transform-origin: 0 50%; }
.lp-q svg, .lp-q p { position: relative; }
.lp-q svg { flex: none; display: block; }
.lp-q p { margin: 0; font-weight: 700; font-size: 14px; line-height: 16px; width: 148px; }
.lp-a { display: grid; grid-template-columns: 1fr 1fr; gap: 8px 12px; }
.lp-a button { all: unset; position: relative; overflow: hidden; height: 56px; box-sizing: border-box; border-radius: 8px; background: rgba(0,0,0,.8); box-shadow: 0 4px 8px rgba(0,0,0,.25), 0 2px 0 rgba(247,255,26,.5); display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 4px; padding: 0 4px; text-align: center; cursor: pointer; font-weight: 700; font-size: 15px; line-height: 1; transition: box-shadow .2s ease; }
.lp-a button .f { position: absolute; left: 0; top: 0; bottom: 0; width: 0; background: rgba(249,250,250,.12); transition: width .7s ease; }
.lp-a button span { position: relative; }
.lp-a button .pc { font-size: 12px; color: #c5c7ca; display: none; }
.lp.voted .lp-a button .pc { display: block; }
.lp.voted .lp-a button { cursor: default; }
.lp-a button.mine { box-shadow: inset 0 0 0 2px #FFFA00, 0 4px 8px rgba(0,0,0,.25); }
.lp-a button.mine .f { background: rgba(255,250,0,.25); }
/* fan battle */
.lb { right: 100px; bottom: 28px; width: 204px; }
.lb .lc-x { left: 180px; top: -32px; }
.lb-coins { position: absolute; left: 0; top: -24px; height: 16px; padding: 0 4px; border-radius: 8px; background: rgba(0,0,0,.6); backdrop-filter: blur(40px); -webkit-backdrop-filter: blur(40px); display: flex; align-items: center; gap: 2px; font-weight: 700; font-size: 12px; line-height: 16px; font-variant-numeric: tabular-nums; }
.lb-coins img, .lb-gift i img { width: 12px; height: 12px; display: block; }
.lb-switch { position: absolute; left: 103px; top: -24px; height: 18px; box-sizing: border-box; padding: 0 8px; border-radius: 16px; background: rgba(8,14,18,.64); border: 1px solid rgba(249,250,250,.2); display: flex; align-items: center; gap: 2px; font-weight: 700; font-size: 12px; cursor: pointer; }
.lb-strip { position: relative; height: 32px; border-radius: 100px; overflow: hidden; background: rgba(0,0,0,.8); border: 1px solid rgba(249,250,250,.1); box-sizing: border-box; }
.lb-team { position: absolute; top: 0; bottom: 0; transition: width .5s ease; }
.lb-team.h { left: 0; background: linear-gradient(90deg, rgba(0,0,0,.5), rgba(0,0,0,0) 59px), #DC052D; }
.lb-team.a { right: 0; background: linear-gradient(270deg, rgba(0,0,0,.5), rgba(0,0,0,0) 55px), #FDE100; }
.lb-logo { position: absolute; top: 3px; width: 24px; height: 24px; box-sizing: border-box; border-radius: 36px; border: 1.125px solid #fff; overflow: hidden; display: flex; align-items: center; justify-content: center; }
.lb-logo img { width: 17px; height: 17px; object-fit: contain; display: block; }
.lb-team.h .lb-logo { left: 6px; background: #DC052D; } .lb-team.a .lb-logo { right: 6px; background: #FDE100; }
.lb-t { position: absolute; left: 50%; top: 50%; transform: translate(-50%,-50%); background: #f9fafa; border: 1px solid rgba(36,32,37,.2); border-radius: 8px; padding: 2px 4px; color: #0c161c; font-weight: 700; font-size: 12px; line-height: 1; font-variant-numeric: tabular-nums; }
.lb-gifts { display: flex; justify-content: space-between; margin-top: 8px; }
.lb-gift { all: unset; width: 60px; height: 60px; border-radius: 12px; background: rgba(0,0,0,.8); box-shadow: 0 3.88px 7.76px rgba(0,0,0,.25), 0 1.94px 0 rgba(247,255,26,.5); display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 2px; cursor: pointer; transition: transform .12s ease; }
.lb-gift:active { transform: scale(.94); }
.lb-gift > img { width: 31px; height: 31px; object-fit: contain; display: block; }
.lb-gift i { font-style: normal; display: flex; align-items: center; gap: 2px; font-weight: 700; font-size: 12px; line-height: 12px; }
.lb-fly { position: absolute; width: 52px; height: 52px; pointer-events: none; }
.lb-fly img { position: absolute; left: 5px; top: 7px; width: 32px; height: 32px; object-fit: contain; }
.lb-fly b { position: absolute; right: 5px; bottom: 7px; background: #f9fafa; border: 1px solid #242d33; border-radius: 16px; padding: 2px 4px; color: #0c161c; font-size: 10px; line-height: 1; letter-spacing: .1px; font-family: "DAZN Oscine", system-ui, sans-serif; }
.lb-big { position: absolute; left: 554px; top: 115px; width: 112px; height: 112px; object-fit: contain; pointer-events: none; }
/* pinned image */
.lpin { right: 98px; bottom: 28px; padding: 8px; border-radius: 12px; background: rgba(0,0,0,.7); backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); border: 1px solid rgba(249,250,250,.1); }
.lpin .lc-x { right: 0; top: -32px; }
.lpin-ad { position: relative; width: 168px; height: 105px; box-sizing: border-box; border-radius: 8px; border: 1px solid #FFFA00; overflow: hidden; background: radial-gradient(90px 70px at 12% 100%, #ff9a2e 0%, rgba(255,154,46,0) 100%), radial-gradient(80px 70px at 100% 90%, #ff6a00 0%, rgba(255,106,0,0) 100%), #ff7f00; cursor: pointer; }
.lpin-ad .je { position: absolute; left: 55px; top: 8px; width: 58px; height: 14px; display: block; }
.lpin-ad .t { position: absolute; left: 34px; top: 29px; width: 99px; margin: 0; text-align: center; font-weight: 700; font-size: 11px; line-height: 1; letter-spacing: .22px; color: #fff; }
.lpin-ad .v { position: absolute; left: 46px; top: 69px; width: 75px; height: 17px; border-radius: 999px; background: #fff; color: #f70; font-weight: 800; font-size: 9px; text-transform: uppercase; display: flex; align-items: center; justify-content: center; letter-spacing: .1px; }
.lpin-ad .k { position: absolute; left: 0; right: 0; top: 89px; text-align: center; font-weight: 700; font-size: 8px; letter-spacing: .16px; color: #fff; }
/* share moment, current */
.lsc { right: 94px; bottom: 26px; width: 209px; display: flex; flex-direction: column; gap: 4px; }
.lsc .lc-x { right: 0; top: -32px; }
.lsc-card { position: relative; height: 161px; box-sizing: border-box; border-radius: 12px; background: rgba(0,0,0,.8); backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); border: 1px solid rgba(249,250,250,.1); }
.lsc-hd { position: absolute; left: 8px; top: 8px; display: flex; gap: 8px; align-items: center; }
.lsc-hd svg { flex: none; display: block; }
.lsc-hd p { margin: 0; width: 153px; font-weight: 700; font-size: 14px; line-height: 16px; }
.lsc-clip { position: absolute; left: 8px; top: 48px; width: 193px; height: 104.7px; box-sizing: border-box; border: 1.03px solid #3d4549; border-radius: 4.1px; overflow: hidden; }
.lsc-clip video { width: 100%; height: 100%; object-fit: cover; display: block; background: #000; }
.lsc-btn { all: unset; position: relative; height: 32px; cursor: pointer; filter: drop-shadow(0 4px 4px rgba(0,0,0,.16)); }
.lsc-btn span { position: absolute; left: 0; right: 0; top: 0; bottom: 3px; box-sizing: border-box; border-radius: 8px; background: rgba(0,0,0,.8); border: 2px solid rgba(255,255,0,.7); display: flex; align-items: center; justify-content: center; gap: 4px; font-weight: 700; font-size: 14px; }
'''
s = s.replace('</style></head>', CSS + '</style></head>', 1)

HTML = '''
  <div class="lc lp" id="lp" hidden>
    <button class="lc-x" type="button" aria-label="Close">''' + X + '''</button>
    <div class="lp-q"><span class="lp-bar" id="lpBar"></span>''' + POLLIC + '''<p dir="auto">Who will win the Champions League this season?</p></div>
    <div class="lp-a" id="lpA"></div>
  </div>
  <div class="lc lb" id="lb" hidden>
    <div class="lb-coins"><img src="assets/landscape/coin.svg" alt=""><span id="lbCoins">34,645</span></div>
    <div class="lb-switch" role="button" aria-label="Switch team">switch''' + SWITCH + '''</div>
    <button class="lc-x" type="button" aria-label="Close">''' + X + '''</button>
    <div class="lb-strip"><div class="lb-team h" id="lbH" style="width:50%"><span class="lb-logo"><img src="assets/poll/logo-fcb.png" alt="Bayern"></span></div><div class="lb-team a" id="lbA" style="width:50%"><span class="lb-logo"><img src="assets/poll/logo-bvb.png" alt="Dortmund"></span></div><span class="lb-t" id="lbT">01:00</span></div>
    <div class="lb-gifts">
      <button class="lb-gift" type="button" data-g="red-finger" data-c="50" aria-label="Send for 50 coins"><img src="assets/gifts/red-finger.png" alt=""><i>50<img src="assets/landscape/coin.svg" alt=""></i></button>
      <button class="lb-gift" type="button" data-g="red-drum" data-c="60" aria-label="Send for 60 coins"><img src="assets/gifts/red-drum.png" alt=""><i>60<img src="assets/landscape/coin.svg" alt=""></i></button>
      <button class="lb-gift" type="button" data-g="red-flag" data-c="120" aria-label="Send for 120 coins"><img src="assets/gifts/red-flag.png" alt=""><i>120<img src="assets/landscape/coin.svg" alt=""></i></button>
    </div>
  </div>
  <div class="lc lpin" id="lpin" hidden>
    <button class="lc-x" type="button" aria-label="Close">''' + X + '''</button>
    <div class="lpin-ad" role="img" aria-label="Just Eat: Vote on next poll and get a chance to win a £10 gift card"><img class="je" src="assets/landscape/justeat.svg" alt="Just Eat"><p class="t">Vote on next poll and get a chance to win a £10 gift card</p><span class="v">Vote now</span><span class="k">&amp; Keep watching</span></div>
  </div>
  <div class="lc lsc" id="lsc" hidden>
    <button class="lc-x" type="button" aria-label="Close">''' + X + '''</button>
    <div class="lsc-card"><div class="lsc-hd">''' + SHAREIC + '''<p dir="auto">Harry Kane’s goal | 28’</p></div><div class="lsc-clip"><video id="lscVid" src="assets/landscape/match-lite.mp4#t=12" muted loop playsinline preload="auto" aria-hidden="true"></video></div></div>
    <button class="lsc-btn" type="button" aria-label="Share"><span>Share''' + SHARE + '''</span></button>
  </div>
'''
a = '  <div class="share-moment" id="sm" hidden>'
assert s.count(a) == 1
s = s.replace(a, HTML + a)

JS = r'''
<script>
(function () {
  var v = new URLSearchParams(location.search).get("v") || "current";
  var map = { poll: "lp", battle: "lb", pin: "lpin", sharecur: "lsc" };
  if (!map[v]) return;
  var $ = function (id) { return document.getElementById(id); };
  var box = $(map[v]), again = 0;
  function show() { box.hidden = false; box.classList.remove("lc-in"); void box.offsetWidth; box.classList.add("lc-in"); if (v === "poll") pollStart(); if (v === "battle") battleStart(); if (v === "sharecur") { var mv = $("lscVid"); try { mv.currentTime = 12; mv.play(); } catch (e) {} } }
  // the X closes it; it comes back a few seconds later so the page keeps showing the feature
  box.querySelector(".lc-x").addEventListener("click", function () { box.hidden = true; clearTimeout(again); again = setTimeout(show, 3000); });
  // poll: the same question and answers as the portrait poll
  var O = [["Arsenal", 41], ["Real Madrid", 17], ["Bayern Munich", 21], ["Barcelona", 21]], pT = 0;
  function pollStart() {
    var a = $("lpA"); box.classList.remove("voted"); a.innerHTML = "";
    O.forEach(function (o, i) {
      var b = document.createElement("button"); b.type = "button";
      b.innerHTML = '<span class="f"></span><span class="n"></span><span class="pc"></span>';
      b.querySelector(".n").textContent = o[0];
      b.addEventListener("click", function () {
        if (box.classList.contains("voted")) return;
        var p = O.map(function (x) { return x[1]; }); var j = p.indexOf(Math.max.apply(null, p.filter(function (_, k) { return k !== i; }))); var amt = Math.min(6, p[j] - 5); p[i] += amt; p[j] -= amt;
        box.classList.add("voted"); b.classList.add("mine");
        [].forEach.call(a.children, function (c, k) { c.querySelector(".pc").textContent = p[k] + "%"; c.querySelector(".f").style.width = p[k] + "%"; });
      });
      a.appendChild(b);
    });
    var bar = $("lpBar"); bar.getAnimations().forEach(function (x) { x.cancel(); });
    bar.animate([{ transform: "scaleX(1)" }, { transform: "scaleX(0)" }], { duration: 30000, easing: "linear", fill: "forwards" });
  }
  // fan battle: send gifts for Bayern; fans of both teams send theirs up the right side
  var coins = 34645, secs = 60, tick = 0, amb = 0, share = 50;
  function fmt(n) { return n.toLocaleString("en-US"); }
  function fly(src, n, x, y, dim) {
    var f = document.createElement("div"); f.className = "lb-fly"; f.style.left = x + "px"; f.style.top = y + "px";
    f.innerHTML = '<img alt=""><b></b>'; f.querySelector("img").src = src; f.querySelector("b").textContent = "+" + n;
    document.querySelector(".stage").appendChild(f);
    var o = dim ? .55 : 1;
    f.animate([{ opacity: 0, transform: "translateY(30px) scale(.6)" }, { opacity: o, transform: "translateY(0) scale(1)", offset: .15 }, { opacity: o, transform: "translate(" + (Math.random() * 14 - 7) + "px,-120px)", offset: .8 }, { opacity: 0, transform: "translate(" + (Math.random() * 14 - 7) + "px,-160px)" }], { duration: 2600, easing: "ease-out" }).onfinish = function () { f.remove(); };
  }
  function push(d) { share = Math.max(22, Math.min(78, share + d)); $("lbH").style.width = share + "%"; $("lbA").style.width = (100 - share) + "%"; }
  function battleStart() {
    clearInterval(tick); clearInterval(amb); secs = 60; coins = 34645; share = 50; push(0); $("lbCoins").textContent = fmt(coins); $("lbT").textContent = "01:00";
    tick = setInterval(function () { secs = secs > 0 ? secs - 1 : 60; $("lbT").textContent = "00:" + String(secs).padStart(2, "0").replace("00:60", "01:00"); if (secs === 60) $("lbT").textContent = "01:00"; }, 1000);
    var G = ["red-finger", "red-drum", "red-flag", "red-fireworks", "yellow-horn", "yellow-drum", "yellow-fireworks", "yellow-flag"];
    amb = setInterval(function () { var g = G[Math.floor(Math.random() * G.length)]; fly("assets/gifts/" + g + ".png", [20, 120, 432, 832, 999][Math.floor(Math.random() * 5)], 655 + Math.random() * 18, 190, true); push(g.indexOf("red") === 0 ? 1 : -1); }, 900);
  }
  [].forEach.call(document.querySelectorAll(".lb-gift"), function (b) {
    b.addEventListener("click", function () {
      var c = +b.dataset.c; if (coins < c) return; coins -= c; $("lbCoins").textContent = fmt(coins);
      var src = "assets/gifts/" + b.dataset.g + ".png";
      fly(src, c, 664, 200, false); push(3);
      var big = document.createElement("img"); big.className = "lb-big"; big.src = src; big.alt = "";
      document.querySelector(".stage").appendChild(big);
      big.animate([{ opacity: 0, transform: "scale(.3) rotate(-12deg)" }, { opacity: 1, transform: "scale(1.08) rotate(4deg)", offset: .35 }, { opacity: 1, transform: "scale(1) rotate(0)", offset: .7 }, { opacity: 0, transform: "scale(.9) translateY(-20px)" }], { duration: 1300, easing: "cubic-bezier(.2,.8,.2,1)" }).onfinish = function () { big.remove(); };
    });
  });
  setTimeout(show, 700);
})();
</script>
'''
s = s.replace('</body></html>', JS + '</body></html>', 1)
open(p, 'w').write(s); print("land-currents ok")
