import { Field, Input, Textarea, Select, Checkbox, RepeatableList, SuggestionChips } from '../../components/forms'
import { SCENARIO_PRIORITIES, USER_STATES, SCENARIO_SUGGESTIONS } from '../../data/options'
import { uid } from '../../data/factory'
import type { ScenarioPriority, UserState } from '../../types'
import { Helper, type StepProps } from './shared'

export function StepPlatformsMarkets({ draft, update }: StepProps) {
  return (
    <div>
      <Helper>Select every platform in scope and flag which ones are part of the MVP.</Helper>

      <Field label="Platforms">
        <div className="stack">
          {draft.platforms.map((p) => (
            <div key={p.name} className="repeat-item" style={{ marginBottom: 0 }}>
              <Checkbox
                checked={p.selected}
                onChange={(v) => update((d) => (d.platforms.find((x) => x.name === p.name)!.selected = v))}
                label={<strong>{p.name}</strong>}
              />
              {p.selected && (
                <div style={{ marginTop: 8 }}>
                  <div className="field-row">
                    <Field label="Notes">
                      <Input value={p.notes} onChange={(v) => update((d) => (d.platforms.find((x) => x.name === p.name)!.notes = v))} />
                    </Field>
                    <Field label="Any different behavior?">
                      <Input value={p.differentBehavior} onChange={(v) => update((d) => (d.platforms.find((x) => x.name === p.name)!.differentBehavior = v))} />
                    </Field>
                  </div>
                  <Checkbox
                    checked={p.inMvp}
                    onChange={(v) => update((d) => (d.platforms.find((x) => x.name === p.name)!.inMvp = v))}
                    label="Included in MVP"
                  />
                </div>
              )}
            </div>
          ))}
        </div>
      </Field>

      <div className="divider" />

      <Field label="Markets / regions">
        <RepeatableList
          items={draft.markets}
          itemLabel="Market"
          addLabel="Add market"
          emptyHint="No markets added yet."
          onAdd={() => update((d) => d.markets.push({ id: uid('mkt'), name: '', inScope: true, notes: '' }))}
          onRemove={(id) => update((d) => (d.markets = d.markets.filter((m) => m.id !== id)))}
          renderItem={(m) => (
            <>
              <div className="field-row">
                <Field label="Market name">
                  <Input value={m.name} placeholder="e.g. Germany" onChange={(v) => update((d) => (d.markets.find((x) => x.id === m.id)!.name = v))} />
                </Field>
                <Field label="In scope?">
                  <Select
                    value={m.inScope ? 'Yes' : 'No'}
                    options={['Yes', 'No'] as const}
                    onChange={(v) => update((d) => (d.markets.find((x) => x.id === m.id)!.inScope = v === 'Yes'))}
                  />
                </Field>
              </div>
              <Field label="Notes">
                <Input value={m.notes} onChange={(v) => update((d) => (d.markets.find((x) => x.id === m.id)!.notes = v))} />
              </Field>
            </>
          )}
        />
      </Field>
    </div>
  )
}

