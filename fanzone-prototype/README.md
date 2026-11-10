# FanZone prototype (combined)

One clickable prototype of the FanZone product, built by merging two earlier prototypes:

| Source prototype | What it contributed |
| --- | --- |
| **Personal Fan Card – Phase 2** (Claude Design) | The app shell: Home, match page (Bayern–BVB), FanZone live chat, Profile & Settings, Fan Card (designs A / B / C), other fans' cards, favorite / following / avatar drawers |
| **Replies – Mobile** (Claude Design) | The Comments & Replies experience: threads, replying with @mentions, reaction picker, delete / report, toasts, keyboard, No Internet state |

The Fan Card prototype had its own static comment list on the match page. The Comments & Replies
experience replaced it. Fans who already appeared in the Fan Card comments (Futcrunch, Mariana,
Sandra45, MisterFotball12) keep their Fan Cards: tapping their avatar or name opens their card.
Tapping your own avatar opens My Card.

## Files

- `index.html`: the shell testers open. It shows the device, a settings panel (start screen,
  new or existing fan, My Card design A/B/C, Following section on/off, restart) and a list of
  things to try. On a phone the device fills the screen and settings open from the top bar.
- `FanZone.dc.html`: the merged app (Claude Design `.dc.html` format, rendered by `support.js`).
  You can also open it directly. It reads its settings from the URL:
  `?start=fanzone&profile=full&card=B&following=0&reset=1`.
- `assets/`, `uploads/`: images, video and DAZN Oscine fonts used by the app.
- `tools/merge-prototypes.py`: the script that produced `FanZone.dc.html` from the two source pages.

## Run locally

```bash
cd fanzone-prototype
python3 -m http.server 8000
```

Then open http://localhost:8000. The app loads React from unpkg.com, so it needs internet access.
