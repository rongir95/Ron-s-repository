/**
 * Yahoo Finance, over two transports.
 *
 * The data source is the same either way — no API key, no registration, no
 * practical rate limit, and quotes *and* daily history from one endpoint. What
 * differs is how a browser is allowed to reach it, because Yahoo's public
 * endpoints send no CORS headers and so cannot be fetched cross-origin:
 *
 *   `yahooProvider`       same-origin via the `/yf` proxy in vite.config.ts /
 *                         vercel.json / netlify.toml. Nothing leaves for a third
 *                         party. Needs the app to be served by one of those.
 *
 *   `yahooRelayProvider`  through a public CORS relay, which adds the missing
 *                         header. Works from a plain static host or a file://
 *                         page with no key and no deploy — at the cost of a
 *                         third party seeing the request (ticker symbols only)
 *                         and of that relay's own availability.
 *
 * Freshness: for US-listed equities the chart endpoint reports the live
 * consolidated price, typically under a minute behind the tape. Some non-US
 * exchanges are delayed by their exchange's own rules (commonly 15 minutes).
 */
import { fetchJson, mapLimit } from '../http'
import { MarketDataError, type HistoryPoint, type HistoryRange, type MarketDataProvider, type Quote, type SymbolMatch } from '../types'

const ORIGIN = 'https://query1.finance.yahoo.com'

/** Maps a Yahoo path onto a URL this browser is actually allowed to fetch. */
type Transport = (path: string) => string

const sameOrigin: Transport = (path) => `/yf${path}`

/**
 * Public CORS relays, tried in order until one answers with usable JSON. More
 * than one because free relays come and go, and a personal dashboard should not
 * die with whichever happened to be listed first.
 */
const RELAYS: Array<(absolute: string) => string> = [
  (url) => `https://api.allorigins.win/raw?url=${encodeURIComponent(url)}`,
  (url) => `https://api.codetabs.com/v1/proxy?quest=${encodeURIComponent(url)}`,
  (url) => `https://corsproxy.io/?url=${encodeURIComponent(url)}`,
]

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

function chartPath(symbol: string, range: string, interval: string): string {
  return `/v8/finance/chart/${encodeURIComponent(symbol)}?range=${range}&interval=${interval}`
}

/** Fetches a Yahoo path over the given transport. */
async function get<T>(transport: Transport, path: string): Promise<T> {
  return fetchJson<T>(transport(path))
}

/** Tries each relay in turn; reports the last failure if none answer. */
async function getViaRelays<T>(path: string): Promise<T> {
  const absolute = `${ORIGIN}${path}`
  let lastError: unknown = null
  for (const relay of RELAYS) {
    try {
      return await fetchJson<T>(relay(absolute))
    } catch (err) {
      lastError = err
    }
  }
  throw new MarketDataError(
    `None of the ${RELAYS.length} public relays could reach Yahoo Finance. They are free services with no uptime ` +
      'promise — try again, or use a data source that does not depend on one (Settings explains the options). ' +
      `Last error: ${lastError instanceof Error ? lastError.message : 'unknown'}`,
    lastError,
  )
}

async function chart(fetchPath: <T>(path: string) => Promise<T>, symbol: string, range: string, interval: string) {
  const body = await fetchPath<ChartResponse>(chartPath(symbol, range, interval))
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

interface YahooVariant {
  id: string
  label: string
  freshness: string
  /** How this variant reaches a Yahoo path. */
  fetchPath: <T>(path: string) => Promise<T>
}

/** Both variants parse identical responses; only the transport differs. */
function buildYahooProvider({ id, label, freshness, fetchPath }: YahooVariant): MarketDataProvider {
  return {
    id,
    label,
    freshness,

    async getQuotes(symbols) {
      const out: Record<string, Quote> = {}
      let firstError: unknown = null
      // One tiny request per symbol; 4 at a time is plenty for a personal portfolio.
      await mapLimit(symbols, 4, async (symbol) => {
        try {
          const { meta } = await chart(fetchPath, symbol, '1d', '1d')
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
      const result = await chart(fetchPath, symbol, range, '1d')
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
      const body = await fetchPath<SearchResponse>(
        `/v1/finance/search?q=${encodeURIComponent(query)}&quotesCount=8&newsCount=0&listsCount=0`,
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
        const { meta } = await chart(fetchPath, `${from}${to}=X`, '1d', '1d')
        const rate = meta.regularMarketPrice
        return Number.isFinite(rate) && (rate as number) > 0 ? (rate as number) : null
      } catch {
        return null
      }
    },
  }
}

/** Default: same-origin through the app's own `/yf` proxy. */
export const yahooProvider = buildYahooProvider({
  id: 'yahoo',
  label: 'Yahoo Finance',
  freshness:
    'Live price, usually under a minute behind the tape for US listings. Some other exchanges are delayed ~15 min. No API key.',
  fetchPath: (path) => get(sameOrigin, path),
})

/** Same prices, reached through a public CORS relay — no proxy, no key. */
export const yahooRelayProvider = buildYahooProvider({
  id: 'yahoo-relay',
  label: 'Yahoo Finance via a public relay',
  freshness:
    'The same Yahoo Finance prices — live for US listings, some exchanges delayed ~15 min — reached through a free ' +
    'public CORS relay, so no API key and no deploy. The relays are third-party services with no uptime promise; only ' +
    'ticker symbols are sent to them.',
  fetchPath: (path) => getViaRelays(path),
})
