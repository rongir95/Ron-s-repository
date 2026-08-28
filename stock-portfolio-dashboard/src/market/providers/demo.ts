/**
 * Demo provider — deterministic synthetic prices, no network.
 *
 * Purpose: let the dashboard be explored, demonstrated and tested end to end
 * with no API key and no connectivity (and to keep the UI honest about it — the
 * header shows a "Demo data" badge whenever this provider is selected).
 *
 * Prices are a seeded random walk, so the same ticker always produces the same
 * history, and the "current" price drifts on a 5-minute bucket so that pressing
 * Refresh visibly does something.
 */
import type { HistoryPoint, HistoryRange, MarketDataProvider, NewsItem, Quote, SymbolMatch } from '../types'

const KNOWN: Record<string, { name: string; currency: string; base: number }> = {
  AAPL: { name: 'Apple Inc.', currency: 'USD', base: 190 },
  MSFT: { name: 'Microsoft Corporation', currency: 'USD', base: 410 },
  NVDA: { name: 'NVIDIA Corporation', currency: 'USD', base: 118 },
  GOOGL: { name: 'Alphabet Inc.', currency: 'USD', base: 168 },
  AMZN: { name: 'Amazon.com, Inc.', currency: 'USD', base: 182 },
  TSLA: { name: 'Tesla, Inc.', currency: 'USD', base: 245 },
  META: { name: 'Meta Platforms, Inc.', currency: 'USD', base: 505 },
  VOO: { name: 'Vanguard S&P 500 ETF', currency: 'USD', base: 505 },
  VTI: { name: 'Vanguard Total Stock Market ETF', currency: 'USD', base: 268 },
  QQQ: { name: 'Invesco QQQ Trust', currency: 'USD', base: 448 },
  SPY: { name: 'SPDR S&P 500 ETF Trust', currency: 'USD', base: 545 },
  AMD: { name: 'Advanced Micro Devices, Inc.', currency: 'USD', base: 152 },
  NFLX: { name: 'Netflix, Inc.', currency: 'USD', base: 680 },
  DIS: { name: 'The Walt Disney Company', currency: 'USD', base: 92 },
  KO: { name: 'The Coca-Cola Company', currency: 'USD', base: 64 },
  NKE: { name: 'NIKE, Inc.', currency: 'USD', base: 78 },
  'TEVA.TA': { name: 'Teva Pharmaceutical Industries', currency: 'ILS', base: 6100 },
  'VWCE.DE': { name: 'Vanguard FTSE All-World ETF', currency: 'EUR', base: 122 },
}

const DEMO_FX: Record<string, number> = { 'USD->ILS': 3.72, 'EUR->USD': 1.08, 'ILS->USD': 0.269, 'USD->EUR': 0.926 }

const DAY_MS = 86_400_000
const ANCHOR_DAY = Math.floor(Date.UTC(2019, 0, 1) / DAY_MS)
const DAYS: Record<HistoryRange, number> = { '1mo': 30, '3mo': 92, '6mo': 184, '1y': 366, '5y': 1826 }

function hash(text: string): number {
  let h = 2166136261
  for (let i = 0; i < text.length; i++) {
    h ^= text.charCodeAt(i)
    h = Math.imul(h, 16777619)
  }
  return h >>> 0
}

/** mulberry32 — small, fast, good enough, and identical across runs. */
function rand(seed: number): number {
  let t = (seed + 0x6d2b79f5) >>> 0
  t = Math.imul(t ^ (t >>> 15), t | 1)
  t ^= t + Math.imul(t ^ (t >>> 7), t | 61)
  return ((t ^ (t >>> 14)) >>> 0) / 4294967296
}

function profile(symbol: string) {
  const known = KNOWN[symbol]
  if (known) return known
  const seed = hash(symbol)
  return {
    name: `${symbol} (demo instrument)`,
    currency: 'USD',
    base: 20 + (seed % 40_000) / 100,
  }
}

interface Walk {
  closes: Map<number, number>
  /** Highest day index generated so far — the walk only ever extends forward. */
  lastDay: number
  price: number
  drift: number
  vol: number
  floor: number
}

const walks = new Map<string, Walk>()

function walkFor(symbol: string): Walk {
  let walk = walks.get(symbol)
  if (!walk) {
    const { base } = profile(symbol)
    const seed = hash(symbol)
    walk = {
      closes: new Map(),
      lastDay: ANCHOR_DAY - 1,
      price: base * 0.55,
      // Each ticker gets its own mild drift and volatility, stable across runs.
      drift: (rand(seed) - 0.42) * 0.0011,
      vol: 0.008 + rand(seed ^ 0x9e3779b9) * 0.022,
      floor: base * 0.05,
    }
    walks.set(symbol, walk)
  }
  return walk
}

