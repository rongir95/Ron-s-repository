/**
 * Unit checks for the portfolio maths. Run with `npm test`.
 *
 * Deliberately dependency-free — a handful of assertions and a tiny runner, so
 * there is no test framework to install or keep in sync, and the file typechecks
 * inside the same project as the app (no Node-only APIs).
 */
import type { Portfolio, Position } from '../types'
import type { HistoryPoint, Quote } from '../market/types'
import {
  annualisedReturn,
  averageCost,
  buildCashFlows,
  buildSeries,
  computePortfolio,
  fxRateFor,
  nativeCostBasis,
  totalShares,
} from './calc'

const assert = {
  ok(condition: unknown, message?: string): void {
    if (!condition) throw new Error(message ?? 'expected a truthy value')
  },
  equal(actual: unknown, expected: unknown, message?: string): void {
    if (actual !== expected) {
      throw new Error(message ?? `expected ${JSON.stringify(actual)} to equal ${JSON.stringify(expected)}`)
    }
  },
  deepEqual(actual: unknown, expected: unknown, message?: string): void {
    if (JSON.stringify(actual) !== JSON.stringify(expected)) {
      throw new Error(message ?? `expected ${JSON.stringify(actual)} to deep-equal ${JSON.stringify(expected)}`)
    }
  },
}

let passed = 0
const failures: string[] = []
function test(name: string, fn: () => void) {
  try {
    fn()
    passed++
  } catch (err) {
    failures.push(`${name}\n    ${(err as Error).message.split('\n').join('\n    ')}`)
  }
}
const close = (a: number, b: number, eps = 1e-6, msg?: string) =>
  assert.ok(Math.abs(a - b) < eps, msg ?? `expected ${a} to be within ${eps} of ${b}`)

// --- fixtures -------------------------------------------------------------

function position(over: Partial<Position> & { symbol: string; lots: Position['lots'] }): Position {
  return { id: `p-${over.symbol}`, colorSlot: 0, createdAt: '2024-01-01T00:00:00.000Z', ...over }
}
function portfolio(positions: Position[], baseCurrency = 'USD'): Portfolio {
  return { id: 'pf', name: 'Test', baseCurrency, positions, createdAt: '2024-01-01T00:00:00.000Z' }
}
function quote(symbol: string, price: number, previousClose: number, currency = 'USD'): Quote {
  return { symbol, price, previousClose, currency }
}

// --- lot maths ------------------------------------------------------------

test('averages several lots bought at different prices by share weight', () => {
  const p = position({
    symbol: 'AAPL',
    lots: [
      { id: 'l1', shares: 10, price: 100 },
      { id: 'l2', shares: 30, price: 200 },
    ],
  })
  close(totalShares(p), 40)
  close(nativeCostBasis(p), 10 * 100 + 30 * 200)
  // Weighted, not the naive (100+200)/2 = 150.
  close(averageCost(p), 7000 / 40)
  close(averageCost(p), 175)
})

test('an empty position does not divide by zero', () => {
  const p = position({ symbol: 'X', lots: [] })
  close(totalShares(p), 0)
  close(averageCost(p), 0)
})

test('handles fractional shares', () => {
  const p = position({ symbol: 'AMZN', lots: [{ id: 'l1', shares: 0.375, price: 160 }] })
  close(nativeCostBasis(p), 60)
  close(averageCost(p), 160)
})

// --- position + portfolio metrics ----------------------------------------

test('computes value, P/L and day change for a gaining position', () => {
  const p = position({ symbol: 'AAPL', lots: [{ id: 'l1', shares: 10, price: 100 }] })
  const m = computePortfolio(portfolio([p]), { AAPL: quote('AAPL', 150, 140) })
  const row = m.positions[0]
  close(row.marketValue, 1500)
  close(row.costBasis, 1000)
  close(row.pl, 500)
  close(row.plPct, 0.5)
  close(row.dayChange, 100) // 10 shares x (150 - 140)
  close(row.dayChangePct, 150 / 140 - 1)
  close(row.weight, 1)
})

