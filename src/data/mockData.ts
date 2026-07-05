import type { FeatureBrief } from '../types'
import { createBlankBrief, uid, blankChecklist } from './factory'

// A fully-populated example brief used to seed the app on first run so both the
// PM and UX sides have something realistic to explore.
export function createMockBrief(): FeatureBrief {
  const b = createBlankBrief()
  b.id = 'brief_mock_social_onboarding'
  b.featureName = 'Post-Signup Social Profile Onboarding'
  b.shortSummary =
    'A guided onboarding journey shown after signup that helps users set up their social profile by choosing an avatar, following relevant entities, selecting a favourite team, and providing optional profile information.'
  b.status = 'In UX Review'
  b.priority = 'High'
  b.createdAt = '2026-06-10T09:00:00.000Z'
  b.updatedAt = '2026-06-28T14:30:00.000Z'
  b.submittedAt = '2026-06-25T11:00:00.000Z'

  b.owners = {
    productOwner: 'Maya Chen',
    designer: 'Tom Ferreira',
    techLead: 'Ravi Patel',
    dataOwner: 'Lena Ortiz',
    qaOwner: 'Sam Njoroge',
    uxOwner: 'Priya Desai',
  }

  b.overview = {
    featureName: 'Post-Signup Social Profile Onboarding',
    shortSummary: b.shortSummary,
    documentStatus: 'In Review',
    targetRelease: 'Q3 2026',
    relatedInitiative: 'DEP-482 — Social Engagement Program',
    priority: 'High',
  }

  b.background = {
    whatExistsToday:
      'Social Profile already exists in the product, but it is buried in the account settings area and most new users never discover it.',
    whatIsMissing:
      'There is no early, guided path that introduces the social profile and encourages users to set it up while intent is high.',
    whyNow:
      'Engagement metrics show social profile completion strongly correlates with 30-day retention, and the Social Engagement Program has this as a Q3 priority.',
    relatedAreas: 'Account settings, Following system, Team preferences, Avatar picker.',
    marketContext:
      'Competitors surface social setup immediately after signup. A summer sports campaign in Q3 makes team-following especially timely.',
  }

  b.problem = {
    businessProblem:
      'Low discovery and completion of the Social Profile limits social engagement, which is a leading indicator of long-term retention.',
    userProblem:
      'New users do not realise they can personalise their experience by following teams and entities, so their feed feels generic and less relevant.',
    evidence:
      'Only 8% of new users complete a social profile in their first week. Cohort analysis shows completers retain 22% better at day 30.',
    doNothing:
      'Social engagement stays flat, feeds remain generic for new users, and the retention opportunity is missed for the campaign window.',
  }

  b.objectives = {
    primaryObjective:
      'Increase exposure and completion of Social Profile in order to improve long-term engagement and retention.',
    secondaryObjectives:
      'Increase the number of entities followed per new user and grow favourite-team selection ahead of the summer campaign.',
    businessValue:
      'Higher social engagement improves retention and increases inventory for personalised and campaign content.',
    expectedImpact:
      'Lift social profile completion from 8% to 25% among new users within one quarter of launch.',
    strategicRelevance: 'Directly supports the Social Engagement Program (DEP-482).',
    goals: [
      'Increase engagement',
      'Increase retention',
      'Improve onboarding',
      'Improve personalization',
      'Support campaign / market launch',
    ],
  }

  b.targetUsers = [
    {
      id: uid('user'),
      name: 'New users after signup',
      description: 'Users who have just completed account creation and have no social profile yet.',
      priority: 'Primary',
      userState: 'New user',
      notes: 'Highest intent moment — they just chose to join.',
    },
    {
      id: uid('user'),
      name: 'Existing users with incomplete social profile',
      description: 'Returning users who signed up before this feature and never completed setup.',
      priority: 'Secondary',
      userState: 'Existing user',
      notes: 'Reached via a secondary entry point rather than the signup flow.',
    },
    {
      id: uid('user'),
      name: 'TV users accessing profile from avatar entry point',
      description: 'Users on tvOS / Android TV who open the profile from the avatar shortcut.',
      priority: 'Future',
      userState: 'Logged in',
      notes: 'Input constraints on TV — keep interactions minimal.',
    },
  ]

  b.userNeed = {
    needStatement:
      'New users need a simple, guided way to personalise their profile right after signup so their experience feels relevant from day one.',
    userStory:
      'As a new user, I need to quickly set up my social profile, so that my feed and recommendations feel personal to me.',
    shouldUnderstand: 'That personalising their profile makes the product more relevant to them.',
    shouldBeAbleToDo: 'Pick an avatar, follow entities, choose a favourite team, and optionally add profile info.',
    shouldFeel: 'In control and unpressured — it should never feel like a mandatory chore.',
  }

  b.proposedSolution = {
    description:
      'After signup, present a short multi-step onboarding that walks the user through choosing an avatar, following suggested entities, selecting a favourite team, and optionally completing profile details. Each step is skippable and resumable.',
    mainActions: 'Choose avatar → Follow entities → Select favourite team → Add optional info → Done.',
    expectedOutcome: 'A meaningfully completed social profile and a personalised feed on first session.',
    newOrExtension: 'Extension',
    mandatoryOrOptional: 'Optional',
    canSkip: true,
    canReturnLater: true,
    canEditLater: true,
  }

  b.platforms = b.platforms.map((p) => {
    if (['Web', 'iOS', 'Android', 'tvOS', 'Android TV'].includes(p.name)) {
      return {
        ...p,
        selected: true,
        inMvp: p.name === 'Web' || p.name === 'iOS' || p.name === 'Android',
        notes:
          p.name === 'tvOS' || p.name === 'Android TV'
            ? 'Reduced flow — avatar + favourite team only.'
            : '',
        differentBehavior:
          p.name === 'tvOS' || p.name === 'Android TV'
            ? 'No optional profile info step; remote-friendly navigation.'
            : '',
      }
    }
    return p
  })

  b.markets = [
    { id: uid('mkt'), name: 'United States', inScope: true, notes: 'Primary launch market.' },
    { id: uid('mkt'), name: 'United Kingdom', inScope: true, notes: '' },
    { id: uid('mkt'), name: 'Germany', inScope: true, notes: 'Localisation review required.' },
    { id: uid('mkt'), name: 'Japan', inScope: false, notes: 'Deferred — entity catalog incomplete.' },
  ]

  b.scenarios = [
    {
      id: uid('scn'),
      name: 'First-time user sees the feature',
      description: 'A brand new user finishes signup and immediately enters the onboarding flow.',
      userState: 'New user',
      trigger: 'Signup completed',
      expectedBehavior: 'Onboarding launches automatically with the avatar step.',
      priority: 'Must',
    },
    {
      id: uid('scn'),
      name: 'Returning user continues incomplete flow',
      description: 'A user who skipped part of onboarding returns and resumes where they left off.',
      userState: 'Returning user',
      trigger: 'Re-entry from profile prompt',
      expectedBehavior: 'Flow resumes at the first incomplete step.',
      priority: 'Should',
    },
    {
      id: uid('scn'),
      name: 'User skips the flow',
      description: 'The user dismisses onboarding without completing any steps.',
      userState: 'New user',
      trigger: 'Skip / dismiss action',
      expectedBehavior: 'Flow closes gracefully; a re-entry point remains available.',
      priority: 'Must',
    },
    {
      id: uid('scn'),
      name: 'User accesses from another platform',
      description: 'A user starts on web and later opens the app on TV.',
      userState: 'Logged in',
      trigger: 'Open profile on TV',
      expectedBehavior: 'Completion state is respected; only remaining TV-relevant steps show.',
      priority: 'Could',
    },
  ]

  b.entryPoints = [
    {
      id: uid('ep'),
      name: 'Post-signup automatic launch',
      platform: 'Web, iOS, Android',
      trigger: 'Immediately after signup success',
      userState: 'New user',
      frequency: 'Once per new user',
      stopCondition: 'Flow completed or explicitly skipped',
      automaticOrManual: 'Automatic',
      blockingOrDismissible: 'Dismissible',
      notes: 'Must not block the user from reaching the main app.',
    },
    {
      id: uid('ep'),
      name: 'Profile completion prompt',
      platform: 'Web, iOS, Android',
      trigger: 'User with incomplete profile opens home',
      userState: 'Existing user',
      frequency: 'Up to 3 times, then suppressed',
      stopCondition: 'Profile completed or dismissed 3 times',
      automaticOrManual: 'Automatic',
      blockingOrDismissible: 'Dismissible',
      notes: 'Frequency capping handled by messaging service.',
    },
  ]

  b.journey = {
    initialState: 'Avatar selection step with suggested avatars.',
    returningState: 'Resume at first incomplete step with progress preserved.',
    completedState: 'Confirmation screen summarising choices with a link to the personalised feed.',
    editState: 'All choices editable later from the social profile settings.',
    emptyState: 'If no entity suggestions are available, show a generic follow-search field.',
    loadingState: 'Skeleton placeholders while suggestions load.',
    errorState: 'Inline retry with the ability to skip the step if loading fails.',
    steps: [
      {
        id: uid('step'),
        name: 'Choose avatar',
        purpose: 'Give the profile a face and a sense of ownership.',
        inputRequired: 'Avatar selection (from set or upload).',
        userActions: 'Select or upload an avatar.',
        validation: 'None — any valid image or preset.',
        skipBehavior: 'Default avatar assigned.',
        successBehavior: 'Advance to Follow entities.',
        errorBehavior: 'Upload failure shows inline retry.',
        uxNotes: 'Keep upload optional and lightweight.',
      },
      {
        id: uid('step'),
        name: 'Follow entities',
        purpose: 'Seed the feed with relevant content.',
        inputRequired: 'Selected entities to follow.',
        userActions: 'Tap suggested entities or search.',
        validation: 'Zero selections allowed (can skip).',
        skipBehavior: 'Proceed with no follows; generic feed.',
        successBehavior: 'Advance to Favourite team.',
        errorBehavior: 'Show retry if suggestions fail to load.',
        uxNotes: 'Show why each suggestion is relevant.',
      },
      {
        id: uid('step'),
        name: 'Select favourite team',
        purpose: 'Enable team-based personalisation and campaign content.',
        inputRequired: 'One favourite team (optional).',
        userActions: 'Pick a team from a searchable list.',
        validation: 'Optional.',
        skipBehavior: 'No team set.',
        successBehavior: 'Advance to optional profile info.',
        errorBehavior: 'Inline error with retry.',
        uxNotes: 'Tie into the summer campaign visuals.',
      },
    ],
  }

  b.requirements = [
    {
      id: uid('req'),
      title: 'Resume from first incomplete step',
      description: 'The flow must persist progress and resume at the first incomplete step on re-entry.',
      priority: 'Must',
      platform: 'All',
      owner: 'Ravi Patel',
      status: 'Ready',
      notes: 'Depends on UMS completion state.',
    },
    {
      id: uid('req'),
      title: 'Every step is skippable',
      description: 'Each step must offer a clear skip action; no step blocks progression.',
      priority: 'Must',
      platform: 'All',
      owner: 'Maya Chen',
      status: 'Open',
      notes: '',
    },
    {
      id: uid('req'),
      title: 'Reduced TV flow',
      description: 'On tvOS / Android TV, show only avatar and favourite-team steps.',
      priority: 'Should',
      platform: 'tvOS, Android TV',
      owner: 'Tom Ferreira',
      status: 'Open',
      notes: 'Remote-friendly navigation required.',
    },
    {
      id: uid('req'),
      title: 'Editable later from settings',
      description: 'All onboarding choices must be editable from social profile settings.',
      priority: 'Should',
      platform: 'All',
      owner: 'Maya Chen',
      status: 'Ready',
      notes: '',
    },
  ]

  b.uxGoals = {
    shouldFeel: 'Welcoming, quick, and personal — a helpful head start rather than a form to fill out.',
    shouldAvoid: 'Feeling mandatory, long, or like a data-collection gate before using the product.',
    designPrinciples: 'Progressive, skippable, and consistent with existing onboarding patterns.',
    selectedPrinciples: [
      'Clear and easy to understand',
      'Lightweight and not overwhelming',
      'Easy to skip',
      'Easy to complete later',
      'Transparent about why data is requested',
      'Flexible across platforms',
    ],
  }

  b.copyRequirements = {
    toneOfVoice: 'Friendly, encouraging, concise.',
    mandatoryMessages: 'Explain that everything is optional and can be changed later.',
    wordsToAvoid: 'Avoid "required", "mandatory", and anything implying the user must complete it.',
    localisation: 'All strings must support DE and other launch-market locales; watch for long German strings.',
    legalCopyRequired: true,
    errorGuidance: 'Errors should be reassuring and always offer skip or retry.',
    confirmationGuidance: 'End on a positive confirmation that shows what was personalised.',
    copyDocLink: 'https://example.com/docs/social-onboarding-copy',
  }

  b.dataPrivacy = [
    {
      id: uid('dp'),
      name: 'Followed entities',
      whyNeeded: 'Drives feed personalisation.',
      mandatory: false,
      storedWhere: 'UMS (User Management Service).',
      displayedWhere: 'Social profile and feed.',
      canEdit: true,
      canDelete: true,
      privacyNotes: 'User-controlled; part of standard profile data.',
    },
    {
      id: uid('dp'),
      name: 'Favourite team',
      whyNeeded: 'Team-based personalisation and campaign targeting.',
      mandatory: false,
      storedWhere: 'UMS.',
      displayedWhere: 'Social profile.',
      canEdit: true,
      canDelete: true,
      privacyNotes: 'Requires privacy copy for campaign use.',
    },
  ]

  b.analytics = {
    kpis: [
      {
        id: uid('kpi'),
        goal: 'Increase onboarding completion',
        name: 'Social profile completion rate',
        definition: 'Share of new users who complete at least 2 onboarding steps in week 1.',
        successTarget: '25% (up from 8%)',
        notes: 'Primary success metric.',
      },
      {
        id: uid('kpi'),
        goal: 'Increase engagement',
        name: 'Avg. entities followed per new user',
        definition: 'Mean number of entities followed within 7 days of signup.',
        successTarget: '≥ 3',
        notes: '',
      },
    ],
    events: [
      { id: uid('evt'), name: 'feature_started', trigger: 'Onboarding launches after signup', properties: 'entry_point, platform', notes: '' },
      { id: uid('evt'), name: 'step_completed', trigger: 'User completes a step', properties: 'step_name, index', notes: '' },
      { id: uid('evt'), name: 'step_skipped', trigger: 'User skips a step', properties: 'step_name', notes: '' },
      { id: uid('evt'), name: 'feature_completed', trigger: 'User finishes the flow', properties: 'steps_completed', notes: '' },
      { id: uid('evt'), name: 'feature_dismissed', trigger: 'User dismisses onboarding', properties: 'step_name', notes: '' },
    ],
  }

  b.dependencies = [
    {
      id: uid('dep'),
      name: 'UMS completion state per step',
      type: 'Backend',
      owner: 'Ravi Patel',
      status: 'In Progress',
      blockingUx: true,
      notes: 'UMS needs to provide completion state for each onboarding step.',
    },
    {
      id: uid('dep'),
      name: 'Entity suggestion API',
      type: 'API',
      owner: 'Data team',
      status: 'Open',
      blockingUx: false,
      notes: 'Relevance ranking for suggested entities.',
    },
    {
      id: uid('dep'),
      name: 'Campaign privacy copy sign-off',
      type: 'Legal',
      owner: 'Legal',
      status: 'Open',
      blockingUx: false,
      notes: 'Needed before favourite-team data is used for campaigns.',
    },
  ]

  b.risks = [
    {
      id: uid('risk'),
      risk: 'Different platform behavior may create inconsistent user expectations.',
      impact: 'Users switching platforms may be confused by differing flows.',
      mitigation: 'Document platform differences clearly and keep core flow consistent.',
      severity: 'Medium',
      owner: 'Tom Ferreira',
    },
    {
      id: uid('risk'),
      risk: 'Onboarding may feel intrusive right after signup.',
      impact: 'Potential drop-off or negative first impression.',
      mitigation: 'Keep it short, skippable, and clearly optional.',
      severity: 'High',
      owner: 'Maya Chen',
    },
  ]

  b.edgeCases = [
    {
      id: uid('edge'),
      edgeCase: 'User already completed part of the flow',
      expectedBehavior: 'Resume at the first incomplete step; do not repeat completed steps.',
      priority: 'Must',
      notes: '',
    },
    {
      id: uid('edge'),
      edgeCase: 'API returns partial data',
      expectedBehavior: 'Show available suggestions; allow search fallback.',
      priority: 'Should',
      notes: '',
    },
    {
      id: uid('edge'),
      edgeCase: 'Long translated text breaks layout',
      expectedBehavior: 'Layout must accommodate long DE strings without truncation issues.',
      priority: 'Should',
      notes: 'Test with German pseudo-localisation.',
    },
  ]

  b.outOfScope = [
    {
      id: uid('oos'),
      item: 'Editing social profile privacy settings within onboarding',
      reason: 'Handled by existing settings; out of scope for the initial flow.',
      futureConsideration: true,
    },
    {
      id: uid('oos'),
      item: 'Roku support',
      reason: 'Not part of the Q3 launch platforms.',
      futureConsideration: true,
    },
  ]

  b.openQuestions = [
    {
      id: uid('q'),
      question: 'Which API should frontend use to determine which onboarding steps are already completed?',
      askedBy: 'Tom Ferreira',
      owner: 'Ravi Patel',
      status: 'Open',
      blockingUx: true,
      deadline: '2026-07-10',
      answer: '',
      dateAnswered: '',
    },
    {
      id: uid('q'),
      question: 'Do we need a distinct reduced flow spec for tvOS vs Android TV?',
      askedBy: 'Priya Desai',
      owner: 'Maya Chen',
      status: 'Open',
      blockingUx: true,
      deadline: '2026-07-12',
      answer: '',
      dateAnswered: '',
    },
    {
      id: uid('q'),
      question: 'Should favourite-team selection reuse the existing team picker component?',
      askedBy: 'Tom Ferreira',
      owner: 'Tom Ferreira',
      status: 'Answered',
      blockingUx: false,
      deadline: '',
      answer: 'Yes — reuse the existing picker with campaign theming.',
      dateAnswered: '2026-06-27',
    },
  ]

  b.decisionLog = [
    {
      id: uid('dec'),
      date: '2026-06-20',
      decision: 'Onboarding will be fully optional and skippable at every step.',
      owner: 'Maya Chen',
      reason: 'Avoids harming the signup-to-activation funnel.',
      impactOnUx: 'Every step needs a clear, low-friction skip affordance.',
      related: 'Risk: onboarding may feel intrusive',
    },
    {
      id: uid('dec'),
      date: '2026-06-24',
      decision: 'TV platforms get a reduced flow (avatar + favourite team only).',
      owner: 'Priya Desai',
      reason: 'Text input on TV is costly and error-prone.',
      impactOnUx: 'Design a remote-friendly, minimal TV variant.',
      related: 'Requirement: Reduced TV flow',
    },
  ]

  b.references = [
    { id: uid('ref'), type: 'Figma', label: 'Onboarding explorations', url: 'https://figma.com/file/example-onboarding' },
    { id: uid('ref'), type: 'Product docs', label: 'Social Engagement Program (DEP-482)', url: 'https://example.com/dep-482' },
    { id: uid('ref'), type: 'Research', label: 'New-user activation study', url: 'https://example.com/research/activation' },
    { id: uid('ref'), type: 'Design system references', label: 'Onboarding patterns', url: 'https://example.com/ds/onboarding' },
  ]

  // Seed the UX review layer so the UX side has content to show.
  b.uxReview = {
    readinessScore: 0, // recomputed live by the UI
    readinessStatus: 'Almost ready',
    missingInformation: [],
    uxNotes: [
      {
        id: uid('note'),
        section: 'Entry points',
        text: 'Confirm frequency-capping behavior is consistent across web and app messaging services.',
        createdBy: 'Priya Desai',
        date: '2026-06-27',
        priority: 'Medium',
      },
      {
        id: uid('note'),
        section: 'Platforms & markets',
        text: 'Need a clear spec for the reduced TV flow before we can storyboard it.',
        createdBy: 'Priya Desai',
        date: '2026-06-28',
        priority: 'High',
      },
    ],
    uxQuestions: [
      {
        id: uid('uxq'),
        question: 'Can we get final relevance rules for entity suggestions, or should we design for a generic fallback first?',
        section: 'Proposed solution',
        blockingUx: false,
        status: 'Open',
        pmAnswer: '',
      },
    ],
    designReadinessChecklist: blankChecklist().map((item) => {
      const ready = [
        'Problem statement is clear',
        'User problem is defined',
        'Target users are defined',
        'Must-have requirements are clear',
        'Out of scope is clear',
        'Success metrics are defined',
        'Copy owner is defined',
        'Relevant references are linked',
      ]
      return ready.includes(item.label) ? { ...item, state: 'Ready' as const } : item
    }),
    reviewStatus: 'In UX Review',
    reviewedBy: 'Priya Desai',
    reviewedAt: '2026-06-28T14:30:00.000Z',
  }

  return b
}

