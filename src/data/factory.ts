import type {
  FeatureBrief,
  PlatformEntry,
  PlatformName,
  ChecklistItem,
} from '../types'

// A small id helper. crypto.randomUUID is available in all modern browsers; we
// fall back to a timestamp-based id just in case (e.g. non-secure contexts).
export function uid(prefix = 'id'): string {
  if (typeof crypto !== 'undefined' && 'randomUUID' in crypto) {
    return `${prefix}_${crypto.randomUUID()}`
  }
  return `${prefix}_${Math.random().toString(36).slice(2)}${Date.now().toString(36)}`
}

export const ALL_PLATFORMS: PlatformName[] = [
  'Web',
  'iOS',
  'Android',
  'tvOS',
  'Android TV',
  'Roku',
  'Other',
]

export function blankPlatforms(): PlatformEntry[] {
  return ALL_PLATFORMS.map((name) => ({
    name,
    selected: false,
    notes: '',
    differentBehavior: '',
    inMvp: false,
    rtl: false,
  }))
}

export const DEFAULT_CHECKLIST_LABELS = [
  'Problem statement is clear',
  'User problem is defined',
  'Target users are defined',
  'Platforms and markets are confirmed',
  'Entry points are defined',
  'Core flow is defined',
  'Must-have requirements are clear',
  'Out of scope is clear',
  'Main dependencies are known',
  'Blocking open questions are identified',
  'Success metrics are defined',
  'Copy owner is defined',
  'Relevant references are linked',
]

export function blankChecklist(): ChecklistItem[] {
  return DEFAULT_CHECKLIST_LABELS.map((label) => ({
    id: uid('chk'),
    label,
    state: 'Missing',
    notes: '',
  }))
}

export function createBlankBrief(): FeatureBrief {
  const now = new Date().toISOString()
  return {
    id: uid('brief'),
    featureName: '',
    shortSummary: '',
    status: 'Draft',
    priority: 'Medium',
    createdAt: now,
    updatedAt: now,
    submittedAt: '',
    owners: {
      productOwner: '',
      designer: '',
      techLead: '',
      dataOwner: '',
      qaOwner: '',
      uxOwner: '',
    },
    overview: {
      featureName: '',
      shortSummary: '',
      documentStatus: 'Draft',
      targetRelease: '',
      relatedInitiative: '',
      priority: 'Medium',
    },
    background: {
      whatExistsToday: '',
      whatIsMissing: '',
      whyNow: '',
      relatedAreas: '',
      marketContext: '',
    },
    problem: {
      businessProblem: '',
      userProblem: '',
      evidence: '',
      doNothing: '',
    },
    objectives: {
      primaryObjective: '',
      secondaryObjectives: '',
      businessValue: '',
      expectedImpact: '',
      strategicRelevance: '',
      goals: [],
    },
    targetUsers: [],
    userNeed: {
      needStatement: '',
      userStory: '',
      shouldUnderstand: '',
      shouldBeAbleToDo: '',
      shouldFeel: '',
    },
    proposedSolution: {
      description: '',
      mainActions: '',
      expectedOutcome: '',
      newOrExtension: '',
      mandatoryOrOptional: '',
      canSkip: false,
      canReturnLater: false,
      canEditLater: false,
    },
    platforms: blankPlatforms(),
    markets: [],
    scenarios: [],
    entryPoints: [],
    journey: {
      initialState: '',
      returningState: '',
      completedState: '',
      editState: '',
      emptyState: '',
      loadingState: '',
      errorState: '',
      steps: [],
    },
    requirements: [],
    uxGoals: {
      shouldFeel: '',
      shouldAvoid: '',
      designPrinciples: '',
      selectedPrinciples: [],
    },
    copyRequirements: {
      toneOfVoice: '',
      mandatoryMessages: '',
      wordsToAvoid: '',
      localisation: '',
      legalCopyRequired: false,
      errorGuidance: '',
      confirmationGuidance: '',
      copyDocLink: '',
    },
    dataPrivacy: [],
    analytics: { kpis: [], events: [] },
    dependencies: [],
    risks: [],
    edgeCases: [],
    outOfScope: [],
    openQuestions: [],
    decisionLog: [],
    references: [],
    uxReview: {
      readinessScore: 0,
      readinessStatus: 'Not ready',
      missingInformation: [],
      uxNotes: [],
      uxQuestions: [],
      designReadinessChecklist: blankChecklist(),
      reviewStatus: 'Draft',
      reviewedBy: '',
      reviewedAt: '',
    },
  }
}
