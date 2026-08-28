# Stock Portfolio Dashboard

> Three brothers, one dashboard, separate portfolios.

A dashboard for tracking stock positions that were bought somewhere else. You
enter a ticker, how many shares you hold and what you paid; it fetches the
current market price and works out value, profit and loss, allocation and
performance. Each person gets their own portfolio, switched from the header, so
whoever manages the money can see whose holdings are whose.

Built with **React + TypeScript + Vite**, no runtime dependencies beyond React,
and persisted in **localStorage** — there is no backend and no account.

---

## Running it

**With live prices** — the way to actually use it:

```bash
cd stock-portfolio-dashboard
npm install
npm run dev          # http://localhost:5173
```

That is the only mode that reaches Yahoo Finance, because the dev server carries
the `/yf` proxy it needs (see *Market data* below). Deploying to Vercel or
Netlify gives the same thing at a shareable URL — both config files are
committed.

**Without installing anything** — `portfolio-dashboard.standalone.html` at the
root of this folder is the whole app inlined into one file. Double-click it and
it opens in any browser, offline. A `file://` page cannot proxy `/yf`, so it
starts on offline demo prices; Settings → *Twelve Data* plus a free API key gives
it real prices, since that provider is callable straight from the browser.
Rebuild it with `npm run build:standalone`.

Other scripts:

```bash
npm run build             # type-check + production build to dist/
npm run build:standalone  # build + inline everything into one HTML file
npm run preview           # serve the production build (proxy included)
npm run typecheck         # type-check only
npm test                  # unit checks for the portfolio maths
```

---

## Market data

### Which source, and why

**Yahoo Finance is the default**, called through a same-origin proxy at `/yf`.
It was the right pick on the three things that actually matter here:

| | Yahoo Finance | Twelve Data | Alpha Vantage | Finnhub |
|---|---|---|---|---|
| API key | none | free key | free key | free key |
| Request limit | none in practice | 8/min, 800/day | **25/day** | 60/min |
| Quotes | live (US) | live (US) | live | live |
| Daily history | yes, same endpoint | yes | yes | paid only |
| Callable from a browser | **no CORS headers** | yes | yes | yes |

Alpha Vantage's 25 requests a day cannot refresh a five-holding portfolio more
than a few times, which rules it out. Finnhub puts historical candles behind its
paid tier, so there would be no performance chart. Yahoo wins on limits and
gives quotes *and* history from one endpoint — its only problem is that its
public endpoints send no CORS headers, so a browser cannot call them directly.

That problem is solved with configuration rather than code: `/yf/*` is proxied
to `https://query1.finance.yahoo.com/*` in three places, so the client fetches
a same-origin URL and needs no key anywhere.

| Where | Mechanism |
|---|---|
| `npm run dev` / `npm run preview` | `server.proxy` / `preview.proxy` in `vite.config.ts` |
| Vercel | `rewrites` in `vercel.json` |
| Netlify | a `status = 200` redirect in `netlify.toml` |

There is no serverless function to maintain, and the same client code runs in
all three.

### Update frequency — what "real-time" actually means here

There is no genuinely real-time free stock API; every free tier is either
snapshot-polled or exchange-delayed. What this dashboard does:

- **Yahoo Finance (default)** — the live consolidated price for US listings,
  typically **under a minute** behind the tape. Some non-US exchanges impose
  their own delay, commonly 15 minutes.
- **Twelve Data** — real-time for US listings on the free plan; other venues may
  be delayed by the exchange.
- **Demo data** — synthetic, generated in the browser. Nothing is fetched.

The app **polls**; it does not stream. Auto-refresh defaults to once a minute
and is configurable in Settings (30s to 15 minutes, or manual only). It pauses
while the browser tab is in the background, and slows to a tenth of the chosen
rate when every market you hold is closed. The header always shows how long ago
prices were fetched and whether the market is open, so a stale number is never
presented as a fresh one. Settings restates the freshness of whichever source is
selected.

### If the proxy is not available

Hosting the built `dist/` on a plain static host (GitHub Pages, S3, a `file://`
page) means there is no `/yf` proxy, and Yahoo will fail. The app detects this,
explains it, and offers a one-click route to Settings, where you can switch to:

- **Twelve Data** — works from anywhere with a free API key, stored only in your
  browser.
- **Demo data** — synthetic prices, for trying the dashboard out offline.

---

## What it shows

**Per holding:** current price, today's change, 30-day sparkline, share count,
share-weighted average cost, amount invested, current value, profit/loss in both
money and percent, and share of the portfolio. Sortable on any numeric column.

**Per portfolio:** total value (the hero figure), total invested, overall
profit/loss in money and percent, today's change, best and worst performer,
allocation by holding, value-versus-invested over time (1M–5Y), return by
holding, and a money-weighted annualised return.

**Across portfolios:** an "All portfolios" panel listing every portfolio's
value, invested, profit/loss and return side by side — the view for whoever
manages more than one — with the same figures in the portfolio switcher.

Beyond the brief, a few things that earn their place in daily use:

- **Today's change**, separately from all-time — the number you actually look at
  when you open the dashboard.
- **Money-weighted annualised return (XIRR)**, solved by bisection. Shown only
  when every purchase has a date, because it is meaningless without them.
- **Concentration** — the largest holding's weight, stated beside the allocation
  chart.
- **Live ticker lookup with a quote preview** while adding, so a mistyped symbol
  is caught before it is saved rather than showing up as a mystery row later.
- **Privacy mode** — blurs money amounts and leaves percentages readable, for
  when someone else is looking at the screen.
- **Backup, CSV export and JSON import** — the data lives in one browser, so
  this is both the safety net and how one brother hands a portfolio to another.
