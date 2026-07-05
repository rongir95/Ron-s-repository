import { useCallback, useEffect, useMemo, useRef, useState } from 'react'
import type { FeatureBrief } from '../../types'
import { useStore } from '../../store/store'
import { useNav } from '../../store/nav'
import { Button, ProgressBar, EmptyState } from '../../components/ui'
import { StatusChip } from '../../components/chips'
import { WIZARD_STEPS, REVIEW_STEP_TITLE } from './steps'
import { StepHead } from './shared'
import { ReviewStep } from './ReviewStep'
import { Field, Textarea, Select } from '../../components/forms'
import { GenericChip } from '../../components/chips'

export function Wizard() {
  const { getBrief } = useStore()
  const nav = useNav()
  const brief = nav.briefId ? getBrief(nav.briefId) : undefined

  if (!brief) {
    return (
      <EmptyState icon="🔍" title="No brief selected" action={<Button variant="primary" onClick={() => nav.navigate('dashboard')}>Go to dashboard</Button>}>
        Open a brief from the dashboard to start editing.
      </EmptyState>
    )
  }

  return <WizardInner key={brief.id} initial={brief} />
}

function WizardInner({ initial }: { initial: FeatureBrief }) {
  const { saveBrief, toast } = useStore()
  const nav = useNav()
  const [draft, setDraft] = useState<FeatureBrief>(() => structuredClone(initial))
  const [stepIndex, setStepIndex] = useState(0)
  const saveTimer = useRef<number | undefined>(undefined)

  const totalSteps = WIZARD_STEPS.length + 1 // + review
  const isReview = stepIndex === WIZARD_STEPS.length

  // Mutation helper: edit a clone so nested writes are ergonomic.
  const update = useCallback((mutator: (d: FeatureBrief) => void) => {
    setDraft((prev) => {
      const next = structuredClone(prev)
      mutator(next)
      next.updatedAt = new Date().toISOString()
      return next
    })
  }, [])

  // Debounced autosave to localStorage (via the store).
  useEffect(() => {
    if (saveTimer.current) window.clearTimeout(saveTimer.current)
    saveTimer.current = window.setTimeout(() => {
      saveBrief(draft)
    }, 500)
    return () => {
      if (saveTimer.current) window.clearTimeout(saveTimer.current)
    }
  }, [draft, saveBrief])

  const sectionStatus = useMemo(
    () => WIZARD_STEPS.map((s) => ({ key: s.key, title: s.title, done: s.hasContent(draft) })),
    [draft],
  )
  const completedCount = sectionStatus.filter((s) => s.done).length
  const completionPct = Math.round((completedCount / WIZARD_STEPS.length) * 100)

  const saveNow = (message = 'Draft saved') => {
    saveBrief(draft)
    toast(message, 'success')
  }

  const handleSubmit = () => {
    const submitted: FeatureBrief = {
      ...draft,
      status: 'In UX Review',
      submittedAt: new Date().toISOString(),
      uxReview: { ...draft.uxReview, reviewStatus: 'In UX Review' },
    }
    setDraft(submitted)
    saveBrief(submitted)
    toast('Submitted for UX review', 'success')
    nav.navigate('dashboard')
  }

  const goTo = (i: number) => {
    setStepIndex(i)
    window.scrollTo({ top: 0 })
  }

  const ActiveComponent = isReview ? null : WIZARD_STEPS[stepIndex].component

  return (
    <div>
      <div className="page-head">
        <div>
          <div className="row" style={{ marginBottom: 6 }}>
            <button className="link-btn" onClick={() => nav.navigate('dashboard')}>
              ← Dashboard
            </button>
            <StatusChip status={draft.status} />
          </div>
          <h1>{draft.featureName || 'Untitled feature brief'}</h1>
          <p>Complete each section — your progress saves automatically.</p>
        </div>
        <div className="page-head-actions">
          <Button onClick={() => saveNow()}>Save Draft</Button>
        </div>
      </div>

      <div className="card card-pad" style={{ marginBottom: 20 }}>
        <div className="row" style={{ marginBottom: 8, justifyContent: 'space-between' }}>
          <strong className="text-sm">Completion</strong>
          <span className="muted text-sm">
            {completedCount}/{WIZARD_STEPS.length} sections · {completionPct}%
          </span>
        </div>
        <ProgressBar value={completionPct} tone={completionPct >= 80 ? 'green' : completionPct >= 50 ? 'orange' : 'red'} />
      </div>

      <UxFeedbackBanner draft={draft} update={update} />

      <div className="wizard-layout">
        <nav className="stepper" aria-label="Wizard steps">
          {WIZARD_STEPS.map((s, i) => {
            const done = sectionStatus[i].done
            return (
              <button
                key={s.key}
                className={`step-item ${i === stepIndex ? 'active' : ''} ${done ? 'done' : ''}`}
                onClick={() => goTo(i)}
              >
                <span className="step-num">{done ? '✓' : i + 1}</span>
                <span className="step-label">{s.title}</span>
              </button>
            )
          })}
          <button
            className={`step-item ${isReview ? 'active' : ''}`}
            onClick={() => goTo(WIZARD_STEPS.length)}
          >
            <span className="step-num">★</span>
            <span className="step-label">{REVIEW_STEP_TITLE}</span>
          </button>
        </nav>

        <div className="card card-pad">
          {isReview ? (
            <>
              <StepHead step={totalSteps} total={totalSteps} title={REVIEW_STEP_TITLE} />
              <ReviewStep draft={draft} sectionStatus={sectionStatus} onSaveDraft={() => saveNow()} onSubmit={handleSubmit} />
            </>
          ) : (
            <>
              <StepHead step={stepIndex + 1} total={totalSteps} title={WIZARD_STEPS[stepIndex].title} />
              {ActiveComponent && <ActiveComponent draft={draft} update={update} />}
              <div className="wizard-footer">
                <Button onClick={() => goTo(Math.max(0, stepIndex - 1))} disabled={stepIndex === 0}>
                  ← Back
                </Button>
                <span className="spacer" />
                <Button variant="primary" onClick={() => goTo(stepIndex + 1)}>
                  {stepIndex === WIZARD_STEPS.length - 1 ? 'Review & Submit →' : 'Next →'}
                </Button>
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  )
}

// Shown to the PM when the UX team has left questions or asked for more info.
function UxFeedbackBanner({ draft, update }: { draft: FeatureBrief; update: (m: (d: FeatureBrief) => void) => void }) {
  const questions = draft.uxReview.uxQuestions
  const notes = draft.uxReview.uxNotes
  const needsInfo = draft.status === 'Needs More Info'
  if (questions.length === 0 && notes.length === 0 && !needsInfo) return null

  return (
    <div className="card card-pad" style={{ marginBottom: 20, borderColor: needsInfo ? 'var(--orange)' : 'var(--border)' }}>
      <div className="row" style={{ marginBottom: 10 }}>
        <strong style={{ fontSize: 15 }}>{needsInfo ? '⚠ UX needs more info' : 'Feedback from UX'}</strong>
        {needsInfo && <GenericChip label="Action needed" tone="orange" />}
      </div>

      {questions.length > 0 && (
        <div className="stack" style={{ marginBottom: notes.length ? 16 : 0 }}>
          {questions.map((q) => (
            <div key={q.id} className="repeat-item" style={{ marginBottom: 0 }}>
              <div className="row wrap" style={{ marginBottom: 6 }}>
                <GenericChip label={q.section} tone="purple" />
                {q.blockingUx && <GenericChip label="Blocking UX" tone="red" />}
                <GenericChip label={q.status} tone={q.status === 'Answered' ? 'green' : 'orange'} />
              </div>
              <div className="text-sm" style={{ marginBottom: 8 }}>{q.question}</div>
              <Field label="Your answer">
                <Textarea
                  value={q.pmAnswer}
                  rows={2}
                  placeholder="Answer the UX team…"
                  onChange={(v) => update((d) => (d.uxReview.uxQuestions.find((x) => x.id === q.id)!.pmAnswer = v))}
                />
              </Field>
              <Select
                value={q.status}
                options={['Open', 'Answered'] as const}
                onChange={(v) => update((d) => (d.uxReview.uxQuestions.find((x) => x.id === q.id)!.status = v))}
              />
            </div>
          ))}
        </div>
      )}

      {notes.length > 0 && (
        <>
          <div className="muted text-sm" style={{ marginBottom: 6, fontWeight: 600 }}>UX notes</div>
          <div className="stack" style={{ gap: 6 }}>
            {notes.map((n) => (
              <div key={n.id} className="text-sm row wrap">
                <GenericChip label={n.section} />
                <span>{n.text}</span>
              </div>
            ))}
          </div>
        </>
      )}
    </div>
  )
}
