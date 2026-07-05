import type { FeatureBrief } from '../../types'
import type { StepProps } from './shared'
import type { ComponentType } from 'react'
import { StepOverview, StepBackground, StepProblem, StepObjectives } from './StepsBasics'
import { StepTargetUsers, StepUserNeed, StepProposedSolution } from './StepsUsers'
import { StepPlatformsMarkets, StepScenarios, StepEntryPoints, StepJourney } from './StepsFlow'
import { StepRequirements, StepUxGoals, StepCopy, StepDataPrivacy, StepAnalytics } from './StepsRequirements'
import {
  StepDependencies,
  StepRisks,
  StepEdgeCases,
  StepOutOfScope,
  StepOpenQuestions,
  StepDecisionLog,
  StepReferences,
} from './StepsClosing'

export interface StepDef {
  key: string
  title: string
  component: ComponentType<StepProps>
  // Whether the section has meaningful content (drives the stepper checkmarks
  // and the wizard completion percentage).
  hasContent: (b: FeatureBrief) => boolean
}

const t = (s: string | undefined) => Boolean(s && s.trim())

export const WIZARD_STEPS: StepDef[] = [
  { key: 'overview', title: 'Feature Overview', component: StepOverview, hasContent: (b) => t(b.featureName) && t(b.shortSummary) },
  { key: 'background', title: 'Background & Context', component: StepBackground, hasContent: (b) => t(b.background.whatExistsToday) || t(b.background.whyNow) },
  { key: 'problem', title: 'Problem Statement', component: StepProblem, hasContent: (b) => t(b.problem.businessProblem) || t(b.problem.userProblem) },
  { key: 'objectives', title: 'Objective & Value', component: StepObjectives, hasContent: (b) => t(b.objectives.primaryObjective) },
  { key: 'targetUsers', title: 'Target Users', component: StepTargetUsers, hasContent: (b) => b.targetUsers.length > 0 },
  { key: 'userNeed', title: 'User Need', component: StepUserNeed, hasContent: (b) => t(b.userNeed.needStatement) || t(b.userNeed.userStory) },
  { key: 'solution', title: 'Proposed Solution', component: StepProposedSolution, hasContent: (b) => t(b.proposedSolution.description) },
  { key: 'platforms', title: 'Platforms & Markets', component: StepPlatformsMarkets, hasContent: (b) => b.platforms.some((p) => p.selected) },
  { key: 'scenarios', title: 'Main Scenarios', component: StepScenarios, hasContent: (b) => b.scenarios.length > 0 },
  { key: 'entryPoints', title: 'Entry Points', component: StepEntryPoints, hasContent: (b) => b.entryPoints.length > 0 },
  { key: 'journey', title: 'Journey Structure', component: StepJourney, hasContent: (b) => t(b.journey.initialState) || b.journey.steps.length > 0 },
  { key: 'requirements', title: 'Core Requirements', component: StepRequirements, hasContent: (b) => b.requirements.length > 0 },
  { key: 'uxGoals', title: 'UX Goals', component: StepUxGoals, hasContent: (b) => t(b.uxGoals.shouldFeel) || b.uxGoals.selectedPrinciples.length > 0 },
  { key: 'copy', title: 'Content & Copy', component: StepCopy, hasContent: (b) => t(b.copyRequirements.toneOfVoice) },
  { key: 'dataPrivacy', title: 'Data & Privacy', component: StepDataPrivacy, hasContent: (b) => b.dataPrivacy.length > 0 },
  { key: 'analytics', title: 'Analytics & Metrics', component: StepAnalytics, hasContent: (b) => b.analytics.kpis.length > 0 || b.analytics.events.length > 0 },
  { key: 'dependencies', title: 'Dependencies', component: StepDependencies, hasContent: (b) => b.dependencies.length > 0 },
  { key: 'risks', title: 'Risks & Constraints', component: StepRisks, hasContent: (b) => b.risks.length > 0 },
  { key: 'edgeCases', title: 'Edge Cases', component: StepEdgeCases, hasContent: (b) => b.edgeCases.length > 0 },
  { key: 'outOfScope', title: 'Out of Scope', component: StepOutOfScope, hasContent: (b) => b.outOfScope.length > 0 },
  { key: 'openQuestions', title: 'Open Questions', component: StepOpenQuestions, hasContent: (b) => b.openQuestions.length > 0 },
  { key: 'decisionLog', title: 'Decision Log', component: StepDecisionLog, hasContent: (b) => b.decisionLog.length > 0 },
  { key: 'references', title: 'References', component: StepReferences, hasContent: (b) => b.references.length > 0 },
]

// The review step is index WIZARD_STEPS.length (rendered specially).
export const REVIEW_STEP_TITLE = 'Submit / Share'
