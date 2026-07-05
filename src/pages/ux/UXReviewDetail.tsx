import { useCallback, useState } from 'react'
import type { FeatureBrief, BriefStatus } from '../../types'
import { useStore } from '../../store/store'
import { useNav } from '../../store/nav'
import { computeReadiness } from '../../utils/readiness'
import { briefToMarkdown, briefToJson, downloadFile, copyToClipboard } from '../../utils/export'
import { uid } from '../../data/factory'
import { Button, Card, ReadinessRing, EmptyState, IconButton, ConfirmModal } from '../../components/ui'
import { StatusChip, PriorityChip, ReadinessChip, GenericChip } from '../../components/chips'
import { Field, Input, Textarea, Select } from '../../components/forms'
import { BriefDocument } from '../../components/BriefDocument'
import { NOTE_PRIORITIES } from '../../data/options'

const SECTION_NAMES = [
  'Overview', 'Context', 'Problem', 'Objective', 'Target users', 'Proposed solution',
  'Platforms & markets', 'Scenarios', 'Entry points', 'Journey structure', 'Requirements',
  'UX goals', 'Copy', 'Data/privacy', 'Analytics', 'Dependencies', 'Risks', 'Edge cases',
  'Out of scope', 'Open questions', 'Decisions', 'References',
]

const CHECKLIST_STATES = ['Ready', 'Missing', 'Not relevant'] as const