export function StepScenarios({ draft, update }: StepProps) {
  const addScenario = (name = '') =>
    update((d) =>
      d.scenarios.push({
        id: uid('scn'),
        name,
        description: '',
        userState: 'New user',
        trigger: '',
        expectedBehavior: '',
        priority: 'Should',
      }),
    )
  return (
    <div>
      <Helper>Add the key scenarios UX should design for. Start from the suggestions below.</Helper>
      <SuggestionChips options={SCENARIO_SUGGESTIONS} onPick={(s) => addScenario(s)} />
      <RepeatableList
        items={draft.scenarios}
        itemLabel="Scenario"
        addLabel="Add scenario"
        emptyHint="No scenarios yet. Add at least one main scenario."
        onAdd={() => addScenario()}
        onRemove={(id) => update((d) => (d.scenarios = d.scenarios.filter((s) => s.id !== id)))}
        renderItem={(s) => (
          <>
            <div className="field-row">
              <Field label="Scenario name">
                <Input value={s.name} onChange={(v) => update((d) => (d.scenarios.find((x) => x.id === s.id)!.name = v))} />
              </Field>
              <Field label="Priority">
                <Select
                  value={s.priority}
                  options={SCENARIO_PRIORITIES}
                  onChange={(v: ScenarioPriority) => update((d) => (d.scenarios.find((x) => x.id === s.id)!.priority = v))}
                />
              </Field>
            </div>
            <Field label="Description">
              <Textarea value={s.description} rows={2} onChange={(v) => update((d) => (d.scenarios.find((x) => x.id === s.id)!.description = v))} />
            </Field>
            <div className="field-row-3">
              <Field label="User state">
                <Select
                  value={s.userState}
                  options={USER_STATES}
                  onChange={(v: UserState) => update((d) => (d.scenarios.find((x) => x.id === s.id)!.userState = v))}
                />
              </Field>
              <Field label="Trigger">
                <Input value={s.trigger} onChange={(v) => update((d) => (d.scenarios.find((x) => x.id === s.id)!.trigger = v))} />
              </Field>
              <Field label="Expected behavior">
                <Input value={s.expectedBehavior} onChange={(v) => update((d) => (d.scenarios.find((x) => x.id === s.id)!.expectedBehavior = v))} />
              </Field>
            </div>
          </>
        )}
      />
    </div>
  )
}

export function StepEntryPoints({ draft, update }: StepProps) {
  return (
    <div>
      <Helper>
        For each entry point think: when does the user first see this? How many times can it appear?
        When should it stop? What happens on dismiss? Does it differ across platforms?
      </Helper>
      <RepeatableList
        items={draft.entryPoints}
        itemLabel="Entry point"
        addLabel="Add entry point"
        emptyHint="No entry points defined yet."
        onAdd={() =>
          update((d) =>
            d.entryPoints.push({
              id: uid('ep'),
              name: '',
              platform: '',
              trigger: '',
              userState: 'New user',
              frequency: '',
              stopCondition: '',
              automaticOrManual: 'Automatic',
              blockingOrDismissible: 'Dismissible',
              notes: '',
            }),
          )
        }
        onRemove={(id) => update((d) => (d.entryPoints = d.entryPoints.filter((e) => e.id !== id)))}
        renderItem={(e) => (
          <>
            <div className="field-row">
              <Field label="Entry point name">
                <Input value={e.name} onChange={(v) => update((d) => (d.entryPoints.find((x) => x.id === e.id)!.name = v))} />
              </Field>
              <Field label="Platform">
                <Input value={e.platform} placeholder="e.g. Web, iOS, Android" onChange={(v) => update((d) => (d.entryPoints.find((x) => x.id === e.id)!.platform = v))} />
              </Field>
            </div>
            <div className="field-row-3">
              <Field label="Trigger">
                <Input value={e.trigger} onChange={(v) => update((d) => (d.entryPoints.find((x) => x.id === e.id)!.trigger = v))} />
              </Field>
              <Field label="User state">
                <Select
                  value={e.userState}
                  options={USER_STATES}
                  onChange={(v: UserState) => update((d) => (d.entryPoints.find((x) => x.id === e.id)!.userState = v))}
                />
              </Field>
              <Field label="Frequency">
                <Input value={e.frequency} placeholder="e.g. Once per user" onChange={(v) => update((d) => (d.entryPoints.find((x) => x.id === e.id)!.frequency = v))} />
              </Field>
            </div>
            <Field label="Stop condition">
              <Input value={e.stopCondition} onChange={(v) => update((d) => (d.entryPoints.find((x) => x.id === e.id)!.stopCondition = v))} />
            </Field>
            <div className="field-row">
              <Field label="Automatic or manual?">
                <Select
                  value={e.automaticOrManual}
                  options={['Automatic', 'Manual'] as const}
                  placeholder="Select…"
                  onChange={(v) => update((d) => (d.entryPoints.find((x) => x.id === e.id)!.automaticOrManual = v))}
                />
              </Field>
              <Field label="Blocking or dismissible?">
                <Select
                  value={e.blockingOrDismissible}
                  options={['Blocking', 'Dismissible'] as const}
                  placeholder="Select…"
                  onChange={(v) => update((d) => (d.entryPoints.find((x) => x.id === e.id)!.blockingOrDismissible = v))}
                />
              </Field>
            </div>
            <Field label="Notes">
              <Input value={e.notes} onChange={(v) => update((d) => (d.entryPoints.find((x) => x.id === e.id)!.notes = v))} />
            </Field>
          </>
        )}
      />
    </div>
  )
}

