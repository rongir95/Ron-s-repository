/**
 * Portfolio allocation — a donut pie chart with a labelled legend.
 *
 * A pie was asked for directly. It is a genuinely risky form for comparing
 * close values, so two things carry the precision the angles cannot: every
 * slice is direct-labelled with its exact percentage in the legend, and the
 * holdings table below states every figure in text. Three of the light-mode
 * series hues also sit below 3:1 against the surface, so those labels are the
 * contrast relief as well — identity never rests on colour alone.
 *
 * The hole in the middle carries the total, which is the number the chart is
 * a breakdown of.
 *
 * Holdings past the eighth fold into one neutral "Other" slice; the validated
 * palette is never cycled into a ninth generated hue.
 */
import { useState } from 'react'
import type { PositionMetrics } from '../../lib/calc'
import { compactMoney, money, percent, signedMoney, signedPercent } from '../../lib/format'
import { seriesColor } from '../../lib/series'
import { OTHER_SLOT } from '../../store/store'

interface Slice {
  key: string
  label: string
  sublabel?: string
  value: number
  weight: number
  pl: number
  plPct: number
  /** False when this slice is sized by cost, so profit/loss is unknown. */
  hasPl: boolean
  color: string
  /** Symbols folded into this slice, when it is the "Other" aggregate. */
  members?: string[]
}

/**
 * What the slices are sized by. Market value is the point of the chart, but it
 * needs live prices — so with no prices available we fall back to the amount
 * invested, which is knowable from the purchase records alone. A pie of
 * nothing would be the worse answer.
 */
type Basis = 'value' | 'cost'

function buildSlices(positions: PositionMetrics[]): { slices: Slice[]; basis: Basis } {
  const priced = positions.filter((position) => position.hasQuote && position.marketValue > 0)
  const basis: Basis = priced.length ? 'value' : 'cost'
  const source = basis === 'value' ? priced : positions.filter((position) => position.costBasis > 0)
  const amountOf = (position: PositionMetrics) =>
    basis === 'value' ? position.marketValue : position.costBasis

  const total = source.reduce((sum, position) => sum + amountOf(position), 0)
  // Weights are derived from this chart's own total rather than read off the
  // position, so they stay correct on either basis.
  const weightOf = (amount: number) => (total > 0 ? amount / total : 0)

  const named = source.filter((position) => position.colorSlot < OTHER_SLOT)
  const tail = source.filter((position) => position.colorSlot >= OTHER_SLOT)

  const slices: Slice[] = named
    .map((position) => ({
      key: position.id,
      label: position.symbol,
      sublabel: position.name,
      value: amountOf(position),
      weight: weightOf(amountOf(position)),
      pl: position.pl,
      plPct: position.plPct,
      hasPl: position.hasQuote,
      color: seriesColor(position.colorSlot),
    }))
    .sort((a, b) => b.weight - a.weight)

  if (tail.length) {
    const amount = tail.reduce((sum, p) => sum + amountOf(p), 0)
    const cost = tail.reduce((sum, p) => sum + p.costBasis, 0)
    const pl = tail.reduce((sum, p) => sum + p.pl, 0)
    slices.push({
      key: '__other__',
      label: `Other (${tail.length})`,
      value: amount,
      weight: weightOf(amount),
      pl,
      plPct: cost > 0 ? pl / cost : 0,
      hasPl: tail.every((p) => p.hasQuote),
      color: 'var(--series-other)',
      members: tail.map((p) => p.symbol),
    })
  }
  return { slices, basis }
}

const SIZE = 208
const R_OUTER = 100
const R_INNER = 62
const CENTRE = SIZE / 2

/** Polar to cartesian, with 0 radians at twelve o'clock, running clockwise. */
function point(angle: number, radius: number) {
  return {
    x: CENTRE + radius * Math.sin(angle),
    y: CENTRE - radius * Math.cos(angle),
  }
}

function arcPath(start: number, end: number): string {
  const largeArc = end - start > Math.PI ? 1 : 0
  const o1 = point(start, R_OUTER)
  const o2 = point(end, R_OUTER)
  const i2 = point(end, R_INNER)
  const i1 = point(start, R_INNER)
  return [
    `M${o1.x.toFixed(2)},${o1.y.toFixed(2)}`,
    `A${R_OUTER},${R_OUTER} 0 ${largeArc} 1 ${o2.x.toFixed(2)},${o2.y.toFixed(2)}`,
    `L${i2.x.toFixed(2)},${i2.y.toFixed(2)}`,
    `A${R_INNER},${R_INNER} 0 ${largeArc} 0 ${i1.x.toFixed(2)},${i1.y.toFixed(2)}`,
    'Z',
  ].join(' ')
}

