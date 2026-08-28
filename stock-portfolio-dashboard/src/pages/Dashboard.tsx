/**
 * The dashboard.
 *
 * Reading order is deliberate, and front-loads what gets checked daily: what is
 * it worth (hero + allocation) -> how is it doing (KPI row) -> what do I hold
 * (the holdings table) -> how did it get here (performance, return by holding)
 * -> everyone else's portfolios. Every number a chart encodes in colour is also
 * written out in the holdings table.
 */
import { useMemo, useState } from 'react'
import { AllocationChart } from '../components/charts/AllocationChart'
import { PerformanceChart } from '../components/charts/PerformanceChart'
import { ReturnsChart } from '../components/charts/ReturnsChart'
import { CashPanel } from '../components/CashPanel'
import { PositionForm } from '../components/PositionForm'
import { SellForm } from '../components/SellForm'
import { PositionsTable } from '../components/PositionsTable'
import { PortfolioAvatar } from '../components/PortfolioSwitcher'
import {
  Banner,
  Button,
  Card,
  Chip,
  ConfirmDialog,
  EmptyState,
  Segmented,
  Value,
  toneClass,
} from '../components/ui'
import { annualisedReturn, buildCashFlows, buildSeries, computePortfolio } from '../lib/calc'
import { money, percent, relativeTime, signedCompactMoney, signedPercent, todayIso } from '../lib/format'
import type { HistoryRange, Quote } from '../market/types'
import { useHistory } from '../market/useMarketData'
import { useStore } from '../store/store'

const RANGES: Array<{ value: HistoryRange; label: string }> = [
  { value: '1mo', label: '1M' },
  { value: '3mo', label: '3M' },
  { value: '6mo', label: '6M' },
  { value: '1y', label: '1Y' },
  { value: '5y', label: '5Y' },
]

