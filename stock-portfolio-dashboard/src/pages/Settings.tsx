/**
 * Settings — data source, appearance, backup, and the destructive actions.
 */
import { useState } from 'react'
import { CURRENCIES, PortfolioAvatar } from '../components/PortfolioSwitcher'
import { Banner, Button, Card, Chip, ConfirmDialog, Field, Input, Modal, Select } from '../components/ui'
import { PROVIDER_CHOICES, getProvider } from '../market'
import { useResolvedTheme } from '../lib/theme'
import { exportAll, exportCsv, exportPortfolio, pickJsonFile } from '../lib/transfer'
import { normalise, useStore } from '../store/store'
import type { ProviderId } from '../types'

const REFRESH_OPTIONS = [
  { value: 0, label: 'Manual only' },
  { value: 30, label: 'Every 30 seconds' },
  { value: 60, label: 'Every minute' },
  { value: 300, label: 'Every 5 minutes' },
  { value: 900, label: 'Every 15 minutes' },
]

export function Settings({ onDone }: { onDone: () => void }) {
  const { data, portfolio, settings, updateSettings, setPortfolioCurrency, deletePortfolio, replaceAll, startFresh, toast } =
    useStore()
  const [confirm, setConfirm] = useState<null | 'fresh' | 'delete-portfolio'>(null)
  const resolvedTheme = useResolvedTheme(settings.theme)
  const [freshName, setFreshName] = useState(portfolio.name)
  const provider = getProvider(settings)

  async function importBackup() {
    try {
      const raw = await pickJsonFile()
      const parsed = normalise(raw)
      if (!parsed) {
        toast('That file does not contain any portfolios.', 'error')
        return
      }
      replaceAll(parsed)
      toast(
        `Imported ${parsed.portfolios.length} portfolio${parsed.portfolios.length === 1 ? '' : 's'}`,
        'success',
      )
    } catch (err) {
      toast((err as Error).message || 'Import failed.', 'error')
    }
  }

  return (
    <div className="stack" style={{ maxWidth: 780, margin: '0 auto' }}>
      <div className="section-head">
        <div>
          <h1 style={{ fontSize: 20 }}>Settings</h1>
          <div className="section-sub">Everything is stored in this browser. Nothing is sent anywhere but the price feed.</div>
        </div>
        <Button onClick={onDone}>Back to dashboard</Button>
      </div>

      {/* --- Data source ---------------------------------------------------- */}

      <Card>
        <div className="card-head">
          <div>
            <div className="card-title">Market data</div>
            <div className="card-note">Where prices come from, and how often they refresh.</div>
          </div>
        </div>

        <div className="stack" style={{ gap: 10 }}>
          {PROVIDER_CHOICES.map((choice) => (
            <label
              key={choice.id}
              className="switch-row"
              style={{
                cursor: 'pointer',
                border: '1px solid',
                borderColor: settings.providerId === choice.id ? 'var(--accent-border)' : 'var(--border)',
                background: settings.providerId === choice.id ? 'var(--accent-weak)' : 'transparent',
                borderRadius: 'var(--radius-sm)',
                padding: '12px 14px',
              }}
            >
              <span>
                <span className="switch-label">{choice.label}</span>
                <span className="switch-sub">{choice.blurb}</span>
              </span>
              <input
                type="radio"
                name="provider"
                checked={settings.providerId === choice.id}
                onChange={() => updateSettings({ providerId: choice.id as ProviderId })}
                style={{ flex: 'none', width: 18, height: 18, accentColor: 'var(--accent)' }}
              />
            </label>
          ))}
        </div>

        {settings.providerId === 'twelvedata' && (
          <div style={{ marginTop: 14 }}>
            <Field
              label="Twelve Data API key"
              htmlFor="td-key"
              hint="Free at twelvedata.com. Stored only in this browser."
            >
              <Input
                id="td-key"
                value={settings.twelveDataKey}
                placeholder="Paste your API key"
                onChange={(event) => updateSettings({ twelveDataKey: event.target.value.trim() })}
              />
            </Field>
          </div>
        )}

        <div style={{ marginTop: 16 }}>
          <Banner tone="info" title={`Update frequency — ${provider.label}`}>
            {provider.freshness}
          </Banner>
        </div>

        <div style={{ marginTop: 14 }}>
          <Field label="Auto-refresh" htmlFor="refresh">
            <Select
              id="refresh"
              value={String(settings.refreshSeconds)}
              onChange={(event) => updateSettings({ refreshSeconds: Number(event.target.value) })}
            >
              {REFRESH_OPTIONS.map((option) => (
                <option key={option.value} value={option.value}>
                  {option.label}
                </option>
              ))}
            </Select>
            <span className="field-hint">
              Pauses while the tab is in the background, and slows to a tenth of this rate when the markets you hold are
              closed.
            </span>
          </Field>
        </div>
      </Card>

      {/* --- Appearance ----------------------------------------------------- */}

      <Card>
        <div className="card-head">
          <div className="card-title">Appearance</div>
        </div>
        <div className="switch-row">
          <span>
            <span className="switch-label">Theme</span>
            <span className="switch-sub">
              The sun / moon button in the header flips between light and dark. Pick “System” here to follow your
              device instead — it is currently {resolvedTheme}.
            </span>
          </span>
          <Select
            value={settings.theme}
            onChange={(event) => updateSettings({ theme: event.target.value as typeof settings.theme })}
            style={{ width: 150, flex: 'none' }}
            aria-label="Theme"
          >
            <option value="system">System ({resolvedTheme})</option>
            <option value="light">Light</option>
            <option value="dark">Dark</option>
          </Select>
        </div>
        <div className="switch-row">
          <span>
            <span className="switch-label">Blur amounts</span>
            <span className="switch-sub">
              Hides money amounts behind a blur while leaving percentages readable — handy when someone else is looking
              at the screen.
            </span>
          </span>
          <input
            type="checkbox"
            checked={settings.privacyMode}
            onChange={(event) => updateSettings({ privacyMode: event.target.checked })}
            style={{ flex: 'none', width: 18, height: 18, accentColor: 'var(--accent)' }}
            aria-label="Blur amounts"
          />
        </div>
        <div className="switch-row">
          <span>
            <span className="switch-label">Currency for “{portfolio.name}”</span>
            <span className="switch-sub">Totals are reported in this currency; holdings quoted elsewhere are converted.</span>
          </span>
          <Select
            value={portfolio.baseCurrency}
            onChange={(event) => setPortfolioCurrency(portfolio.id, event.target.value)}
            style={{ width: 110, flex: 'none' }}
            aria-label="Base currency"
          >
            {CURRENCIES.map((code) => (
              <option key={code} value={code}>
                {code}
              </option>
            ))}
          </Select>
        </div>
      </Card>

      {/* --- Backup --------------------------------------------------------- */}

      <Card>
        <div className="card-head">
          <div>
            <div className="card-title">Backup &amp; transfer</div>
            <div className="card-note">
              Portfolios live in this browser’s local storage. Clearing site data would wipe them, so keep a backup —
              it is also how you move a portfolio to another device or hand one to someone else.
            </div>
          </div>
        </div>
        <div className="row-wrap">
          <Button onClick={() => exportAll(data)}>Export everything (JSON)</Button>
          <Button onClick={() => exportPortfolio(portfolio)}>Export “{portfolio.name}” (JSON)</Button>
          <Button onClick={() => exportCsv(portfolio)}>Export “{portfolio.name}” (CSV)</Button>
          <Button onClick={importBackup}>Import a JSON backup…</Button>
        </div>
        <p className="field-hint" style={{ marginTop: 10 }}>
          Importing replaces everything currently in this browser. Export first if you are not sure.
        </p>
      </Card>

      {/* --- Portfolios ----------------------------------------------------- */}

      <Card>
        <div className="card-head">
          <div>
            <div className="card-title">Portfolios</div>
            <div className="card-note">One per person. Switch between them from the header.</div>
          </div>
        </div>
        <div className="stack" style={{ gap: 8 }}>
          {data.portfolios.map((entry) => (
            <div className="switch-row" key={entry.id}>
              <span className="row" style={{ gap: 9 }}>
                <PortfolioAvatar id={entry.id} name={entry.name} size={22} />
                <span>
                  <span className="switch-label">{entry.name}</span>
                  <span className="switch-sub">
                    {entry.positions.length} holding{entry.positions.length === 1 ? '' : 's'} · {entry.baseCurrency}
                  </span>
                </span>
                {entry.sample && <Chip tone="warn">Sample</Chip>}
              </span>
              <Button
                size="sm"
                variant="danger"
                disabled={data.portfolios.length <= 1}
                onClick={() => {
                  if (entry.id === portfolio.id) setConfirm('delete-portfolio')
                  else {
                    deletePortfolio(entry.id)
                    toast(`${entry.name} deleted`, 'success')
                  }
                }}
              >
                Delete
              </Button>
            </div>
          ))}
        </div>
      </Card>

      {/* --- Danger zone ---------------------------------------------------- */}

      <Card>
        <div className="card-head">
          <div>
            <div className="card-title">Start fresh</div>
            <div className="card-note">
              Deletes every portfolio in this browser and leaves one empty one. Use it to clear the sample data.
            </div>
          </div>
          <Button variant="danger" onClick={() => setConfirm('fresh')}>
            Delete all data
          </Button>
        </div>
      </Card>

      {confirm === 'fresh' && (
        <Modal
          title="Delete everything?"
          onClose={() => setConfirm(null)}
          footer={
            <>
              <Button onClick={() => setConfirm(null)}>Cancel</Button>
              <Button
                variant="danger"
                onClick={() => {
                  startFresh(freshName)
                  setConfirm(null)
                  toast('All data cleared', 'success')
                  onDone()
                }}
              >
                Delete all data
              </Button>
            </>
          }
        >
          <p style={{ margin: 0, color: 'var(--text-2)' }}>
            All {data.portfolios.length} portfolio{data.portfolios.length === 1 ? '' : 's'} and every holding in them
            will be removed from this browser. This cannot be undone — export a backup first if you might want them
            back.
          </p>
          <Field label="Name for the new empty portfolio" htmlFor="fresh-name">
            <Input id="fresh-name" value={freshName} onChange={(event) => setFreshName(event.target.value)} />
          </Field>
        </Modal>
      )}

      {confirm === 'delete-portfolio' && (
        <ConfirmDialog
          title={`Delete “${portfolio.name}”?`}
          destructive
          confirmLabel="Delete portfolio"
          message={`All ${portfolio.positions.length} holdings in this portfolio will be removed. This cannot be undone.`}
          onCancel={() => setConfirm(null)}
          onConfirm={() => {
            deletePortfolio(portfolio.id)
            toast('Portfolio deleted', 'success')
            setConfirm(null)
          }}
        />
      )}
    </div>
  )
}
