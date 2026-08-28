/**
 * All portfolio maths. Pure functions only — no React, no I/O — so the numbers
 * can be unit-tested (see calc.test.ts) and reused anywhere.
 *
 * Currency: a quote arrives in the instrument's own trading currency. Both the
 * price and the cost basis are converted into the portfolio's base currency at
 * today's rate, which keeps P/L% currency-invariant. (It does not model the FX
 * rate in force on the purchase date; see README.)
 */
import type { Portfolio, Position } from '../types'
import type { HistoryPoint, Quote } from '../market/types'

export interface PositionMetrics {
  id: string
  symbol: string
  name?: string
  colorSlot: number
  shares: number
  /** Weighted average purchase price, in the instrument's currency. */
  avgCost: number
  /** The instrument's trading currency. */
  currency: string
  /** Applied instrument-currency -> base-currency rate (1 when no conversion). */
  fxRate: number
  /** True when the instrument trades in a currency other than the base. */
  converted: boolean
  hasQuote: boolean
  /** Everything below is in the portfolio's base currency. */
  price: number
  previousClose: number
  costBasis: number
  marketValue: number
  pl: number
  plPct: number
  dayChange: number
  dayChangePct: number
  /** Share of the portfolio's market value, as a fraction. */
  weight: number
  lotCount: number
  firstPurchase?: string
}

export interface PortfolioMetrics {
  baseCurrency: string
  positions: PositionMetrics[]
  totalValue: number
  totalInvested: number
  totalPl: number
  totalPlPct: number
  dayChange: number
  dayChangePct: number
  /** Positions we could not price — their value is excluded from the totals. */
  unpriced: PositionMetrics[]
  best?: PositionMetrics
  worst?: PositionMetrics
  largest?: PositionMetrics
  /** Weight of the largest holding, as a fraction — a concentration read. */
  concentration: number
  /** True when at least one holding trades in a non-base currency. */
  mixedCurrency: boolean
}

// --- position-level -------------------------------------------------------

export function totalShares(position: Position): number {
  return position.lots.reduce((sum, lot) => sum + (Number(lot.shares) || 0), 0)
}

/** Cost basis in the instrument's own currency. */
export function nativeCostBasis(position: Position): number {
  return position.lots.reduce(
    (sum, lot) => sum + (Number(lot.shares) || 0) * (Number(lot.price) || 0),
    0,
  )
}

/** Weighted average purchase price across every lot. */
export function averageCost(position: Position): number {
  const sh = totalShares(position)
  return sh > 0 ? nativeCostBasis(position) / sh : 0
}

export function firstPurchaseDate(position: Position): string | undefined {
  const dates = position.lots.map((l) => l.date).filter((d): d is string => !!d)
  return dates.length ? dates.slice().sort()[0] : undefined
}

// --- portfolio-level ------------------------------------------------------

/**
 * @param fxRates map of `${FROM}->${TO}` to a multiplier.
 */
export function computePortfolio(
  portfolio: Portfolio,
  quotes: Record<string, Quote>,
  fxRates: Record<string, number> = {},
): PortfolioMetrics {
  const base = portfolio.baseCurrency
  const rows: PositionMetrics[] = portfolio.positions.map((position) => {
    const quote = quotes[position.symbol]
    const sh = totalShares(position)
    const avgCost = averageCost(position)
    const currency = quote?.currency || base
    const fxRate = fxRateFor(currency, base, fxRates)
    const hasQuote = !!quote && Number.isFinite(quote.price) && quote.price > 0

    const price = hasQuote ? quote.price * fxRate : 0
    const previousClose =
      hasQuote && Number.isFinite(quote.previousClose) && quote.previousClose > 0
        ? quote.previousClose * fxRate
        : price
    const costBasis = nativeCostBasis(position) * fxRate
    const marketValue = hasQuote ? sh * price : 0
    const pl = hasQuote ? marketValue - costBasis : 0
    const dayChange = hasQuote ? sh * (price - previousClose) : 0

    return {
      id: position.id,
      symbol: position.symbol,
      name: position.name,
      colorSlot: position.colorSlot,
      shares: sh,
      avgCost,
      currency,
      fxRate,
      converted: currency !== base,
      hasQuote,
      price,
      previousClose,
      costBasis,
      marketValue,
      pl,
      plPct: costBasis > 0 && hasQuote ? pl / costBasis : 0,
      dayChange,
      dayChangePct: previousClose > 0 && hasQuote ? price / previousClose - 1 : 0,
      weight: 0,
      lotCount: position.lots.length,
      firstPurchase: firstPurchaseDate(position),
    }
  })

  const priced = rows.filter((r) => r.hasQuote)
  const unpriced = rows.filter((r) => !r.hasQuote)

  const totalValue = priced.reduce((s, r) => s + r.marketValue, 0)
  // Only priced holdings count toward invested, so the P/L% compares like with like.
  const totalInvested = priced.reduce((s, r) => s + r.costBasis, 0)
  const totalPl = totalValue - totalInvested
  const dayChange = priced.reduce((s, r) => s + r.dayChange, 0)
  const previousValue = priced.reduce((s, r) => s + r.shares * r.previousClose, 0)

  for (const row of rows) {
    row.weight = totalValue > 0 && row.hasQuote ? row.marketValue / totalValue : 0
  }

  const byPct = priced.slice().sort((a, b) => b.plPct - a.plPct)
  const byWeight = priced.slice().sort((a, b) => b.weight - a.weight)

  return {
    baseCurrency: base,
    positions: rows,
    totalValue,
    totalInvested,
    totalPl,
    totalPlPct: totalInvested > 0 ? totalPl / totalInvested : 0,
    dayChange,
    dayChangePct: previousValue > 0 ? totalValue / previousValue - 1 : 0,
    unpriced,
    best: byPct[0],
    worst: byPct.length > 1 ? byPct[byPct.length - 1] : undefined,
    largest: byWeight[0],
    concentration: byWeight[0]?.weight ?? 0,
    mixedCurrency: rows.some((r) => r.converted),
  }
}

