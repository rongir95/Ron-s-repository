import { useMemo, useState } from 'react'
import { useStore } from '../store/store'
import { useNav } from '../store/nav'
import { createBlankBrief } from '../data/factory'
import { computeReadiness, getMissingRequiredFields } from '../utils/readiness'
import { Button, Card, EmptyState } from '../components/ui'
import { StatusChip, PriorityChip, ReadinessChip, GenericChip } from '../components/chips'
import { BRIEF_STATUSES, PRIORITIES } from '../data/options'
import type { FeatureBrief } from '../types'

function formatDate(iso: string): string {
  if (!iso) return '—'
  const d = new Date(iso)
  return d.toLocaleDateString(undefined, { month: 'short', day: 'numeric', year: 'numeric' })
}

function readinessBucket(score: number) {
  if (score >= 80) return 'Ready'
  if (score >= 50) return 'Almost ready'
  return 'Not ready'
}

export function Dashboard() {
  const { briefs, role, addBrief } = useStore()
  const nav = useNav()

  const [search, setSearch] = useState('')
  const [status, setStatus] = useState('')
  const [owner, setOwner] = useState('')
  const [priority, setPriority] = useState('')
  const [readiness, setReadiness] = useState('')

  const owners = useMemo(
    () => Array.from(new Set(briefs.map((b) => b.owners.productOwner).filter(Boolean))).sort(),
    [briefs],
  )

  const rows = useMemo(() => {
    return briefs
      .map((b) => ({ brief: b, readiness: computeReadiness(b), missing: getMissingRequiredFields(b).length }))
      .filter(({ brief, readiness: r }) => {
        if (search && !brief.featureName.toLowerCase().includes(search.toLowerCase())) return false
        if (status && brief.status !== status) return false
        if (owner && brief.owners.productOwner !== owner) return false
        if (priority && brief.priority !== priority) return false
        if (readiness && readinessBucket(r.score) !== readiness) return false
        return true
      })
      .sort((a, b) => new Date(b.brief.updatedAt).getTime() - new Date(a.brief.updatedAt).getTime())
  }, [briefs, search, status, owner, priority, readiness])

  const createNew = () => {
    const b = createBlankBrief()
    addBrief(b)
    nav.openWizard(b.id)
  }

  const openBrief = (b: FeatureBrief) => {
    if (role === 'ux') nav.openUxDetail(b.id)
    else nav.openWizard(b.id)
  }

  return (
    <div>
      <div className="page-head">
        <div>
          <h1>Briefs Dashboard</h1>
          <p>All feature briefs across the workspace.</p>
        </div>
        <div className="page-head-actions">
          {role === 'pm' && (
            <Button variant="primary" onClick={createNew}>
              + New Brief
            </Button>
          )}
        </div>
      </div>

      <div className="filters">
        <input
          className="input search"
          placeholder="Search by feature name…"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
        <select className="select" value={status} onChange={(e) => setStatus(e.target.value)}>
          <option value="">All statuses</option>
          {BRIEF_STATUSES.map((s) => (
            <option key={s} value={s}>
              {s}
            </option>
          ))}
        </select>
        <select className="select" value={owner} onChange={(e) => setOwner(e.target.value)}>
          <option value="">All owners</option>
          {owners.map((o) => (
            <option key={o} value={o}>
              {o}
            </option>
          ))}
        </select>
        <select className="select" value={priority} onChange={(e) => setPriority(e.target.value)}>
          <option value="">All priorities</option>
          {PRIORITIES.map((p) => (
            <option key={p} value={p}>
              {p}
            </option>
          ))}
        </select>
        <select className="select" value={readiness} onChange={(e) => setReadiness(e.target.value)}>
          <option value="">All readiness</option>
          <option value="Ready">Ready</option>
          <option value="Almost ready">Almost ready</option>
          <option value="Not ready">Not ready</option>
        </select>
      </div>

      {rows.length === 0 ? (
        <EmptyState
          icon="🗂"
          title="No briefs match your filters"
          action={role === 'pm' ? <Button variant="primary" onClick={createNew}>+ Create a brief</Button> : undefined}
        >
          Try clearing the filters{role === 'pm' ? ', or create a new feature brief to get started.' : '.'}
        </EmptyState>
      ) : (
        <div className="brief-grid">
          {rows.map(({ brief, readiness: r, missing }) => {
            const blocking = brief.openQuestions.filter((q) => q.blockingUx && q.status !== 'Answered').length
            const platforms = brief.platforms.filter((p) => p.selected).map((p) => p.name)
            return (
              <Card key={brief.id} className="brief-card" onClick={() => openBrief(brief)}>
                <div className="brief-meta" style={{ marginBottom: 8 }}>
                  <StatusChip status={brief.status} />
                  <PriorityChip priority={brief.priority} />
                </div>
                <h3>{brief.featureName || 'Untitled brief'}</h3>
                <p className="summary">{brief.shortSummary || 'No summary yet.'}</p>

                <div className="brief-meta">
                  <ReadinessChip status={r.status} />
                  {platforms.slice(0, 3).map((p) => (
                    <GenericChip key={p} label={p} />
                  ))}
                  {platforms.length > 3 && <GenericChip label={`+${platforms.length - 3}`} />}
                </div>

                <div className="stat-row" style={{ marginTop: 12 }}>
                  <span className="stat">
                    <strong>{r.score}%</strong> ready
                  </span>
                  {blocking > 0 && (
                    <span className="stat warn">
                      ⚠ <strong>{blocking}</strong> blocking
                    </span>
                  )}
                  {missing > 0 && (
                    <span className="stat">
                      <strong>{missing}</strong> missing fields
                    </span>
                  )}
                </div>

                <div className="brief-card-foot">
                  <span>{brief.owners.productOwner || 'Unassigned'}</span>
                  <span>Updated {formatDate(brief.updatedAt)}</span>
                </div>
              </Card>
            )
          })}
        </div>
      )}
    </div>
  )
}
