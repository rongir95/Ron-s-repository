import { Field, Input, Textarea, Select, Checkbox, RepeatableList, SuggestionChips } from '../../components/forms'
import {
  DEPENDENCY_TYPES,
  RISK_SEVERITIES,
  SCENARIO_PRIORITIES,
  EDGE_CASE_SUGGESTIONS,
  REFERENCE_TYPES,
} from '../../data/options'
import { uid } from '../../data/factory'
import type { RiskSeverity, ScenarioPriority } from '../../types'
import { Helper, type StepProps } from './shared'

export function StepDependencies({ draft, update }: StepProps) {
  return (
    <div>
      <Helper>Flag anything UX depends on — especially dependencies that block design work.</Helper>
      <RepeatableList
        items={draft.dependencies}
        itemLabel="Dependency"
        addLabel="Add dependency"
        emptyHint="No dependencies yet."
        onAdd={() =>
          update((d) =>
            d.dependencies.push({ id: uid('dep'), name: '', type: 'API', owner: '', status: 'Open', blockingUx: false, notes: '' }),
          )
        }
        onRemove={(id) => update((d) => (d.dependencies = d.dependencies.filter((x) => x.id !== id)))}
        renderItem={(dep) => {
          const set = (field: keyof typeof dep) => (v: string) =>
            update((d) => ((d.dependencies.find((x) => x.id === dep.id)![field] as string) = v))
          return (
            <>
              <div className="field-row">
                <Field label="Dependency name">
                  <Input value={dep.name} onChange={set('name')} />
                </Field>
                <Field label="Type">
                  <Select value={dep.type} options={DEPENDENCY_TYPES} onChange={(v) => update((d) => (d.dependencies.find((x) => x.id === dep.id)!.type = v))} />
                </Field>
              </div>
              <div className="field-row-3">
                <Field label="Owner">
                  <Input value={dep.owner} onChange={set('owner')} />
                </Field>
                <Field label="Status">
                  <Select value={dep.status} options={['Open', 'In Progress', 'Ready', 'Blocked'] as const} onChange={(v) => update((d) => (d.dependencies.find((x) => x.id === dep.id)!.status = v))} />
                </Field>
                <Field label="Notes">
                  <Input value={dep.notes} onChange={set('notes')} />
                </Field>
              </div>
              <Checkbox
                checked={dep.blockingUx}
                onChange={(v) => update((d) => (d.dependencies.find((x) => x.id === dep.id)!.blockingUx = v))}
                label="This is blocking UX"
              />
            </>
          )
        }}
      />
    </div>
  )
}

export function StepRisks({ draft, update }: StepProps) {
  return (
    <div>
      <RepeatableList
        items={draft.risks}
        itemLabel="Risk"
        addLabel="Add risk"
        emptyHint="No risks or constraints added yet."
        onAdd={() => update((d) => d.risks.push({ id: uid('risk'), risk: '', impact: '', mitigation: '', severity: 'Medium', owner: '' }))}
        onRemove={(id) => update((d) => (d.risks = d.risks.filter((x) => x.id !== id)))}
        renderItem={(r) => {
          const set = (field: keyof typeof r) => (v: string) =>
            update((d) => ((d.risks.find((x) => x.id === r.id)![field] as string) = v))
          return (
            <>
              <Field label="Risk / constraint">
                <Textarea value={r.risk} rows={2} onChange={set('risk')} />
              </Field>
              <div className="field-row">
                <Field label="Impact">
                  <Input value={r.impact} onChange={set('impact')} />
                </Field>
                <Field label="Mitigation">
                  <Input value={r.mitigation} onChange={set('mitigation')} />
                </Field>
              </div>
              <div className="field-row">
                <Field label="Severity">
                  <Select value={r.severity} options={RISK_SEVERITIES} onChange={(v: RiskSeverity) => update((d) => (d.risks.find((x) => x.id === r.id)!.severity = v))} />
                </Field>
                <Field label="Owner">
                  <Input value={r.owner} onChange={set('owner')} />
                </Field>
              </div>
            </>
          )
        }}
      />
    </div>
  )
}

