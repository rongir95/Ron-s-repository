import type { FeatureBrief, ReadinessStatus } from '../types'

// A single readiness criterion: a human label + a predicate over the brief.
interface Criterion {
  key: string
  label: string
  missingLabel: string
  met: (b: FeatureBrief) => boolean
}

const hasText = (s: string | undefined) => Boolean(s && s.trim().length > 0)

// The criteria that drive the automatic readiness score. Each is weighted
// equally; the score is the percentage met.
export const READINESS_CRITERIA: Criterion[] = [
  {
    key: 'overview',
    label: 'Feature overview completed',
    missingLabel: 'Feature name or summary is missing',
    met: (b) => hasText(b.featureName) && hasText(b.shortSummary),
  },
  {
    key: 'userProblem',
    label: 'User problem defined',
    missingLabel: 'User problem is missing',
    met: (b) => hasText(b.problem.userProblem),
  },
  {
    key: 'businessProblem',
    label: 'Business problem defined',
    missingLabel: 'Business / product problem is missing',
    met: (b) => hasText(b.problem.businessProblem),
  },
  {
    key: 'objective',
    label: 'Primary objective defined',
    missingLabel: 'Primary objective is missing',
    met: (b) => hasText(b.objectives.primaryObjective),
  },
  {
    key: 'targetUsers',
    label: 'Target users defined',
    missingLabel: 'Target users are not defined',
    met: (b) => b.targetUsers.length > 0,
  },
  {
    key: 'platforms',
    label: 'Platforms defined',
    missingLabel: 'No platforms selected',
    met: (b) => b.platforms.some((p) => p.selected),
  },
  {
    key: 'solution',
    label: 'Proposed solution described',
    missingLabel: 'Proposed solution is missing',
    met: (b) => hasText(b.proposedSolution.description),
  },
  {
    key: 'scenarios',
    label: 'Main scenarios defined',
    missingLabel: 'No main scenarios added',
    met: (b) => b.scenarios.length > 0,
  },
  {
    key: 'entryPoints',
    label: 'Entry points defined',
    missingLabel: 'No entry points added',
    met: (b) => b.entryPoints.length > 0,
  },
  {
    key: 'requirements',
    label: 'Core requirements defined',
    missingLabel: 'No core requirements added',
    met: (b) => b.requirements.length > 0,
  },
  {
    key: 'outOfScope',
    label: 'Out of scope defined',
    missingLabel: 'Out of scope is still empty',
    met: (b) => b.outOfScope.length > 0,
  },
  {
    key: 'dependencies',
    label: 'Dependencies identified',
    missingLabel: 'No dependencies identified',
    met: (b) => b.dependencies.length > 0,
  },
  {
    key: 'metrics',
    label: 'Success metrics defined',
    missingLabel: 'No success metrics added',
    met: (b) => b.analytics.kpis.length > 0,
  },
  {
    key: 'edgeCases',
    label: 'Edge cases considered',
    missingLabel: 'No edge cases added',
    met: (b) => b.edgeCases.length > 0,
  },
  {
    key: 'blockingQuestions',
    label: 'No unresolved blocking questions',
    missingLabel: '', // handled dynamically below
    met: (b) =>
      b.openQuestions.filter((q) => q.blockingUx && q.status !== 'Answered').length === 0,
  },
]

export interface ReadinessResult {
  score: number
  status: ReadinessStatus
  metKeys: string[]
  missing: string[]
}

export function computeReadiness(brief: FeatureBrief): ReadinessResult {
  const total = READINESS_CRITERIA.length
  const metKeys: string[] = []
  const missing: string[] = []

  for (const c of READINESS_CRITERIA) {
    if (c.met(brief)) {
      metKeys.push(c.key)
    } else if (c.key === 'blockingQuestions') {
      const n = brief.openQuestions.filter(
        (q) => q.blockingUx && q.status !== 'Answered',
      ).length
      missing.push(`There ${n === 1 ? 'is' : 'are'} ${n} blocking UX question${n === 1 ? '' : 's'}`)
    } else if (c.missingLabel) {
      missing.push(c.missingLabel)
    }
  }

  const score = Math.round((metKeys.length / total) * 100)
  let status: ReadinessStatus = 'Not ready'
  if (score >= 80) status = 'Ready for UX'
  else if (score >= 50) status = 'Almost ready'

  return { score, status, metKeys, missing }
}

// ---------------------------------------------------------------------------
// Minimum required fields before a PM can submit a brief for UX review.
// ---------------------------------------------------------------------------

export interface RequiredField {
  label: string
  met: (b: FeatureBrief) => boolean
}

export const REQUIRED_FIELDS: RequiredField[] = [
  { label: 'Feature name', met: (b) => hasText(b.featureName) },
  { label: 'Short summary', met: (b) => hasText(b.shortSummary) },
  { label: 'Product owner', met: (b) => hasText(b.owners.productOwner) },
  { label: 'Problem statement (business)', met: (b) => hasText(b.problem.businessProblem) },
  { label: 'User problem', met: (b) => hasText(b.problem.userProblem) },
  { label: 'Primary objective', met: (b) => hasText(b.objectives.primaryObjective) },
  { label: 'At least one target user', met: (b) => b.targetUsers.length > 0 },
  { label: 'Proposed solution', met: (b) => hasText(b.proposedSolution.description) },
  { label: 'At least one platform', met: (b) => b.platforms.some((p) => p.selected) },
  { label: 'At least one main scenario', met: (b) => b.scenarios.length > 0 },
  { label: 'At least one core requirement', met: (b) => b.requirements.length > 0 },
  { label: 'Out of scope section', met: (b) => b.outOfScope.length > 0 },
]

export function getMissingRequiredFields(brief: FeatureBrief): string[] {
  return REQUIRED_FIELDS.filter((f) => !f.met(brief)).map((f) => f.label)
}

export function canSubmit(brief: FeatureBrief): boolean {
  return getMissingRequiredFields(brief).length === 0
}
