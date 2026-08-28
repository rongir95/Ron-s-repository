/**
 * Whose portfolio am I looking at?
 *
 * This is the answer to the original problem — one dashboard, one portfolio per
 * person, switched in one click, with each person's total shown right in the
 * menu so the person managing both can compare without switching at all.
 */
import { useState } from 'react'
import { computePortfolio } from '../lib/calc'
import { compactMoney, signedPercent } from '../lib/format'
import type { Quote } from '../market/types'
import { useStore } from '../store/store'
import { Button, Field, Input, Modal, Select, useDismiss } from './ui'

const CURRENCIES = ['USD', 'EUR', 'GBP', 'ILS', 'CAD', 'AUD', 'CHF', 'JPY', 'SEK', 'INR']

/** A stable colour per portfolio, derived from its id so it never shifts. */
function avatarHue(id: string): string {
  let hash = 0
  for (let i = 0; i < id.length; i++) hash = (hash * 31 + id.charCodeAt(i)) >>> 0
  const slots = ['var(--series-1)', 'var(--series-7)', 'var(--series-3)', 'var(--series-2)', 'var(--series-5)']
  return slots[hash % slots.length]
}

export function PortfolioAvatar({ id, name, size = 22 }: { id: string; name: string; size?: number }) {
  return (
    <span
      className="pf-avatar"
      style={{ background: avatarHue(id), width: size, height: size, fontSize: size * 0.48 }}
      aria-hidden="true"
    >
      {name.trim().charAt(0).toUpperCase() || '?'}
    </span>
  )
}

export function PortfolioSwitcher({
  quotes,
  fxRates,
  masked,
}: {
  quotes: Record<string, Quote>
  fxRates: Record<string, number>
  masked?: boolean
}) {
  const { data, portfolio, setActivePortfolio, addPortfolio, renamePortfolio, setPortfolioCurrency, toast } = useStore()
  const [open, setOpen] = useState(false)
  const [creating, setCreating] = useState(false)
  const [renaming, setRenaming] = useState(false)
  const [draftName, setDraftName] = useState('')
  const [draftCurrency, setDraftCurrency] = useState('USD')
  const ref = useDismiss(open, () => setOpen(false))

  function close() {
    setCreating(false)
    setRenaming(false)
  }

  /** The single save path, shared by the Save button and the Enter key. */
  function submit() {
    const name = draftName.trim()
    if (!name) return
    if (creating) {
      addPortfolio(name, draftCurrency)
      toast(`${name} created`, 'success')
    } else {
      renamePortfolio(portfolio.id, name)
      setPortfolioCurrency(portfolio.id, draftCurrency)
      toast(`Renamed to ${name}`, 'success')
    }
    close()
  }

  return (
    <>
      <div className="pf-switch" ref={ref}>
        <button
          type="button"
          className="pf-button"
          aria-haspopup="menu"
          aria-expanded={open}
          onClick={() => setOpen((value) => !value)}
        >
          <PortfolioAvatar id={portfolio.id} name={portfolio.name} />
          <span className="pf-name">{portfolio.name}</span>
          <span aria-hidden="true" style={{ color: 'var(--text-3)', fontSize: 10 }}>
            ▼
          </span>
        </button>

        {open && (
          <div className="pf-menu" role="menu">
            <div className="pf-menu-label">Portfolios</div>
            {data.portfolios.map((entry) => {
              const metrics = computePortfolio(entry, quotes, fxRates)
              return (
                <button
                  key={entry.id}
                  type="button"
                  role="menuitemradio"
                  aria-checked={entry.id === portfolio.id}
                  aria-current={entry.id === portfolio.id}
                  className="pf-item"
                  onClick={() => {
                    setActivePortfolio(entry.id)
                    setOpen(false)
                  }}
                >
                  <PortfolioAvatar id={entry.id} name={entry.name} />
                  <span style={{ overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>{entry.name}</span>
                  <span className="pf-meta">
                    <span className={masked ? 'privacy-mask' : undefined}>
                      {compactMoney(metrics.totalValue, entry.baseCurrency)}
                    </span>{' '}
                    <span className={metrics.totalPl >= 0 ? 'v-gain' : 'v-loss'}>
                      {signedPercent(metrics.totalPlPct, 1)}
                    </span>
                  </span>
                </button>
              )
            })}
            <div className="pf-divider" />
            <button
              type="button"
              role="menuitem"
              className="pf-item"
              onClick={() => {
                setDraftName('')
                setDraftCurrency(portfolio.baseCurrency)
                setCreating(true)
                setOpen(false)
              }}
            >
              + New portfolio
            </button>
            <button
              type="button"
              role="menuitem"
              className="pf-item"
              onClick={() => {
                setDraftName(portfolio.name)
                setDraftCurrency(portfolio.baseCurrency)
                setRenaming(true)
                setOpen(false)
              }}
            >
              ✎ Rename “{portfolio.name}”
            </button>
          </div>
        )}
      </div>

      {(creating || renaming) && (
        <Modal
          title={creating ? 'New portfolio' : 'Rename portfolio'}
          subtitle={creating ? 'One per person keeps everyone’s holdings separate.' : undefined}
          onClose={close}
          footer={
            <>
              <Button onClick={close}>Cancel</Button>
              <Button variant="primary" disabled={!draftName.trim()} onClick={submit}>
                {creating ? 'Create' : 'Save'}
              </Button>
            </>
          }
        >
          <Field label="Name" htmlFor="pf-new-name" hint="Whose portfolio is this?">
            <Input
              id="pf-new-name"
              value={draftName}
              placeholder="e.g. Ron, or Younger brother"
              onChange={(event) => setDraftName(event.target.value)}
              onKeyDown={(event) => {
                if (event.key === 'Enter') {
                  event.preventDefault()
                  submit()
                }
              }}
            />
          </Field>
          <Field
            label="Report totals in"
            htmlFor="pf-new-currency"
            hint="Holdings quoted in another currency are converted at today's rate."
          >
            <Select
              id="pf-new-currency"
              value={draftCurrency}
              onChange={(event) => setDraftCurrency(event.target.value)}
            >
              {CURRENCIES.map((code) => (
                <option key={code} value={code}>
                  {code}
                </option>
              ))}
            </Select>
          </Field>
        </Modal>
      )}
    </>
  )
}

export { CURRENCIES }
