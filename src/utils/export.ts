import type { FeatureBrief } from '../types'
import { computeReadiness } from './readiness'

// Build a clean, human-readable Markdown version of a brief. This is what the
// UX team copies out or prints.
export function briefToMarkdown(b: FeatureBrief): string {
  const readiness = computeReadiness(b)
  const lines: string[] = []
  const h = (t: string) => lines.push(`\n## ${t}\n`)
  const kv = (k: string, v: string) => v && v.trim() && lines.push(`- **${k}:** ${v}`)
  const p = (t: string) => t && t.trim() && lines.push(t)

  lines.push(`# ${b.featureName || 'Untitled feature'}`)
  lines.push(`\n> ${b.shortSummary || '_No summary provided._'}`)
  lines.push('')
  kv('Status', b.status)
  kv('Priority', b.priority)
  kv('Readiness', `${readiness.score}% — ${readiness.status}`)
  kv('Product owner', b.owners.productOwner)
  kv('Designer', b.owners.designer)
  kv('Tech lead', b.owners.techLead)
  kv('Target release', b.overview.targetRelease)
  kv('Related initiative', b.overview.relatedInitiative)

  h('Background & Context')
  kv('What exists today', b.background.whatExistsToday)
  kv('What is missing', b.background.whatIsMissing)
  kv('Why now', b.background.whyNow)
  kv('Related areas', b.background.relatedAreas)
  kv('Market context', b.background.marketContext)

  h('Problem Statement')
  kv('Business problem', b.problem.businessProblem)
  kv('User problem', b.problem.userProblem)
  kv('Evidence', b.problem.evidence)
  kv('If we do nothing', b.problem.doNothing)

  h('Objective & Business Value')
  kv('Primary objective', b.objectives.primaryObjective)
  kv('Secondary objectives', b.objectives.secondaryObjectives)
  kv('Business value', b.objectives.businessValue)
  kv('Expected impact', b.objectives.expectedImpact)
  kv('Strategic relevance', b.objectives.strategicRelevance)
  if (b.objectives.goals.length) kv('Goals', b.objectives.goals.join(', '))

  h('Target Users')
  b.targetUsers.forEach((u) => {
    lines.push(`- **${u.name}** (${u.priority}, ${u.userState})`)
    if (u.description) lines.push(`  - ${u.description}`)
    if (u.notes) lines.push(`  - _Notes: ${u.notes}_`)
  })

  h('User Need')
  kv('Need statement', b.userNeed.needStatement)
  kv('User story', b.userNeed.userStory)
  kv('Should understand', b.userNeed.shouldUnderstand)
  kv('Should be able to do', b.userNeed.shouldBeAbleToDo)
  kv('Should feel', b.userNeed.shouldFeel)

  h('Proposed Solution')
  p(b.proposedSolution.description)
  kv('Main actions', b.proposedSolution.mainActions)
  kv('Expected outcome', b.proposedSolution.expectedOutcome)
  kv('New or extension', b.proposedSolution.newOrExtension)
  kv('Mandatory or optional', b.proposedSolution.mandatoryOrOptional)
  kv('Can skip', b.proposedSolution.canSkip ? 'Yes' : 'No')
  kv('Can return later', b.proposedSolution.canReturnLater ? 'Yes' : 'No')
  kv('Can edit later', b.proposedSolution.canEditLater ? 'Yes' : 'No')

  h('Platforms & Markets')
  const selectedPlatforms = b.platforms.filter((pl) => pl.selected)
  selectedPlatforms.forEach((pl) => {
    lines.push(`- **${pl.name}**${pl.inMvp ? ' (MVP)' : ''}`)
    if (pl.notes) lines.push(`  - ${pl.notes}`)
    if (pl.differentBehavior) lines.push(`  - Different behavior: ${pl.differentBehavior}`)
  })
  if (b.markets.length) {
    lines.push('\n**Markets**')
    b.markets.forEach((m) =>
      lines.push(`- ${m.name} — ${m.inScope ? 'In scope' : 'Out of scope'}${m.notes ? ` (${m.notes})` : ''}`),
    )
  }

  h('Main Scenarios')
  b.scenarios.forEach((s) => {
    lines.push(`- **${s.name}** [${s.priority}]`)
    if (s.description) lines.push(`  - ${s.description}`)
    if (s.trigger) lines.push(`  - Trigger: ${s.trigger}`)
    if (s.expectedBehavior) lines.push(`  - Expected: ${s.expectedBehavior}`)
  })

  h('Entry Points')
  b.entryPoints.forEach((e) => {
    lines.push(`- **${e.name}** (${e.platform})`)
    if (e.trigger) lines.push(`  - Trigger: ${e.trigger}`)
    if (e.frequency) lines.push(`  - Frequency: ${e.frequency}`)
    if (e.stopCondition) lines.push(`  - Stops when: ${e.stopCondition}`)
  })

  h('Journey Structure')
  kv('Initial state', b.journey.initialState)
  kv('Returning / incomplete', b.journey.returningState)
  kv('Completed state', b.journey.completedState)
  kv('Edit / update state', b.journey.editState)
  kv('Empty state', b.journey.emptyState)
  kv('Loading state', b.journey.loadingState)
  kv('Error state', b.journey.errorState)
  if (b.journey.steps.length) {
    lines.push('\n**Steps**')
    b.journey.steps.forEach((st, i) => {
      lines.push(`${i + 1}. **${st.name}** — ${st.purpose}`)
    })
  }

  h('Core Requirements')
  if (b.requirements.length) {
    lines.push('| Requirement | Priority | Platform | Owner | Status |')
    lines.push('| --- | --- | --- | --- | --- |')
    b.requirements.forEach((r) =>
      lines.push(`| ${r.title} | ${r.priority} | ${r.platform} | ${r.owner} | ${r.status} |`),
    )
  }

  h('UX Goals / Experience Principles')
  kv('Should feel', b.uxGoals.shouldFeel)
  kv('Should avoid', b.uxGoals.shouldAvoid)
  kv('Design principles', b.uxGoals.designPrinciples)
  if (b.uxGoals.selectedPrinciples.length)
    kv('Selected principles', b.uxGoals.selectedPrinciples.join(', '))

  h('Content & Copy')
  kv('Tone of voice', b.copyRequirements.toneOfVoice)
  kv('Mandatory messages', b.copyRequirements.mandatoryMessages)
  kv('Words to avoid', b.copyRequirements.wordsToAvoid)
  kv('Localisation', b.copyRequirements.localisation)
  kv('Legal copy required', b.copyRequirements.legalCopyRequired ? 'Yes' : 'No')

  h('Data, Privacy & Permissions')
  b.dataPrivacy.forEach((d) => {
    lines.push(`- **${d.name}** (${d.mandatory ? 'Mandatory' : 'Optional'})`)
    if (d.whyNeeded) lines.push(`  - Why: ${d.whyNeeded}`)
  })

  h('Analytics & Success Metrics')
  if (b.analytics.kpis.length) {
    lines.push('**KPIs**')
    b.analytics.kpis.forEach((k) => lines.push(`- ${k.name}: ${k.definition} (target: ${k.successTarget})`))
  }
  if (b.analytics.events.length) {
    lines.push('\n**Tracking events**')
    b.analytics.events.forEach((e) => lines.push(`- \`${e.name}\` — ${e.trigger}`))
  }

  h('Dependencies')
  b.dependencies.forEach((d) =>
    lines.push(`- **${d.name}** (${d.type}, ${d.status})${d.blockingUx ? ' — ⚠️ Blocking UX' : ''}`),
  )

  h('Risks & Constraints')
  b.risks.forEach((r) => lines.push(`- **${r.risk}** [${r.severity}] — ${r.mitigation}`))

  h('Edge Cases')
  b.edgeCases.forEach((e) => lines.push(`- **${e.edgeCase}** — ${e.expectedBehavior}`))

  h('Out of Scope')
  b.outOfScope.forEach((o) =>
    lines.push(`- ${o.item}${o.reason ? ` — ${o.reason}` : ''}${o.futureConsideration ? ' (future)' : ''}`),
  )

  h('Open Questions')
  const blocking = b.openQuestions.filter((q) => q.blockingUx)
  const nonBlocking = b.openQuestions.filter((q) => !q.blockingUx)
  if (blocking.length) {
    lines.push('**Blocking UX**')
    blocking.forEach((q) => lines.push(`- ${q.question} (${q.status})`))
  }
  if (nonBlocking.length) {
    lines.push('\n**Not blocking UX**')
    nonBlocking.forEach((q) => lines.push(`- ${q.question} (${q.status})`))
  }

  h('Decision Log')
  b.decisionLog.forEach((d) => lines.push(`- ${d.date}: ${d.decision} (${d.owner})`))

  h('References')
  b.references.forEach((r) => lines.push(`- [${r.label || r.type}](${r.url})`))

  return lines.join('\n')
}

export function briefToJson(b: FeatureBrief): string {
  return JSON.stringify(b, null, 2)
}

export function downloadFile(filename: string, content: string, type = 'application/json') {
  const blob = new Blob([content], { type })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = filename
  a.click()
  URL.revokeObjectURL(url)
}

export async function copyToClipboard(text: string): Promise<boolean> {
  try {
    await navigator.clipboard.writeText(text)
    return true
  } catch {
    return false
  }
}
