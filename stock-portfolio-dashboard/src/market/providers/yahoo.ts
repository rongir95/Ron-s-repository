/**
 * Yahoo Finance — the default provider.
 *
 * No API key, no registration, no practical rate limit, and it returns quotes
 * *and* daily history from the same endpoint. Its public endpoints send no CORS
 * headers, so we call them same-origin through the `/yf` proxy configured in
 * vite.config.ts / vercel.json / netlify.toml.
 *
 * Freshness: for US-listed equities the chart endpoint reports the live
 * consolidated price, typically under a minute behind the tape. Some non-US
 * exchanges are delayed by their exchange's own rules (commonly 15 minutes).
 */
import { fetchJson, mapLimit } from '../http'
import { MarketDataError, type HistoryPoint, type HistoryRange, type MarketDataProvider, type Quote, type SymbolMatch } from '../types'

const BASE = '/yf'

interface ChartMeta {
  symbol: string
  currency?: string
  exchangeName?: string
  regularMarketPrice?: number
  regularMarketTime?: number
  previousClose?: number
  chartPreviousClose?: number
  longName?: string
  shortName?: string
  currentTradingPeriod?: { regular?: { start?: number; end?: number } }
}

interface ChartResponse {
  chart: {
    result?: Array<{
      meta: ChartMeta
      timestamp?: number[]
      indicators?: { quote?: Array<{ close?: Array<number | null> }> }
    }>
    error?: { code?: string; description?: string } | null
  }
}

function chartUrl(symbol: string, range: string, interval: string): string {
  return `${BASE}/v8/finance/chart/${encodeURIComponent(symbol)}?range=${range}&interval=${interval}`
}

async function chart(symbol: string, range: string, interval: string) {
  const body = await fetchJson<ChartResponse>(chartUrl(symbol, range, interval))
  if (body?.chart?.error) {
    throw new MarketDataError(body.chart.error.description || `Yahoo Finance does not know the symbol "${symbol}".`)
  }
  const result = body?.chart?.result?.[0]
  if (!result) throw new MarketDataError(`No market data returned for "${symbol}".`)
  return result
}

function isMarketOpen(meta: ChartMeta): boolean | undefined {
  const regular = meta.currentTradingPeriod?.regular
  if (!regular?.start || !regular?.end) return undefined
  const nowSecs = Date.now() / 1000
  return nowSecs >= regular.start && nowSecs <= regular.end
}

/** ISO date in the *exchange-independent* sense: whatever calendar day the bar
 *  falls on in the viewer's zone. Good enough for a daily series. */
function isoDate(epochSecs: number): string {
  const d = new Date(epochSecs * 1000)
  const y = d.getFullYear()
  const m = `${d.getMonth() + 1}`.padStart(2, '0')
  const day = `${d.getDate()}`.padStart(2, '0')
  return `${y}-${m}-${day}`
}

export const yahooProvider: MarketDataProvider = {
  id: 'yahoo',
  label: 'Yahoo Finance',
  freshness:
    'Live price, usually under a minute behind the tape for US listings. Some other exchanges are delayed ~15 min. No API key.',

  async getQuotes(symbols) {
    const out: Record<string, Quote> = {}
    let firstError: unknown = null
    // One tiny request per symbol; 4 at a time is plenty for a personal portfolio.
    await mapLimit(symbols, 4, async (symbol) => {
      try {
        const { meta } = await chart(symbol, '1d', '1d')
        const price = meta.regularMarketPrice
        if (!Number.isFinite(price)) return
        out[symbol] = {
          symbol,
          price: price as number,
          previousClose: meta.previousClose ?? meta.chartPreviousClose ?? (price as number),
          currency: (meta.currency || 'USD').toUpperCase(),
          name: meta.longName || meta.shortName,
          exchange: meta.exchangeName,
          quotedAt: meta.regularMarketTime ? meta.regularMarketTime * 1000 : Date.now(),
          marketOpen: isMarketOpen(meta),
        }
      } catch (err) {
        // A single bad ticker must not sink the whole refresh; the caller
        // surfaces it as an unpriced holding instead.
        if (!firstError) firstError = err
      }
    })
    // But if not one symbol resolved, the tickers are not the problem — the
    // connection is, and that error is the useful one to report.
    if (!Object.keys(out).length && firstError) throw firstError
    return out
  },

  async getHistory(symbol, range: HistoryRange) {
    const result = await chart(symbol, range, '1d')
    const stamps = result.timestamp ?? []
    const closes = result.indicators?.quote?.[0]?.close ?? []
    const points: HistoryPoint[] = []
    for (let i = 0; i < stamps.length; i++) {
      const close = closes[i]
      if (close == null || !Number.isFinite(close)) continue
      points.push({ date: isoDate(stamps[i]), close })
    }
    return points
  },

  async search(query) {
    interface SearchResponse {
      quotes?: Array<{
        symbol?: string
        shortname?: string
        longname?: string
        exchDisp?: string
        quoteType?: string
        isYahooFinance?: boolean
      }>
    }
    const body = await fetchJson<SearchResponse>(
      `${BASE}/v1/finance/search?q=${encodeURIComponent(query)}&quotesCount=8&newsCount=0&listsCount=0`,
    )
    const matches: SymbolMatch[] = []
    for (const q of body.quotes ?? []) {
      if (!q.symbol || q.isYahooFinance === false) continue
      matches.push({
        symbol: q.symbol,
        name: q.longname || q.shortname || q.symbol,
        exchange: q.exchDisp,
        type: q.quoteType,
      })
    }
    return matches
  },

  async getFxRate(from, to) {
    if (from === to) return 1
    try {
      const { meta } = await chart(`${from}${to}=X`, '1d', '1d')
      const rate = meta.regularMarketPrice
      return Number.isFinite(rate) && (rate as number) > 0 ? (rate as number) : null
    } catch {
      return null
    }
  },
}