export function StepEdgeCases({ draft, update }: StepProps) {
  const add = (edgeCase = '') =>
    update((d) => d.edgeCases.push({ id: uid('edge'), edgeCase, expectedBehavior: '', priority: 'Should', notes: '' }))
  return (
    <div>
      <Helper>Edge cases surface hidden design work early. Add from the suggestions or your own.</Helper>
      <SuggestionChips options={EDGE_CASE_SUGGESTIONS} onPick={(e) => add(e)} />
      <RepeatableList
        items={draft.edgeCases}
        itemLabel="Edge case"
        addLabel="Add edge case"
        emptyHint="No edge cases added yet."
        onAdd={() => add()}
        onRemove={(id) => update((d) => (d.edgeCases = d.edgeCases.filter((x) => x.id !== id)))}
        renderItem={(e) => {
          const set = (field: keyof typeof e) => (v: string) =>
            update((d) => ((d.edgeCases.find((x) => x.id === e.id)![field] as string) = v))
          return (
            <>
              <Field label="Edge case">
                <Input value={e.edgeCase} onChange={set('edgeCase')} />
              </Field>
              <Field label="Expected behavior">
                <Textarea value={e.expectedBehavior} rows={2} onChange={set('expectedBehavior')} />
              </Field>
              <div className="field-row">
                <Field label="Priority">
                  <Select value={e.priority} options={SCENARIO_PRIORITIES} onChange={(v: ScenarioPriority) => update((d) => (d.edgeCases.find((x) => x.id === e.id)!.priority = v))} />
                </Field>
                <Field label="Notes">
                  <Input value={e.notes} onChange={set('notes')} />
                </Field>
              </div>
            </>
          )
        }}
      />
    </div>
  )
}

export function StepOutOfScope({ draft, update }: StepProps) {
  return (
    <div>
      <Helper>Even "None for now" is useful — it tells UX the boundary is intentional.</Helper>
      <RepeatableList
        items={draft.outOfScope}
        itemLabel="Item"
        addLabel="Add out-of-scope item"
        emptyHint="Nothing marked out of scope yet."
        onAdd={() => update((d) => d.outOfScope.push({ id: uid('oos'), item: '', reason: '', futureConsideration: false }))}
        onRemove={(id) => update((d) => (d.outOfScope = d.outOfScope.filter((x) => x.id !== id)))}
        renderItem={(o) => {
          const set = (field: keyof typeof o) => (v: string) =>
            update((d) => ((d.outOfScope.find((x) => x.id === o.id)![field] as string) = v))
          return (
            <>
              <Field label="Item">
                <Input value={o.item} onChange={set('item')} />
              </Field>
              <Field label="Reason">
                <Input value={o.reason} onChange={set('reason')} />
              </Field>
              <Checkbox
                checked={o.futureConsideration}
                onChange={(v) => update((d) => (d.outOfScope.find((x) => x.id === o.id)!.futureConsideration = v))}
                label="Future consideration"
              />
            </>
          )
        }}
      />
    </div>
  )
}

