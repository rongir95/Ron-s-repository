import { useMemo, useState } from 'react'
import { useStore } from '../../store/store'
import { useNav } from '../../store/nav'
import { computeReadiness, getMissingRequiredFields } from '../../utils/readiness'
import { Card, EmptyState, ReadinessRing } from '../../components/ui'
import { StatusChip, PriorityChip, GenericChip } from '../../components/chips'

function formatDate(iso: string): string {
  if (!iso) return '—'
  return new Date(iso).toLocaleDateString(undefined, { month: 'short', day: 'numeric' })
}

// Briefs that are relevant to the UX team (submitted / in review / etc).
const UX_VISIBLE_STATUSES = ['Submitted', 'In UX Review', 'Needs More Info', 'Ready for Design', 'Approved']

export function UXReviewList() {
  const { briefs } = useStore()
  const nav = useNav()
  const [showAll, setShowAll] = useState(false)

  const rows = useMemo(() => {
    return briefs
      .filter((b) => showAll || UX_VISIBLE_STATUSES.includes(b.status))
      .map((b) => ({
        brief: b,
        readiness: computeReadiness(b),
        missing: getMissingRequiredFields(b).length,
        blocking: b.openQuestions.filter((q) => q.blockingUx && q.status !== 'Answered').length,
      }))
      .sort((a, b) => new Date(b.brief.updatedAt).getTime() - new Date(a.brief.updatedAt).getTime())
  }, [briefs, showAll])

  return (
    <div>
      <div className="page-head">
        <div>
          <h1>UX Review</h1>
          <p>Briefs submitted by PMs for design review.</p>
        </div>
        <div className="page-head-actions">
          <label className="checkbox-row" style={{ padding: 0 }}>
            <input type="checkbox" checked={showAll} onChange={(e) => setShowAll(e.target.checked)} />
            <span className="text-sm">Show drafts too</span>
          </label>
        </div>
      </div>

      {rows.length === 0 ? (
        <EmptyState icon="📥" title="No briefs to review yet">
          When a PM submits a brief for UX review it will appear here.
        </EmptyState>
      ) : (
        <div className="stack" style={{ gap: 14 }}>
          {rows.map(({ brief, readiness, missing, blocking }) => (
            <Card key={brief.id} className="brief-card" onClick={() => nav.openUxDetail(brief.id)}>
              <div className="row wrap" style={{ alignItems: 'flex-start', gap: 18 }}>
                <ReadinessRing score={readiness.score} />
                <div className="grow" style={{ minWidth: 200 }}>
                  <div className="brief-meta" style={{ marginBottom: 6 }}>
                    <StatusChip status={brief.status} />
                    <PriorityChip priority={brief.priority} />
                    {brief.platforms.filter((p) => p.selected).slice(0, 4).map((p) => (
                      <GenericChip key={p.name} label={p.name} />
                    ))}
                  </div>
                  <h3>{brief.featureName}</h3>
                  <p className="summary">{brief.shortSummary}</p>
                  <div className="stat-row">
                    <span className="stat">
                      <strong>{brief.owners.productOwner || '—'}</strong>&nbsp;· PM
                    </span>
                    <span className="stat">Release: <strong>{brief.overview.targetRelease || '—'}</strong></span>
                    {blocking > 0 && (
                      <span className="stat warn">⚠ <strong>{blocking}</strong> blocking question{blocking === 1 ? '' : 's'}</span>
                    )}
                    {missing > 0 && <span className="stat"><strong>{missing}</strong> missing fields</span>}
                    <span className="stat">Updated <strong>{formatDate(brief.updatedAt)}</strong></span>
                  </div>
                </div>
              </div>
            </Card>
          ))}
        </div>
      )}
    </div>
  )
}