test('losses come through negative, not absolute', () => {
  const p = position({ symbol: 'NKE', lots: [{ id: 'l1', shares: 5, price: 120 }] })
  const m = computePortfolio(portfolio([p]), { NKE: quote('NKE', 90, 95) })
  close(m.totalPl, -150)
  close(m.totalPlPct, -0.25)
  close(m.dayChange, -25)
  assert.ok(m.totalPl < 0)
})

test('weights across holdings sum to 1 and identify the largest', () => {
  const positions = [
    position({ symbol: 'A', lots: [{ id: 'l1', shares: 10, price: 10 }] }),
    position({ symbol: 'B', lots: [{ id: 'l2', shares: 10, price: 10 }] }),
    position({ symbol: 'C', lots: [{ id: 'l3', shares: 10, price: 10 }] }),
  ]
  const m = computePortfolio(portfolio(positions), {
    A: quote('A', 50, 50),
    B: quote('B', 30, 30),
    C: quote('C', 20, 20),
  })
  close(m.totalValue, 1000)
  close(m.positions.reduce((s, r) => s + r.weight, 0), 1)
  close(m.positions[0].weight, 0.5)
  assert.equal(m.largest?.symbol, 'A')
  close(m.concentration, 0.5)
})

test('picks best and worst performers by percentage, not amount', () => {
  const positions = [
    // +10% on a big position = +$1000 in absolute terms…
    position({ symbol: 'BIG', lots: [{ id: 'l1', shares: 100, price: 100 }] }),
    // …but +50% on a small one is the better performer.
    position({ symbol: 'SMALL', lots: [{ id: 'l2', shares: 1, price: 100 }] }),
    position({ symbol: 'DOWN', lots: [{ id: 'l3', shares: 1, price: 100 }] }),
  ]
  const m = computePortfolio(portfolio(positions), {
    BIG: quote('BIG', 110, 110),
    SMALL: quote('SMALL', 150, 150),
    DOWN: quote('DOWN', 70, 70),
  })
  assert.equal(m.best?.symbol, 'SMALL')
  assert.equal(m.worst?.symbol, 'DOWN')
})

test('a single holding has no "worst" performer to contrast against', () => {
  const m = computePortfolio(
    portfolio([position({ symbol: 'A', lots: [{ id: 'l1', shares: 1, price: 1 }] })]),
    { A: quote('A', 2, 2) },
  )
  assert.equal(m.best?.symbol, 'A')
  assert.equal(m.worst, undefined)
})

test('an unpriced holding is quarantined instead of silently valued at zero', () => {
  const positions = [
    position({ symbol: 'AAPL', lots: [{ id: 'l1', shares: 10, price: 100 }] }),
    position({ symbol: 'WAT', lots: [{ id: 'l2', shares: 10, price: 100 }] }),
  ]
  const m = computePortfolio(portfolio(positions), { AAPL: quote('AAPL', 150, 150) })
  assert.equal(m.unpriced.length, 1)
  assert.equal(m.unpriced[0].symbol, 'WAT')
  // The unpriced holding drags neither the value nor the invested total.
  close(m.totalValue, 1500)
  close(m.totalInvested, 1000)
  close(m.totalPlPct, 0.5)
})

test('an empty portfolio yields zeros, not NaN', () => {
  const m = computePortfolio(portfolio([]), {})
  close(m.totalValue, 0)
  close(m.totalInvested, 0)
  close(m.totalPl, 0)
  close(m.totalPlPct, 0)
  close(m.dayChangePct, 0)
  assert.equal(m.best, undefined)
})

