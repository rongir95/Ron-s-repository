/**
 * Portfolio allocation — part-to-whole.
 *
 * A horizontal stacked bar (the recommended form for part-to-whole with many,
 * long-named categories) over a ranked bar list that direct-labels every
 * holding. Three of the light-mode series hues sit below 3:1 against the
 * surface, so the relief rule applies: the labels here and the positions table
 * carry the identity, never colour alone.
 *
 * Holdings past the eighth fold into a single neutral "Other" segment — the
 * palette is never cycled.
 */
import { useState } from 'react'
import type { PositionMetrics } from '../../lib/calc'
import { money, percent } from '../../lib/format'
import { seriesColor } from '../../lib/series'
import { OTHER_SLOT } from '../../store/store'

interface Slice {
  key: string
  label: string
  sublabel?: string
  value: number
  weight: number
  color: string
}

function buildSlices(positions: PositionMetrics[]): Slice[] {
  const priced = positions.filter((position) => position.hasQuote && position.marketValue > 0)
  const named = priced.filter((position) => position.colorSlot < OTHER_SLOT)
  const tail = priced.filter((position) => position.colorSlot >= OTHER_SLOT)

  const slices: Slice[] = named
    .map((position) => ({
      key: position.id,
      label: position.symbol,
      sublabel: position.name,
      value: position.marketValue,
      weight: position.weight,
      color: seriesColor(position.colorSlot),
    }))
    .sort((a, b) => b.weight - a.weight)

  if (tail.length) {
    slices.push({
      key: '__other__',
      label: `Other (${tail.length})`,
      sublabel: tail.map((position) => position.symbol).join(', '),
      value: tail.reduce((sum, position) => sum + position.marketValue, 0),
      weight: tail.reduce((sum, position) => sum + position.weight, 0),
      color: 'var(--series-other)',
    })
  }
  return slices
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
  const [hovered, setHovered] = useState<string | null>(null)
  const slices = buildSlices(positions)

  if (!slices.length) {
    return <p style={{ color: 'var(--text-3)', fontSize: 13, margin: 0 }}>No priced holdings to allocate yet.</p>
  }

  const maxWeight = Math.max(...slices.map((slice) => slice.weight))

  return (
    <div>
      <div className="alloc-bar" role="img" aria-label="Allocation by holding">
        {slices.map((slice) => (
          <div
            key={slice.key}
            className="alloc-seg"
            style={{
              flexGrow: Math.max(slice.weight, 0.005),
              background: slice.color,
              opacity: hovered && hovered !== slice.key ? 0.4 : 1,
              transition: 'opacity 120ms ease',
            }}
            onMouseEnter={() => setHovered(slice.key)}
            onMouseLeave={() => setHovered(null)}
            title={`${slice.label} — ${percent(slice.weight, 1)}`}
          />
        ))}
      </div>

      <div className="alloc-list">
        {slices.map((slice) => (
          <div
            key={slice.key}
            className="alloc-row"
            onMouseEnter={() => setHovered(slice.key)}
            onMouseLeave={() => setHovered(null)}
          >
            <span className="alloc-name" title={slice.sublabel}>
              <span className="swatch" style={{ background: slice.color }} aria-hidden="true" />
              {slice.label}
            </span>
            <span className="alloc-track">
              {/* Bar length is the weight relative to the largest holding, so
                  small positions stay visible; the % label carries the truth. */}
              <span
                className="alloc-fill"
                style={{
                  width: `${Math.max((slice.weight / maxWeight) * 100, 1.5)}%`,
                  background: slice.color,
                  opacity: hovered && hovered !== slice.key ? 0.45 : 1,
                  transition: 'opacity 120ms ease',
                }}
              />
            </span>
            <span className="alloc-value">
              <strong style={{ color: 'var(--text)' }}>{percent(slice.weight, 1)}</strong>
              <span className={masked ? 'privacy-mask' : undefined}> · {money(slice.value, currency, { decimals: 0 })}</span>
            </span>
          </div>
        ))}
      </div>
    </div>
  )
}
