/**
 * Sell shares from a position.
 *
 * Shares come off every purchase lot pro rata, so the average cost you see does
 * not move; the proceeds land in available cash and the gain or loss is banked
 * as realised. The preview spells all of that out before you commit, because a
 * sale is the one action here that changes two balances at once.
 */
import { useMemo, useState } from 'react'
import { applySale, averageCost, fxRateFor, totalShares } from '../lib/calc'
import { money, shares as fmtShares, signedMoney, signedPercent, todayIso } from '../lib/format'
import type { Quote } from '../market/types'
import { useStore } from '../store/store'
import type { Position } from '../types'
import { Button, Field, Input, Modal } from './ui'

function parseNumber(text: string): number {
  const cleaned = text.trim().replace(/\s/g, '').replace(/,(?=\d{3}\b)/g, '')
  const normalised = cleaned.includes(',') && !cleaned.includes('.') ? cleaned.replace(',', '.') : cleaned
  const value = Number.parseFloat(normalised)
  return Number.isFinite(value) ? value : NaN
}

export function SellForm({
  position,
  quote,
  fxRates,
  onClose,
}: {
  position: Position
  quote?: Quote
  fxRates: Record<string, number>
  onClose: () => void
}) {
  const { portfolio, sellPosition, toast } = useStore()
  const held = totalShares(position)
  const avgCost = averageCost(position)
  const currency = quote?.currency || portfolio.baseCurrency
  const fxRate = fxRateFor(currency, portfolio.baseCurrency, fxRates)

  const [sharesText, setSharesText] = useState('')
  const [priceText, setPriceText] = useState(quote ? String(quote.price) : '')
  const [date, setDate] = useState(todayIso())
  const [errors, setErrors] = useState<Record<string, string>>({})

  const sharesToSell = parseNumber(sharesText)
  const price = parseNumber(priceText)

  const preview = useMemo(() => {
    if (!Number.isFinite(sharesToSell) || !Number.isFinite(price) || sharesToSell <= 0) return null
    return applySale(position, sharesToSell, price, fxRate)
  }, [position, sharesToSell, price, fxRate])

  function submit() {
    const next: Record<string, string> = {}
    if (!Number.isFinite(sharesToSell) || sharesToSell <= 0) {
      next.shares = 'Enter how many shares you sold.'
    } else if (sharesToSell > held + 1e-9) {
      next.shares = `You only hold ${fmtShares(held)} shares.`
    }
    if (!Number.isFinite(price) || price < 0) next.price = 'Enter the price you sold at.'
    setErrors(next)
    if (Object.keys(next).length) return

    const result = sellPosition(position.id, { shares: sharesToSell, price, fxRate })
    if (!result) {
      toast('Nothing was sold.', 'error')
      return
    }
    const soldOut = result.sharesRemaining <= 0
    toast(
      `Sold ${fmtShares(result.sharesSold)} ${position.symbol}${soldOut ? ' (position closed)' : ''} · ` +
        `${money(result.proceeds, portfolio.baseCurrency)} added to cash`,
      'success',
    )
    onClose()
  }

  return (
    <Modal
      title={`Sell ${position.symbol}`}
      subtitle={`Holding ${fmtShares(held)} shares at an average cost of ${money(avgCost, currency)}`}
      onClose={onClose}
      footer={
        <>
          <Button onClick={onClose}>Cancel</Button>
          <Button variant="primary" onClick={submit}>
            Record sale
          </Button>
        </>
      }
    >
      <div className="form-grid cols-3">
        <Field label="Shares to sell" error={errors.shares} htmlFor="sell-shares">
          <Input
            id="sell-shares"
            inputMode="decimal"
            autoFocus
            placeholder={fmtShares(held)}
            aria-invalid={!!errors.shares || undefined}
            value={sharesText}
            onChange={(event) => setSharesText(event.target.value)}
          />
        </Field>
        <Field label="Sale price per share" error={errors.price} htmlFor="sell-price" hint={`In ${currency}`}>
          <Input
            id="sell-price"
            inputMode="decimal"
            aria-invalid={!!errors.price || undefined}
            value={priceText}
            onChange={(event) => setPriceText(event.target.value)}
          />
        </Field>
        <Field label="Sale date" htmlFor="sell-date" hint="Optional — for your own record.">
          <Input id="sell-date" type="date" max={todayIso()} value={date} onChange={(event) => setDate(event.target.value)} />
        </Field>
      </div>

      <div className="row-wrap">
        <Button
          size="sm"
          onClick={() => {
            setSharesText(String(held))
            setErrors({})
          }}
        >
          Sell all {fmtShares(held)}
        </Button>
        <Button
          size="sm"
          onClick={() => {
            setSharesText(String(held / 2))
            setErrors({})
          }}
        >
          Sell half
        </Button>
        {quote && (
          <Button size="sm" variant="ghost" onClick={() => setPriceText(String(quote.price))}>
            Use market price ({money(quote.price, currency)})
          </Button>
        )}
      </div>

      {preview && (
        <div className="sell-preview" aria-live="polite">
          <div className="tooltip-row">
            <span>Proceeds into cash</span>
            <strong>{money(preview.proceeds, portfolio.baseCurrency)}</strong>
          </div>
          <div className="tooltip-row">
            <span>Realised profit / loss</span>
            <strong className={preview.realised >= 0 ? 'v-gain' : 'v-loss'}>
              <span aria-hidden="true">{preview.realised >= 0 ? '▲' : '▼'}</span>{' '}
              {signedMoney(preview.realised, portfolio.baseCurrency)}
              {avgCost > 0 && (
                <span style={{ fontWeight: 500 }}> ({signedPercent(price / avgCost - 1)})</span>
              )}
            </strong>
          </div>
          <div className="tooltip-row">
            <span>Shares left</span>
            <strong>
              {preview.sharesRemaining <= 0 ? 'None — position closed' : fmtShares(preview.sharesRemaining)}
            </strong>
          </div>
          <div className="tooltip-row" style={{ borderTop: '1px solid var(--border)', paddingTop: 6, marginTop: 2 }}>
            <span>Cash after the sale</span>
            <strong>{money(portfolio.cash + preview.proceeds, portfolio.baseCurrency)}</strong>
          </div>
          {preview.sharesRemaining > 0 && (
            <p className="field-hint" style={{ margin: '6px 0 0' }}>
              Average cost stays {money(avgCost, currency)} — shares come off each purchase in proportion.
            </p>
          )}
        </div>
      )}
    </Modal>
  )
}
