import { Field, Input, Textarea, Select, Checkbox, ChipSelect, RepeatableList, SuggestionChips } from '../../components/forms'
import { MOSCOW, UX_PRINCIPLES, EVENT_SUGGESTIONS } from '../../data/options'
import { uid } from '../../data/factory'
import type { MoSCoW } from '../../types'
import { Helper, type StepProps } from './shared'

export function StepRequirements({ draft, update }: StepProps) {
  return (
    <div>
      <Helper>List the core requirements. Mark each with a MoSCoW priority so UX knows what is essential.</Helper>
      <RepeatableList
        items={draft.requirements}
        itemLabel="Requirement"
        addLabel="Add requirement"
        emptyHint="No requirements yet. Add at least one core requirement."
        onAdd={() =>
          update((d) =>
            d.requirements.push({
              id: uid('req'),
              title: '',
              description: '',
              priority: 'Must',
              platform: 'All',
              owner: '',
              status: 'Open',
              notes: '',
            }),
          )
        }
        onRemove={(id) => update((d) => (d.requirements = d.requirements.filter((r) => r.id !== id)))}
        renderItem={(r) => {
          const set = (field: keyof typeof r) => (v: string) =>
            update((d) => ((d.requirements.find((x) => x.id === r.id)![field] as string) = v))
          return (
            <>
              <Field label="Requirement title">
                <Input value={r.title} onChange={set('title')} />
              </Field>
              <Field label="Description">
                <Textarea value={r.description} rows={2} onChange={set('description')} />
              </Field>
              <div className="field-row-3">
                <Field label="Priority">
                  <Select value={r.priority} options={MOSCOW} onChange={(v: MoSCoW) => update((d) => (d.requirements.find((x) => x.id === r.id)!.priority = v))} />
                </Field>
                <Field label="Platform">
                  <Input value={r.platform} onChange={set('platform')} />
                </Field>
                <Field label="Owner">
                  <Input value={r.owner} onChange={set('owner')} />
                </Field>
              </div>
              <div className="field-row">
                <Field label="Status">
                  <Select
                    value={r.status}
                    options={['Open', 'Ready', 'Blocked', 'Changed'] as const}
                    onChange={(v) => update((d) => (d.requirements.find((x) => x.id === r.id)!.status = v))}
                  />
                </Field>
                <Field label="Notes">
                  <Input value={r.notes} onChange={set('notes')} />
                </Field>
              </div>
            </>
          )
        }}
      />
    </div>
  )
}

export function StepUxGoals({ draft, update }: StepProps) {
  const g = draft.uxGoals
  const toggle = (p: string) =>
    update((d) => {
      const set = new Set(d.uxGoals.selectedPrinciples)
      set.has(p) ? set.delete(p) : set.add(p)
      d.uxGoals.selectedPrinciples = Array.from(set)
    })
  return (
    <div>
      <Field label="How should the experience feel?">
        <Textarea value={g.shouldFeel} onChange={(v) => update((d) => (d.uxGoals.shouldFeel = v))} />
      </Field>
      <Field label="What should the experience avoid?">
        <Textarea value={g.shouldAvoid} onChange={(v) => update((d) => (d.uxGoals.shouldAvoid = v))} />
      </Field>
      <Field label="Design principles for this feature">
        <Textarea value={g.designPrinciples} rows={2} onChange={(v) => update((d) => (d.uxGoals.designPrinciples = v))} />
      </Field>
      <Field label="Experience principles" hint="Select the principles that apply.">
        <ChipSelect options={UX_PRINCIPLES} selected={g.selectedPrinciples} onToggle={toggle} />
      </Field>
    </div>
  )
}

export function StepCopy({ draft, update }: StepProps) {
  const c = draft.copyRequirements
  return (
    <div>
      <Field label="Tone of voice">
        <Input value={c.toneOfVoice} onChange={(v) => update((d) => (d.copyRequirements.toneOfVoice = v))} />
      </Field>
      <Field label="Mandatory messages">
        <Textarea value={c.mandatoryMessages} rows={2} onChange={(v) => update((d) => (d.copyRequirements.mandatoryMessages = v))} />
      </Field>
      <div className="field-row">
        <Field label="Words or terms to avoid">
          <Input value={c.wordsToAvoid} onChange={(v) => update((d) => (d.copyRequirements.wordsToAvoid = v))} />
        </Field>
        <Field label="Localisation considerations">
          <Input value={c.localisation} onChange={(v) => update((d) => (d.copyRequirements.localisation = v))} />
        </Field>
      </div>
      <Field label="Error message guidance">
        <Textarea value={c.errorGuidance} rows={2} onChange={(v) => update((d) => (d.copyRequirements.errorGuidance = v))} />
      </Field>
      <Field label="Confirmation message guidance">
        <Textarea value={c.confirmationGuidance} rows={2} onChange={(v) => update((d) => (d.copyRequirements.confirmationGuidance = v))} />
      </Field>
      <Field label="Link to copy doc">
        <Input value={c.copyDocLink} placeholder="https://…" onChange={(v) => update((d) => (d.copyRequirements.copyDocLink = v))} />
      </Field>
      <Checkbox
        checked={c.legalCopyRequired}
        onChange={(v) => update((d) => (d.copyRequirements.legalCopyRequired = v))}
        label="Legal / privacy copy is required"
      />
    </div>
  )
}