export function UXReviewDetail() {
  const { getBrief, saveBrief, toast, settings } = useStore()
  const nav = useNav()
  const brief = nav.briefId ? getBrief(nav.briefId) : undefined
  const [confirmReady, setConfirmReady] = useState(false)

  const update = useCallback(
    (mutator: (d: FeatureBrief) => void) => {
      if (!brief) return
      const next = structuredClone(brief)
      mutator(next)
      next.updatedAt = new Date().toISOString()
      saveBrief(next)
    },
    [brief, saveBrief],
  )

  if (!brief) {
    return (
      <EmptyState icon="🔍" title="Brief not found" action={<Button variant="primary" onClick={() => nav.navigate('ux-review')}>Back to UX Review</Button>}>
        This brief may have been deleted.
      </EmptyState>
    )
  }

  const readiness = computeReadiness(brief)

  const setStatus = (status: BriefStatus, message: string) => {
    update((d) => {
      d.status = status
      d.uxReview.reviewStatus = status
      d.uxReview.reviewedBy = settings.currentUserName
      d.uxReview.reviewedAt = new Date().toISOString()
    })
    toast(message, 'success')
  }

  const exportMarkdown = async () => {
    const ok = await copyToClipboard(briefToMarkdown(brief))
    toast(ok ? 'Markdown copied to clipboard' : 'Copy failed — check permissions', ok ? 'success' : 'error')
  }
  const exportJson = () => {
    downloadFile(`${brief.featureName || 'brief'}.json`.replace(/\s+/g, '-').toLowerCase(), briefToJson(brief))
    toast('JSON downloaded', 'success')
  }

  return (
    <div>
      {confirmReady && (
        <ConfirmModal
          title="Mark as Ready for Design?"
          message="This tells the UX team the brief has enough context to start designing. You can change it later."
          confirmLabel="Mark as Ready"
          onCancel={() => setConfirmReady(false)}
          onConfirm={() => {
            setConfirmReady(false)
            setStatus('Ready for Design', 'Marked as Ready for Design')
          }}
        />
      )}

      {/* Header */}
      <div className="page-head">
        <div>
          <div className="row" style={{ marginBottom: 6 }}>
            <button className="link-btn" onClick={() => nav.navigate('ux-review')}>
              ← UX Review
            </button>
            <StatusChip status={brief.status} />
            <PriorityChip priority={brief.priority} />
          </div>
          <h1>{brief.featureName}</h1>
          <p>
            PM: {brief.owners.productOwner || '—'} · Designer: {brief.owners.designer || '—'} · Release:{' '}
            {brief.overview.targetRelease || '—'}
          </p>
        </div>
        <div className="page-head-actions">
          <Button onClick={() => setStatus('Needs More Info', 'Requested more info from the PM')}>Request More Info</Button>
          <Button variant="primary" onClick={() => setConfirmReady(true)}>Mark as Ready for Design</Button>
        </div>
      </div>

      {/* Readiness summary */}
      <Card className="card-pad" pad style={{ marginBottom: 18 }}>
        <div className="row wrap" style={{ gap: 20, alignItems: 'center' }}>
          <ReadinessRing score={readiness.score} />
          <div className="grow" style={{ minWidth: 220 }}>
            <div className="row" style={{ marginBottom: 6 }}>
              <strong style={{ fontSize: 16 }}>Readiness</strong>
              <ReadinessChip status={readiness.status} />
            </div>
            <div className="muted text-sm">
              {readiness.metKeys.length} of {readiness.metKeys.length + readiness.missing.length} readiness checks passed.
              {brief.uxReview.reviewedBy && ` Last reviewed by ${brief.uxReview.reviewedBy}.`}
            </div>
          </div>
          <div className="row wrap" style={{ gap: 8 }}>
            <Button size="sm" onClick={exportMarkdown}>Copy as Markdown</Button>
            <Button size="sm" onClick={exportJson}>Export as JSON</Button>
            <Button size="sm" onClick={() => window.print()}>Print / PDF</Button>
          </div>
        </div>
      </Card>

      {/* Missing information */}
      <Card className="card-pad" style={{ marginBottom: 18 }}>
        <h3 className="mb-8" style={{ fontSize: 15 }}>Missing information</h3>
        {readiness.missing.length === 0 ? (
          <div className="callout green">Nothing critical is missing — all readiness checks pass.</div>
        ) : (
          <ul style={{ margin: 0, paddingLeft: 18 }}>
            {readiness.missing.map((m) => (
              <li key={m} style={{ marginBottom: 4 }}>
                {m}
              </li>
            ))}
          </ul>
        )}
      </Card>

      {/* Design readiness checklist */}
      <Card className="card-pad" style={{ marginBottom: 18 }}>
        <h3 className="mb-16" style={{ fontSize: 15 }}>Design readiness checklist</h3>
        <div className="table-wrap">
          <table className="data">
            <thead>
              <tr>
                <th style={{ width: '45%' }}>Item</th>
                <th style={{ width: 160 }}>State</th>
                <th>Notes</th>
              </tr>
            </thead>
            <tbody>
              {brief.uxReview.designReadinessChecklist.map((item) => (
                <tr key={item.id}>
                  <td>{item.label}</td>
                  <td>
                    <Select
                      value={item.state}
                      options={CHECKLIST_STATES}
                      onChange={(v) =>
                        update((d) => {
                          const t = d.uxReview.designReadinessChecklist.find((x) => x.id === item.id)
                          if (t) t.state = v
                        })
                      }
                    />
                  </td>
                  <td>
                    <Input
                      value={item.notes}
                      onChange={(v) =>
                        update((d) => {
                          const t = d.uxReview.designReadinessChecklist.find((x) => x.id === item.id)
                          if (t) t.notes = v
                        })
                      }
                    />
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>

      {/* UX notes + questions */}
      <div className="field-row" style={{ alignItems: 'start', marginBottom: 18 }}>
        <UxNotesPanel brief={brief} update={update} />
        <UxQuestionsPanel brief={brief} update={update} />
      </div>

      {/* Full brief view */}
      <h3 style={{ margin: '24px 0 12px', fontSize: 16 }}>Full brief</h3>
      <BriefDocument brief={brief} />
    </div>
  )
}

function UxNotesPanel({ brief, update }: { brief: FeatureBrief; update: (m: (d: FeatureBrief) => void) => void }) {
  const { settings } = useStore()
  const [section, setSection] = useState('Overview')
  const [text, setText] = useState('')
  const [priority, setPriority] = useState<'Low' | 'Medium' | 'High'>('Medium')

  const add = () => {
    if (!text.trim()) return
    update((d) =>
      d.uxReview.uxNotes.push({
        id: uid('note'),
        section,
        text: text.trim(),
        createdBy: settings.currentUserName,
        date: new Date().toISOString().slice(0, 10),
        priority,
      }),
    )
    setText('')
  }

  return (
    <Card className="card-pad">
      <h3 className="mb-16" style={{ fontSize: 15 }}>UX notes ({brief.uxReview.uxNotes.length})</h3>
      <div className="stack" style={{ marginBottom: 14 }}>
        {brief.uxReview.uxNotes.length === 0 && <p className="muted text-sm mt-0">No notes yet.</p>}
        {brief.uxReview.uxNotes.map((n) => (
          <div key={n.id} className="repeat-item" style={{ marginBottom: 0, background: 'var(--surface)' }}>
            <div className="row" style={{ marginBottom: 4 }}>
              <GenericChip label={n.section} tone="brand" />
              <GenericChip label={n.priority} tone={n.priority === 'High' ? 'red' : n.priority === 'Medium' ? 'orange' : 'gray'} />
              <span className="spacer grow" />
              <IconButton onClick={() => update((d) => (d.uxReview.uxNotes = d.uxReview.uxNotes.filter((x) => x.id !== n.id)))} />
            </div>
            <div className="text-sm">{n.text}</div>
            <div className="muted text-sm" style={{ marginTop: 4 }}>{n.createdBy} · {n.date}</div>
          </div>
        ))}
      </div>
      <div className="field-row">
        <Field label="Section">
          <Select value={section} options={SECTION_NAMES} onChange={setSection} />
        </Field>
        <Field label="Priority">
          <Select value={priority} options={NOTE_PRIORITIES} onChange={(v) => setPriority(v)} />
        </Field>
      </div>
      <Field label="Note">
        <Textarea value={text} rows={2} placeholder="Add an internal UX note…" onChange={setText} />
      </Field>
      <Button variant="primary" size="sm" onClick={add} disabled={!text.trim()}>
        Add note
      </Button>
    </Card>
  )
}

function UxQuestionsPanel({ brief, update }: { brief: FeatureBrief; update: (m: (d: FeatureBrief) => void) => void }) {
  const [question, setQuestion] = useState('')
  const [section, setSection] = useState('Overview')
  const [blocking, setBlocking] = useState(false)

  const add = () => {
    if (!question.trim()) return
    update((d) =>
      d.uxReview.uxQuestions.push({
        id: uid('uxq'),
        question: question.trim(),
        section,
        blockingUx: blocking,
        status: 'Open',
        pmAnswer: '',
      }),
    )
    setQuestion('')
    setBlocking(false)
  }

  return (
    <Card className="card-pad">
      <h3 className="mb-16" style={{ fontSize: 15 }}>Questions back to PM ({brief.uxReview.uxQuestions.length})</h3>
      <div className="stack" style={{ marginBottom: 14 }}>
        {brief.uxReview.uxQuestions.length === 0 && <p className="muted text-sm mt-0">No questions raised yet.</p>}
        {brief.uxReview.uxQuestions.map((q) => (
          <div key={q.id} className="repeat-item" style={{ marginBottom: 0, background: 'var(--surface)' }}>
            <div className="row" style={{ marginBottom: 4 }}>
              <GenericChip label={q.section} tone="brand" />
              {q.blockingUx && <GenericChip label="Blocking UX" tone="red" />}
              <GenericChip label={q.status} tone={q.status === 'Answered' ? 'green' : 'orange'} />
              <span className="spacer grow" />
              <IconButton onClick={() => update((d) => (d.uxReview.uxQuestions = d.uxReview.uxQuestions.filter((x) => x.id !== q.id)))} />
            </div>
            <div className="text-sm">{q.question}</div>
            {q.pmAnswer && <div className="muted text-sm" style={{ marginTop: 4 }}>PM: {q.pmAnswer}</div>}
          </div>
        ))}
      </div>
      <div className="field-row">
        <Field label="Section">
          <Select value={section} options={SECTION_NAMES} onChange={setSection} />
        </Field>
        <Field label="Blocking UX?">
          <Select value={blocking ? 'Yes' : 'No'} options={['Yes', 'No'] as const} onChange={(v) => setBlocking(v === 'Yes')} />
        </Field>
      </div>
      <Field label="Question">
        <Textarea value={question} rows={2} placeholder="Ask the PM a question…" onChange={setQuestion} />
      </Field>
      <Button variant="primary" size="sm" onClick={add} disabled={!question.trim()}>
        Add question
      </Button>
    </Card>
  )
}
