# FanZone prototype (combined)

One clickable prototype of the FanZone product, built by merging two earlier prototypes:

| Source prototype | What it contributed |
| --- | --- |
| **Personal Fan Card – Phase 2** (Claude Design) | The app shell: Home, match page (Bayern–BVB), FanZone live chat, Profile & Settings, Fan Card (designs A / B / C), other fans' cards, favorite / following / avatar drawers |
| **Replies – Mobile** (Claude Design) | The Comments & Replies experience: threads, replying with @mentions, reaction picker, delete / report, toasts, keyboard, No Internet state |

From a third prototype, **FanZone Prototype** (landscape player + FanZone, Design canvas), only the
**Poll** was taken. In the portrait FanZone screen it slides down from under the FanZone header, over
the top of the chat, when a tester presses
**Start poll** in the shell (side panel on desktop, top bar on phones). The button works only while
FanZone is open. Fans vote, see live results, and can collapse the poll. It closes when its timer runs out.

**FanZone entry** (from a screen recording of the product): Home > Watch now opens the match page,
and FanZone opens by itself over it, under the video, after a short loading spinner. X closes FanZone
and leaves a FanZone card ("Join chat") on the match page; tapping it opens FanZone again. The arrow
next to the FanZone title collapses the panel to its header bar and expands it again. The Message
field works: type, press Enter or the send button, and the message joins the chat as you.

**Tooltips**: "Let's make a unique fan profile" (Home) and "Meet your Fan Card" (FanZone) are off by
default; each has an On / Off switch in the shell's Settings tab.

The Fan Card prototype had its own static comment list on the match page. The Comments & Replies
experience replaced it. Fans who already appeared in the Fan Card comments (Futcrunch, Mariana,
Sandra45, MisterFotball12) keep their Fan Cards: tapping their avatar or name opens their card.
Tapping your own avatar opens My Card.

## Files

- `index.html`: the shell testers open. It shows the device with an always-visible Restart button beside it, the
  Start poll button, and two tabs: Settings (start screen, new or existing fan, My Card design A/B/C,
  Following section, tooltips) and Things to try. On a phone the device fills the screen; Restart and
  Start poll sit in the top bar and the tabs open from Settings & tips.
- `FanZone.dc.html`: the merged app (Claude Design `.dc.html` format, rendered by `support.js`).
  You can also open it directly. It reads its settings from the URL:
  `?start=fanzone&profile=full&card=B&following=0&reset=1`.
- `assets/`, `uploads/`: images, video and DAZN Oscine fonts used by the app.
- `tools/merge-prototypes.py`: the script that produced `FanZone.dc.html` from the two source pages.
- `tools/add-poll.py`: adds the live poll to `FanZone.dc.html` (run after the merge script).
- `tools/fanzone-entry.py`: the FanZone entry flow above.
- `tools/fanzone-panel.py`: collapse / expand for the FanZone panel, FanZone messages and the tooltip switches.
- `tools/chat-bayern-bvb.py`: rewrites the FanZone chat for Bayern vs Dortmund.
- `tools/fanzone-figma.py`: aligns the FanZone drawer with the Figma screen (node 496:103459): message rows, my avatar ring, and the sponsored (Coca-Cola) header, which the shell's "FanZone header: Sponsored" switch turns on; the regular header is the default.
- `tools/chat-avatars.py`: one avatar style for every fan in the chat, per FanZone DS `.UserIndicator`: 24px ring, 18px picture or the nickname's initial (run last).

To rebuild `FanZone.dc.html`, run the seven scripts in the order above on the two source pages.

## Run locally

```bash
cd fanzone-prototype
python3 -m http.server 8000
```

Then open http://localhost:8000. The app loads React from unpkg.com, so it needs internet access.
