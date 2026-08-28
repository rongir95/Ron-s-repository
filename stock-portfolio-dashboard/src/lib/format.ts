/** Currency / number / date formatting. All display strings come from here. */

const symbolCache = new Map<string, string>()

/** The bare currency symbol, e.g. "$", "€", "₪" — falls back to the code. */
export function currencySymbol(currency: string): string {
  const hit = symbolCache.get(currency)
  if (hit) return hit
  let out = currency
  try {
    const parts = new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency,
      currencyDisplay: 'narrowSymbol',
    }).formatToParts(0)
    out = parts.find((p) => p.type === 'currency')?.value ?? currency
  } catch {
    /* unknown currency code — keep the code itself */
  }
  symbolCache.set(currency, out)
  return out
}

export function money(value: number, currency = 'USD', opts: { decimals?: number } = {}): string {
  if (!Number.isFinite(value)) return '—'
  const decimals = opts.decimals ?? 2
  try {
    return new Intl.NumberFormat(undefined, {
      style: 'currency',
      currency,
      currencyDisplay: 'narrowSymbol',
      minimumFractionDigits: decimals,
      maximumFractionDigits: decimals,
    }).format(value)
  } catch {
    return `${currencySymbol(currency)}${value.toFixed(decimals)}`
  }
}

/** Signed money, always carrying an explicit + or − (never colour alone). */
export function signedMoney(value: number, currency = 'USD'): string {
  if (!Number.isFinite(value)) return '—'
  const sign = value > 0 ? '+' : value < 0 ? '−' : ''
  return `${sign}${money(Math.abs(value), currency)}`
}

/** Compact money for hero figures and axis ticks: $1.2K, $4.3M. */
export function compactMoney(value: number, currency = 'USD'): string {
  if (!Number.isFinite(value)) return '—'
  const abs = Math.abs(value)
  if (abs < 10_000) return money(value, currency, { decimals: abs < 100 ? 2 : 0 })
  try {
    return new Intl.NumberFormat(undefined, {
      style: 'currency',
      currency,
      currencyDisplay: 'narrowSymbol',
      notation: 'compact',
      maximumFractionDigits: 1,
    }).format(value)
  } catch {
    return money(value, currency, { decimals: 0 })
  }
}

/** Signed compact money, carrying the same explicit minus sign as the rest of
 *  the app (Intl's own compact output uses a plain hyphen). */
export function signedCompactMoney(value: number, currency = 'USD'): string {
  if (!Number.isFinite(value)) return '—'
  const sign = value > 0 ? '+' : value < 0 ? '−' : ''
  return `${sign}${compactMoney(Math.abs(value), currency)}`
}

/** `ratio` is a fraction (0.1234 -> "12.34%"). */
export function percent(ratio: number, decimals = 2): string {
  if (!Number.isFinite(ratio)) return '—'
  return `${(ratio * 100).toFixed(decimals)}%`
}

export function signedPercent(ratio: number, decimals = 2): string {
  if (!Number.isFinite(ratio)) return '—'
  const sign = ratio > 0 ? '+' : ratio < 0 ? '−' : ''
  return `${sign}${Math.abs(ratio * 100).toFixed(decimals)}%`
}

/** ▲ / ▼ / • — the secondary encoding that carries direction without colour. */
export function directionGlyph(value: number): string {
  if (value > 0) return '▲'
  if (value < 0) return '▼'
  return '•'
}

export function shares(value: number): string {
  if (!Number.isFinite(value)) return '—'
  const decimals = Number.isInteger(value) ? 0 : value < 1 ? 6 : 4
  return new Intl.NumberFormat(undefined, {
    minimumFractionDigits: 0,
    maximumFractionDigits: decimals,
  }).format(value)
}

export function relativeTime(from: number, now = Date.now()): string {
  const secs = Math.max(0, Math.round((now - from) / 1000))
  if (secs < 5) return 'just now'
  if (secs < 60) return `${secs}s ago`
  const mins = Math.round(secs / 60)
  if (mins < 60) return `${mins}m ago`
  const hours = Math.round(mins / 60)
  if (hours < 24) return `${hours}h ago`
  return `${Math.round(hours / 24)}d ago`
}

export function shortDate(iso: string): string {
  const d = new Date(`${iso}T00:00:00`)
  if (Number.isNaN(d.getTime())) return iso
  return d.toLocaleDateString(undefined, { month: 'short', day: 'numeric' })
}

export function mediumDate(iso: string): string {
  const d = new Date(`${iso}T00:00:00`)
  if (Number.isNaN(d.getTime())) return iso
  return d.toLocaleDateString(undefined, { year: 'numeric', month: 'short', day: 'numeric' })
}

export function todayIso(now = new Date()): string {
  const y = now.getFullYear()
  const m = `${now.getMonth() + 1}`.padStart(2, '0')
  const d = `${now.getDate()}`.padStart(2, '0')
  return `${y}-${m}-${d}`
}