export function StepDataPrivacy({ draft, update }: StepProps) {
  return (
    <div>
      <Helper>List every data point the feature captures. UX needs to know what is mandatory and editable.</Helper>
      <RepeatableList
        items={draft.dataPrivacy}
        itemLabel="Data point"
        addLabel="Add data point"
        emptyHint="No data points added yet."
        onAdd={() =>
          update((d) =>
            d.dataPrivacy.push({
              id: uid('dp'),
              name: '',
              whyNeeded: '',
              mandatory: false,
              storedWhere: '',
              displayedWhere: '',
              canEdit: true,
              canDelete: true,
              privacyNotes: '',
            }),
          )
        }
        onRemove={(id) => update((d) => (d.dataPrivacy = d.dataPrivacy.filter((x) => x.id !== id)))}
        renderItem={(dp) => {
          const set = (field: keyof typeof dp) => (v: string) =>
            update((d) => ((d.dataPrivacy.find((x) => x.id === dp.id)![field] as string) = v))
          const setBool = (field: keyof typeof dp) => (v: boolean) =>
            update((d) => ((d.dataPrivacy.find((x) => x.id === dp.id)![field] as boolean) = v))
          return (
            <>
              <div className="field-row">
                <Field label="Data point name">
                  <Input value={dp.name} onChange={set('name')} />
                </Field>
                <Field label="Why it is needed">
                  <Input value={dp.whyNeeded} onChange={set('whyNeeded')} />
                </Field>
              </div>
              <div className="field-row">
                <Field label="Where is it stored?">
                  <Input value={dp.storedWhere} onChange={set('storedWhere')} />
                </Field>
                <Field label="Where is it displayed?">
                  <Input value={dp.displayedWhere} onChange={set('displayedWhere')} />
                </Field>
              </div>
              <div className="row wrap">
                <Checkbox checked={dp.mandatory} onChange={setBool('mandatory')} label="Mandatory" />
                <Checkbox checked={dp.canEdit} onChange={setBool('canEdit')} label="User can edit" />
                <Checkbox checked={dp.canDelete} onChange={setBool('canDelete')} label="User can delete" />
              </div>
              <Field label="Privacy / legal notes">
                <Input value={dp.privacyNotes} onChange={set('privacyNotes')} />
              </Field>
            </>
          )
        }}
      />
    </div>
  )
}

export function StepAnalytics({ draft, update }: StepProps) {
  const addEvent = (name = '') =>
    update((d) => d.analytics.events.push({ id: uid('evt'), name, trigger: '', properties: '', notes: '' }))
  return (
    <div>
      <h3 className="mb-8" style={{ fontSize: 15 }}>A. Product KPIs</h3>
      <RepeatableList
        items={draft.analytics.kpis}
        itemLabel="KPI"
        addLabel="Add KPI"
        emptyHint="No KPIs added yet."
        onAdd={() => update((d) => d.analytics.kpis.push({ id: uid('kpi'), goal: '', name: '', definition: '', successTarget: '', notes: '' }))}
        onRemove={(id) => update((d) => (d.analytics.kpis = d.analytics.kpis.filter((k) => k.id !== id)))}
        renderItem={(k) => {
          const set = (field: keyof typeof k) => (v: string) =>
            update((d) => ((d.analytics.kpis.find((x) => x.id === k.id)![field] as string) = v))
          return (
            <>
              <div className="field-row">
                <Field label="Goal">
                  <Input value={k.goal} onChange={set('goal')} />
                </Field>
                <Field label="KPI name">
                  <Input value={k.name} onChange={set('name')} />
                </Field>
              </div>
              <Field label="Definition">
                <Textarea value={k.definition} rows={2} onChange={set('definition')} />
              </Field>
              <div className="field-row">
                <Field label="Success target">
                  <Input value={k.successTarget} onChange={set('successTarget')} />
                </Field>
                <Field label="Notes">
                  <Input value={k.notes} onChange={set('notes')} />
                </Field>
              </div>
            </>
          )
        }}
      />

      <div className="divider" />
      <h3 className="mb-8" style={{ fontSize: 15 }}>B. Tracking Events</h3>
      <SuggestionChips options={EVENT_SUGGESTIONS} onPick={(e) => addEvent(e)} />
      <RepeatableList
        items={draft.analytics.events}
        itemLabel="Event"
        addLabel="Add event"
        emptyHint="No tracking events yet."
        onAdd={() => addEvent()}
        onRemove={(id) => update((d) => (d.analytics.events = d.analytics.events.filter((e) => e.id !== id)))}
        renderItem={(e) => {
          const set = (field: keyof typeof e) => (v: string) =>
            update((d) => ((d.analytics.events.find((x) => x.id === e.id)![field] as string) = v))
          return (
            <>
              <div className="field-row">
                <Field label="Event name">
                  <Input value={e.name} onChange={set('name')} />
                </Field>
                <Field label="Trigger">
                  <Input value={e.trigger} onChange={set('trigger')} />
                </Field>
              </div>
              <div className="field-row">
                <Field label="Properties">
                  <Input value={e.properties} onChange={set('properties')} />
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
