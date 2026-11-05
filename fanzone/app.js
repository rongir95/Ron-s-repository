/* FanZone prototype — vanilla JS, no dependencies. */
(() => {
  // ---------- Config ----------
  const CONFIG = {
    launcherSwapDelayMs: 6000, // chat bubble → poll icon
    chatIntervalMs: 2400,      // new chat message
    voteIntervalMs: 900,       // simulated votes after the user votes
    maxChatNodes: 14
  };

  const AVATARS = {
    vulture: 'assets/img/avatars/vulture.png',
    tiger: 'assets/img/avatars/tiger.png',
    b: 'assets/img/avatars/b.png',
    host: 'assets/img/avatars/host-dazn.png'
  };
  const USERS = {
    J: { name: 'Jordan', avatar: AVATARS.vulture },
    Y: { name: 'Yu', avatar: AVATARS.tiger },
    N: { name: 'Ben', avatar: AVATARS.b },
    M: { name: 'Misaki', avatar: AVATARS.host, isHost: true }
  };

  const CHAT_SCRIPT = [
    ['M', 'Welcome to Der Klassiker! Bayern vs Dortmund, the biggest game in German football. Drop your predictions in the poll!'],
    ['J', 'LETS GOOO'],
    ['Y', 'Dortmund pressing so high early on, they are not letting Bayern breathe at all. Love this approach'],
    ['N', 'Too many turnovers'],
    ['J', 'WHAT A SAVE!'],
    ['Y', 'That has to be a yellow, he went straight through the back of him and the ref just waves play on?? Unbelievable'],
    ['N', 'Woodwork again?! Nobody can buy a goal tonight.'],
    ['J', 'unreal'],
    ['M', 'Close call there! Who do you think breaks the deadlock first?'],
    ['Y', 'Bayern have had 70% of the ball and honestly nothing to show for it, Dortmund just sitting deep and waiting for the counter'],
    ['N', 'BVB on the counter is terrifying'],
    ['J', 'PENALTY!!'],
    ['Y', 'VAR checking...'],
    ['N', 'Has to score this. Has to.'],
    ['J', 'MISSED?! Over the bar! I genuinely cannot believe what I just watched, that was the easiest chance of the night'],
    ['Y', 'haha chaos'],
    ['M', 'A penalty miss in Der Klassiker! The chat is on fire tonight'],
    ['N', 'Yellow Wall breathing again'],
    ['J', 'The goal is coming'],
    ['Y', 'Their midfield is running the show right now, every second ball is theirs and the full backs keep getting forward'],
    ['N', 'Time for a sub'],
    ['J', 'GOOOAL!!!'],
    ['Y', 'Top corner. Keeper had zero chance'],
    ['N', 'Dortmund have to respond now, 20 minutes left and they need to start taking some risks going forward'],
    ['J', 'This fixture never disappoints'],
    ['Y', 'POST AGAIN'],
    ['M', 'Three times off the woodwork tonight! Is this the unluckiest Klassiker ever?'],
    ['N', '+5'],
    ['J', 'Hold on Bayern, just hold on, a few more minutes and we take all three points home'],
    ['Y', 'everyone forward now'],
    ['N', 'What a game. Instant classic.']
  ];

  const POLL_OPTIONS = [
    { id: 'fcb', name: 'FC Bayern München', logo: 'assets/img/crests/fcb.png', ring: 'rgba(220,5,45,0.28)', votes: 4600, weight: 0.40 },
    { id: 'bvb', name: 'Borussia Dortmund', logo: 'assets/img/crests/bvb.png', ring: 'rgba(253,225,0,0.22)', votes: 3100, weight: 0.38 },
    { id: 'b04', name: 'Bayer 04 Leverkusen', logo: 'assets/img/crests/b04.png', ring: 'rgba(255,255,255,0.12)', votes: 2300, weight: 0.22 }
  ];

  // ---------- Elements ----------
  const $ = (id) => document.getElementById(id);
  const stage = $('stage');
  const panel = $('panel');
  const launcher = $('launcher');
  const iconChat = $('iconChat');
  const iconPoll = $('iconPoll');
  const launcherDot = $('launcherDot');
  const chat = $('chat');
  const card = $('pollCard');
  const optionsEl = $('options');
  const votesLabel = $('votesLabel');

  // ---------- Scale the 1288×596 stage to fit the window ----------
  function fit() {
    const s = Math.min(window.innerWidth / 1288, window.innerHeight / 596);
    stage.style.transform = `scale(${s})`;
  }
  window.addEventListener('resize', fit);
  fit();

  // ---------- Video: make sure it autoplays muted ----------
  const video = stage.querySelector('video');
  video.muted = true;
  video.play().catch(() => {});

  // ---------- Panel open / close ----------
  let seen = false;
  function setOpen(open) {
    stage.classList.toggle('is-open', open);
    panel.setAttribute('aria-hidden', String(!open));
    if (open) { seen = true; launcherDot.hidden = true; }
  }
  launcher.addEventListener('click', () => setOpen(true));
  $('closeBtn').addEventListener('click', () => setOpen(false));

  // ---------- Launcher: chat bubble → poll icon ----------
  setTimeout(() => {
    iconChat.classList.replace('in', 'out-left');
    iconPoll.classList.replace('out-right', 'in');
    launcher.classList.add('is-alert');
    launcher.setAttribute('aria-label', 'Open FanZone — new poll');
    if (!seen) launcherDot.hidden = false;
  }, CONFIG.launcherSwapDelayMs);

  // ---------- Live chat ----------
  function addMessage([userKey, text]) {
    const u = USERS[userKey];
    const msg = document.createElement('div');
    msg.className = 'msg';
    msg.innerHTML = `
      <img src="${u.avatar}" alt="">
      <div class="msg-body">
        <div class="msg-name"><span></span>${u.isHost ? '<span class="host-badge">HOST</span>' : ''}</div>
        <p class="msg-text"></p>
      </div>`;
    msg.querySelector('.msg-name span').textContent = u.name;
    msg.querySelector('.msg-text').textContent = text;
    chat.appendChild(msg);
    while (chat.children.length > CONFIG.maxChatNodes) chat.firstElementChild.remove();
  }
  let cursor = 0;
  for (; cursor < 4; cursor++) addMessage(CHAT_SCRIPT[cursor]);
  setInterval(() => {
    addMessage(CHAT_SCRIPT[cursor % CHAT_SCRIPT.length]);
    cursor++;
  }, CONFIG.chatIntervalMs);

  // ---------- Poll ----------
  let myVote = null;
  const optionNodes = POLL_OPTIONS.map((o) => {
    const btn = document.createElement('button');
    btn.className = 'option';
    btn.innerHTML = `
      <span class="option-fill"></span>
      <span class="option-crest" style="background:${o.ring}"><img src="${o.logo}" alt=""></span>
      <span class="option-name"></span>
      <span class="option-pct">0%</span>`;
    btn.querySelector('.option-name').textContent = o.name;
    btn.addEventListener('click', () => vote(o.id));
    optionsEl.appendChild(btn);
    return { o, btn, fill: btn.querySelector('.option-fill'), pct: btn.querySelector('.option-pct') };
  });

  function percentages() {
    const total = POLL_OPTIONS.reduce((t, o) => t + o.votes, 0) || 1;
    const pcts = POLL_OPTIONS.map((o) => Math.round((o.votes / total) * 100));
    const drift = 100 - pcts.reduce((a, b) => a + b, 0);
    pcts[pcts.indexOf(Math.max(...pcts))] += drift; // always sum to 100
    return { total, pcts };
  }

  function renderPoll() {
    const { total, pcts } = percentages();
    optionNodes.forEach(({ o, btn, fill, pct }, i) => {
      btn.classList.toggle('is-selected', myVote === o.id);
      fill.style.width = myVote ? pcts[i] + '%' : '0';
      pct.textContent = pcts[i] + '%';
    });
    optionsEl.classList.toggle('has-voted', !!myVote);
    votesLabel.textContent = (total / 1000).toFixed(1) + 'K';
  }

  function vote(id) {
    if (myVote) return; // one vote per user
    myVote = id;
    POLL_OPTIONS.find((o) => o.id === id).votes += 1;
    renderPoll();
  }

  // Simulate other fans voting once the user has voted
  setInterval(() => {
    if (!myVote) return;
    const n = 20 + Math.floor(Math.random() * 60);
    for (let i = 0; i < n; i++) {
      let r = Math.random();
      const pick = POLL_OPTIONS.find((o) => (r -= o.weight) < 0) || POLL_OPTIONS[POLL_OPTIONS.length - 1];
      pick.votes += 1;
    }
    renderPoll();
  }, CONFIG.voteIntervalMs);

  // Collapse / expand
  $('collapseBtn').addEventListener('click', (e) => {
    const collapsed = card.classList.toggle('is-collapsed');
    e.currentTarget.setAttribute('aria-expanded', String(!collapsed));
    e.currentTarget.setAttribute('aria-label', collapsed ? 'Expand' : 'Collapse');
  });

  renderPoll();
})();
