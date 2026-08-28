/**
 * Add / edit a position.
 *
 * Adding is deliberately three fields — ticker, shares, average price — with
 * everything else optional. The ticker box searches the provider as you type
 * and, once a symbol is chosen, pulls a live quote so you can see the current
 * price and what the position would be worth *before* saving. That is the check
 * against a mistyped ticker, which is otherwise the easiest thing to get wrong.
 *
 * Editing exposes the individual lots, so a holding bought at several different
 * prices keeps a correct share-weighted average cost.
 */
import { useEffect, useMemo, useRef, useState } from 'react'
import { getProvider } from '../market'
import type { Quote, SymbolMatch } from '../market/types'
import { averageCost, fxRateFor, nativeCostBasis, totalShares } from '../lib/calc'
import { money, percent, shares as fmtShares, todayIso } from '../lib/format'
import { newId } from '../lib/id'
import { useStore, type NewPositionInput } from '../store/store'
import type { Lot, Position } from '../types'
import { Button, Field, Input, Modal, Textarea, Value } from './ui'

interface Draft {
  shares: string
  price: string
  date: string
}

const blankDraft = (): Draft => ({ shares: '', price: '', date: '' })

function parseNumber(text: string): number {
  // Accept "1,234.5" and "1 234,5" — people paste from brokerage statements.
  const cleaned = text.trim().replace(/\s/g, '').replace(/,(?=\d{3}\b)/g, '')
  const normalised = cleaned.includes(',') && !cleaned.includes('.') ? cleaned.replace(',', '.') : cleaned
  const value = Number.parseFloat(normalised)
  return Number.isFinite(value) ? value : NaN
}

// --- ticker lookup --------------------------------------------------------

