/**
 * Portfolio value over time, against the amount invested.
 *
 * Two series, so a legend is always present. Value is the point of the chart
 * (accent hue, area + line); invested is context (de-emphasised grey line), so
 * this is *emphasis* rather than a categorical pair. One y-axis — never two.
 *
 * The container is sized to include the x-axis band, so the card never grows a
 * nested scrollbar.
 */
import { useCallback, useRef, useState } from 'react'
import type { SeriesPoint } from '../../lib/calc'
import { compactMoney, mediumDate, money, signedPercent } from '../../lib/format'

const PAD = { top: 14, right: 14, bottom: 26, left: 58 }

function niceTicks(min: number, max: number, count = 4): number[] {
  if (!(max > min)) return [min]
  const raw = (max - min) / count
  const magnitude = Math.pow(10, Math.floor(Math.log10(raw)))
  const step = [1, 2, 2.5, 5, 10].map((m) => m * magnitude).find((candidate) => candidate >= raw) ?? magnitude * 10
  const ticks: number[] = []
  for (let tick = Math.ceil(min / step) * step; tick <= max + step * 0.001; tick += step) ticks.push(tick)
  return ticks
}

export function PerformanceChart({
  series,
  currency,
  height = 264,
  masked,
}: {
  series: SeriesPoint[]
  currency: string
  height?: number
  masked?: boolean
}) {
  const [active, setActive] = useState<number | null>(null)
  const [width, setWidth] = useState(760)
  const observer = useRef<ResizeObserver | null>(null)

  // A callback ref rather than an effect, so the observer attaches correctly
  // even though this component can mount and unmount with the data.
  const measure = useCallback((node: HTMLDivElement | null) => {
    observer.current?.disconnect()
    observer.current = null
    if (!node) return
    if (node.clientWidth) setWidth(node.clientWidth)
    if (typeof ResizeObserver === 'undefined') return
    const resize = new ResizeObserver((entries) => {
      const measured = entries[0]?.contentRect.width
      if (measured) setWidth(measured)
    })
    resize.observe(node)
    observer.current = resize
  }, [])

  if (series.length < 2) return null

  const values = series.flatMap((point) => [point.value, point.invested])
  const rawMin = Math.min(...values)
  const rawMax = Math.max(...values)
  // Head-room so the line never touches the frame; the axis starts at a nice
  // tick rather than at zero, which would flatten a portfolio's whole shape.
  const span = rawMax - rawMin || rawMax || 1
  const yMin = Math.max(0, rawMin - span * 0.12)
  const yMax = rawMax + span * 0.08
  const ticks = niceTicks(yMin, yMax)

  const plotW = Math.max(width - PAD.left - PAD.right, 10)
  const plotH = Math.max(height - PAD.top - PAD.bottom, 10)
  const x = (index: number) => PAD.left + (index / (series.length - 1)) * plotW
  const y = (value: number) => PAD.top + (1 - (value - yMin) / (yMax - yMin || 1)) * plotH

  const line = (pick: (point: SeriesPoint) => number) =>
    series.map((point, index) => `${index === 0 ? 'M' : 'L'}${x(index).toFixed(2)},${y(pick(point)).toFixed(2)}`).join(' ')

  const valuePath = line((point) => point.value)
  const investedPath = line((point) => point.invested)
  const areaPath = `${valuePath} L${x(series.length - 1).toFixed(2)},${(PAD.top + plotH).toFixed(2)} L${x(0).toFixed(2)},${(PAD.top + plotH).toFixed(2)} Z`

  const first = series[0]
  const last = series[series.length - 1]
  const periodReturn = first.value > 0 ? last.value / first.value - 1 : 0

  const point = active != null ? series[active] : null
  const pointPl = point ? point.value - point.invested : 0

  // x-axis: label count scales with the available width, so the dates never
  // collide on a phone.
  const maxLabels = width < 420 ? 3 : width < 700 ? 4 : 6
  const labelStep = Math.max(1, Math.ceil((series.length - 1) / (maxLabels - 1)))

  const onMove = (event: React.PointerEvent<SVGSVGElement>) => {
    const rect = event.currentTarget.getBoundingClientRect()
    const ratio = (event.clientX - rect.left - PAD.left) / plotW
    const index = Math.round(ratio * (series.length - 1))
    setActive(Math.min(series.length - 1, Math.max(0, index)))
  }

  return (
    <div className="chart-holder" ref={measure}>
      <div className="row-wrap" style={{ justifyContent: 'space-between', marginBottom: 8 }}>
        <div className="legend">
          <span className="legend-item">
            <svg width="16" height="8" aria-hidden="true">
              <line x1="0" y1="4" x2="16" y2="4" stroke="var(--accent)" strokeWidth="2" />
            </svg>
            Portfolio value
          </span>
          <span className="legend-item">
            <svg width="16" height="8" aria-hidden="true">
              <line x1="0" y1="4" x2="16" y2="4" stroke="var(--series-other)" strokeWidth="2" />
            </svg>
            Amount invested
          </span>
        </div>
        <span style={{ fontSize: 12, color: 'var(--text-3)' }}>
          Value over the period{' '}
          <strong className={periodReturn >= 0 ? 'v-gain' : 'v-loss'}>{signedPercent(periodReturn, 1)}</strong>
        </span>
      </div>

      <svg
        viewBox={`0 0 ${width} ${height}`}
        width="100%"
        height={height}
        className="chart-svg"
        role="img"
        aria-label={`Portfolio value from ${mediumDate(first.date)} to ${mediumDate(last.date)}`}
        onPointerMove={onMove}
        onPointerLeave={() => setActive(null)}
      >
        {/* Recessive solid hairline grid — never dashed. */}
        {ticks.map((tick) => (
          <g key={tick}>
            <line x1={PAD.left} y1={y(tick)} x2={PAD.left + plotW} y2={y(tick)} className="chart-grid" />
            <text x={PAD.left - 8} y={y(tick) + 3.5} textAnchor="end">
              {masked ? '•••' : compactMoney(tick, currency)}
            </text>
          </g>
        ))}

        <defs>
          <linearGradient id="value-fill" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stopColor="var(--accent)" stopOpacity="0.20" />
            <stop offset="100%" stopColor="var(--accent)" stopOpacity="0.01" />
          </linearGradient>
        </defs>
        <path d={areaPath} fill="url(#value-fill)" />
        <path d={investedPath} fill="none" stroke="var(--series-other)" strokeWidth={2} strokeLinecap="round" />
        <path d={valuePath} fill="none" stroke="var(--accent)" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" />

        <line x1={PAD.left} y1={PAD.top + plotH} x2={PAD.left + plotW} y2={PAD.top + plotH} className="chart-axis" />

        {series.map((entry, index) =>
          index % labelStep === 0 || index === series.length - 1 ? (
            <text
              key={entry.date}
              x={x(index)}
              y={height - 8}
              textAnchor={index === 0 ? 'start' : index === series.length - 1 ? 'end' : 'middle'}
            >
              {mediumDate(entry.date).replace(/,? \d{4}$/, '')}
            </text>
          ) : null,
        )}

        {point && active != null && (
          <g pointerEvents="none">
            <line x1={x(active)} y1={PAD.top} x2={x(active)} y2={PAD.top + plotH} className="chart-axis" />
            {/* 2px surface ring so the marker reads over the line it sits on. */}
            <circle cx={x(active)} cy={y(point.value)} r={4.5} fill="var(--accent)" stroke="var(--surface)" strokeWidth={2} />
            <circle cx={x(active)} cy={y(point.invested)} r={4} fill="var(--series-other)" stroke="var(--surface)" strokeWidth={2} />
          </g>
        )}
      </svg>

      {point && active != null && (
        <div
          className="tooltip"
          style={{
            left: Math.min(Math.max(x(active), 84), width - 84),
            top: y(point.value),
          }}
        >
          <div className="tooltip-title">{mediumDate(point.date)}</div>
          <div className="tooltip-row">
            <span>
              <span className="swatch" style={{ background: 'var(--accent)' }} /> Value
            </span>
            <span className={masked ? 'privacy-mask' : undefined}>{money(point.value, currency, { decimals: 0 })}</span>
          </div>
          <div className="tooltip-row">
            <span>
              <span className="swatch" style={{ background: 'var(--series-other)' }} /> Invested
            </span>
            <span className={masked ? 'privacy-mask' : undefined}>{money(point.invested, currency, { decimals: 0 })}</span>
          </div>
          <div className="tooltip-row" style={{ marginTop: 4, borderTop: '1px solid var(--border)', paddingTop: 4 }}>
            <span>Profit / loss</span>
            <strong className={pointPl >= 0 ? 'v-gain' : 'v-loss'}>
              <span aria-hidden="true">{pointPl >= 0 ? '▲' : '▼'}</span>{' '}
              <span className={masked ? 'privacy-mask' : undefined}>
                {money(Math.abs(pointPl), currency, { decimals: 0 })}
              </span>
            </strong>
          </div>
        </div>
      )}
    </div>
  )
}
