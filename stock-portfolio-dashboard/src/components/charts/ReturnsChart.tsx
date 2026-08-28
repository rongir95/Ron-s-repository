/**
 * Return by holding — a diverging bar chart centred on zero.
 *
 * Polarity is the data's job here, so the gain/loss pair does the encoding —
 * and each bar's side of the baseline plus its signed, arrowed label mean
 * direction is never carried by colour alone. Sorted best to worst, so the two
 * ends of the chart are the best and worst performers.
 *
 * Built in CSS grid rather than SVG: the bars are simple rectangles, and this
 * keeps the labels as real, crisp, selectable text at any width.
 */
import type { PositionMetrics } from '../../lib/calc'
import { signedMoney, signedPercent } from '../../lib/format'

export function ReturnsChart({
  positions,
  currency,
  masked,
  metric,
}: {
  positions: PositionMetrics[]
  currency: string
  masked?: boolean
  metric: 'percent' | 'amount'
}) {
  const rows = positions
    .filter((position) => position.hasQuote)
    .map((position) => ({ position, value: metric === 'percent' ? position.plPct : position.pl }))
    .sort((a, b) => b.value - a.value)

  if (!rows.length) {
    return <p style={{ color: 'var(--text-3)', fontSize: 13, margin: 0 }}>No priced holdings yet.</p>
  }

  const extent = Math.max(...rows.map((row) => Math.abs(row.value)), metric === 'percent' ? 0.02 : 1)

  return (
    <div className="diverge" role="img" aria-label={metric === 'percent' ? 'Return by holding, best to worst' : 'Profit and loss by holding, best to worst'}>
      {rows.map(({ position, value }) => {
        const positive = value >= 0
        const width = `${Math.max((Math.abs(value) / extent) * 100, 1.2)}%`
        const title = `${position.symbol}: ${signedPercent(position.plPct)} · ${signedMoney(position.pl, currency)}`
        return (
          <div className="diverge-row" key={position.id} title={title}>
            <span className="diverge-label">{position.symbol}</span>
            <span className="diverge-arm neg">
              {!positive && <span className="diverge-bar loss" style={{ width }} />}
            </span>
            <span className="diverge-arm pos">
              {positive && <span className="diverge-bar gain" style={{ width }} />}
            </span>
            <span className={`diverge-value ${positive ? 'v-gain' : 'v-loss'}`}>
              <span className="arrow" aria-hidden="true">
                {positive ? '▲' : '▼'}
              </span>{' '}
              <span className={metric === 'amount' && masked ? 'privacy-mask' : undefined}>
                {metric === 'percent' ? signedPercent(value, 1) : signedMoney(value, currency)}
              </span>
            </span>
          </div>
        )
      })}
    </div>
  )
}
