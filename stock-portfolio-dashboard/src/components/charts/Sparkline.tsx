/**
 * A 30-ish point sparkline for a table row. No axes, no labels — the numeric
 * change sits beside it in the row, so the line only has to carry shape.
 */
export function Sparkline({
  values,
  width = 92,
  height = 26,
  label,
}: {
  values: number[]
  width?: number
  height?: number
  label?: string
}) {
  const clean = values.filter((value) => Number.isFinite(value))
  if (clean.length < 2) {
    return (
      <svg width={width} height={height} role="presentation" className="chart-svg" style={{ width, height }}>
        <line
          x1={0}
          y1={height / 2}
          x2={width}
          y2={height / 2}
          className="chart-axis"
        />
      </svg>
    )
  }

  const min = Math.min(...clean)
  const max = Math.max(...clean)
  const span = max - min || 1
  const pad = 2
  const stepX = (width - pad * 2) / (clean.length - 1)
  const y = (value: number) => pad + (1 - (value - min) / span) * (height - pad * 2)

  const path = clean.map((value, index) => `${index === 0 ? 'M' : 'L'}${(pad + index * stepX).toFixed(2)},${y(value).toFixed(2)}`).join(' ')
  const rising = clean[clean.length - 1] >= clean[0]
  const stroke = rising ? 'var(--gain)' : 'var(--loss)'

  return (
    <svg
      width={width}
      height={height}
      viewBox={`0 0 ${width} ${height}`}
      className="chart-svg"
      style={{ width, height }}
      role="img"
      aria-label={label ?? (rising ? 'Trending up over the period' : 'Trending down over the period')}
    >
      <path d={path} fill="none" stroke={stroke} strokeWidth={1.5} strokeLinecap="round" strokeLinejoin="round" />
      <circle cx={pad + (clean.length - 1) * stepX} cy={y(clean[clean.length - 1])} r={2.2} fill={stroke} />
    </svg>
  )
}