- **Keyboard**: `r` refreshes; `Esc` closes any dialog; the ticker lookup is
  arrow-key navigable.

---

## Design decisions

### Positions are lot-based

A `Position` holds a list of `Lot`s (shares, price, optional date) rather than a
single average price. Buying more of something you already hold appends a lot and
the share-weighted average cost is recomputed — adding `TSLA` twice gives one row
with a correct average, not two rows that each look wrong. It also means the
performance chart can count a purchase only from the date it happened.

Entering a position is still just three fields; the lot editor appears when you
edit one.

### Charts

Charts are hand-rolled SVG and CSS — no chart library, matching the project's
dependency-light approach — and follow a few rules deliberately:

- **The categorical palette is validated, not eyeballed.** Eight hues, checked
  for lightness band, chroma floor, colour-vision-deficiency separation and
  contrast in both light and dark mode. Holdings past the eighth fold into a
  single neutral "Other" segment; the palette is never cycled into a ninth
  generated hue.
- **A hue belongs to a holding, not to its rank.** Each position stores a
  `colorSlot` assigned once, so re-sorting or filtering never repaints the
  survivors. (Importing a file that would give two holdings the same hue is
  repaired on load.)
- **Gain/loss never depends on colour alone.** Green-versus-red sits in the
  marginal band for colour-vision deficiency, and it is too strong a domain
  convention to abandon — so every gain/loss figure also carries an explicit
  `+`/`−` sign and a ▲/▼ arrow, and the diverging bars put gains and losses on
  opposite sides of a zero baseline.
- **One y-axis, ever.** Value and invested share a scale, so the gap between the
  lines is the profit.
- Allocation is a stacked bar plus a ranked, direct-labelled list rather than a
  donut — three of the light-mode hues sit below 3:1 against the surface, so the
  labels and the positions table carry identity, not colour.

### Currency

Each portfolio reports in one base currency. A holding quoted in another
currency is converted at today's rate, fetched from the same provider; both the
price and the cost basis are converted at that one rate, which keeps the
profit/loss *percentage* currency-invariant. It does not model the exchange rate
in force on the purchase date, so a converted holding's profit/loss *amount* is
approximate — the table flags mixed currencies rather than hiding this.

### Honest numbers

- A holding whose price cannot be fetched is **excluded** from the totals and
  called out, rather than silently valued at zero — a wrong total is worse than a
  visibly incomplete one.
- The value-over-time chart is your **current** share counts valued at past
  closing prices, with dated purchases counted from their date. Without a full
  transaction history (including sales), that is the most honest reconstruction
  available, and the card says so.
- The annualised return is withheld, not guessed, when purchase dates are missing.

---

## Project structure

```
src/
  types.ts                  # The data model: Portfolio, Position, Lot, Settings
  main.tsx / App.tsx        # Entry point, top bar, theme, view switch

  lib/
    calc.ts                 # All portfolio maths (pure; unit-tested)
    calc.test.ts            # 24 checks — averaging, P/L, weights, FX, XIRR
    format.ts               # Currency / percent / date formatting
    series.ts               # colour slot -> palette token
    transfer.ts             # JSON backup, CSV export, import
    id.ts

  market/
    types.ts                # The MarketDataProvider contract
    index.ts                # Provider registry
    http.ts                 # fetch with timeout + user-safe error messages
    useMarketData.ts        # Quote/history hooks, refresh cadence, staleness
    providers/
      yahoo.ts              # Default: no key, via the /yf proxy
      twelvedata.ts         # No-proxy fallback, free key, batched quotes
      demo.ts               # Deterministic synthetic prices, fully offline

  store/store.tsx           # Portfolios + settings, localStorage persistence
  data/seed.ts              # First-run sample data

  components/
    ui.tsx                  # Button, Card, Modal, Field, Chip, Value, icons
    PositionForm.tsx        # Add / edit, with ticker lookup and lot editor
    PositionsTable.tsx      # Table (wide) and cards (narrow)
    PortfolioSwitcher.tsx   # Per-person portfolios
    charts/
      AllocationChart.tsx   # Stacked bar + ranked list
      PerformanceChart.tsx  # Value vs invested, crosshair tooltip
      ReturnsChart.tsx      # Diverging bars, best to worst
      Sparkline.tsx

  pages/
    Dashboard.tsx
    Settings.tsx
  index.css                 # Design tokens (light + dark) and components
```

---

## Limitations

- **No sales or dividends.** This tracks what you hold and what you paid, not a
  full transaction ledger, so realised gains and dividend income are out of
  scope.
- **Data lives in one browser.** Clearing site data wipes it. Settings →
  *Export everything* is the backup, and the import is how you move it.
- **Polling, not streaming.** See *Update frequency* above.
- **Yahoo Finance's endpoints are undocumented.** They are widely used and
  stable in practice, but they carry no availability promise — which is exactly
  why the provider layer is pluggable and there are two alternatives in Settings.

## Deploying

Vercel and Netlify work with no extra configuration — `vercel.json` and
`netlify.toml` are committed, and both proxy `/yf` for you.

```bash
npm run build     # -> dist/
```

On any other static host, expect to switch the data source to Twelve Data in
Settings, since `/yf` will not be proxied.

### Which mode gives what

| | Live prices | Needs an API key | Setup |
|---|---|---|---|
| `npm run dev` / `npm run preview` | ✅ Yahoo | no | `npm install` |
| Vercel / Netlify deploy | ✅ Yahoo | no | push; configs committed |
| `portfolio-dashboard.standalone.html` | via Twelve Data | free key | none — double-click |
| Other static host | via Twelve Data | free key | upload `dist/` |