test('a missing previous close falls back to the current price (no fake day move)', () => {
  const p = position({ symbol: 'A', lots: [{ id: 'l1', shares: 10, price: 5 }] })
  const m = computePortfolio(portfolio([p]), { A: { symbol: 'A', price: 10, previousClose: 0, currency: 'USD' } })
  close(m.dayChange, 0)
  close(m.dayChangePct, 0)
})

// --- currency -------------------------------------------------------------

test('converts a foreign-currency holding into the base currency', () => {
  const p = position({ symbol: 'TEVA.TA', lots: [{ id: 'l1', shares: 100, price: 10 }] })
  const m = computePortfolio(portfolio([p], 'USD'), { 'TEVA.TA': quote('TEVA.TA', 20, 20, 'ILS') }, { 'ILS->USD': 0.27 })
  const row = m.positions[0]
  assert.equal(row.converted, true)
  close(row.fxRate, 0.27)
  close(row.marketValue, 100 * 20 * 0.27)
  close(row.costBasis, 100 * 10 * 0.27)
  // Converting both sides at one rate leaves P/L% currency-invariant.
  close(row.plPct, 1)
  assert.equal(m.mixedCurrency, true)
})

test('fx lookup uses the inverse rate when only the reverse pair is known', () => {
  close(fxRateFor('USD', 'ILS', { 'ILS->USD': 0.25 }), 4)
  close(fxRateFor('USD', 'USD', {}), 1)
  close(fxRateFor('USD', 'EUR', {}), 1) // unknown -> no conversion rather than a wrong one
})

// --- history series -------------------------------------------------------

const hist = (pairs: [string, number][]): HistoryPoint[] => pairs.map(([date, cl]) => ({ date, close: cl }))

test('values undated lots across the whole window', () => {
  const p = position({ symbol: 'A', lots: [{ id: 'l1', shares: 10, price: 100 }] })
  const series = buildSeries([p], { A: hist([['2024-01-01', 100], ['2024-01-02', 110]]) }, 'USD')
  assert.equal(series.length, 2)
  close(series[0].value, 1000)
  close(series[1].value, 1100)
  close(series[0].invested, 1000)
  close(series[1].invested, 1000)
})

test('a dated lot only counts from its purchase date onward', () => {
  const p = position({
    symbol: 'A',
    lots: [
      { id: 'l1', shares: 10, price: 100, date: '2024-01-01' },
      { id: 'l2', shares: 10, price: 120, date: '2024-01-03' },
    ],
  })
  const series = buildSeries(
    [p],
    { A: hist([['2024-01-01', 100], ['2024-01-02', 110], ['2024-01-03', 120]]) },
    'USD',
  )
  close(series[0].value, 1000)
  close(series[0].invested, 1000)
  close(series[1].value, 1100) // still only the first lot
  close(series[1].invested, 1000)
  close(series[2].value, 20 * 120) // both lots now held
  close(series[2].invested, 1000 + 1200)
})

test('forward-fills a gap in one symbol rather than dropping to zero', () => {
  const positions = [
    position({ symbol: 'A', lots: [{ id: 'l1', shares: 1, price: 1 }] }),
    position({ symbol: 'B', lots: [{ id: 'l2', shares: 1, price: 1 }] }),
  ]
  const series = buildSeries(
    positions,
    {
      A: hist([['2024-01-01', 100], ['2024-01-02', 100], ['2024-01-03', 100]]),
      B: hist([['2024-01-01', 50], ['2024-01-03', 60]]), // 01-02 missing
    },
    'USD',
  )
  close(series[1].value, 150) // B carried forward at 50, not 0
  close(series[2].value, 160)
})

test('back-fills a late-listing holding so the series has no spurious dip', () => {
  const positions = [
    position({ symbol: 'OLD', lots: [{ id: 'l1', shares: 1, price: 1 }] }),
    position({ symbol: 'NEW', lots: [{ id: 'l2', shares: 1, price: 1 }] }),
  ]
  const series = buildSeries(
    positions,
    {
      OLD: hist([['2024-01-01', 100], ['2024-01-02', 100]]),
      NEW: hist([['2024-01-02', 40]]), // no data on 01-01
    },
    'USD',
  )
  close(series[0].value, 140) // NEW valued at its first known close
})

