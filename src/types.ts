// ============================================================================
// Feature Brief Builder — Data Model
// ============================================================================
// A single FeatureBrief captures everything a PM fills in via the wizard plus
// the UX team's review layer. The model is intentionally flat-ish and made of
// plain serialisable objects so it round-trips cleanly through localStorage and
// could later be persisted to a real backend without transformation.
// ============================================================================

export type Role = 'pm' | 'ux'

export type BriefStatus =
  | 'Draft'
  | 'Submitted'
  | 'In UX Review'
  | 'Needs More Info'
  | 'Ready for Design'
  | 'Approved'
  | 'Archived'

export type Priority = 'Low' | 'Medium' | 'High' | 'Critical'
export type MoSCoW = 'Must' | 'Should' | 'Could' | "Won't"
export type ScenarioPriority = 'Must' | 'Should' | 'Could'
export type UserPriority = 'Primary' | 'Secondary' | 'Future'
export type ReadinessStatus = 'Not ready' | 'Almost ready' | 'Ready for UX'
export type NotePriority = 'Low' | 'Medium' | 'High'
export type RiskSeverity = 'Low' | 'Medium' | 'High'

export type UserState =
  | 'New user'
  | 'Existing user'
  | 'Returning user'
  | 'Logged out'
  | 'Logged in'
  | 'Other'

export type PlatformName =
  | 'Web'
  | 'iOS'
  | 'Android'
  | 'tvOS'
  | 'Android TV'
  | 'Roku'
  | 'Other'

// --- Section-level shapes -------------------------------------------------

export interface Owners {
  productOwner: string
  designer: string
  techLead: string
  dataOwner: string
  qaOwner: string
  uxOwner: string
}

export interface Overview {
  featureName: string
  shortSummary: string
  documentStatus: 'Draft' | 'In Review' | 'Approved'
  targetRelease: string
  relatedInitiative: string
  priority: Priority
}

export interface Background {
  whatExistsToday: string
  whatIsMissing: string
  whyNow: string
  relatedAreas: string
  marketContext: string
}

export interface ProblemStatement {
  businessProblem: string
  userProblem: string
  evidence: string
  doNothing: string
}

export interface Objectives {
  primaryObjective: string
  secondaryObjectives: string
  businessValue: string
  expectedImpact: string
  strategicRelevance: string
  goals: string[] // checkbox selections
}

export interface TargetUser {
  id: string
  name: string
  description: string
  priority: UserPriority
  userState: UserState
  notes: string
}

export interface UserNeed {
  needStatement: string
  userStory: string
  shouldUnderstand: string
  shouldBeAbleToDo: string
  shouldFeel: string
}

export interface ProposedSolution {
  description: string
  mainActions: string
  expectedOutcome: string
  newOrExtension: 'New feature' | 'Extension' | ''
  mandatoryOrOptional: 'Mandatory' | 'Optional' | ''
  canSkip: boolean
  canReturnLater: boolean
  canEditLater: boolean
}

export interface PlatformEntry {
  name: PlatformName
  selected: boolean
  notes: string
  differentBehavior: string
  inMvp: boolean
  rtl: boolean // needs a dedicated right-to-left design on this platform
}

export interface Market {
  id: string
  name: string
  inScope: boolean
  notes: string
}

export interface Scenario {
  id: string
  name: string
  description: string
  userState: UserState
  trigger: string
  expectedBehavior: string
  priority: ScenarioPriority
}

export interface EntryPoint {
  id: string
  name: string
  platform: string
  trigger: string
  userState: UserState
  frequency: string
  stopCondition: string
  automaticOrManual: 'Automatic' | 'Manual' | ''
  blockingOrDismissible: 'Blocking' | 'Dismissible' | ''
  notes: string
}

export interface JourneyStep {
  id: string
  name: string
  purpose: string
  inputRequired: string
  userActions: string
  validation: string
  skipBehavior: string
  successBehavior: string
  errorBehavior: string
  uxNotes: string
}

export interface Journey {
  initialState: string
  returningState: string
  completedState: string
  editState: string
  emptyState: string
  loadingState: string
  errorState: string
  steps: JourneyStep[]
}