export function Dashboard({
  quotes,
  fxRates,
  quotesLoading,
  quotesError,
  lastUpdated,
  onOpenSettings,
}: {
  quotes: Record<string, Quote>
  fxRates: Record<string, number>
  quotesLoading: boolean
  quotesError: string | null
  lastUpdated: number | null
  onOpenSettings: () => void
}) {
  const { data, portfolio, settings, removePosition, toast } = useStore()
  const [range, setRange] = useState<HistoryRange>('6mo')
  const [returnMetric, setReturnMetric] = useState<'percent' | 'amount'>('percent')
  const [adding, setAdding] = useState(false)
  const [editingId, setEditingId] = useState<string | null>(null)
  const [deletingId, setDeletingId] = useState<string | null>(null)
  const [sellingId, setSellingId] = useState<string | null>(null)

  const masked = settings.privacyMode
  const currency = portfolio.baseCurrency
  const symbols = useMemo(() => portfolio.positions.map((position) => position.symbol), [portfolio.positions])
  const { history, loading: historyLoading, error: historyError } = useHistory(symbols, range)

  const metrics = useMemo(() => computePortfolio(portfolio, quotes, fxRates), [portfolio, quotes, fxRates])
  const series = useMemo(
    () => buildSeries(portfolio.positions, history, currency, quotes, fxRates),
    [portfolio.positions, history, currency, quotes, fxRates],
  )
  const annualised = useMemo(
    () => annualisedReturn(buildCashFlows(portfolio.positions, metrics, todayIso())),
    [portfolio.positions, metrics],
  )

  const editing = editingId ? portfolio.positions.find((position) => position.id === editingId) : undefined
  const deleting = deletingId ? portfolio.positions.find((position) => position.id === deletingId) : undefined
  const selling = sellingId ? portfolio.positions.find((position) => position.id === sellingId) : undefined

  // --- empty state --------------------------------------------------------

  if (!portfolio.positions.length) {
    return (
      <div className="stack">
        <CashPanel metrics={metrics} masked={masked} />
        <Card>
          <EmptyState
            icon={<span style={{ fontSize: 22 }}>📈</span>}
            title={`${portfolio.name} has no holdings yet`}
            action={
              <Button variant="primary" onClick={() => setAdding(true)}>
                Add your first position
              </Button>
            }
          >
            Add a stock with its ticker, how many shares you hold, and the average price you paid. Prices, profit and
            loss, and allocation are worked out from there.
          </EmptyState>
        </Card>
        {adding && <PositionForm fxRates={fxRates} onClose={() => setAdding(false)} />}
      </div>
    )
  }

  return (
    <div className="stack">
      {portfolio.sample && (
        <Banner
          tone="info"
          title="You’re looking at sample holdings"
          action={
            <Button size="sm" onClick={onOpenSettings}>
              Start fresh
            </Button>
          }
        >
          They’re here so the dashboard has something to show. Edit or delete any of them, or clear everything from
          Settings.
        </Banner>
      )}

      {quotesError && (
        <Banner
          tone="error"
          title="Market data unavailable"
          action={
            <Button size="sm" onClick={onOpenSettings}>
              Change data source
            </Button>
          }
        >
          {quotesError}
        </Banner>
      )}

      {!!metrics.unpriced.length && !quotesError && (
        <Banner title={`No price for ${metrics.unpriced.map((row) => row.symbol).join(', ')}`}>
          {metrics.unpriced.length === 1 ? 'This holding is' : 'These holdings are'} excluded from the totals until the
          symbol resolves. Check the ticker — non-US listings usually need an exchange suffix, like{' '}
          <code>TEVA.TA</code> or <code>VWCE.DE</code>.
        </Banner>
      )}

      {/*
        --- Summary row ------------------------------------------------------
        Two columns of matched height. Value and cash stack on the left because
        each is short; allocation is tall, so one against two balances out and
        neither column is left with dead space. Previously the value panel sat
        alone beside the taller allocation column and floated in empty air.
      */}

      <div className="summary-grid">
        <div className="summary-col">
          <Card pad={false} className="value-card">
            <div className="value-panel-head">
              <span className="value-panel-label">
                <PortfolioAvatar id={portfolio.id} name={portfolio.name} size={18} />
                {portfolio.name} · total value
              </span>
              <div className={`hero-value ${masked ? 'privacy-mask' : ''}`}>{money(metrics.totalValue, currency)}</div>
            </div>
            {/* The total and the two returns are one fact at three horizons, so
                hairlines divide them rather than gaps. */}
            <div className="value-panel-stats">
              <div className="value-stat">
                <span className="value-stat-label">All time</span>
                <span className="value-stat-value">
                  <Value amount={metrics.totalPl} currency={currency} masked={masked} />
                  <span className={`value-stat-pct ${toneClass(metrics.totalPl)}`}>
                    {signedPercent(metrics.totalPlPct)}
                  </span>
                </span>
              </div>
              <div className="value-stat">
                <span className="value-stat-label">Today</span>
                <span className="value-stat-value">
                  <Value amount={metrics.dayChange} currency={currency} masked={masked} />
                  <span className={`value-stat-pct ${toneClass(metrics.dayChange)}`}>
                    {signedPercent(metrics.dayChangePct)}
                  </span>
                </span>
              </div>
            </div>
          </Card>

          <CashPanel metrics={metrics} masked={masked} />
        </div>

        <Card className="alloc-card">
          <div className="card-head" style={{ marginBottom: 12 }}>
            <div>
              <div className="card-title">Allocation</div>
              <div className="card-note">
                {metrics.positions.some((row) => row.hasQuote)
                  ? 'Share of current market value'
                  : 'Share of the amount invested'}
                {metrics.largest ? (
                  <>
                    {' · largest is '}
                    <strong style={{ color: 'var(--text-2)' }}>{metrics.largest.symbol}</strong>
                    {` at ${percent(metrics.concentration, 1)}`}
                  </>
                ) : null}
              </div>
            </div>
          </div>
          <AllocationChart positions={metrics.positions} currency={currency} masked={masked} />
        </Card>
      </div>

      {/* --- KPI row -------------------------------------------------------- */}

      <div className="kpi-grid">
        <Card className="tile" pad={false}>
          <span className="tile-label">Total invested</span>
          <span className={`tile-value ${masked ? 'privacy-mask' : ''}`}>{money(metrics.totalInvested, currency)}</span>
          <span className="tile-foot">
            Across {metrics.positions.length} holding{metrics.positions.length === 1 ? '' : 's'}
          </span>
        </Card>

        <Card className="tile" pad={false}>
          <span className="tile-label">Best performer</span>
          {metrics.best ? (
            <>
              <span className="tile-value">{metrics.best.symbol}</span>
              <span className={`tile-delta ${toneClass(metrics.best.plPct)}`}>
                <span aria-hidden="true">{metrics.best.plPct >= 0 ? '▲' : '▼'}</span>
                {signedPercent(metrics.best.plPct)}
                <span className={masked ? 'privacy-mask' : undefined} style={{ color: 'var(--text-3)', fontWeight: 500 }}>
                  {' '}
                  · {signedCompactMoney(metrics.best.pl, currency)}
                </span>
              </span>
            </>
          ) : (
            <span className="tile-value">—</span>
          )}
        </Card>

        <Card className="tile" pad={false}>
          <span className="tile-label">Worst performer</span>
          {metrics.worst ? (
            <>
              <span className="tile-value">{metrics.worst.symbol}</span>
              <span className={`tile-delta ${toneClass(metrics.worst.plPct)}`}>
                <span aria-hidden="true">{metrics.worst.plPct >= 0 ? '▲' : '▼'}</span>
                {signedPercent(metrics.worst.plPct)}
                <span className={masked ? 'privacy-mask' : undefined} style={{ color: 'var(--text-3)', fontWeight: 500 }}>
                  {' '}
                  · {signedCompactMoney(metrics.worst.pl, currency)}
                </span>
              </span>
            </>
          ) : (
            <span className="tile-value">—</span>
          )}
        </Card>

        <Card className="tile" pad={false}>
          <span className="tile-label">Annualised return</span>
          <span className="tile-value">
            {annualised === null ? '—' : <span className={toneClass(annualised)}>{signedPercent(annualised, 1)}</span>}
          </span>
          <span className="tile-foot">
            {annualised === null
              ? 'Needs purchase dates on every holding'
              : 'Money-weighted, per year'}
          </span>
        </Card>
      </div>

      {/* --- Positions ------------------------------------------------------ */}

      <Card pad={false}>
        <div className="card-head" style={{ padding: '18px 20px 0', marginBottom: 12 }}>
          <div>
            <div className="card-title">Holdings</div>
            <div className="card-note">
              {lastUpdated ? `Prices updated ${relativeTime(lastUpdated)}` : 'Fetching prices…'}
              {quotesLoading && lastUpdated ? ' · refreshing' : ''}
            </div>
          </div>
          <div className="row-wrap">
            {metrics.mixedCurrency && (
              <Chip tone="warn" title="Converted at today's exchange rate">
                Mixed currencies
              </Chip>
            )}
            <Button variant="primary" size="sm" onClick={() => setAdding(true)}>
              + Add position
            </Button>
          </div>
        </div>
        <PositionsTable
          rows={metrics.positions}
          currency={currency}
          history={history}
          masked={masked}
          onEdit={setEditingId}
          onSell={setSellingId}
          onDelete={setDeletingId}
        />
      </Card>

      {/* --- Performance ---------------------------------------------------- */}

      <Card>
        <div className="card-head">
          <div>
            <div className="card-title">Value over time</div>
            <div className="card-note">
              Your current holdings valued at each day’s closing price. Purchases with a date are only counted from that
              date, so the invested line steps up when money actually went in.
            </div>
          </div>
          <Segmented value={range} options={RANGES} onChange={setRange} label="Time range" />
        </div>
        {historyError && (
          <div style={{ marginBottom: 12 }}>
            <Banner>{historyError}</Banner>
          </div>
        )}
        {series.length >= 2 ? (
          <PerformanceChart series={series} currency={currency} masked={masked} />
        ) : historyLoading ? (
          <div style={{ height: 264, display: 'grid', placeItems: 'center', color: 'var(--text-3)', fontSize: 13 }}>
            Loading price history…
          </div>
        ) : (
          <div style={{ height: 160, display: 'grid', placeItems: 'center', color: 'var(--text-3)', fontSize: 13 }}>
            No price history available for this range.
          </div>
        )}
      </Card>

      {/* --- Returns by holding --------------------------------------------- */}

      <Card>
        <div className="card-head">
          <div>
            <div className="card-title">Return by holding</div>
            <div className="card-note">Best to worst. Gains sit right of the zero line, losses left of it.</div>
          </div>
          <Segmented
            value={returnMetric}
            options={[
              { value: 'percent', label: '%' },
              { value: 'amount', label: currency },
            ]}
            onChange={setReturnMetric}
            label="Return measure"
          />
        </div>
        <ReturnsChart positions={metrics.positions} currency={currency} masked={masked} metric={returnMetric} />
      </Card>

      {/* --- All portfolios ------------------------------------------------- */}

      {data.portfolios.length > 1 && <HouseholdSummary quotes={quotes} fxRates={fxRates} masked={masked} />}

      {/* --- Dialogs -------------------------------------------------------- */}

      {adding && <PositionForm fxRates={fxRates} onClose={() => setAdding(false)} />}
      {editing && <PositionForm position={editing} fxRates={fxRates} onClose={() => setEditingId(null)} />}
      {selling && (
        <SellForm
          position={selling}
          quote={quotes[selling.symbol]}
          fxRates={fxRates}
          onClose={() => setSellingId(null)}
        />
      )}
      {deleting && (
        <ConfirmDialog
          title={`Remove ${deleting.symbol}?`}
          destructive
          confirmLabel="Remove position"
          message={
            <>
              {deleting.symbol}
              {deleting.name ? ` (${deleting.name})` : ''} will be removed from <strong>{portfolio.name}</strong>, along
              with {deleting.lots.length === 1 ? 'its purchase record' : `all ${deleting.lots.length} purchase records`}.
              This cannot be undone.
            </>
          }
          onCancel={() => setDeletingId(null)}
          onConfirm={() => {
            removePosition(deleting.id)
            toast(`${deleting.symbol} removed`, 'success')
            setDeletingId(null)
          }}
        />
      )}
    </div>
  )
}

