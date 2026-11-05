# FanZone Prototype

Interactive prototype of the FanZone side panel over a live match stream (mobile landscape, 1288×596, scaled to fit the window).

## Run it

Open `index.html` in a browser, or serve the folder:

```bash
npx serve .
# or
python3 -m http.server 8000
```

## What it does

- **Background video** loops muted, always playing.
- **Launcher button** (bottom-right of the video) starts as a chat bubble, then after 6s animates into the poll icon (spin, pop, yellow ring, red dot).
- **Clicking the launcher** shrinks the video and slides in the FanZone panel; the launcher hides until the panel is closed with ✕.
- **Live chat** adds a message every 2.4s from a scripted Bayern vs Dortmund conversation, looping forever.
- **Poll**: tap a team to vote (one vote). Percentages then update live as simulated fans vote; "fans voted" counter updates too. The chevron collapses/expands the poll.

## Structure

```
index.html   markup for the stage, video, launcher, panel, poll, composer
styles.css   design tokens (:root), layout, animations
app.js       behaviour + content (CONFIG timings, chat script, poll options)
assets/
  fonts/     DAZN Oscine (Light, Regular, Bold — Latin subset, woff2)
  video/     match-bg.mp4 (compressed, no audio)
  img/       sponsor, club crests, chat avatars, reactions
```

Timings, chat lines and poll options live at the top of `app.js`.

## Notes

- `assets/img/reactions/reaction-3.png` came from an incomplete export (no face) — replace with the final asset.
- The DAZN Oscine fonts were subset to Latin characters; Japanese glyphs are not included.
- Club crests, sponsor and broadcaster logos are third-party marks supplied for this prototype.
