import type { BriefStatus, Priority, ReadinessStatus, MoSCoW } from '../types'

type Tone = 'green' | 'orange' | 'red' | 'blue' | 'purple' | 'brand' | 'gray'

function Chip({ tone, children }: { tone: Tone; children: React.ReactNode }) {
  const cls = tone === 'gray' ? 'chip' : `chip ${tone}`
  return (
    <span className={cls}>
      <span className="dot" />
      {children}
    </span>
  )
}

const STATUS_TONES: Record<BriefStatus, Tone> = {
  Draft: 'gray',
  Submitted: 'blue',
  'In UX Review': 'purple',
  'Needs More Info': 'orange',
  'Ready for Design': 'green',
  Approved: 'green',
  Archived: 'gray',
}

export function StatusChip({ status }: { status: BriefStatus }) {
  return <Chip tone={STATUS_TONES[status]}>{status}</Chip>
}

const PRIORITY_TONES: Record<Priority, Tone> = {
  Low: 'gray',
  Medium: 'blue',
  High: 'orange',
  Critical: 'red',
}

export function PriorityChip({ priority }: { priority: Priority }) {
  return <Chip tone={PRIORITY_TONES[priority]}>{priority}</Chip>
}

const MOSCOW_TONES: Record<MoSCoW, Tone> = {
  Must: 'red',
  Should: 'orange',
  Could: 'blue',
  "Won't": 'gray',
}

export function MoscowChip({ priority }: { priority: MoSCoW }) {
  return <Chip tone={MOSCOW_TONES[priority]}>{priority}</Chip>
}

export function ReadinessChip({ status }: { status: ReadinessStatus }) {
  const tone: Tone = status === 'Ready for UX' ? 'green' : status === 'Almost ready' ? 'orange' : 'red'
  return <Chip tone={tone}>{status}</Chip>
}

export function GenericChip({ label, tone = 'gray' }: { label: string; tone?: Tone }) {
  return <Chip tone={tone}>{label}</Chip>
}
