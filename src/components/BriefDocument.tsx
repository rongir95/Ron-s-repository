import type { FeatureBrief } from '../types'
import { Collapsible } from './ui'
import { StatusChip, PriorityChip, MoscowChip, GenericChip } from './chips'
import type { ReactNode } from 'react'

// A read-only definition list row. Empty values render as a muted placeholder.
function Row({ label, value }: { label: string; value?: string | ReactNode }) {
  const empty = value === undefined || value === null || value === ''
  return (
    <div className="dl-row">
      <dt>{label}</dt>
      <dd className={empty ? 'empty-val' : ''}>{empty ? 'Not provided' : value}</dd>
    </div>
  )
}

function DL({ children }: { children: ReactNode }) {
  return <dl className="dl">{children}</dl>
}

function Count({ n }: { n: number }) {
  return <GenericChip label={String(n)} tone={n > 0 ? 'brand' : 'gray'} />
}

export function BriefDocument({ brief: b }: { brief: FeatureBrief }) {
  const selectedPlatforms = b.platforms.filter((p) => p.selected)
  const blocking = b.openQuestions.filter((q) => q.blockingUx)
  const nonBlocking = b.openQuestions.filter((q) => !q.blockingUx)

  return (
    <div className="brief-doc">
      <Collapsible title="Overview" defaultOpen>
        <DL>
          <Row label="Feature name" value={b.featureName} />
          <Row label="Summary" value={b.shortSummary} />
          <Row label="Status" value={<StatusChip status={b.status} />} />
          <Row label="Priority" value={<PriorityChip priority={b.priority} />} />
          <Row label="Document status" value={b.overview.documentStatus} />
          <Row label="Target release" value={b.overview.targetRelease} />
          <Row label="Related initiative" value={b.overview.relatedInitiative} />
          <Row label="Product owner" value={b.owners.productOwner} />
          <Row label="Designer" value={b.owners.designer} />
          <Row label="Tech lead" value={b.owners.techLead} />
          <Row label="Data owner" value={b.owners.dataOwner} />
          <Row label="QA owner" value={b.owners.qaOwner} />
        </DL>
      </Collapsible>

      <Collapsible title="Context">
        <DL>
          <Row label="What exists today" value={b.background.whatExistsToday} />
          <Row label="What is missing" value={b.background.whatIsMissing} />
          <Row label="Why now" value={b.background.whyNow} />
          <Row label="Related areas" value={b.background.relatedAreas} />
          <Row label="Market context" value={b.background.marketContext} />
        </DL>
      </Collapsible>

      <Collapsible title="Problem">
        <DL>
          <Row label="Business problem" value={b.problem.businessProblem} />
          <Row label="User problem" value={b.problem.userProblem} />
          <Row label="Evidence" value={b.problem.evidence} />
          <Row label="If we do nothing" value={b.problem.doNothing} />
        </DL>
      </Collapsible>

      <Collapsible title="Objective">
        <DL>
          <Row label="Primary objective" value={b.objectives.primaryObjective} />
          <Row label="Secondary objectives" value={b.objectives.secondaryObjectives} />
          <Row label="Business value" value={b.objectives.businessValue} />
          <Row label="Expected impact" value={b.objectives.expectedImpact} />
          <Row label="Strategic relevance" value={b.objectives.strategicRelevance} />
          <Row
            label="Goals"
            value={
              b.objectives.goals.length ? (
                <div className="row wrap">{b.objectives.goals.map((g) => <GenericChip key={g} label={g} />)}</div>
              ) : (
                ''
              )
            }
          />
        </DL>
      </Collapsible>

      <Collapsible title="Target users" right={<Count n={b.targetUsers.length} />}>
        {b.targetUsers.length === 0 ? (
          <p className="muted">No target users defined.</p>
        ) : (
          b.targetUsers.map((u) => (
            <div key={u.id} className="repeat-item" style={{ background: 'var(--surface)' }}>
              <div className="row" style={{ marginBottom: 6 }}>
                <strong>{u.name || 'Unnamed group'}</strong>
                <GenericChip label={u.priority} tone={u.priority === 'Primary' ? 'brand' : 'gray'} />
                <GenericChip label={u.userState} />
              </div>
              <div className="text-sm">{u.description}</div>
              {u.notes && <div className="muted text-sm" style={{ marginTop: 4 }}>Notes: {u.notes}</div>}
            </div>
          ))
        )}
      </Collapsible>

      <Collapsible title="Proposed solution">
        <DL>
          <Row label="Description" value={b.proposedSolution.description} />
          <Row label="Main actions" value={b.proposedSolution.mainActions} />
          <Row label="Expected outcome" value={b.proposedSolution.expectedOutcome} />
          <Row label="New or extension" value={b.proposedSolution.newOrExtension} />
          <Row label="Mandatory or optional" value={b.proposedSolution.mandatoryOrOptional} />
          <Row label="Can skip" value={b.proposedSolution.canSkip ? 'Yes' : 'No'} />
          <Row label="Can return later" value={b.proposedSolution.canReturnLater ? 'Yes' : 'No'} />
          <Row label="Can edit later" value={b.proposedSolution.canEditLater ? 'Yes' : 'No'} />
        </DL>
        <h4 style={{ margin: '16px 0 8px', fontSize: 13 }}>User need</h4>
        <DL>
          <Row label="Need statement" value={b.userNeed.needStatement} />
          <Row label="User story" value={b.userNeed.userStory} />
          <Row label="Should understand" value={b.userNeed.shouldUnderstand} />
          <Row label="Should be able to do" value={b.userNeed.shouldBeAbleToDo} />
          <Row label="Should feel" value={b.userNeed.shouldFeel} />
        </DL>
      </Collapsible>

      <Collapsible title="Platforms & markets" right={<Count n={selectedPlatforms.length} />}>
        {selectedPlatforms.length === 0 ? (
          <p className="muted">No platforms selected.</p>
        ) : (
          <div className="stack">
            {selectedPlatforms.map((p) => (
              <div key={p.name} className="row wrap">
                <strong style={{ minWidth: 90 }}>{p.name}</strong>
                {p.inMvp && <GenericChip label="MVP" tone="green" />}
                <span className="text-sm muted">{p.differentBehavior || p.notes || 'Standard behavior'}</span>
              </div>
            ))}
          </div>
        )}
        {b.markets.length > 0 && (
          <>
            <h4 style={{ margin: '16px 0 8px', fontSize: 13 }}>Markets</h4>
            <div className="row wrap">
              {b.markets.map((m) => (
                <GenericChip key={m.id} label={`${m.name}${m.inScope ? '' : ' (out)'}`} tone={m.inScope ? 'green' : 'gray'} />
              ))}
            </div>
          </>
        )}
      </Collapsible>

      <Collapsible title="Scenarios" right={<Count n={b.scenarios.length} />}>
        {b.scenarios.length === 0 ? (
          <p className="muted">No scenarios defined.</p>
        ) : (
          b.scenarios.map((s) => (
            <div key={s.id} className="repeat-item" style={{ background: 'var(--surface)' }}>
              <div className="row" style={{ marginBottom: 4 }}>
                <strong>{s.name}</strong>
                <MoscowChip priority={s.priority} />
              </div>
              <div className="text-sm">{s.description}</div>
              <div className="muted text-sm" style={{ marginTop: 4 }}>
                {s.trigger && `Trigger: ${s.trigger}. `}
                {s.expectedBehavior && `Expected: ${s.expectedBehavior}`}
              </div>
            </div>
          ))
        )}
      </Collapsible>

      <Collapsible title="Entry points" right={<Count n={b.entryPoints.length} />}>
        {b.entryPoints.length === 0 ? (
          <p className="muted">No entry points defined.</p>
        ) : (
          b.entryPoints.map((e) => (
            <div key={e.id} className="repeat-item" style={{ background: 'var(--surface)' }}>
              <div className="row" style={{ marginBottom: 4 }}>
                <strong>{e.name}</strong>
                <GenericChip label={e.platform} />
                <GenericChip label={e.blockingOrDismissible} tone={e.blockingOrDismissible === 'Blocking' ? 'orange' : 'gray'} />
              </div>
              <div className="muted text-sm">
                {e.trigger && `Trigger: ${e.trigger}. `}
                {e.frequency && `Frequency: ${e.frequency}. `}
                {e.stopCondition && `Stops: ${e.stopCondition}.`}
              </div>
            </div>
          ))
        )}
      </Collapsible>

      <Collapsible title="Journey structure">
        <DL>
          <Row label="Initial state" value={b.journey.initialState} />
          <Row label="Returning state" value={b.journey.returningState} />
          <Row label="Completed state" value={b.journey.completedState} />
          <Row label="Edit state" value={b.journey.editState} />
          <Row label="Empty state" value={b.journey.emptyState} />
          <Row label="Loading state" value={b.journey.loadingState} />
          <Row label="Error state" value={b.journey.errorState} />
        </DL>
        {b.journey.steps.length > 0 && (
          <>
            <h4 style={{ margin: '16px 0 8px', fontSize: 13 }}>Steps</h4>
            <ol style={{ margin: 0, paddingLeft: 18 }}>
              {b.journey.steps.map((s) => (
                <li key={s.id} style={{ marginBottom: 6 }}>
                  <strong>{s.name}</strong> — {s.purpose}
                </li>
              ))}
            </ol>
          </>
        )}
      </Collapsible>

      <Collapsible title="Requirements" right={<Count n={b.requirements.length} />}>
        {b.requirements.length === 0 ? (
          <p className="muted">No requirements defined.</p>
        ) : (
          <div className="table-wrap">
            <table className="data">
              <thead>
                <tr>
                  <th>Requirement</th>
                  <th>Priority</th>
                  <th>Platform</th>
                  <th>Owner</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                {b.requirements.map((r) => (
                  <tr key={r.id}>
                    <td>
                      <strong>{r.title}</strong>
                      {r.description && <div className="muted text-sm">{r.description}</div>}
                    </td>
                    <td><MoscowChip priority={r.priority} /></td>
                    <td>{r.platform}</td>
                    <td>{r.owner || '—'}</td>
                    <td>{r.status}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </Collapsible>

      <Collapsible title="UX goals">
        <DL>
          <Row label="Should feel" value={b.uxGoals.shouldFeel} />
          <Row label="Should avoid" value={b.uxGoals.shouldAvoid} />
          <Row label="Design principles" value={b.uxGoals.designPrinciples} />
          <Row
            label="Selected principles"
            value={
              b.uxGoals.selectedPrinciples.length ? (
                <div className="row wrap">{b.uxGoals.selectedPrinciples.map((p) => <GenericChip key={p} label={p} />)}</div>
              ) : (
                ''
              )
            }
          />
        </DL>
      </Collapsible>

      <Collapsible title="Copy">
        <DL>
          <Row label="Tone of voice" value={b.copyRequirements.toneOfVoice} />
          <Row label="Mandatory messages" value={b.copyRequirements.mandatoryMessages} />
          <Row label="Words to avoid" value={b.copyRequirements.wordsToAvoid} />
          <Row label="Localisation" value={b.copyRequirements.localisation} />
          <Row label="Legal copy required" value={b.copyRequirements.legalCopyRequired ? 'Yes' : 'No'} />
          <Row label="Error guidance" value={b.copyRequirements.errorGuidance} />
          <Row label="Confirmation guidance" value={b.copyRequirements.confirmationGuidance} />
          <Row label="Copy doc" value={b.copyRequirements.copyDocLink ? <a href={b.copyRequirements.copyDocLink} target="_blank" rel="noreferrer">{b.copyRequirements.copyDocLink}</a> : ''} />
        </DL>
      </Collapsible>

      <Collapsible title="Data / privacy" right={<Count n={b.dataPrivacy.length} />}>
        {b.dataPrivacy.length === 0 ? (
          <p className="muted">No data points defined.</p>
        ) : (
          b.dataPrivacy.map((d) => (
            <div key={d.id} className="repeat-item" style={{ background: 'var(--surface)' }}>
              <div className="row" style={{ marginBottom: 4 }}>
                <strong>{d.name}</strong>
                <GenericChip label={d.mandatory ? 'Mandatory' : 'Optional'} tone={d.mandatory ? 'orange' : 'gray'} />
              </div>
              <div className="muted text-sm">
                {d.whyNeeded}
                {d.storedWhere && ` · Stored: ${d.storedWhere}`}
              </div>
            </div>
          ))
        )}
      </Collapsible>

      <Collapsible title="Analytics" right={<Count n={b.analytics.kpis.length + b.analytics.events.length} />}>
        {b.analytics.kpis.length > 0 && (
          <>
            <h4 style={{ margin: '0 0 8px', fontSize: 13 }}>KPIs</h4>
            {b.analytics.kpis.map((k) => (
              <div key={k.id} className="text-sm" style={{ marginBottom: 6 }}>
                <strong>{k.name}</strong> — {k.definition} <span className="muted">(target: {k.successTarget})</span>
              </div>
            ))}
          </>
        )}
        {b.analytics.events.length > 0 && (
          <>
            <h4 style={{ margin: '14px 0 8px', fontSize: 13 }}>Tracking events</h4>
            <div className="row wrap">
              {b.analytics.events.map((e) => (
                <GenericChip key={e.id} label={e.name} tone="purple" />
              ))}
            </div>
          </>
        )}
        {b.analytics.kpis.length === 0 && b.analytics.events.length === 0 && <p className="muted">No metrics defined.</p>}
      </Collapsible>

      <Collapsible title="Dependencies" right={<Count n={b.dependencies.length} />}>
        {b.dependencies.length === 0 ? (
          <p className="muted">No dependencies identified.</p>
        ) : (
          b.dependencies.map((d) => (
            <div key={d.id} className="row wrap" style={{ marginBottom: 8 }}>
              <strong>{d.name}</strong>
              <GenericChip label={d.type} />
              <GenericChip label={d.status} tone={d.status === 'Ready' ? 'green' : d.status === 'Blocked' ? 'red' : 'orange'} />
              {d.blockingUx && <GenericChip label="Blocking UX" tone="red" />}
            </div>
          ))
        )}
      </Collapsible>

      <Collapsible title="Risks" right={<Count n={b.risks.length} />}>
        {b.risks.length === 0 ? (
          <p className="muted">No risks captured.</p>
        ) : (
          b.risks.map((r) => (
            <div key={r.id} className="repeat-item" style={{ background: 'var(--surface)' }}>
              <div className="row" style={{ marginBottom: 4 }}>
                <strong>{r.risk}</strong>
                <GenericChip label={r.severity} tone={r.severity === 'High' ? 'red' : r.severity === 'Medium' ? 'orange' : 'gray'} />
              </div>
              <div className="muted text-sm">Impact: {r.impact}. Mitigation: {r.mitigation}</div>
            </div>
          ))
        )}
      </Collapsible>

      <Collapsible title="Edge cases" right={<Count n={b.edgeCases.length} />}>
        {b.edgeCases.length === 0 ? (
          <p className="muted">No edge cases added.</p>
        ) : (
          b.edgeCases.map((e) => (
            <div key={e.id} className="text-sm" style={{ marginBottom: 8 }}>
              <strong>{e.edgeCase}</strong> <MoscowChip priority={e.priority} />
              <div className="muted">{e.expectedBehavior}</div>
            </div>
          ))
        )}
      </Collapsible>

      <Collapsible title="Out of scope" right={<Count n={b.outOfScope.length} />}>
        {b.outOfScope.length === 0 ? (
          <p className="muted">Nothing marked out of scope.</p>
        ) : (
          <ul style={{ margin: 0, paddingLeft: 18 }}>
            {b.outOfScope.map((o) => (
              <li key={o.id} style={{ marginBottom: 4 }}>
                {o.item} {o.reason && <span className="muted">— {o.reason}</span>}
                {o.futureConsideration && <GenericChip label="Future" tone="blue" />}
              </li>
            ))}
          </ul>
        )}
      </Collapsible>

      <Collapsible title="Open questions" right={<Count n={b.openQuestions.length} />}>
        <div className="callout red mb-16">
          <strong>Blocking UX ({blocking.length})</strong>
          {blocking.length > 0 ? (
            <ul style={{ margin: '8px 0 0', paddingLeft: 18 }}>
              {blocking.map((q) => (
                <li key={q.id}>
                  {q.question} <GenericChip label={q.status} tone={q.status === 'Answered' ? 'green' : 'orange'} />
                </li>
              ))}
            </ul>
          ) : (
            <div className="text-sm" style={{ marginTop: 6 }}>None — nothing is blocking design.</div>
          )}
        </div>
        <div className="callout blue">
          <strong>Not blocking UX ({nonBlocking.length})</strong>
          {nonBlocking.length > 0 && (
            <ul style={{ margin: '8px 0 0', paddingLeft: 18 }}>
              {nonBlocking.map((q) => (
                <li key={q.id}>
                  {q.question} <GenericChip label={q.status} tone={q.status === 'Answered' ? 'green' : 'gray'} />
                </li>
              ))}
            </ul>
          )}
        </div>
      </Collapsible>

      <Collapsible title="Decisions" right={<Count n={b.decisionLog.length} />}>
        {b.decisionLog.length === 0 ? (
          <p className="muted">No decisions logged.</p>
        ) : (
          b.decisionLog.map((d) => (
            <div key={d.id} className="text-sm" style={{ marginBottom: 8 }}>
              <strong>{d.date || '—'}:</strong> {d.decision}
              <div className="muted">Impact on UX: {d.impactOnUx || '—'}</div>
            </div>
          ))
        )}
      </Collapsible>

      <Collapsible title="References" right={<Count n={b.references.length} />}>
        {b.references.length === 0 ? (
          <p className="muted">No references linked.</p>
        ) : (
          <ul style={{ margin: 0, paddingLeft: 18 }}>
            {b.references.map((r) => (
              <li key={r.id} style={{ marginBottom: 4 }}>
                <GenericChip label={r.type} />{' '}
                <a href={r.url} target="_blank" rel="noreferrer">
                  {r.label || r.url}
                </a>
              </li>
            ))}
          </ul>
        )}
      </Collapsible>
    </div>
  )
}
