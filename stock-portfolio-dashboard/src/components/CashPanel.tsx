/**
 * Cash available for investment.
 *
 * Maintained by hand, because there is no brokerage connection to read it from
 * — but buying and selling move it automatically, so it only needs correcting
 * when money enters or leaves the account.
 */
import { useState } from 'react'
import type { PortfolioMetrics } from '../lib/calc'
import { money, percent } from '../lib/format'
import { useStore } from '../store/store'
import { Button, Card, Field, Input, Modal, Value } from './ui'

type Mode = 'set' | 'deposit' | 'withdraw'

const COPY: Record<Mode, { title: string; label: string; action: string; hint: string }> = {
  set: {
    title: 'Update available cash',
    label: 'Cash available',
    action: 'Save',
    hint: 'The balance sitting in the account, ready to invest.',
  },
  deposit: {
    title: 'Add cash',
    label: 'Amount to add',
    action: 'Add cash',
    hint: 'Money paid into the account.',
  },
  withdraw: {
    title: 'Withdraw cash',
    label: 'Amount to withdraw',
    action: 'Withdraw',
    hint: 'Money taken out of the account.',
  },
}

function parseAmount(text: string): number {
  const cleaned = text.trim().replace(/[\s,]/g, '').replace(/[^\d.-]/g, '')
  const value = Number.parseFloat(cleaned)
  return Number.isFinite(value) ? value : NaN
}

export function CashPanel({ metrics, masked }: { metrics: PortfolioMetrics; masked?: boolean }) {
  const { portfolio, setCash, adjustCash, toast } = useStore()
  const [mode, setMode] = useState<Mode | null>(null)
  const [draft, setDraft] = useState('')
  const [error, setError] = useState('')
  const currency = portfolio.baseCurrency

  function open(next: Mode) {
    setMode(next)
    setDraft(next === 'set' ? String(portfolio.cash || '') : '')
    setError('')
  }

  function submit() {
    const amount = parseAmount(draft)
    if (!Number.isFinite(amount)) {
      setError('Enter an amount.')
      return
    }
    if (mode !== 'set' && amount <= 0) {
      setError('Enter an amount above zero.')
      return
    }
    if (mode === 'set' && amount < 0) {
      setError('Cash cannot be negative.')
      return
    }
    if (mode === 'withdraw' && amount > portfolio.cash) {
      setError(`You only have ${money(portfolio.cash, currency)} available.`)
      return
    }

    if (mode === 'set') {
      setCash(amount)
      toast(`Cash set to ${money(amount, currency)}`, 'success')
    } else if (mode === 'deposit') {
      adjustCash(amount)
      toast(`Added ${money(amount, currency)} to available cash`, 'success')
    } else {
      adjustCash(-amount)
      toast(`Withdrew ${money(amount, currency)}`, 'success')
    }
    setMode(null)
  }

  const preview =
    mode && mode !== 'set' && Number.isFinite(parseAmount(draft))
      ? portfolio.cash + (mode === 'deposit' ? parseAmount(draft) : -parseAmount(draft))
      : null

  return (
    <>
      <Card>
        <div className="cash-panel">
          <div className="cash-main">
            <div className="cash-label">Cash available for investment</div>
            <div className={`cash-value ${masked ? 'privacy-mask' : ''}`}>{money(metrics.cash, currency)}</div>
            <div className="row-wrap" style={{ marginTop: 12 }}>
              <Button size="sm" onClick={() => open('set')}>
                Update
              </Button>
              <Button size="sm" onClick={() => open('deposit')}>
                + Add cash
              </Button>
              <Button size="sm" variant="ghost" onClick={() => open('withdraw')} disabled={portfolio.cash <= 0}>
                Withdraw
              </Button>
            </div>
          </div>

          <div className="cash-stats">
            <div className="cash-stat">
              <span className="cash-stat-key">Total account value</span>
              <span className={`cash-stat-val ${masked ? 'privacy-mask' : ''}`}>
                {money(metrics.accountValue, currency)}
              </span>
              <span className="cash-stat-sub">Holdings plus cash</span>
            </div>
            <div className="cash-stat">
              <span className="cash-stat-key">Held as cash</span>
              <span className="cash-stat-val">{percent(metrics.cashWeight, 1)}</span>
              <span className="cash-stat-sub">{percent(1 - metrics.cashWeight, 1)} invested</span>
            </div>
            {metrics.realisedPl !== 0 && (
              <div className="cash-stat">
                <span className="cash-stat-key">Realised profit / loss</span>
                <span className="cash-stat-val">
                  <Value amount={metrics.realisedPl} currency={currency} masked={masked} />
                </span>
                <span className="cash-stat-sub">Banked through sales</span>
              </div>
            )}
          </div>
        </div>
      </Card>

      {mode && (
        <Modal
          title={COPY[mode].title}
          subtitle={`${portfolio.name} · currently ${money(portfolio.cash, currency)}`}
          onClose={() => setMode(null)}
          footer={
            <>
              <Button onClick={() => setMode(null)}>Cancel</Button>
              <Button variant="primary" onClick={submit}>
                {COPY[mode].action}
              </Button>
            </>
          }
        >
          <Field label={`${COPY[mode].label} (${currency})`} htmlFor="cash-amount" hint={COPY[mode].hint} error={error}>
            <Input
              id="cash-amount"
              inputMode="decimal"
              autoFocus
              value={draft}
              aria-invalid={!!error || undefined}
              placeholder="0.00"
              onChange={(event) => {
                setDraft(event.target.value)
                setError('')
              }}
              onKeyDown={(event) => {
                if (event.key === 'Enter') {
                  event.preventDefault()
                  submit()
                }
              }}
            />
          </Field>
          {preview !== null && (
            <div className="lot-summary">
              <span>New available cash</span>
              <strong>{money(preview, currency)}</strong>
            </div>
          )}
        </Modal>
      )}
    </>
  )
}
