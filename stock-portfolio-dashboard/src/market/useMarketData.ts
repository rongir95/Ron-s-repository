/**
 * Quote and history fetching, refresh cadence, and staleness — everything that
 * talks to a provider lives here so the components stay declarative.
 */
import { useCallback, useEffect, useMemo, useRef, useState } from 'react'
import { useStore } from '../store/store'
import { getProvider } from './index'
import type { HistoryPoint, HistoryRange, Quote } from './types'

export interface QuotesState {
  quotes: Record<string, Quote>
  /** `${FROM}->${TO}` -> multiplier. */
  fxRates: Record<string, number>
  loading: boolean
  error: string | null
  lastUpdated: number | null
  marketOpen: boolean | null
  refresh: () => void
}

function errorMessage(err: unknown): string {
  if (err instanceof Error && err.message) return err.message
  return 'Could not fetch market data.'
}

/**
 * Quotes for every symbol across every portfolio (one fetch serves both the
 * active dashboard and the all-portfolios comparison), plus any FX rates needed
 * to express them in each portfolio's base currency.
 */
export function useQuotes(): QuotesState {
  const { data, settings, portfolio } = useStore()

  const symbols = useMemo(() => {
    const set = new Set<string>()
    for (const pf of data.portfolios) for (const position of pf.positions) set.add(position.symbol)
    return [...set].sort()
  }, [data.portfolios])

  const baseCurrencies = useMemo(
    () => [...new Set(data.portfolios.map((pf) => pf.baseCurrency))].sort(),
    [data.portfolios],
  )

  const [quotes, setQuotes] = useState<Record<string, Quote>>({})
  const [fxRates, setFxRates] = useState<Record<string, number>>({})
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [lastUpdated, setLastUpdated] = useState<number | null>(null)
  const [tick, setTick] = useState(0)

  const symbolKey = symbols.join(',')
  const currencyKey = baseCurrencies.join(',')
  // Re-created when the provider settings change; kept out of the deps of the
  // fetch effect via a ref so that typing an API key does not fire a request.
  const providerKey = `${settings.providerId}:${settings.twelveDataKey}`
  const requestId = useRef(0)

  const refresh = useCallback(() => setTick((n) => n + 1), [])

  useEffect(() => {
    if (!symbolKey) {
      setQuotes({})
      setFxRates({})
      setError(null)
      setLastUpdated(null)
      return
    }
    const id = ++requestId.current
    const provider = getProvider(settings)
    let cancelled = false
    setLoading(true)

    ;(async () => {
      try {
        const fetched = await provider.getQuotes(symbolKey.split(','))
        if (cancelled || id !== requestId.current) return
        setQuotes(fetched)
        setLastUpdated(Date.now())

        const priced = Object.values(fetched)
        if (!priced.length) {
          setError(
            'No prices came back for any holding. Check the ticker symbols, or switch data source in Settings.',
          )
        } else {
          setError(null)
        }

        // Only fetch the FX pairs actually needed to report in each base currency.
        const pairs = new Set<string>()
        for (const quote of priced) {
          for (const base of currencyKey.split(',')) {
            if (quote.currency && base && quote.currency !== base) pairs.add(`${quote.currency}->${base}`)
          }
        }
        if (pairs.size) {
          const resolved: Record<string, number> = {}
          await Promise.all(
            [...pairs].map(async (pair) => {
              const [from, to] = pair.split('->')
              const rate = await provider.getFxRate(from, to).catch(() => null)
              if (rate) resolved[pair] = rate
            }),
          )
          if (!cancelled && id === requestId.current) setFxRates(resolved)
        } else {
          setFxRates({})
        }
      } catch (err) {
        if (!cancelled && id === requestId.current) setError(errorMessage(err))
      } finally {
        if (!cancelled && id === requestId.current) setLoading(false)
      }
    })()

    return () => {
      cancelled = true
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [symbolKey, currencyKey, providerKey, tick])

  const marketOpen = useMemo(() => {
    const flags = Object.values(quotes)
      .map((q) => q.marketOpen)
      .filter((flag): flag is boolean => typeof flag === 'boolean')
    return flags.length ? flags.some(Boolean) : null
  }, [quotes])

  // Auto-refresh: paused while the tab is hidden, and slowed right down when
  // every market we hold is closed (prices are not moving anyway).
  useEffect(() => {
    if (!settings.refreshSeconds || !symbolKey) return
    const period = settings.refreshSeconds * (marketOpen === false ? 10 : 1) * 1000
    let timer = window.setTimeout(function run() {
      if (!document.hidden) refresh()
      timer = window.setTimeout(run, period)
    }, period)
    return () => clearTimeout(timer)
  }, [settings.refreshSeconds, symbolKey, marketOpen, refresh])

  // A tab that comes back after being hidden shows a stale price otherwise.
  useEffect(() => {
    const onVisible = () => {
      if (!document.hidden && lastUpdated && Date.now() - lastUpdated > 60_000) refresh()
    }
    document.addEventListener('visibilitychange', onVisible)
    return () => document.removeEventListener('visibilitychange', onVisible)
  }, [lastUpdated, refresh])

  void portfolio
  return { quotes, fxRates, loading, error, lastUpdated, marketOpen, refresh }
}

export interface HistoryState {
  history: Record<string, HistoryPoint[]>
  loading: boolean
  error: string | null
}

/** Daily closes for the given symbols over `range`. */
export function useHistory(symbols: string[], range: HistoryRange): HistoryState {
  const { settings } = useStore()
  const [history, setHistory] = useState<Record<string, HistoryPoint[]>>({})
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const symbolKey = [...symbols].sort().join(',')
  const providerKey = `${settings.providerId}:${settings.twelveDataKey}`
  const requestId = useRef(0)

  useEffect(() => {
    if (!symbolKey) {
      setHistory({})
      setError(null)
      return
    }
    const id = ++requestId.current
    const provider = getProvider(settings)
    let cancelled = false
    setLoading(true)

    ;(async () => {
      const list = symbolKey.split(',')
      const out: Record<string, HistoryPoint[]> = {}
      let failures = 0
      // Sequential: Twelve Data's free tier allows only 8 requests a minute, and
      // a personal portfolio is small enough that this stays fast.
      for (const symbol of list) {
        if (cancelled || id !== requestId.current) return
        try {
          out[symbol] = await provider.getHistory(symbol, range)
        } catch {
          failures++
        }
      }
      if (cancelled || id !== requestId.current) return
      setHistory(out)
      setError(
        failures === list.length
          ? 'Could not load price history.'
          : failures > 0
            ? `Price history unavailable for ${failures} of ${list.length} holdings.`
            : null,
      )
      setLoading(false)
    })()

    return () => {
      cancelled = true
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [symbolKey, range, providerKey])

  return { history, loading, error }
}
