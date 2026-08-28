/**
 * Headlines for the holdings in this portfolio.
 *
 * Each story is tagged with the holding(s) it concerns, in that holding's own
 * palette hue, so the panel reads as part of the same dashboard rather than a
 * bolted-on feed. Stories open in a new tab; sample headlines from the demo
 * provider are never linked, because a plausible-looking fake headline about a
 * real company would be worse than showing none.
 */
import { useMemo, useState } from 'react'
import type { PositionMetrics } from '../lib/calc'
import { relativeTime } from '../lib/format'
import { seriesColor } from '../lib/series'
import type { NewsItem } from '../market/types'
import { Banner, Button, Card, Skeleton } from './ui'

const SHOWN_BY_DEFAULT = 8

export function NewsPanel({
  news,
  loading,
  error,
  supported,
  fetchedAt,
  positions,
  providerLabel,
  onRefresh,
  onOpenSettings,
}: {
  news: NewsItem[]
  loading: boolean
  error: string | null
  supported: boolean
  fetchedAt: number | null
  positions: PositionMetrics[]
  providerLabel: string
  onRefresh: () => void
  onOpenSettings: () => void
}) {
  const [expanded, setExpanded] = useState(false)
  const [symbolFilter, setSymbolFilter] = useState<string | null>(null)

  // Hue per ticker, taken from the holding so the tags match the table and pie.
  const hues = useMemo(() => {
    const map = new Map<string, string>()
    for (const position of positions) map.set(position.symbol, seriesColor(position.colorSlot))
    return map
  }, [positions])

  const filtered = useMemo(
    () => (symbolFilter ? news.filter((item) => item.symbols.includes(symbolFilter)) : news),
    [news, symbolFilter],
  )
  const visible = expanded ? filtered : filtered.slice(0, SHOWN_BY_DEFAULT)

  // Only offer a filter for holdings that actually have a story.
  const withNews = useMemo(() => {
    const set = new Set<string>()
    for (const item of news) for (const symbol of item.symbols) set.add(symbol)
    return positions.filter((position) => set.has(position.symbol)).map((position) => position.symbol)
  }, [news, positions])

  if (!supported) {
    return (
      <Card>
        <div className="card-head">
          <div>
            <div className="card-title">News</div>
            <div className="card-note">Headlines for your holdings.</div>
          </div>
        </div>
        <Banner
          action={
            <Button size="sm" onClick={onOpenSettings}>
              Change data source
            </Button>
          }
        >
          {providerLabel} does not provide news. Either of the Yahoo Finance sources does.
        </Banner>
      </Card>
    )
  }

  return (
    <Card>
      <div className="card-head">
        <div>
          <div className="card-title">News</div>
          <div className="card-note">
            Headlines for your holdings
            {fetchedAt ? ` · fetched ${relativeTime(fetchedAt)}` : ''}
          </div>
        </div>
        <div className="row-wrap">
          {withNews.length > 1 && (
            <div className="news-filter" role="group" aria-label="Filter headlines by holding">
              <button
                type="button"
                aria-pressed={symbolFilter === null}
                onClick={() => setSymbolFilter(null)}
              >
                All
              </button>
              {withNews.map((symbol) => (
                <button
                  key={symbol}
                  type="button"
                  aria-pressed={symbolFilter === symbol}
                  onClick={() => setSymbolFilter(symbolFilter === symbol ? null : symbol)}
                >
                  <span className="swatch" style={{ background: hues.get(symbol) }} aria-hidden="true" />
                  {symbol}
                </button>
              ))}
            </div>
          )}
          <Button size="sm" onClick={onRefresh} disabled={loading}>
            {loading ? 'Loading…' : 'Refresh'}
          </Button>
        </div>
      </div>

      {loading && !news.length ? (
        <ul className="news-list">
          {[0, 1, 2, 3].map((row) => (
            <li className="news-item" key={row}>
              <Skeleton width="100%" height={15} />
              <Skeleton width={180} height={11} />
            </li>
          ))}
        </ul>
      ) : error && !news.length ? (
        <Banner
          action={
            <Button size="sm" onClick={onRefresh}>
              Try again
            </Button>
          }
        >
          {error}
        </Banner>
      ) : !filtered.length ? (
        <p className="field-hint" style={{ margin: 0 }}>
          No headlines{symbolFilter ? ` for ${symbolFilter}` : ''} right now.
        </p>
      ) : (
        <>
          <ul className="news-list">
            {visible.map((item) => (
              <li className="news-item" key={item.id}>
                {item.real ? (
                  <a className="news-title" href={item.url} target="_blank" rel="noreferrer noopener">
                    {item.title}
                  </a>
                ) : (
                  <span className="news-title placeholder">{item.title}</span>
                )}
                <span className="news-meta">
                  {item.symbols.map((symbol) => (
                    <span className="news-tag" key={symbol}>
                      <span className="swatch" style={{ background: hues.get(symbol) }} aria-hidden="true" />
                      {symbol}
                    </span>
                  ))}
                  {item.publisher && <span>{item.publisher}</span>}
                  {item.publishedAt && <span>{relativeTime(item.publishedAt)}</span>}
                </span>
              </li>
            ))}
          </ul>
          {filtered.length > SHOWN_BY_DEFAULT && (
            <Button size="sm" variant="ghost" onClick={() => setExpanded((value) => !value)}>
              {expanded ? 'Show fewer' : `Show all ${filtered.length}`}
            </Button>
          )}
        </>
      )}
    </Card>
  )
}