export interface Requirement {
  id: string
  title: string
  description: string
  priority: MoSCoW
  platform: string
  owner: string
  status: 'Open' | 'Ready' | 'Blocked' | 'Changed'
  notes: string
}

export interface UxGoals {
  shouldFeel: string
  shouldAvoid: string
  designPrinciples: string
  selectedPrinciples: string[]
}

export interface CopyRequirements {
  toneOfVoice: string
  mandatoryMessages: string
  wordsToAvoid: string
  localisation: string
  legalCopyRequired: boolean
  errorGuidance: string
  confirmationGuidance: string
  copyDocLink: string
}

export interface DataPoint {
  id: string
  name: string
  whyNeeded: string
  mandatory: boolean
  storedWhere: string
  displayedWhere: string
  canEdit: boolean
  canDelete: boolean
  privacyNotes: string
}

export interface Kpi {
  id: string
  goal: string
  name: string
  definition: string
  successTarget: string
  notes: string
}

export interface TrackingEvent {
  id: string
  name: string
  trigger: string
  properties: string
  notes: string
}

export interface Analytics {
  kpis: Kpi[]
  events: TrackingEvent[]
}

export interface Dependency {
  id: string
  name: string
  type: 'API' | 'Design' | 'Data' | 'Copy' | 'Legal' | 'Backend' | 'Frontend' | 'Other'
  owner: string
  status: 'Open' | 'In Progress' | 'Ready' | 'Blocked'
  blockingUx: boolean
  notes: string
}

export interface Risk {
  id: string
  risk: string
  impact: string
  mitigation: string
  severity: RiskSeverity
  owner: string
}

export interface EdgeCase {
  id: string
  edgeCase: string
  expectedBehavior: string
  priority: ScenarioPriority
  notes: string
}

export interface OutOfScopeItem {
  id: string
  item: string
  reason: string
  futureConsideration: boolean
}

export interface OpenQuestion {
  id: string
  question: string
  askedBy: string
  owner: string
  status: 'Open' | 'Answered' | 'Blocked'
  blockingUx: boolean
  deadline: string
  answer: string
  dateAnswered: string
}

export interface Decision {
  id: string
  date: string
  decision: string
  owner: string
  reason: string
  impactOnUx: string
  related: string
}

export interface ReferenceLink {
  id: string
  type: string
  label: string
  url: string
}

// --- UX review layer -------------------------------------------------------

export interface UxNote {
  id: string
  section: string
  text: string
  createdBy: string
  date: string
  priority: NotePriority
}

export interface UxQuestion {
  id: string
  question: string
  section: string
  blockingUx: boolean
  status: 'Open' | 'Answered'
  pmAnswer: string
}

export type ChecklistState = 'Ready' | 'Missing' | 'Not relevant'

export interface ChecklistItem {
  id: string
  label: string
  state: ChecklistState
  notes: string
}

export interface UxReview {
  readinessScore: number
  readinessStatus: ReadinessStatus
  missingInformation: string[]
  uxNotes: UxNote[]
  uxQuestions: UxQuestion[]
  designReadinessChecklist: ChecklistItem[]
  reviewStatus: BriefStatus
  reviewedBy: string
  reviewedAt: string
}

// --- The root object -------------------------------------------------------

export interface FeatureBrief {
  id: string
  featureName: string
  shortSummary: string
  status: BriefStatus
  priority: Priority
  createdAt: string
  updatedAt: string
  submittedAt: string
  owners: Owners
  overview: Overview
  background: Background
  problem: ProblemStatement
  objectives: Objectives
  targetUsers: TargetUser[]
  userNeed: UserNeed
  proposedSolution: ProposedSolution
  platforms: PlatformEntry[]
  markets: Market[]
  scenarios: Scenario[]
  entryPoints: EntryPoint[]
  journey: Journey
  requirements: Requirement[]
  uxGoals: UxGoals
  copyRequirements: CopyRequirements
  dataPrivacy: DataPoint[]
  analytics: Analytics
  dependencies: Dependency[]
  risks: Risk[]
  edgeCases: EdgeCase[]
  outOfScope: OutOfScopeItem[]
  openQuestions: OpenQuestion[]
  decisionLog: Decision[]
  references: ReferenceLink[]
  uxReview: UxReview
}