test('no history yields an empty series rather than a broken chart', () => {
  assert.deepEqual(buildSeries([position({ symbol: 'A', lots: [] })], {}, 'USD'), [])
})

// --- annualised return ----------------------------------------------------

test('annualises a simple doubling over two years to roughly 41%', () => {
  const p = position({ symbol: 'A', lots: [{ id: 'l1', shares: 10, price: 100, date: '2022-01-01' }] })
  const m = computePortfolio(portfolio([p]), { A: quote('A', 200, 200) })
  const rate = annualisedReturn(buildCashFlows([p], m, '2024-01-01'))
  assert.ok(rate !== null, 'expected a rate')
  close(rate!, Math.pow(2, 1 / 2) - 1, 1e-3) // ~0.4142
})

test('a one-year flat portfolio annualises to zero', () => {
  const p = position({ symbol: 'A', lots: [{ id: 'l1', shares: 1, price: 100, date: '2023-01-01' }] })
  const m = computePortfolio(portfolio([p]), { A: quote('A', 100, 100) })
  close(annualisedReturn(buildCashFlows([p], m, '2024-01-01'))!, 0, 1e-6)
})

test('weights later contributions less — two dated lots solve to one rate', () => {
  const p = position({
    symbol: 'A',
    lots: [
      { id: 'l1', shares: 1, price: 100, date: '2022-01-01' },
      { id: 'l2', shares: 1, price: 100, date: '2023-01-01' },
    ],
  })
  const m = computePortfolio(portfolio([p]), { A: quote('A', 150, 150) })
  const rate = annualisedReturn(buildCashFlows([p], m, '2024-01-01'))!
  // 200 in (staggered) -> 300 today. Verify by discounting at the solved rate.
  const npvAtRate =
    -100 / Math.pow(1 + rate, 0) +
    -100 / Math.pow(1 + rate, 1) +
    300 / Math.pow(1 + rate, 2)
  close(npvAtRate, 0, 1e-4)
  assert.ok(rate > 0.2 && rate < 0.35, `unexpected rate ${rate}`)
})

test('declines to annualise when any lot has no purchase date', () => {
  const p = position({ symbol: 'A', lots: [{ id: 'l1', shares: 1, price: 100 }] })
  const m = computePortfolio(portfolio([p]), { A: quote('A', 200, 200) })
  assert.equal(buildCashFlows([p], m, '2024-01-01'), null)
  assert.equal(annualisedReturn(null), null)
})

test('declines to annualise over too short a period', () => {
  const p = position({ symbol: 'A', lots: [{ id: 'l1', shares: 1, price: 100, date: '2024-01-01' }] })
  const m = computePortfolio(portfolio([p]), { A: quote('A', 110, 110) })
  assert.equal(annualisedReturn(buildCashFlows([p], m, '2024-01-20')), null)
})

test('survives a total wipeout without hanging or throwing', () => {
  const p = position({ symbol: 'A', lots: [{ id: 'l1', shares: 1, price: 100, date: '2022-01-01' }] })
  const m = computePortfolio(portfolio([p]), { A: quote('A', 0.01, 0.01) })
  const rate = annualisedReturn(buildCashFlows([p], m, '2024-01-01'))
  assert.ok(rate === null || rate < 0, `expected a loss, got ${rate}`)
})

// --- report ---------------------------------------------------------------

if (failures.length) {
  for (const failure of failures) console.error(`  ✗ ${failure}\n`)
  // Throwing (rather than process.exit) keeps this file free of Node-only APIs
  // while still giving the runner a non-zero exit code.
  throw new Error(`${passed} passed, ${failures.length} failed`)
}
console.log(`✓ ${passed} calc checks passed`)
