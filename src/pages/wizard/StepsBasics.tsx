import { Field, Input, Textarea, Select, ChipSelect } from '../../components/forms'
import { PRIORITIES, DOCUMENT_STATUSES, OBJECTIVE_GOALS } from '../../data/options'
import type { Priority } from '../../types'
import { Helper, type StepProps } from './shared'

export function StepOverview({ draft, update }: StepProps) {
  const o = draft.overview
  return (
    <div>
      <Helper>
        Start with a short summary of what this feature is, who it is for, and what it is expected to
        achieve.
      </Helper>

      <Field label="Feature name" required>
        <Input
          value={o.featureName}
          placeholder="e.g. Post-Signup Social Profile Onboarding"
          onChange={(v) =>
            update((d) => {
              d.overview.featureName = v
              d.featureName = v
            })
          }
        />
      </Field>

      <Field label="Short summary" required hint="One or two sentences the UX team can grasp instantly.">
        <Textarea
          value={o.shortSummary}
          rows={3}
          placeholder="A guided onboarding journey shown after signup that helps users…"
          onChange={(v) =>
            update((d) => {
              d.overview.shortSummary = v
              d.shortSummary = v
            })
          }
        />
      </Field>

      <div className="field-row">
        <Field label="Document status">
          <Select
            value={o.documentStatus}
            options={DOCUMENT_STATUSES}
            onChange={(v) => update((d) => (d.overview.documentStatus = v))}
          />
        </Field>
        <Field label="Priority">
          <Select
            value={o.priority}
            options={PRIORITIES}
            onChange={(v: Priority) =>
              update((d) => {
                d.overview.priority = v
                d.priority = v
              })
            }
          />
        </Field>
      </div>

      <div className="field-row-3">
        <Field label="Product owner" required>
          <Input value={draft.owners.productOwner} onChange={(v) => update((d) => (d.owners.productOwner = v))} />
        </Field>
        <Field label="Designer">
          <Input value={draft.owners.designer} onChange={(v) => update((d) => (d.owners.designer = v))} />
        </Field>
        <Field label="Tech lead">
          <Input value={draft.owners.techLead} onChange={(v) => update((d) => (d.owners.techLead = v))} />
        </Field>
      </div>

      <div className="field-row-3">
        <Field label="Data / Analytics owner">
          <Input value={draft.owners.dataOwner} onChange={(v) => update((d) => (d.owners.dataOwner = v))} />
        </Field>
        <Field label="QA owner">
          <Input value={draft.owners.qaOwner} onChange={(v) => update((d) => (d.owners.qaOwner = v))} />
        </Field>
        <Field label="UX owner">
          <Input value={draft.owners.uxOwner} onChange={(v) => update((d) => (d.owners.uxOwner = v))} />
        </Field>
      </div>

      <div className="field-row">
        <Field label="Target release">
          <Input value={o.targetRelease} placeholder="e.g. Q3 2026" onChange={(v) => update((d) => (d.overview.targetRelease = v))} />
        </Field>
        <Field label="Related initiative / DEP / Epic link">
          <Input value={o.relatedInitiative} placeholder="e.g. DEP-482" onChange={(v) => update((d) => (d.overview.relatedInitiative = v))} />
        </Field>
      </div>
    </div>
  )
}

export function StepBackground({ draft, update }: StepProps) {
  const b = draft.background
  return (
    <div>
      <Helper>This section helps UX understand the bigger picture before jumping into solutions.</Helper>
      <Field label="What exists today?">
        <Textarea value={b.whatExistsToday} onChange={(v) => update((d) => (d.background.whatExistsToday = v))} />
      </Field>
      <Field label="What is missing or not working well?">
        <Textarea value={b.whatIsMissing} onChange={(v) => update((d) => (d.background.whatIsMissing = v))} />
      </Field>
      <Field label="Why are we doing this now?">
        <Textarea value={b.whyNow} onChange={(v) => update((d) => (d.background.whyNow = v))} />
      </Field>
      <Field label="Related product areas or previous decisions">
        <Textarea value={b.relatedAreas} onChange={(v) => update((d) => (d.background.relatedAreas = v))} />
      </Field>
      <Field label="Business / market / campaign context">
        <Textarea value={b.marketContext} onChange={(v) => update((d) => (d.background.marketContext = v))} />
      </Field>
    </div>
  )
}

export function StepProblem({ draft, update }: StepProps) {
  const p = draft.problem
  return (
    <div>
      <Helper>
        Try to separate the business problem from the user problem. UX needs to understand both.
      </Helper>
      <Field label="Product / business problem" required>
        <Textarea value={p.businessProblem} onChange={(v) => update((d) => (d.problem.businessProblem = v))} />
      </Field>
      <Field label="User problem" required>
        <Textarea value={p.userProblem} onChange={(v) => update((d) => (d.problem.userProblem = v))} />
      </Field>
      <Field label="Evidence / signal that this problem exists">
        <Textarea value={p.evidence} onChange={(v) => update((d) => (d.problem.evidence = v))} />
      </Field>
      <Field label="What happens if we do nothing?">
        <Textarea value={p.doNothing} onChange={(v) => update((d) => (d.problem.doNothing = v))} />
      </Field>
    </div>
  )
}

export function StepObjectives({ draft, update }: StepProps) {
  const o = draft.objectives
  const toggle = (goal: string) =>
    update((d) => {
      const set = new Set(d.objectives.goals)
      set.has(goal) ? set.delete(goal) : set.add(goal)
      d.objectives.goals = Array.from(set)
    })
  return (
    <div>
      <Field label="Primary objective" required>
        <Textarea value={o.primaryObjective} onChange={(v) => update((d) => (d.objectives.primaryObjective = v))} />
      </Field>
      <Field label="Secondary objectives">
        <Textarea value={o.secondaryObjectives} onChange={(v) => update((d) => (d.objectives.secondaryObjectives = v))} />
      </Field>
      <Field label="Business value">
        <Textarea value={o.businessValue} onChange={(v) => update((d) => (d.objectives.businessValue = v))} />
      </Field>
      <Field label="Expected product impact">
        <Textarea value={o.expectedImpact} onChange={(v) => update((d) => (d.objectives.expectedImpact = v))} />
      </Field>
      <Field label="Strategic relevance">
        <Textarea value={o.strategicRelevance} onChange={(v) => update((d) => (d.objectives.strategicRelevance = v))} />
      </Field>
      <Field label="Goals this feature supports" hint="Select all that apply.">
        <ChipSelect options={OBJECTIVE_GOALS} selected={o.goals} onToggle={toggle} />
      </Field>
    </div>
  )
}