export function AllocationChart({
  positions,
  currency,
  masked,
}: {
  positions: PositionMetrics[]
  currency: string
  masked?: boolean
}) {
  const [active, setActive] = useState<string | null>(null)
  const { slices, basis } = buildSlices(positions)

  if (!slices.length) {
    return (
      <p style={{ color: 'var(--text-3)', fontSize: 13, margin: 0 }}>
        {positions.length
          ? 'Your holdings have no share count or purchase price recorded yet, so there is nothing to break down. Edit a holding to add them.'
          : 'Add a holding and it will appear here, broken down by stock.'}
      </p>
    )
  }

  const total = slices.reduce((sum, slice) => sum + slice.value, 0)
  const hovered = slices.find((slice) => slice.key === active)

  // Lay the slices out clockwise from twelve o'clock, largest first.
  let cursor = 0
  const laid = slices.map((slice) => {
    const sweep = total > 0 ? (slice.value / total) * Math.PI * 2 : 0
    const start = cursor
    cursor += sweep
    return { slice, start, end: start + sweep }
  })

  const single = laid.length === 1

  return (
    <div className="alloc">
      {basis === 'cost' && (
        <p className="alloc-basis">
          Live prices are unavailable, so these slices are sized by what you paid rather than what the holdings are
          worth now.
        </p>
      )}

      <div className="alloc-chart chart-holder">
        <svg
          viewBox={`0 0 ${SIZE} ${SIZE}`}
          className="chart-svg"
          role="img"
          aria-label={`Allocation by holding: ${slices
            .map((slice) => `${slice.label} ${percent(slice.weight, 1)}`)
            .join(', ')}`}
          onMouseLeave={() => setActive(null)}
        >
          {single ? (
            // One holding is the whole pie; a full-circle arc cannot be drawn
            // with a single path command, so stroke a ring instead.
            <circle
              cx={CENTRE}
              cy={CENTRE}
              r={(R_OUTER + R_INNER) / 2}
              fill="none"
              stroke={laid[0].slice.color}
              strokeWidth={R_OUTER - R_INNER}
              onMouseEnter={() => setActive(laid[0].slice.key)}
            />
          ) : (
            laid.map(({ slice, start, end }) => (
              <path
                key={slice.key}
                d={arcPath(start, end)}
                fill={slice.color}
                /* A 2px surface stroke, not a border: it reads as a gap
                   between neighbouring fills. */
                stroke="var(--surface)"
                strokeWidth={2}
                opacity={active && active !== slice.key ? 0.35 : 1}
                style={{ transition: 'opacity 120ms ease', cursor: 'pointer' }}
                onMouseEnter={() => setActive(slice.key)}
              >
                <title>{`${slice.label} — ${percent(slice.weight, 1)}`}</title>
              </path>
            ))
          )}

          {/* The hole carries what the chart is a breakdown of — or, on hover,
              the slice under the pointer. */}
          <text x={CENTRE} y={CENTRE - 6} textAnchor="middle" className="alloc-hole-label">
            {hovered ? hovered.label : basis === 'cost' ? 'Invested' : 'Total'}
          </text>
          <text x={CENTRE} y={CENTRE + 14} textAnchor="middle" className="alloc-hole-value">
            {masked ? '•••' : compactMoney(hovered ? hovered.value : total, currency)}
          </text>
        </svg>

      </div>

      {/* The legend direct-labels every slice — the precision the angles cannot carry. */}
      <ul className="alloc-legend">
        {slices.map((slice) => (
          <li
            key={slice.key}
            className="alloc-legend-item"
            data-active={active === slice.key}
            onMouseEnter={() => setActive(slice.key)}
            onMouseLeave={() => setActive(null)}
          >
            <span className="swatch" style={{ background: slice.color }} aria-hidden="true" />
            <span className="alloc-legend-sym">{slice.label}</span>
            <span className="alloc-legend-pct">{percent(slice.weight, 1)}</span>
            <span className={`alloc-legend-val ${masked ? 'privacy-mask' : ''}`}>
              {compactMoney(slice.value, currency)}
            </span>
          </li>
        ))}
      </ul>

      {/*
        Hover detail goes in a reserved strip rather than a floating tooltip: the
        donut is only ~200px across, so a box big enough to hold these four
        figures would cover the very slice being inspected. The height is fixed
        so hovering never shifts the layout.
      */}
      <div className="alloc-detail" aria-live="polite">
        {hovered ? (
          <>
            <span className="alloc-detail-head">
              <span className="swatch" style={{ background: hovered.color }} aria-hidden="true" />
              <strong>{hovered.label}</strong>
              {hovered.sublabel && <span className="alloc-detail-name">{hovered.sublabel}</span>}
              {hovered.members && <span className="alloc-detail-name">{hovered.members.join(', ')}</span>}
            </span>
            <span className="alloc-detail-figs">
              <span>
                <span className="alloc-detail-key">{basis === 'cost' ? 'Invested' : 'Value'}</span>
                <strong className={masked ? 'privacy-mask' : undefined}>{money(hovered.value, currency)}</strong>
              </span>
              <span>
                <span className="alloc-detail-key">Share</span>
                <strong>{percent(hovered.weight, 1)}</strong>
              </span>
              {hovered.hasPl && (
                <span>
                  <span className="alloc-detail-key">Profit / loss</span>
                  <strong className={hovered.pl >= 0 ? 'v-gain' : 'v-loss'}>
                    <span aria-hidden="true">{hovered.pl >= 0 ? '▲' : '▼'}</span>{' '}
                    <span className={masked ? 'privacy-mask' : undefined}>{signedMoney(hovered.pl, currency)}</span>
                    <span style={{ fontWeight: 500 }}> ({signedPercent(hovered.plPct, 1)})</span>
                  </strong>
                </span>
              )}
            </span>
          </>
        ) : (
          <span className="alloc-detail-hint">
            {basis === 'cost'
              ? 'Hover a slice for the amount invested and its share.'
              : 'Hover a slice for its value, share and profit or loss.'}
          </span>
        )}
      </div>
    </div>
  )
}
