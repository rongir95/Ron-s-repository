import { useEffect, useRef, useState } from 'react'
import { PortfolioSwitcher } from './components/PortfolioSwitcher'
import { Button, Chip, IconGear, IconMoon, IconRefresh, IconSun } from './components/ui'
import { relativeTime } from './lib/format'
import { useResolvedTheme } from './lib/theme'
import { useQuotes } from './market/useMarketData'
import { Dashboard } from './pages/Dashboard'
import { Settings } from './pages/Settings'
import { StoreProvider, useStore } from './store/store'

type View = 'dashboard' | 'settings'

function Shell() {
  const { settings, updateSettings, toasts, dismissToast, portfolio } = useStore()
  const [view, setView] = useState<View>('dashboard')
  const { quotes, fxRates, loading, error, lastUpdated, marketOpen, refresh } = useQuotes()
  const resolvedTheme = useResolvedTheme(settings.theme)

  // Theme: an explicit choice stamps data-theme on the root element; "system"
  // leaves the media query to decide. We only ever clear a stamp we set
  // ourselves — when this page is embedded, the host may stamp its own theme,
  // and "system" should defer to it rather than fight it.
  const stampedTheme = useRef(false)
  useEffect(() => {
    const root = document.documentElement
    if (settings.theme === 'system') {
      if (stampedTheme.current) {
        root.removeAttribute('data-theme')
        stampedTheme.current = false
      }
      return
    }
    root.setAttribute('data-theme', settings.theme)
    stampedTheme.current = true
  }, [settings.theme])

  // A ticking clock so "updated 12s ago" stays honest without a re-fetch.
  const [, setNow] = useState(0)
  useEffect(() => {
    const timer = window.setInterval(() => setNow((n) => n + 1), 15_000)
    return () => clearInterval(timer)
  }, [])

  // Keyboard shortcuts: r to refresh, ? nothing fancy — kept minimal.
  useEffect(() => {
    const onKeyDown = (event: KeyboardEvent) => {
      const target = event.target as HTMLElement | null
      if (target && /^(INPUT|TEXTAREA|SELECT)$/.test(target.tagName)) return
      if (event.metaKey || event.ctrlKey || event.altKey) return
      if (event.key === 'r') {
        event.preventDefault()
        refresh()
      }
    }
    document.addEventListener('keydown', onKeyDown)
    return () => document.removeEventListener('keydown', onKeyDown)
  }, [refresh])

  return (
    <div className="app">
      <header className="topbar">
        <div className="topbar-inner">
          <span className="brand">
            <span className="brand-mark" aria-hidden="true">
              <svg width="14" height="14" viewBox="0 0 14 14" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
                <path d="M1.5 10.5 5 6.5l2.6 2.2L12.5 3" />
                <path d="M9.4 3h3.1v3.1" />
              </svg>
            </span>
          </span>

          <PortfolioSwitcher quotes={quotes} fxRates={fxRates} masked={settings.privacyMode} />

          <span className="topbar-spacer" />

          <span className="meta-line desktop-only" aria-live="polite">
            {settings.providerId === 'demo' && <Chip tone="warn">Demo data</Chip>}
            {marketOpen !== null && (
              <span className="row" style={{ gap: 6 }}>
                <span className={`dot ${marketOpen ? 'live' : 'closed'}`} aria-hidden="true" />
                {marketOpen ? 'Market open' : 'Market closed'}
              </span>
            )}
            <span>
              {error ? 'Prices unavailable' : loading && !lastUpdated ? 'Loading prices…' : lastUpdated ? `Updated ${relativeTime(lastUpdated)}` : '—'}
            </span>
          </span>

          <Button
            size="sm"
            onClick={refresh}
            disabled={loading}
            title="Refresh prices (r)"
            aria-label="Refresh prices"
          >
            <IconRefresh />
            <span className="btn-label">{loading ? 'Refreshing…' : 'Refresh'}</span>
          </Button>
          <Button
            size="sm"
            iconOnly
            aria-label={resolvedTheme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode'}
            title={resolvedTheme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode'}
            onClick={() => updateSettings({ theme: resolvedTheme === 'dark' ? 'light' : 'dark' })}
          >
            {/* The icon shows the theme you would switch to, not the current one. */}
            {resolvedTheme === 'dark' ? <IconSun /> : <IconMoon />}
          </Button>
          <Button
            size="sm"
            variant={view === 'settings' ? 'primary' : 'default'}
            iconOnly
            aria-label="Settings"
            title="Settings"
            onClick={() => setView(view === 'settings' ? 'dashboard' : 'settings')}
          >
            <IconGear />
          </Button>
        </div>
      </header>

      <main className="page">
        {view === 'settings' ? (
          <Settings onDone={() => setView('dashboard')} />
        ) : (
          <Dashboard
            key={portfolio.id}
            quotes={quotes}
            fxRates={fxRates}
            quotesLoading={loading}
            quotesError={error}
            lastUpdated={lastUpdated}
            onOpenSettings={() => setView('settings')}
          />
        )}
      </main>

      <div className="toasts" role="status" aria-live="polite">
        {toasts.map((entry) => (
          <div className={`toast ${entry.tone}`} key={entry.id}>
            <span className="grow">{entry.message}</span>
            <Button variant="ghost" size="sm" iconOnly aria-label="Dismiss" onClick={() => dismissToast(entry.id)}>
              ✕
            </Button>
          </div>
        ))}
      </div>
    </div>
  )
}

export default function App() {
  return (
    <StoreProvider>
      <Shell />
    </StoreProvider>
  )
}
