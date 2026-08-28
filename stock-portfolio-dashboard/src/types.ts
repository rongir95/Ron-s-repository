/**
 * The complete data model. Everything here is a plain, serialisable object so it
 * round-trips cleanly through localStorage (and later, any backend).
 */

/** A single purchase. Positions are lot-based so one holding can be bought at
 *  several different prices and the average cost stays correct. */
export interface Lot {
  id: string
  shares: number
  /** Price per share paid for this lot, in the instrument's own currency. */
  price: number
  /** ISO date (YYYY-MM-DD). Optional — enables purchase-date-aware history. */
  date?: string
}

export interface Position {
  id: string
  /** Uppercase ticker as the data provider knows it, e.g. AAPL, VWCE.DE, TEVA.TA */
  symbol: string
  /** Company / instrument name, filled in from the provider when available. */
  name?: string
  lots: Lot[]
  /**
   * Stable index into the categorical palette, assigned once when the position
   * is created and never recomputed. Charts must colour by entity, never by
   * rank, so that re-sorting or filtering never repaints the survivors.
   */
  colorSlot: number
  notes?: string
  createdAt: string
}

export interface Portfolio {
  id: string
  /** Whose portfolio this is — "Ron", "Younger brother", … */
  name: string
  /** Currency all totals are reported in. Quotes are converted into it. */
  baseCurrency: string
  positions: Position[]
  /**
   * Un-invested cash available to buy with, in `baseCurrency`. Maintained by
   * hand — buying a stock deducts the purchase amount, selling credits the
   * proceeds, and it can be topped up or drawn down directly.
   */
  cash: number
  /**
   * Cumulative realised profit/loss from sales, in `baseCurrency`. Without it,
   * selling a winner would silently shrink the portfolio's profit — the gain
   * would leave the unrealised figure with nowhere to go.
   */
  realisedPl: number
  /** Set on first-run sample portfolios; cleared as soon as one is edited. */
  sample?: boolean
  createdAt: string
}

export type ProviderId = 'yahoo' | 'twelvedata' | 'demo'

export interface Settings {
  providerId: ProviderId
  /** Free API key, only needed by the twelvedata provider. */
  twelveDataKey: string
  theme: 'system' | 'light' | 'dark'
  /** Auto-refresh cadence in seconds while the market is open. 0 = manual only. */
  refreshSeconds: number
  /** Hide absolute money amounts — handy when sharing a screen. */
  privacyMode: boolean
}

export interface AppData {
  version: 1
  portfolios: Portfolio[]
  activePortfolioId: string
  settings: Settings
}
