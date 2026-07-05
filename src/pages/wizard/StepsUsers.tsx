import { Field, Input, Textarea, Select, Checkbox, RepeatableList } from '../../components/forms'
import { USER_PRIORITIES, USER_STATES } from '../../data/options'
import { uid } from '../../data/factory'
import type { UserPriority, UserState } from '../../types'
import { Helper, type StepProps } from './shared'

export function StepTargetUsers({ draft, update }: StepProps) {
  return (
    <div>
      <Helper>
        Add each distinct user group. UX designs differently for a new user vs. an existing user with
        partial data.
      </Helper>
      <RepeatableList
        items={draft.targetUsers}
        itemLabel="User group"
        addLabel="Add user group"
        emptyHint="No user groups yet. Add at least one primary group."
        onAdd={() =>
          update((d) =>
            d.targetUsers.push({
              id: uid('user'),
              name: '',
              description: '',
              priority: 'Primary',
              userState: 'New user',
              notes: '',
            }),
          )
        }
        onRemove={(id) => update((d) => (d.targetUsers = d.targetUsers.filter((u) => u.id !== id)))}
        renderItem={(u) => (
          <>
            <div className="field-row">
              <Field label="User group name">
                <Input
                  value={u.name}
                  placeholder="e.g. New users after signup"
                  onChange={(v) => update((d) => (d.targetUsers.find((x) => x.id === u.id)!.name = v))}
                />
              </Field>
              <Field label="Priority">
                <Select
                  value={u.priority}
                  options={USER_PRIORITIES}
                  onChange={(v: UserPriority) => update((d) => (d.targetUsers.find((x) => x.id === u.id)!.priority = v))}
                />
              </Field>
            </div>
            <Field label="Description">
              <Textarea
                value={u.description}
                rows={2}
                onChange={(v) => update((d) => (d.targetUsers.find((x) => x.id === u.id)!.description = v))}
              />
            </Field>
            <div className="field-row">
              <Field label="User state">
                <Select
                  value={u.userState}
                  options={USER_STATES}
                  onChange={(v: UserState) => update((d) => (d.targetUsers.find((x) => x.id === u.id)!.userState = v))}
                />
              </Field>
              <Field label="Notes">
                <Input value={u.notes} onChange={(v) => update((d) => (d.targetUsers.find((x) => x.id === u.id)!.notes = v))} />
              </Field>
            </div>
          </>
        )}
      />
    </div>
  )
}

export function StepUserNeed({ draft, update }: StepProps) {
  const n = draft.userNeed
  return (
    <div>
      <Helper>
        Use the template: <em>"As a [type of user], I need to [goal/action], so that I can [benefit]."</em>
      </Helper>
      <Field label="User need statement">
        <Textarea value={n.needStatement} onChange={(v) => update((d) => (d.userNeed.needStatement = v))} />
      </Field>
      <Field label="User story" hint="As a [type of user], I need to [goal/action], so that I can [benefit].">
        <Textarea
          value={n.userStory}
          placeholder="As a new user, I need to set up my social profile, so that my feed feels personal."
          onChange={(v) => update((d) => (d.userNeed.userStory = v))}
        />
      </Field>
      <Field label="What should the user understand?">
        <Textarea value={n.shouldUnderstand} rows={2} onChange={(v) => update((d) => (d.userNeed.shouldUnderstand = v))} />
      </Field>
      <Field label="What should the user be able to do?">
        <Textarea value={n.shouldBeAbleToDo} rows={2} onChange={(v) => update((d) => (d.userNeed.shouldBeAbleToDo = v))} />
      </Field>
      <Field label="What should the user feel or avoid feeling?">
        <Textarea value={n.shouldFeel} rows={2} onChange={(v) => update((d) => (d.userNeed.shouldFeel = v))} />
      </Field>
    </div>
  )
}

export function StepProposedSolution({ draft, update }: StepProps) {
  const s = draft.proposedSolution
  return (
    <div>
      <Field label="High-level solution description" required>
        <Textarea value={s.description} onChange={(v) => update((d) => (d.proposedSolution.description = v))} />
      </Field>
      <Field label="Main user actions">
        <Textarea value={s.mainActions} rows={2} onChange={(v) => update((d) => (d.proposedSolution.mainActions = v))} />
      </Field>
      <Field label="Expected outcome">
        <Textarea value={s.expectedOutcome} rows={2} onChange={(v) => update((d) => (d.proposedSolution.expectedOutcome = v))} />
      </Field>
      <div className="field-row">
        <Field label="New feature or extension?">
          <Select
            value={s.newOrExtension}
            options={['New feature', 'Extension'] as const}
            placeholder="Select…"
            onChange={(v) => update((d) => (d.proposedSolution.newOrExtension = v))}
          />
        </Field>
        <Field label="Mandatory or optional flow?">
          <Select
            value={s.mandatoryOrOptional}
            options={['Mandatory', 'Optional'] as const}
            placeholder="Select…"
            onChange={(v) => update((d) => (d.proposedSolution.mandatoryOrOptional = v))}
          />
        </Field>
      </div>
      <Field label="Flow flexibility">
        <Checkbox checked={s.canSkip} onChange={(v) => update((d) => (d.proposedSolution.canSkip = v))} label="User can skip it" />
        <Checkbox checked={s.canReturnLater} onChange={(v) => update((d) => (d.proposedSolution.canReturnLater = v))} label="User can return to it later" />
        <Checkbox checked={s.canEditLater} onChange={(v) => update((d) => (d.proposedSolution.canEditLater = v))} label="User can edit / update their choices later" />
      </Field>
    </div>
  )
}