export function fxRateFor(from: string, to: string, rates: Record<string, number>): number {
  if (!from || !to || from === to) return 1
  const direct = rates[`${from}->${to}`]
  if (Number.isFinite(direct) && direct > 0) return direct
  const inverse = rates[`${to}->${from}`]
  if (Number.isFinite(inverse) && inverse > 0) return 1 / inverse
  return 1
}

// --- history --------------------------------------------------------------

export interface SeriesPoint {
  date: string
  /** Market value of the holdings held on that date. */
  value: number
  /** Cost of the lots purchased on or before that date. */
  invested: number
}

/**
 * Value-and-invested over time, reconstructed from the lots.
 *
 * Lots carrying a purchase date only contribute from that date onward, so the
 * chart reflects when money actually went in. Undated lots are treated as held
 * for the whole window (the honest fallback when we do not know better).
 */
export function buildSeries(
  positions: Position[],
  historyBySymbol: Record<string, HistoryPoint[]>,
  baseCurrency: string,
  quotes: Record<string, Quote> = {},
  fxRates: Record<string, number> = {},
): SeriesPoint[] {
  const dates = new Set<string>()
  for (const position of positions) {
    for (const point of historyBySymbol[position.symbol] ?? []) dates.add(point.date)
  }
  const timeline = [...dates].sort()
  if (!timeline.length) return []

  const tracks = positions.map((position) => {
    const history = historyBySymbol[position.symbol] ?? []
    const closes = new Map(history.map((p) => [p.date, p.close]))
    const currency = quotes[position.symbol]?.currency || baseCurrency
    const fx = fxRateFor(currency, baseCurrency, fxRates)
    const lots = position.lots
      .map((lot) => ({
        shares: Number(lot.shares) || 0,
        cost: (Number(lot.shares) || 0) * (Number(lot.price) || 0),
        date: lot.date,
      }))
      .sort((a, b) => (a.date ?? '').localeCompare(b.date ?? ''))
    // Back-fill: before a symbol's first close we value it at that first close,
    // so a late-listing holding does not create a spurious dip.
    const firstClose = history.length ? history[0].close : 0
    return { closes, fx, lots, firstClose, lastClose: firstClose }
  })

  return timeline.map((date) => {
    let value = 0
    let invested = 0
    for (const track of tracks) {
      const close = track.closes.get(date)
      if (close != null && Number.isFinite(close)) track.lastClose = close
      const priceOn = track.lastClose || track.firstClose
      let held = 0
      for (const lot of track.lots) {
        if (!lot.date || lot.date <= date) {
          held += lot.shares
          invested += lot.cost * track.fx
        }
      }
      value += held * priceOn * track.fx
    }
    return { date, value, invested }
  })
}

// --- money-weighted annualised return (XIRR) ------------------------------

export interface CashFlow {
  /** Negative = money in, positive = money out / final value. */
  amount: number
  date: string
}

/** Cash flows implied by the lots plus today's market value. */
export function buildCashFlows(
  positions: Position[],
  metrics: PortfolioMetrics,
  today: string,
): CashFlow[] | null {
  const flows: CashFlow[] = []
  const pricedIds = new Set(metrics.positions.filter((p) => p.hasQuote).map((p) => p.id))
  for (const position of positions) {
    if (!pricedIds.has(position.id)) continue
    const row = metrics.positions.find((p) => p.id === position.id)
    const fx = row?.fxRate ?? 1
    for (const lot of position.lots) {
      // Without a date we cannot place the flow in time, so no XIRR.
      if (!lot.date) return null
      flows.push({ amount: -(Number(lot.shares) || 0) * (Number(lot.price) || 0) * fx, date: lot.date })
    }
  }
  if (flows.length === 0 || metrics.totalValue <= 0) return null
  flows.push({ amount: metrics.totalValue, date: today })
  return flows
}

const DAY_MS = 86_400_000

function npv(flows: CashFlow[], rate: number, t0: number): number {
  return flows.reduce((sum, flow) => {
    const years = (new Date(`${flow.date}T00:00:00Z`).getTime() - t0) / (365 * DAY_MS)
    return sum + flow.amount / Math.pow(1 + rate, years)
  }, 0)
}

/**
 * Money-weighted annualised return, solved by bisection (robust where
 * Newton's method diverges). Returns null when the flows span too short a
 * period to annualise meaningfully, or when no rate brackets a root.
 */
export function annualisedReturn(flows: CashFlow[] | null, minDays = 60): number | null {
  if (!flows || flows.length < 2) return null
  const times = flows.map((f) => new Date(`${f.date}T00:00:00Z`).getTime()).filter((t) => !Number.isNaN(t))
  if (times.length !== flows.length) return null
  const t0 = Math.min(...times)
  const span = (Math.max(...times) - t0) / DAY_MS
  if (span < minDays) return null

  let low = -0.9999
  let high = 10
  let fLow = npv(flows, low, t0)
  let fHigh = npv(flows, high, t0)
  if (!Number.isFinite(fLow) || !Number.isFinite(fHigh) || fLow * fHigh > 0) return null

  for (let i = 0; i < 200; i++) {
    const mid = (low + high) / 2
    const fMid = npv(flows, mid, t0)
    if (!Number.isFinite(fMid)) return null
    if (Math.abs(fMid) < 1e-9) return mid
    if (fLow * fMid <= 0) {
      high = mid
      fHigh = fMid
    } else {
      low = mid
      fLow = fMid
    }
  }
  void fHigh
  return (low + high) / 2
}