/**
 * Every portfolio side by side — the view for whoever manages more than one.
 */
function HouseholdSummary({
  quotes,
  fxRates,
  masked,
}: {
  quotes: Record<string, Quote>
  fxRates: Record<string, number>
  masked?: boolean
}) {
  const { data, portfolio, setActivePortfolio } = useStore()
  const rows = data.portfolios.map((entry) => ({ entry, metrics: computePortfolio(entry, quotes, fxRates) }))

  return (
    <Card>
      <div className="card-head">
        <div>
          <div className="card-title">All portfolios</div>
          <div className="card-note">Every portfolio at once. Select one to open it.</div>
        </div>
      </div>
      <div className="household">
        {rows.map(({ entry, metrics }) => (
          <button
            key={entry.id}
            type="button"
            className="household-row"
            aria-current={entry.id === portfolio.id}
            onClick={() => setActivePortfolio(entry.id)}
          >
            <span className="household-cell">
              <span className="row" style={{ gap: 8 }}>
                <PortfolioAvatar id={entry.id} name={entry.name} size={20} />
                <strong style={{ overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                  {entry.name}
                </strong>
              </span>
              <span className="household-key">
                {entry.positions.length} holding{entry.positions.length === 1 ? '' : 's'}
              </span>
            </span>
            <span className="household-cell">
              <span className="household-key">Value</span>
              <span className={`household-val ${masked ? 'privacy-mask' : ''}`}>
                {money(metrics.totalValue, entry.baseCurrency, { decimals: 0 })}
              </span>
            </span>
            <span className="household-cell">
              <span className="household-key">Invested</span>
              <span className={`household-val ${masked ? 'privacy-mask' : ''}`}>
                {money(metrics.totalInvested, entry.baseCurrency, { decimals: 0 })}
              </span>
            </span>
            <span className="household-cell">
              <span className="household-key">Profit / loss</span>
              <span className="household-val">
                <Value amount={metrics.totalPl} currency={entry.baseCurrency} masked={masked} />
              </span>
            </span>
            <span className="household-cell">
              <span className="household-key">Return · today</span>
              <span className="household-val">
                <Value amount={metrics.totalPlPct} percent />
                <span style={{ color: 'var(--text-3)', fontWeight: 500 }}> · </span>
                <Value amount={metrics.dayChangePct} percent arrow={false} />
              </span>
            </span>
          </button>
        ))}
      </div>
    </Card>
  )
}