function TickerLookup({
  value,
  onChange,
  onPick,
  invalid,
  inputId,
}: {
  value: string
  onChange: (value: string) => void
  onPick: (match: SymbolMatch) => void
  invalid?: boolean
  inputId: string
}) {
  const { settings } = useStore()
  const [matches, setMatches] = useState<SymbolMatch[]>([])
  const [open, setOpen] = useState(false)
  const [activeIndex, setActiveIndex] = useState(0)
  const [searching, setSearching] = useState(false)
  const box = useRef<HTMLDivElement>(null)

  useEffect(() => {
    const query = value.trim()
    if (query.length < 1) {
      setMatches([])
      return
    }
    let cancelled = false
    setSearching(true)
    const timer = window.setTimeout(async () => {
      try {
        const found = await getProvider(settings).search(query)
        if (!cancelled) {
          setMatches(found)
          setActiveIndex(0)
        }
      } catch {
        if (!cancelled) setMatches([])
      } finally {
        if (!cancelled) setSearching(false)
      }
    }, 280)
    return () => {
      cancelled = true
      clearTimeout(timer)
      setSearching(false)
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [value, settings.providerId, settings.twelveDataKey])

  useEffect(() => {
    const onPointerDown = (event: MouseEvent) => {
      if (box.current && !box.current.contains(event.target as Node)) setOpen(false)
    }
    document.addEventListener('mousedown', onPointerDown)
    return () => document.removeEventListener('mousedown', onPointerDown)
  }, [])

  const visible = open && matches.length > 0

  return (
    <div className="lookup" ref={box}>
      <Input
        id={inputId}
        value={value}
        autoComplete="off"
        spellCheck={false}
        placeholder="Search a ticker or company — e.g. AAPL, Microsoft"
        aria-invalid={invalid || undefined}
        aria-expanded={visible}
        aria-autocomplete="list"
        role="combobox"
        aria-controls={`${inputId}-menu`}
        onChange={(event) => {
          onChange(event.target.value.toUpperCase())
          setOpen(true)
        }}
        onFocus={() => setOpen(true)}
        onKeyDown={(event) => {
          if (!visible) return
          if (event.key === 'ArrowDown') {
            event.preventDefault()
            setActiveIndex((index) => (index + 1) % matches.length)
          } else if (event.key === 'ArrowUp') {
            event.preventDefault()
            setActiveIndex((index) => (index - 1 + matches.length) % matches.length)
          } else if (event.key === 'Enter') {
            event.preventDefault()
            onPick(matches[activeIndex])
            setOpen(false)
          } else if (event.key === 'Escape') {
            setOpen(false)
          }
        }}
      />
      {visible && (
        <div className="lookup-menu" id={`${inputId}-menu`} role="listbox">
          {matches.map((match, index) => (
            <button
              key={`${match.symbol}-${index}`}
              type="button"
              role="option"
              aria-selected={index === activeIndex}
              data-active={index === activeIndex}
              className="lookup-item"
              onMouseEnter={() => setActiveIndex(index)}
              onClick={() => {
                onPick(match)
                setOpen(false)
              }}
            >
              <span className="lookup-sym">{match.symbol}</span>
              <span className="lookup-name">{match.name}</span>
              {match.exchange && <span className="lookup-ex">{match.exchange}</span>}
            </button>
          ))}
        </div>
      )}
      {searching && value.trim() && !visible && <span className="field-hint">Searching…</span>}
    </div>
  )
}

// --- the form -------------------------------------------------------------

export function PositionForm({
  position,
  fxRates = {},
  onClose,
}: {
  /** Omit to add a new position. */
  position?: Position
  /** Needed to convert a foreign-currency purchase into the cash balance. */
  fxRates?: Record<string, number>
  onClose: () => void
}) {
  const { settings, portfolio, addPosition, savePosition, toast } = useStore()
  const editing = !!position

  const [symbol, setSymbol] = useState(position?.symbol ?? '')
  const [name, setName] = useState(position?.name ?? '')
  const [notes, setNotes] = useState(position?.notes ?? '')
  const [draft, setDraft] = useState<Draft>(blankDraft)
  const [lots, setLots] = useState<Lot[]>(position?.lots ?? [])
  const [errors, setErrors] = useState<Record<string, string>>({})
  const [quote, setQuote] = useState<Quote | null>(null)
  const [quoteState, setQuoteState] = useState<'idle' | 'loading' | 'missing'>('idle')
  const [deductCash, setDeductCash] = useState(true)

  // Live quote for the chosen symbol — the "did I type the right ticker?" check.
  useEffect(() => {
    const ticker = symbol.trim().toUpperCase()
    if (ticker.length < 1) {
      setQuote(null)
      setQuoteState('idle')
      return
    }
    let cancelled = false
    setQuoteState('loading')
    const timer = window.setTimeout(async () => {
      try {
        const fetched = await getProvider(settings).getQuotes([ticker])
        if (cancelled) return
        const found = fetched[ticker]
        setQuote(found ?? null)
        setQuoteState(found ? 'idle' : 'missing')
        if (found?.name && !name) setName(found.name)
      } catch {
        if (!cancelled) {
          setQuote(null)
          setQuoteState('missing')
        }
      }
    }, 420)
    return () => {
      cancelled = true
      clearTimeout(timer)
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [symbol, settings.providerId, settings.twelveDataKey])

  const currency = quote?.currency || portfolio.baseCurrency

  // Preview of the position being described, in the instrument's own currency.
  const preview = useMemo(() => {
    const list: Lot[] = editing ? [...lots] : []
    const draftShares = parseNumber(draft.shares)
    const draftPrice = parseNumber(draft.price)
    if (!editing && Number.isFinite(draftShares) && Number.isFinite(draftPrice)) {
      list.push({ id: 'draft', shares: draftShares, price: draftPrice })
    }
    const pseudo = { lots: list } as Position
    const sh = totalShares(pseudo)
    const cost = nativeCostBasis(pseudo)
    const avg = averageCost(pseudo)
    const value = quote ? sh * quote.price : 0
    return { shares: sh, cost, avg, value, pl: quote ? value - cost : 0, plPct: cost > 0 && quote ? (value - cost) / cost : 0 }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [editing, lots, draft.shares, draft.price, quote])

  const purchaseFx = fxRateFor(currency, portfolio.baseCurrency, fxRates)
  const costInBase = preview.cost * purchaseFx
  const cashAfter = portfolio.cash - costInBase

  function validate(): boolean {
    const next: Record<string, string> = {}
    if (!symbol.trim()) next.symbol = 'Enter a ticker symbol.'
    if (editing) {
      if (!lots.length) next.lots = 'A position needs at least one purchase.'
      if (lots.some((lot) => !(lot.shares > 0))) next.lots = 'Every purchase needs a share count above zero.'
      if (lots.some((lot) => !(lot.price >= 0))) next.lots = 'Every purchase needs a price.'
    } else {
      const sh = parseNumber(draft.shares)
      const price = parseNumber(draft.price)
      if (!Number.isFinite(sh) || sh <= 0) next.shares = 'Enter how many shares you hold.'
      if (!Number.isFinite(price) || price < 0) next.price = 'Enter the average price you paid.'
    }
    setErrors(next)
    return Object.keys(next).length === 0
  }

  function submit() {
    if (!validate()) return
    const ticker = symbol.trim().toUpperCase()
    const cashSpent = !editing && deductCash ? costInBase : 0
    if (editing && position) {
      savePosition(position.id, {
        symbol: ticker,
        name: name.trim() || undefined,
        lots,
        notes: notes.trim() || undefined,
      })
      toast(`${ticker} updated`, 'success')
    } else {
      const input: NewPositionInput = {
        symbol: ticker,
        name: name.trim() || undefined,
        shares: parseNumber(draft.shares),
        price: parseNumber(draft.price),
        date: draft.date || undefined,
        notes: notes.trim() || undefined,
        cashSpent,
      }
      const existing = portfolio.positions.find((entry) => entry.symbol === ticker)
      addPosition(input)
      const cashNote = cashSpent > 0 ? ` · ${money(cashSpent, portfolio.baseCurrency)} taken from cash` : ''
      toast(
        (existing
          ? `Added to ${ticker} — average cost recalculated across ${existing.lots.length + 1} purchases`
          : `${ticker} added to ${portfolio.name}`) + cashNote,
        'success',
      )
    }
    onClose()
  }

  const existingPosition = !editing ? portfolio.positions.find((entry) => entry.symbol === symbol.trim().toUpperCase()) : undefined

  return (
    <Modal
      wide={editing}
      title={editing ? `Edit ${position.symbol}` : 'Add a position'}
      subtitle={editing ? 'Each purchase is kept separately so the average cost stays correct.' : `Adding to ${portfolio.name}`}
      onClose={onClose}
      footer={
        <>
          <Button onClick={onClose}>Cancel</Button>
          <Button variant="primary" onClick={submit}>
            {editing ? 'Save changes' : 'Add position'}
          </Button>
        </>
      }
    >
      <Field label="Ticker symbol" error={errors.symbol} htmlFor="pf-symbol"
        hint={quoteState === 'missing' && symbol.trim() ? undefined : 'Search by ticker or company name.'}>
        <TickerLookup
          inputId="pf-symbol"
          value={symbol}
          invalid={!!errors.symbol}
          onChange={setSymbol}
          onPick={(match) => {
            setSymbol(match.symbol.toUpperCase())
            setName(match.name)
          }}
        />
      </Field>

      {/* The live quote is the confirmation that the right instrument was picked. */}
      {symbol.trim() && (
        <div className="lot-summary" aria-live="polite">
          {quoteState === 'loading' ? (
            <span style={{ color: 'var(--text-3)' }}>Checking {symbol.trim()}…</span>
          ) : quote ? (
            <>
              <span>
                <strong>{quote.name || quote.symbol}</strong>
                <br />
                <span style={{ color: 'var(--text-3)' }}>
                  {quote.exchange ? `${quote.exchange} · ` : ''}
                  {quote.currency}
                </span>
              </span>
              <span style={{ textAlign: 'right' }}>
                <strong>{money(quote.price, quote.currency)}</strong>
                <br />
                <Value amount={quote.price - quote.previousClose} currency={quote.currency} /> today
              </span>
            </>
          ) : (
            <span style={{ color: 'var(--text-2)' }}>
              No live price for “{symbol.trim()}”. You can still save it — the row will show as unpriced until the
              symbol resolves. Check the exchange suffix (e.g. <code>TEVA.TA</code>, <code>VWCE.DE</code>).
            </span>
          )}
        </div>
      )}

      {existingPosition && (
        <div className="banner info">
          <div className="banner-body">
            You already hold {existingPosition.symbol}. This will be recorded as an additional purchase and the average
            cost recalculated across all {existingPosition.lots.length + 1} of them.
          </div>
        </div>
      )}

      {editing ? (
        <Field label="Purchases" error={errors.lots} hint="Shares, price paid per share, and the date if you know it.">
          <div className="stack" style={{ gap: 8 }}>
            {lots.map((lot, index) => (
              <div className="lot-row" key={lot.id}>
                <Input
                  aria-label={`Shares, purchase ${index + 1}`}
                  inputMode="decimal"
                  value={lot.shares === 0 ? '' : String(lot.shares)}
                  placeholder="Shares"
                  onChange={(event) => {
                    const value = parseNumber(event.target.value)
                    setLots((current) =>
                      current.map((entry, i) => (i === index ? { ...entry, shares: Number.isFinite(value) ? value : 0 } : entry)),
                    )
                  }}
                />
                <Input
                  aria-label={`Price per share, purchase ${index + 1}`}
                  inputMode="decimal"
                  value={lot.price === 0 ? '' : String(lot.price)}
                  placeholder="Price"
                  onChange={(event) => {
                    const value = parseNumber(event.target.value)
                    setLots((current) =>
                      current.map((entry, i) => (i === index ? { ...entry, price: Number.isFinite(value) ? value : 0 } : entry)),
                    )
                  }}
                />
                <Input
                  aria-label={`Purchase date, purchase ${index + 1}`}
                  type="date"
                  max={todayIso()}
                  value={lot.date ?? ''}
                  onChange={(event) =>
                    setLots((current) =>
                      current.map((entry, i) => (i === index ? { ...entry, date: event.target.value || undefined } : entry)),
                    )
                  }
                />
                <Button
                  variant="ghost"
                  iconOnly
                  aria-label={`Remove purchase ${index + 1}`}
                  disabled={lots.length <= 1}
                  onClick={() => setLots((current) => current.filter((_, i) => i !== index))}
                >
                  ✕
                </Button>
              </div>
            ))}
            <Button
              size="sm"
              onClick={() => setLots((current) => [...current, { id: newId('lot'), shares: 0, price: 0 }])}
            >
              + Add another purchase
            </Button>
          </div>
        </Field>
      ) : (
        <div className="form-grid cols-3">
          <Field label="Number of shares" error={errors.shares} htmlFor="pf-shares">
            <Input
              id="pf-shares"
              inputMode="decimal"
              placeholder="18"
              aria-invalid={!!errors.shares || undefined}
              value={draft.shares}
              onChange={(event) => setDraft((current) => ({ ...current, shares: event.target.value }))}
            />
          </Field>
          <Field
            label="Average price paid"
            error={errors.price}
            htmlFor="pf-price"
            hint={quote ? `Per share, in ${currency}` : 'Per share'}
          >
            <Input
              id="pf-price"
              inputMode="decimal"
              placeholder="171.40"
              aria-invalid={!!errors.price || undefined}
              value={draft.price}
              onChange={(event) => setDraft((current) => ({ ...current, price: event.target.value }))}
            />
          </Field>
          <Field label="Purchase date" htmlFor="pf-date" hint="Optional — powers the performance chart.">
            <Input
              id="pf-date"
              type="date"
              max={todayIso()}
              value={draft.date}
              onChange={(event) => setDraft((current) => ({ ...current, date: event.target.value }))}
            />
          </Field>
        </div>
      )}

      {/* What the position would look like once saved. */}
      {preview.shares > 0 && (
        <div className="lot-summary" aria-live="polite">
          <span>
            {fmtShares(preview.shares)} shares · avg {money(preview.avg, currency)}
            <br />
            <span style={{ color: 'var(--text-3)' }}>Invested {money(preview.cost, currency)}</span>
          </span>
          {quote && (
            <span style={{ textAlign: 'right' }}>
              <strong>{money(preview.value, currency)}</strong> now
              <br />
              <Value amount={preview.pl} currency={currency} /> ({percent(preview.plPct, 1)})
            </span>
          )}
        </div>
      )}

      {!editing && costInBase > 0 && (
        <div className="cash-deduct">
          <label className="cash-deduct-row">
            <input
              type="checkbox"
              checked={deductCash}
              onChange={(event) => setDeductCash(event.target.checked)}
              style={{ width: 17, height: 17, flex: 'none', accentColor: 'var(--accent)' }}
            />
            <span>
              <span style={{ fontWeight: 600 }}>
                Pay for this with available cash ({money(costInBase, portfolio.baseCurrency)})
              </span>
              <span className="switch-sub">
                {deductCash
                  ? `Cash goes from ${money(portfolio.cash, portfolio.baseCurrency)} to ${money(cashAfter, portfolio.baseCurrency)}.`
                  : `Cash stays at ${money(portfolio.cash, portfolio.baseCurrency)} — use this if you already adjusted it.`}
              </span>
            </span>
          </label>
          {deductCash && cashAfter < 0 && (
            <p className="field-error" style={{ margin: '2px 0 0' }}>
              That is {money(Math.abs(cashAfter), portfolio.baseCurrency)} more than you have on record. It will be
              saved anyway and cash will show as overdrawn — update the cash balance if it is out of date.
            </p>
          )}
        </div>
      )}

      <Field label="Notes" htmlFor="pf-notes" hint="Optional — why you bought it, a target price, anything.">
        <Textarea
          id="pf-notes"
          value={notes}
          rows={2}
          onChange={(event) => setNotes(event.target.value)}
          placeholder="Long-term hold…"
        />
      </Field>
    </Modal>
  )
}
