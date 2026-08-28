/**
 * The positions table — and, below the table's minimum width, the same data as
 * cards. This is also the "table view" that the allocation chart's contrast
 * relief depends on: every number the charts encode in colour is written out
 * here in text.
 */
import { useMemo, useState } from 'react'
import type { PositionMetrics } from '../lib/calc'
import { money, percent, shares as fmtShares, signedMoney, signedPercent } from '../lib/format'
import { seriesColor } from '../lib/series'
import type { HistoryPoint } from '../market/types'
import { Button, Chip, IconPencil, IconTrash, Value } from './ui'
import { Sparkline } from './charts/Sparkline'

type SortKey = 'symbol' | 'marketValue' | 'pl' | 'plPct' | 'weight' | 'dayChangePct'

const COLUMNS: Array<{ key: SortKey | null; label: string; hint?: string }> = [
  { key: 'symbol', label: 'Holding' },
  { key: null, label: 'Shares' },
  { key: null, label: 'Avg cost' },
  { key: null, label: 'Price' },
  { key: 'dayChangePct', label: 'Today' },
  { key: null, label: '30d' },
  { key: null, label: 'Invested' },
  { key: 'marketValue', label: 'Value' },
  { key: 'pl', label: 'P/L' },
  { key: 'plPct', label: 'P/L %' },
  { key: 'weight', label: 'Weight' },
  { key: null, label: '' },
]

