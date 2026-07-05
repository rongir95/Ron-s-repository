import type { FeatureBrief } from '../../types'
import { computeReadiness, getMissingRequiredFields, canSubmit } from '../../utils/readiness'
import { ReadinessRing, Button } from '../../components/ui'
import { ReadinessChip } from '../../components/chips'
import { Helper } from './shared'

export function ReviewStep({
  draft,
  sectionStatus,
  onSaveDraft,
  onSubmit,
}: {
  draft: FeatureBrief
  sectionStatus: { key: string; title: string; done: boolean }[]
  onSaveDraft: () => void
  onSubmit: () => void
}) {
  const readiness = computeReadiness(draft)
  const missing = getMissingRequiredFields(draft)
  const blocking = draft.openQuestions.filter((q) => q.blockingUx && q.status !== 'Answered')
  const submittable = canSubmit(draft)
  const completedCount = sectionStatus.filter((s) => s.done).length

  return (
    <div>
      <Helper>
        Review everything before sharing. When the minimum required fields are complete you can submit
        the brief for UX review.
      </Helper>

      <div className="card card-pad" style={{ display: 'flex', gap: 20, alignItems: 'center', marginBottom: 18 }}>
        <ReadinessRing score={readiness.score} />
        <div>
          <div className="row" style={{ marginBottom: 4 }}>
            <strong style={{ fontSize: 16 }}>Readiness</strong>
            <ReadinessChip status={readiness.status} />
          </div>
          <div className="muted text-sm">
            {completedCount} of {sectionStatus.length} sections have content ·{' '}
            {readiness.metKeys.length} of {readiness.metKeys.length + readiness.missing.length} readiness checks passed
          </div>
        </div>
      </div>

      <div className="field-row" style={{ alignItems: 'start' }}>
        <div>
          <h3 className="mb-8" style={{ fontSize: 14 }}>Completed sections</h3>
          <div className="stack" style={{ gap: 4 }}>
            {sectionStatus.map((s) => (
              <div key={s.key} className="row text-sm">
                <span style={{ color: s.done ? 'var(--green)' : 'var(--text-3)' }}>{s.done ? '✓' : '○'}</span>
                <span style={{ color: s.done ? 'var(--text)' : 'var(--text-3)' }}>{s.title}</span>
              </div>
            ))}
          </div>
        </div>

        <div>
          <h3 className="mb-8" style={{ fontSize: 14 }}>Before you submit</h3>
          {missing.length === 0 ? (
            <div className="callout green">All required fields are complete. This brief is ready to submit.</div>
          ) : (
            <div className="callout orange">
              <strong>{missing.length} required field{missing.length === 1 ? '' : 's'} missing:</strong>
              <ul style={{ margin: '8px 0 0', paddingLeft: 18 }}>
                {missing.map((m) => (
                  <li key={m}>{m}</li>
                ))}
              </ul>
            </div>
          )}

          {blocking.length > 0 && (
            <div className="callout red" style={{ marginTop: 12 }}>
              <strong>{blocking.length} blocking UX question{blocking.length === 1 ? '' : 's'} still open.</strong>
              <ul style={{ margin: '8px 0 0', paddingLeft: 18 }}>
                {blocking.map((q) => (
                  <li key={q.id}>{q.question || '(untitled question)'}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
      </div>

      <div className="wizard-footer">
        <Button onClick={onSaveDraft}>Save Draft</Button>
        <span className="spacer" />
        <Button variant="primary" disabled={!submittable} onClick={onSubmit} title={submittable ? '' : 'Complete required fields first'}>
          Submit for UX Review →
        </Button>
      </div>
      {!submittable && (
        <p className="muted text-sm center" style={{ marginTop: 10 }}>
          Complete the required fields above to enable submission.
        </p>
      )}
    </div>
  )
}
