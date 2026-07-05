// Shared option lists and selectable suggestions used throughout the wizard.

import type {
  Priority,
  MoSCoW,
  ScenarioPriority,
  UserPriority,
  UserState,
  BriefStatus,
  RiskSeverity,
  NotePriority,
} from '../types'

export const PRIORITIES: Priority[] = ['Low', 'Medium', 'High', 'Critical']
export const MOSCOW: MoSCoW[] = ['Must', 'Should', 'Could', "Won't"]
export const SCENARIO_PRIORITIES: ScenarioPriority[] = ['Must', 'Should', 'Could']
export const USER_PRIORITIES: UserPriority[] = ['Primary', 'Secondary', 'Future']
export const RISK_SEVERITIES: RiskSeverity[] = ['Low', 'Medium', 'High']
export const NOTE_PRIORITIES: NotePriority[] = ['Low', 'Medium', 'High']

export const USER_STATES: UserState[] = [
  'New user',
  'Existing user',
  'Returning user',
  'Logged out',
  'Logged in',
  'Other',
]

export const BRIEF_STATUSES: BriefStatus[] = [
  'Draft',
  'Submitted',
  'In UX Review',
  'Needs More Info',
  'Ready for Design',
  'Approved',
  'Archived',
]

export const DOCUMENT_STATUSES = ['Draft', 'In Review', 'Approved'] as const

export const OBJECTIVE_GOALS = [
  'Increase engagement',
  'Increase retention',
  'Increase conversion',
  'Improve onboarding',
  'Improve discoverability',
  'Reduce friction',
  'Reduce support issues',
  'Capture user data',
  'Improve personalization',
  'Support campaign / market launch',
]

export const UX_PRINCIPLES = [
  'Clear and easy to understand',
  'Lightweight and not overwhelming',
  'Helpful before asking the user to act',
  'Consistent with existing product patterns',
  'Easy to skip',
  'Easy to complete later',
  'Transparent about why data is requested',
  'Flexible across platforms',
  'Accessible and inclusive',
  'Localisation-friendly',
]

export const SCENARIO_SUGGESTIONS = [
  'First-time user sees the feature',
  'Returning user continues incomplete flow',
  'Existing user already has partial data',
  'User skips the flow',
  'User completes the flow',
  'User accesses from another platform',
  'Error or failed submission',
]

export const EDGE_CASE_SUGGESTIONS = [
  'User closes the flow midway',
  'User loses connection',
  'Data fails to save',
  'User already completed part of the flow',
  'User skips all optional steps',
  'User returns from another platform',
  'Feature is not supported in a specific market',
  'API returns partial data',
  'Long translated text breaks layout',
]

export const EVENT_SUGGESTIONS = [
  'feature_viewed',
  'feature_started',
  'step_viewed',
  'step_completed',
  'step_skipped',
  'feature_completed',
  'feature_dismissed',
  'error_shown',
]

export const DEPENDENCY_TYPES = [
  'API',
  'Design',
  'Data',
  'Copy',
  'Legal',
  'Backend',
  'Frontend',
  'Other',
] as const

export const REFERENCE_TYPES = [
  'Figma',
  'Product docs',
  'Technical docs',
  'API docs',
  'Data docs',
  'Copy docs',
  'Research',
  'Previous related features',
  'Design system references',
]
