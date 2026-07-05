import { useState, type ReactNode } from 'react'
import { useStore } from '../store/store'
import { useNav, type View } from '../store/nav'
import type { Role } from '../types'

interface NavLink {
  view: View
  label: string
  icon: string
  roles: Role[]
}

const NAV_LINKS: NavLink[] = [
  { view: 'dashboard', label: 'Briefs Dashboard', icon: '▦', roles: ['pm', 'ux'] },
  { view: 'wizard', label: 'PM Wizard', icon: '✎', roles: ['pm'] },
  { view: 'ux-review', label: 'UX Review', icon: '◎', roles: ['ux'] },
  { view: 'settings', label: 'Template Overview', icon: '❔', roles: ['pm', 'ux'] },
]

function Sidebar({ open, onClose }: { open: boolean; onClose: () => void }) {
  const { role, setRole, briefs } = useStore()
  const nav = useNav()

  const uxReviewCount = briefs.filter((b) =>
    ['In UX Review', 'Submitted', 'Needs More Info'].includes(b.status),
  ).length

  const go = (view: View) => {
    nav.navigate(view)
    onClose()
  }

  return (
    <aside className={`sidebar ${open ? 'open' : ''}`}>
      <div className="sidebar-brand">
        <div className="sidebar-logo">F</div>
        <div className="sidebar-brand-text">
          <strong>Feature Brief Builder</strong>
          <span>Context before design</span>
        </div>
      </div>

      <nav className="sidebar-nav">
        <div className="nav-section-label">Workspace</div>
        {NAV_LINKS.filter((l) => l.roles.includes(role)).map((l) => {
          const active =
            nav.view === l.view ||
            (l.view === 'ux-review' && nav.view === 'ux-detail') ||
            (l.view === 'dashboard' && nav.view === 'wizard' && role === 'ux')
          return (
            <button
              key={l.view}
              className={`nav-item ${active ? 'active' : ''}`}
              onClick={() => go(l.view)}
            >
              <span className="nav-icon">{l.icon}</span>
              <span>{l.label}</span>
              {l.view === 'ux-review' && uxReviewCount > 0 && (
                <span className="nav-badge">{uxReviewCount}</span>
              )}
            </button>
          )
        })}
      </nav>

      <div className="sidebar-footer">
        <div className="nav-section-label" style={{ padding: '0 4px 8px' }}>
          Prototype role
        </div>
        <div className="role-switch">
          <button className={role === 'pm' ? 'active' : ''} onClick={() => setRole('pm')}>
            PM View
          </button>
          <button className={role === 'ux' ? 'active' : ''} onClick={() => setRole('ux')}>
            UX View
          </button>
        </div>
      </div>
    </aside>
  )
}

function ToastStack() {
  const { toasts, dismissToast } = useStore()
  return (
    <div className="toast-stack">
      {toasts.map((t) => (
        <div key={t.id} className={`toast ${t.variant}`} onClick={() => dismissToast(t.id)}>
          <span>{t.variant === 'success' ? '✓' : t.variant === 'error' ? '⚠' : 'ℹ'}</span>
          <span>{t.message}</span>
        </div>
      ))}
    </div>
  )
}

export function Layout({ title, subtitle, children }: { title: string; subtitle?: string; children: ReactNode }) {
  const { role } = useStore()
  const [sidebarOpen, setSidebarOpen] = useState(false)

  return (
    <div className="app">
      <div
        className={`overlay-backdrop ${sidebarOpen ? 'show' : ''}`}
        onClick={() => setSidebarOpen(false)}
      />
      <Sidebar open={sidebarOpen} onClose={() => setSidebarOpen(false)} />
      <div className="main">
        <header className="header">
          <button className="menu-btn" onClick={() => setSidebarOpen((o) => !o)} aria-label="Menu">
            ☰
          </button>
          <div className="header-title">
            <strong>{title}</strong>
            {subtitle && <span>{subtitle}</span>}
          </div>
          <div className="header-spacer" />
          <div className="header-role-pill">
            <span className={`chip ${role === 'pm' ? 'brand' : 'purple'}`} style={{ padding: '2px 8px' }}>
              {role === 'pm' ? 'Product Manager' : 'UX Reviewer'}
            </span>
          </div>
        </header>
        <div className="content">{children}</div>
      </div>
      <ToastStack />
    </div>
  )
}