export function StepOpenQuestions({ draft, update }: StepProps) {
  const blocking = draft.openQuestions.filter((q) => q.blockingUx)
  const nonBlocking = draft.openQuestions.filter((q) => !q.blockingUx)
  const renderQuestion = (q: (typeof draft.openQuestions)[number]) => {
    const set = (field: keyof typeof q) => (v: string) =>
      update((d) => ((d.openQuestions.find((x) => x.id === q.id)![field] as string) = v))
    return (
      <div className="repeat-item" key={q.id}>
        <div className="repeat-item-head">
          <span className="idx">Question</span>
          <span className="spacer" />
          <button className="icon-btn" onClick={() => update((d) => (d.openQuestions = d.openQuestions.filter((x) => x.id !== q.id)))}>
            ✕
          </button>
        </div>
        <Field label="Question">
          <Textarea value={q.question} rows={2} onChange={set('question')} />
        </Field>
        <div className="field-row-3">
          <Field label="Asked by">
            <Input value={q.askedBy} onChange={set('askedBy')} />
          </Field>
          <Field label="Owner">
            <Input value={q.owner} onChange={set('owner')} />
          </Field>
          <Field label="Status">
            <Select value={q.status} options={['Open', 'Answered', 'Blocked'] as const} onChange={(v) => update((d) => (d.openQuestions.find((x) => x.id === q.id)!.status = v))} />
          </Field>
        </div>
        <div className="field-row-3">
          <Field label="Deadline">
            <Input type="date" value={q.deadline} onChange={set('deadline')} />
          </Field>
          <Field label="Date answered">
            <Input type="date" value={q.dateAnswered} onChange={set('dateAnswered')} />
          </Field>
          <Field label="Blocking UX?">
            <Select value={q.blockingUx ? 'Yes' : 'No'} options={['Yes', 'No'] as const} onChange={(v) => update((d) => (d.openQuestions.find((x) => x.id === q.id)!.blockingUx = v === 'Yes'))} />
          </Field>
        </div>
        <Field label="Answer">
          <Textarea value={q.answer} rows={2} onChange={set('answer')} />
        </Field>
      </div>
    )
  }
  return (
    <div>
      <Helper>Blocking questions gate design work — they are shown separately to the UX team.</Helper>
      <div className="callout red" style={{ marginBottom: 12 }}>
        <strong>⚠ Blocking UX ({blocking.length})</strong> — these must be resolved before design can safely proceed.
      </div>
      {blocking.map(renderQuestion)}

      <div className="callout blue" style={{ margin: '18px 0 12px' }}>
        <strong>Not blocking UX ({nonBlocking.length})</strong> — useful to track, but design can continue.
      </div>
      {nonBlocking.map(renderQuestion)}

      <button
        className="btn ghost"
        style={{ borderStyle: 'dashed', borderColor: 'var(--border-strong)', borderWidth: 1, marginTop: 8 }}
        onClick={() =>
          update((d) =>
            d.openQuestions.push({
              id: uid('q'),
              question: '',
              askedBy: '',
              owner: '',
              status: 'Open',
              blockingUx: false,
              deadline: '',
              answer: '',
              dateAnswered: '',
            }),
          )
        }
      >
        + Add question
      </button>
    </div>
  )
}

export function StepDecisionLog({ draft, update }: StepProps) {
  return (
    <div>
      <RepeatableList
        items={draft.decisionLog}
        itemLabel="Decision"
        addLabel="Add decision"
        emptyHint="No decisions logged yet."
        onAdd={() => update((d) => d.decisionLog.push({ id: uid('dec'), date: '', decision: '', owner: '', reason: '', impactOnUx: '', related: '' }))}
        onRemove={(id) => update((d) => (d.decisionLog = d.decisionLog.filter((x) => x.id !== id)))}
        renderItem={(dec) => {
          const set = (field: keyof typeof dec) => (v: string) =>
            update((d) => ((d.decisionLog.find((x) => x.id === dec.id)![field] as string) = v))
          return (
            <>
              <div className="field-row">
                <Field label="Date">
                  <Input type="date" value={dec.date} onChange={set('date')} />
                </Field>
                <Field label="Owner">
                  <Input value={dec.owner} onChange={set('owner')} />
                </Field>
              </div>
              <Field label="Decision">
                <Textarea value={dec.decision} rows={2} onChange={set('decision')} />
              </Field>
              <div className="field-row">
                <Field label="Reason">
                  <Input value={dec.reason} onChange={set('reason')} />
                </Field>
                <Field label="Impact on UX">
                  <Input value={dec.impactOnUx} onChange={set('impactOnUx')} />
                </Field>
              </div>
              <Field label="Related question or dependency">
                <Input value={dec.related} onChange={set('related')} />
              </Field>
            </>
          )
        }}
      />
    </div>
  )
}

export function StepReferences({ draft, update }: StepProps) {
  return (
    <div>
      <Helper>Link everything UX will want to open — Figma, docs, research, related features.</Helper>
      <RepeatableList
        items={draft.references}
        itemLabel="Reference"
        addLabel="Add reference"
        emptyHint="No references linked yet."
        onAdd={() => update((d) => d.references.push({ id: uid('ref'), type: 'Figma', label: '', url: '' }))}
        onRemove={(id) => update((d) => (d.references = d.references.filter((x) => x.id !== id)))}
        renderItem={(ref) => {
          const set = (field: keyof typeof ref) => (v: string) =>
            update((d) => ((d.references.find((x) => x.id === ref.id)![field] as string) = v))
          return (
            <div className="field-row-3">
              <Field label="Type">
                <Select value={ref.type} options={REFERENCE_TYPES} onChange={set('type')} />
              </Field>
              <Field label="Label">
                <Input value={ref.label} onChange={set('label')} />
              </Field>
              <Field label="URL">
                <Input value={ref.url} placeholder="https://…" onChange={set('url')} />
              </Field>
            </div>
          )
        }}
      />
    </div>
  )
}