// A second, lighter draft brief so the dashboard shows more than one row.
export function createDraftMockBrief(): FeatureBrief {
  const b = createBlankBrief()
  b.id = 'brief_mock_saved_searches'
  b.featureName = 'Saved Searches & Alerts'
  b.shortSummary =
    'Let users save a search query and opt in to notifications when new matching results appear.'
  b.status = 'Draft'
  b.priority = 'Medium'
  b.createdAt = '2026-06-30T09:00:00.000Z'
  b.updatedAt = '2026-07-02T16:00:00.000Z'
  b.owners.productOwner = 'David Kim'
  b.overview.featureName = b.featureName
  b.overview.shortSummary = b.shortSummary
  b.overview.priority = 'Medium'
  b.overview.targetRelease = 'Q4 2026'
  b.problem.businessProblem = 'Users who do not find results on first search often churn.'
  b.problem.userProblem = 'Users have to repeat the same searches manually to check for new results.'
  b.objectives.primaryObjective = 'Increase return visits by notifying users of relevant new results.'
  b.platforms = b.platforms.map((p) =>
    p.name === 'Web' || p.name === 'iOS' ? { ...p, selected: true } : p,
  )
  return b
}

export function seedBriefs(): FeatureBrief[] {
  return [createMockBrief(), createDraftMockBrief()]
}