/** Close for `dayIndex`, memoised, generated forward from the anchor date. */
function closeOn(symbol: string, dayIndex: number): number {
  const walk = walkFor(symbol)
  const hit = walk.closes.get(dayIndex)
  if (hit != null) return hit

  const seed = hash(symbol)
  for (let day = walk.lastDay + 1; day <= dayIndex; day++) {
    const step = walk.drift + (rand(seed ^ (day * 2654435761)) - 0.5) * walk.vol
    walk.price = Math.max(walk.price * (1 + step), walk.floor)
    walk.closes.set(day, round(walk.price))
  }
  walk.lastDay = Math.max(walk.lastDay, dayIndex)
  return walk.closes.get(dayIndex) ?? round(walk.price)
}

function round(value: number): number {
  return Math.round(value * 100) / 100
}

function today(): number {
  return Math.floor(Date.now() / DAY_MS)
}

/** Weekends have no bar, same as a real daily series. */
function isTradingDay(dayIndex: number): boolean {
  const weekday = new Date(dayIndex * DAY_MS).getUTCDay()
  return weekday !== 0 && weekday !== 6
}

function isoFromDay(dayIndex: number): string {
  return new Date(dayIndex * DAY_MS).toISOString().slice(0, 10)
}

export const demoProvider: MarketDataProvider = {
  id: 'demo',
  label: 'Demo data (offline)',
  freshness: 'Synthetic prices generated in the browser. Nothing is fetched — for trying the dashboard out.',

  async getQuotes(symbols) {
    const day = today()
    const out: Record<string, Quote> = {}
    for (const symbol of symbols) {
      const { name, currency } = profile(symbol)
      const base = closeOn(symbol, day)
      // Intraday drift on a 5-minute bucket, so Refresh visibly moves the price.
      const bucket = Math.floor(Date.now() / 300_000)
      const intraday = (rand(hash(symbol) ^ bucket) - 0.5) * 0.012
      out[symbol] = {
        symbol,
        price: round(base * (1 + intraday)),
        previousClose: closeOn(symbol, day - (isTradingDay(day - 1) ? 1 : 2)),
        currency,
        name,
        exchange: 'DEMO',
        quotedAt: Date.now(),
        marketOpen: true,
      }
    }
    return out
  },

  async getHistory(symbol, range: HistoryRange) {
    const end = today()
    const start = end - DAYS[range]
    const points: HistoryPoint[] = []
    for (let day = start; day <= end; day++) {
      if (!isTradingDay(day)) continue
      points.push({ date: isoFromDay(day), close: closeOn(symbol, day) })
    }
    return points
  },

  async search(query) {
    const q = query.trim().toUpperCase()
    if (!q) return []
    const matches: SymbolMatch[] = Object.entries(KNOWN)
      .filter(([symbol, meta]) => symbol.includes(q) || meta.name.toUpperCase().includes(q))
      .slice(0, 8)
      .map(([symbol, meta]) => ({ symbol, name: meta.name, exchange: 'DEMO', type: 'EQUITY' }))
    if (!matches.some((m) => m.symbol === q)) {
      matches.push({ symbol: q, name: profile(q).name, exchange: 'DEMO', type: 'EQUITY' })
    }
    return matches
  },

  async getFxRate(from, to) {
    if (from === to) return 1
    return DEMO_FX[`${from}->${to}`] ?? null
  },

  /**
   * Placeholder headlines. Deliberately generic and flagged `real: false` so the
   * UI refuses to link them — a plausible-looking fake headline about a real
   * company would be worse than no news at all.
   */
  async getNews(symbols) {
    const shapes = [
      'quarterly results in focus',
      'analyst price targets revised',
      'sector moves on rate expectations',
      'trading volume above average',
      'index weighting under review',
    ]
    const out: NewsItem[] = []
    const day = Math.floor(Date.now() / DAY_MS)
    for (const [index, symbol] of symbols.slice(0, 8).entries()) {
      const pick = shapes[hash(symbol) % shapes.length]
      out.push({
        id: `demo-${symbol}-${day}`,
        title: `${symbol} — ${pick}`,
        url: '',
        publisher: 'Sample headline, not real news',
        publishedAt: Date.now() - (index + 1) * 3_600_000,
        symbols: [symbol],
        real: false,
      })
    }
    return out
  },
}
