/**
 * Twelve Data — the no-server fallback.
 *
 * Sends `Access-Control-Allow-Origin: *`, so it works straight from the browser
 * on any static host where the `/yf` proxy is not available (GitHub Pages, S3,
 * a file:// page). Needs a free API key from twelvedata.com.
 *
 * Free tier: 8 requests/minute, 800/day — hence quotes for every holding are
 * batched into a single request.
 *
 * Freshness: real-time for US equities on the free plan; other venues may be
 * delayed by the exchange.
 */
import { fetchJson } from '../http'
import { MarketDataError, type HistoryPoint, type HistoryRange, type MarketDataProvider, type Quote, type SymbolMatch } from '../types'

const BASE = 'https://api.twelvedata.com'

const OUTPUT_SIZE: Record<HistoryRange, number> = {
  '1mo': 30,
  '3mo': 92,
  '6mo': 184,
  '1y': 370,
  '5y': 1300,
}

interface TdError {
  status?: string
  code?: number
  message?: string
}

interface TdQuote extends TdError {
  symbol?: string
  name?: string
  currency?: string
  exchange?: string
  close?: string | number
  previous_close?: string | number
  timestamp?: number
  is_market_open?: boolean
}

function num(value: unknown): number {
  const n = typeof value === 'number' ? value : Number.parseFloat(String(value))
  return Number.isFinite(n) ? n : NaN
}

function assertOk(body: TdError, what: string): void {
  if (body?.status === 'error') {
    const message = body.message || 'request rejected'
    if (body.code === 401 || /api key/i.test(message)) {
      throw new MarketDataError('Twelve Data rejected the API key — check it in Settings.')
    }
    if (body.code === 429 || /limit/i.test(message)) {
      throw new MarketDataError(
        'Twelve Data rate limit reached (8 requests/minute on the free plan). Try again shortly.',
      )
    }
    throw new MarketDataError(`Twelve Data: ${message} (${what})`)
  }
}

export function createTwelveDataProvider(apiKey: string): MarketDataProvider {
  const key = apiKey.trim()
  const auth = (url: string) => `${url}${url.includes('?') ? '&' : '?'}apikey=${encodeURIComponent(key)}`
  const requireKey = () => {
    if (!key) throw new MarketDataError('Add a free Twelve Data API key in Settings to fetch prices.')
  }

  return {
    id: 'twelvedata',
    label: 'Twelve Data',
    freshness:
      'Real-time for US listings on the free plan; other exchanges may be delayed. Free tier: 8 requests/min, 800/day.',
    needsKey: !key,

    async getQuotes(symbols) {
      requireKey()
      if (!symbols.length) return {}
      const body = await fetchJson<TdQuote | Record<string, TdQuote>>(
        auth(`${BASE}/quote?symbol=${encodeURIComponent(symbols.join(','))}`),
      )
      // A single symbol comes back flat; several come back keyed by symbol.
      const entries: TdQuote[] =
        symbols.length === 1 ? [body as TdQuote] : Object.values(body as Record<string, TdQuote>)
      // Surface auth/limit problems, which arrive at the top level of a batch call.
      assertOk(body as TdError, 'quotes')

      const out: Record<string, Quote> = {}
      for (const [index, entry] of entries.entries()) {
        if (!entry || entry.status === 'error') continue
        const symbol = entry.symbol || symbols[index]
        const price = num(entry.close)
        if (!symbol || !Number.isFinite(price)) continue
        const previous = num(entry.previous_close)
        out[symbol] = {
          symbol,
          price,
          previousClose: Number.isFinite(previous) ? previous : price,
          currency: (entry.currency || 'USD').toUpperCase(),
          name: entry.name,
          exchange: entry.exchange,
          quotedAt: entry.timestamp ? entry.timestamp * 1000 : Date.now(),
          marketOpen: entry.is_market_open,
        }
      }
      return out
    },

    async getHistory(symbol, range) {
      requireKey()
      interface TdSeries extends TdError {
        values?: Array<{ datetime?: string; close?: string }>
      }
      const body = await fetchJson<TdSeries>(
        auth(
          `${BASE}/time_series?symbol=${encodeURIComponent(symbol)}&interval=1day&outputsize=${OUTPUT_SIZE[range]}`,
        ),
      )
      assertOk(body, `history for ${symbol}`)
      const points: HistoryPoint[] = []
      for (const value of body.values ?? []) {
        const close = num(value.close)
        if (!value.datetime || !Number.isFinite(close)) continue
        points.push({ date: value.datetime.slice(0, 10), close })
      }
      // Twelve Data returns newest-first.
      return points.reverse()
    },

    async search(query) {
      interface TdSearch extends TdError {
        data?: Array<{ symbol?: string; instrument_name?: string; exchange?: string; instrument_type?: string }>
      }
      // symbol_search does not consume quota and needs no key.
      const body = await fetchJson<TdSearch>(`${BASE}/symbol_search?symbol=${encodeURIComponent(query)}&outputsize=8`)
      const matches: SymbolMatch[] = []
      for (const row of body.data ?? []) {
        if (!row.symbol) continue
        matches.push({
          symbol: row.symbol,
          name: row.instrument_name || row.symbol,
          exchange: row.exchange,
          type: row.instrument_type,
        })
      }
      return matches
    },

    async getFxRate(from, to) {
      if (from === to) return 1
      if (!key) return null
      try {
        const body = await fetchJson<{ price?: string } & TdError>(
          auth(`${BASE}/price?symbol=${encodeURIComponent(`${from}/${to}`)}`),
        )
        if (body?.status === 'error') return null
        const rate = num(body.price)
        return Number.isFinite(rate) && rate > 0 ? rate : null
      } catch {
        return null
      }
    },
  }
}