export function StepJourney({ draft, update }: StepProps) {
  const j = draft.journey
  const states: [keyof typeof j, string][] = [
    ['initialState', 'Initial state'],
    ['returningState', 'Returning / incomplete state'],
    ['completedState', 'Completed state'],
    ['editState', 'Edit / update state'],
    ['emptyState', 'Empty state'],
    ['loadingState', 'Loading state'],
    ['errorState', 'Error state'],
  ]
  return (
    <div>
      <Helper>Describe the key states of the experience, then break the flow into steps if needed.</Helper>
      {states.map(([key, label]) => (
        <Field key={key} label={label}>
          <Textarea
            value={j[key] as string}
            rows={2}
            onChange={(v) => update((d) => ((d.journey[key] as string) = v))}
          />
        </Field>
      ))}

      <div className="divider" />
      <Field label="Flow steps" hint="Add the individual steps if the feature is multi-step.">
        <RepeatableList
          items={draft.journey.steps}
          itemLabel="Step"
          addLabel="Add step"
          emptyHint="No steps added. Add steps for a multi-step flow."
          onAdd={() =>
            update((d) =>
              d.journey.steps.push({
                id: uid('step'),
                name: '',
                purpose: '',
                inputRequired: '',
                userActions: '',
                validation: '',
                skipBehavior: '',
                successBehavior: '',
                errorBehavior: '',
                uxNotes: '',
              }),
            )
          }
          onRemove={(id) => update((d) => (d.journey.steps = d.journey.steps.filter((s) => s.id !== id)))}
          renderItem={(s) => {
            const set = (field: keyof typeof s) => (v: string) =>
              update((d) => ((d.journey.steps.find((x) => x.id === s.id)![field] as string) = v))
            return (
              <>
                <div className="field-row">
                  <Field label="Step name">
                    <Input value={s.name} onChange={set('name')} />
                  </Field>
                  <Field label="Purpose">
                    <Input value={s.purpose} onChange={set('purpose')} />
                  </Field>
                </div>
                <div className="field-row">
                  <Field label="Input / data required">
                    <Input value={s.inputRequired} onChange={set('inputRequired')} />
                  </Field>
                  <Field label="User actions">
                    <Input value={s.userActions} onChange={set('userActions')} />
                  </Field>
                </div>
                <div className="field-row-3">
                  <Field label="Validation / restrictions">
                    <Input value={s.validation} onChange={set('validation')} />
                  </Field>
                  <Field label="Skip behavior">
                    <Input value={s.skipBehavior} onChange={set('skipBehavior')} />
                  </Field>
                  <Field label="Success behavior">
                    <Input value={s.successBehavior} onChange={set('successBehavior')} />
                  </Field>
                </div>
                <div className="field-row">
                  <Field label="Error behavior">
                    <Input value={s.errorBehavior} onChange={set('errorBehavior')} />
                  </Field>
                  <Field label="UX notes">
                    <Input value={s.uxNotes} onChange={set('uxNotes')} />
                  </Field>
                </div>
              </>
            )
          }}
        />
      </Field>
    </div>
  )
}
