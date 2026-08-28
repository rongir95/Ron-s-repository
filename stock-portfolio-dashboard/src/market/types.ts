/** The contract every market-data provider implements. */

export interface Quote {
  symbol: string
  /** Latest traded price, in `currency`. */
  price: number
  /** Previous session's close, used for the day's change. */
  previousClose: number
  currency: string
  name?: string
  exchange?: string
  /** When the price itself was last stamped by the exchange (ms epoch). */
  quotedAt?: number
  marketOpen?: boolean
}

export interface HistoryPoint {
  /** ISO date, YYYY-MM-DD. */
  date: string
  close: number
}

export interface SymbolMatch {
  symbol: string
  name: string
  exchange?: string
  type?: string
}

export type HistoryRange = '1mo' | '3mo' | '6mo' | '1y' | '5y'

export interface NewsItem {
  id: string
  title: string
  /** Where to read it. */
  url: string
  publisher?: string
  /** ms epoch. */
  publishedAt?: number
  /** Which of the portfolio's holdings this story relates to. */
  symbols: string[]
  /** False for synthetic sample headlines, so the UI can refuse to link them. */
  real: boolean
}

export interface MarketDataProvider {
  id: string
  label: string
  /** One-line description of freshness, shown in the UI. */
  freshness: string
  /** True when the provider needs an API key that has not been supplied. */
  needsKey?: boolean
  getQuotes(symbols: string[]): Promise<Record<string, Quote>>
  getHistory(symbol: string, range: HistoryRange): Promise<HistoryPoint[]>
  search(query: string): Promise<SymbolMatch[]>
  /** FX rate to convert `from` into `to`. Return null when unavailable. */
  getFxRate(from: string, to: string): Promise<number | null>
  /**
   * Recent headlines for the given symbols. Optional: providers without a news
   * endpoint omit it, and the UI says so rather than showing an empty panel.
   */
  getNews?(symbols: string[]): Promise<NewsItem[]>
}

/** Thrown with a message that is safe (and useful) to show to the user. */
export class MarketDataError extends Error {
  constructor(message: string, readonly cause?: unknown) {
    super(message)
    this.name = 'MarketDataError'
  }
}