export function PositionsTable({
  rows,
  currency,
  history,
  masked,
  onEdit,
  onSell,
  onDelete,
}: {
  rows: PositionMetrics[]
  currency: string
  history: Record<string, HistoryPoint[]>
  masked?: boolean
  onEdit: (id: string) => void
  onSell: (id: string) => void
  onDelete: (id: string) => void
}) {
  const [sort, setSort] = useState<{ key: SortKey; dir: 'asc' | 'desc' }>({ key: 'marketValue', dir: 'desc' })

  const sorted = useMemo(() => {
    const list = [...rows]
    const { key, dir } = sort
    list.sort((a, b) => {
      if (key === 'symbol') return a.symbol.localeCompare(b.symbol) * (dir === 'asc' ? 1 : -1)
      // Unpriced holdings always sort last — they have no number to compare.
      if (a.hasQuote !== b.hasQuote) return a.hasQuote ? -1 : 1
      const diff = (a[key] as number) - (b[key] as number)
      return dir === 'asc' ? diff : -diff
    })
    return list
  }, [rows, sort])

  const toggle = (key: SortKey) =>
    setSort((current) =>
      current.key === key
        ? { key, dir: current.dir === 'asc' ? 'desc' : 'asc' }
        : { key, dir: key === 'symbol' ? 'asc' : 'desc' },
    )

  const totals = rows.reduce(
    (acc, row) => ({
      invested: acc.invested + (row.hasQuote ? row.costBasis : 0),
      value: acc.value + row.marketValue,
      pl: acc.pl + row.pl,
    }),
    { invested: 0, value: 0, pl: 0 },
  )

  const sparkValues = (symbol: string) => (history[symbol] ?? []).slice(-30).map((point) => point.close)

  return (
    <>
      <div className="table-wrap desktop-only">
        <table className="positions">
          <caption className="sr-only">
            Holdings with share count, average cost, current price, profit or loss, and portfolio weight
          </caption>
          <thead>
            <tr>
              {COLUMNS.map((column, index) =>
                column.key ? (
                  <th
                    key={column.label || index}
                    className="sortable"
                    aria-sort={sort.key === column.key ? (sort.dir === 'asc' ? 'ascending' : 'descending') : 'none'}
                    scope="col"
                  >
                    <button type="button" onClick={() => toggle(column.key as SortKey)}>
                      {column.label}
                      {sort.key === column.key && (
                        <span className="sort-arrow" aria-hidden="true">
                          {sort.dir === 'asc' ? '▲' : '▼'}
                        </span>
                      )}
                    </button>
                  </th>
                ) : (
                  <th key={column.label || index} scope="col">
                    {column.label || <span className="sr-only">Actions</span>}
                  </th>
                ),
              )}
            </tr>
          </thead>
          <tbody>
            {sorted.map((row) => (
              <tr key={row.id}>
                <td>
                  <span className="sym-cell">
                    {/* The holding's own hue, so the table and the allocation
                        chart read as one thing. */}
                    <span className="sym-bar" style={{ background: seriesColor(row.colorSlot) }} aria-hidden="true" />
                    <span className="sym-text">
                      <span className="sym-ticker">{row.symbol}</span>
                      <span className="sym-name">{row.name ?? '—'}</span>
                    </span>
                  </span>
                </td>
                <td>{fmtShares(row.shares)}</td>
                <td>
                  {money(row.avgCost, row.currency)}
                  {row.lotCount > 1 && (
                    <>
                      {' '}
                      <span title={`Share-weighted across ${row.lotCount} purchases`} style={{ color: 'var(--text-3)', fontSize: 11 }}>
                        ×{row.lotCount}
                      </span>
                    </>
                  )}
                </td>
                <td>{row.hasQuote ? money(row.price / row.fxRate, row.currency) : <Chip tone="warn">No price</Chip>}</td>
                <td>{row.hasQuote ? <Value amount={row.dayChangePct} percent /> : '—'}</td>
                <td>
                  <Sparkline values={sparkValues(row.symbol)} label={`${row.symbol} 30-day price trend`} />
                </td>
                <td className={masked ? 'privacy-mask' : undefined}>{money(row.costBasis, currency, { decimals: 0 })}</td>
                <td className={masked ? 'privacy-mask' : undefined}>
                  <strong>{row.hasQuote ? money(row.marketValue, currency, { decimals: 0 }) : '—'}</strong>
                </td>
                <td>{row.hasQuote ? <Value amount={row.pl} currency={currency} masked={masked} bold /> : '—'}</td>
                <td>{row.hasQuote ? <Value amount={row.plPct} percent bold /> : '—'}</td>
                <td>{row.hasQuote ? percent(row.weight, 1) : '—'}</td>
                <td>
                  <span className="row-actions">
                    <Button size="sm" variant="ghost" onClick={() => onSell(row.id)} aria-label={`Sell ${row.symbol}`}>
                      Sell
                    </Button>
                    <Button size="sm" variant="ghost" iconOnly aria-label={`Edit ${row.symbol}`} onClick={() => onEdit(row.id)}>
                      <IconPencil />
                    </Button>
                    <Button size="sm" variant="ghost" iconOnly aria-label={`Remove ${row.symbol}`} onClick={() => onDelete(row.id)}>
                      <IconTrash />
                    </Button>
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
          <tfoot>
            <tr>
              <td>
                {rows.length} holding{rows.length === 1 ? '' : 's'}
              </td>
              <td colSpan={5} />
              <td className={masked ? 'privacy-mask' : undefined}>{money(totals.invested, currency, { decimals: 0 })}</td>
              <td className={masked ? 'privacy-mask' : undefined}>{money(totals.value, currency, { decimals: 0 })}</td>
              <td>
                <Value amount={totals.pl} currency={currency} masked={masked} bold />
              </td>
              <td>
                <Value amount={totals.invested > 0 ? totals.pl / totals.invested : 0} percent bold />
              </td>
              <td colSpan={2} />
            </tr>
          </tfoot>
        </table>
      </div>

      {/* Same data, card-shaped, for narrow screens. */}
      <div className="pos-cards mobile-only">
        {sorted.map((row) => (
          <div className="card pos-card" key={row.id}>
            <div className="pos-card-top">
              <span className="sym-cell">
                <span className="sym-bar" style={{ background: seriesColor(row.colorSlot) }} aria-hidden="true" />
                <span className="sym-text">
                  <span className="sym-ticker">{row.symbol}</span>
                  <span className="sym-name">{row.name ?? '—'}</span>
                </span>
              </span>
              <span className="row" style={{ gap: 2 }}>
                <Button size="sm" variant="ghost" onClick={() => onSell(row.id)} aria-label={`Sell ${row.symbol}`}>
                  Sell
                </Button>
                <Button size="sm" variant="ghost" iconOnly aria-label={`Edit ${row.symbol}`} onClick={() => onEdit(row.id)}>
                  <IconPencil />
                </Button>
                <Button size="sm" variant="ghost" iconOnly aria-label={`Remove ${row.symbol}`} onClick={() => onDelete(row.id)}>
                  <IconTrash />
                </Button>
              </span>
            </div>
            <div className="pos-card-grid">
              <span className="pos-card-cell">
                <span className="pos-card-key">Value</span>
                <span className={`pos-card-val ${masked ? 'privacy-mask' : ''}`}>
                  {row.hasQuote ? money(row.marketValue, currency, { decimals: 0 }) : '—'}
                </span>
              </span>
              <span className="pos-card-cell">
                <span className="pos-card-key">P/L</span>
                <span className="pos-card-val">
                  {row.hasQuote ? <Value amount={row.pl} currency={currency} masked={masked} /> : '—'}
                </span>
              </span>
              <span className="pos-card-cell">
                <span className="pos-card-key">P/L %</span>
                <span className="pos-card-val">{row.hasQuote ? <Value amount={row.plPct} percent /> : '—'}</span>
              </span>
              <span className="pos-card-cell">
                <span className="pos-card-key">Today</span>
                <span className="pos-card-val">{row.hasQuote ? <Value amount={row.dayChangePct} percent /> : '—'}</span>
              </span>
              <span className="pos-card-cell">
                <span className="pos-card-key">Weight</span>
                <span className="pos-card-val">{row.hasQuote ? percent(row.weight, 1) : '—'}</span>
              </span>
              <span className="pos-card-cell">
                <span className="pos-card-key">Shares</span>
                <span className="pos-card-val">{fmtShares(row.shares)}</span>
              </span>
              <span className="pos-card-cell">
                <span className="pos-card-key">Avg cost</span>
                <span className="pos-card-val">{money(row.avgCost, row.currency)}</span>
              </span>
              <span className="pos-card-cell">
                <span className="pos-card-key">Price</span>
                <span className="pos-card-val">
                  {row.hasQuote ? money(row.price / row.fxRate, row.currency) : '—'}
                </span>
              </span>
            </div>
          </div>
        ))}
      </div>

      <p className="sr-only">
        Totals: invested {signedMoney(totals.invested, currency)}, value {signedMoney(totals.value, currency)}, profit or
        loss {signedMoney(totals.pl, currency)} ({signedPercent(totals.invested > 0 ? totals.pl / totals.invested : 0)}).
      </p>
    </>
  )
}
