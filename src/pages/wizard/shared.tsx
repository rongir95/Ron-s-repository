import type { ReactNode } from 'react'
import type { FeatureBrief } from '../../types'

// Every wizard step receives the working draft plus a mutation helper. `update`
// takes a mutator that edits a structural clone, so steps can write nested
// fields ergonomically (e.g. `update(d => { d.overview.featureName = v })`).
export interface StepProps {
  draft: FeatureBrief
  update: (mutator: (d: FeatureBrief) => void) => void
}

export function StepHead({
  step,
  total,
  title,
  children,
}: {
  step: number
  total: number
  title: string
  children?: ReactNode
}) {
  return (
    <div className="step-head">
      <div className="eyebrow">
        Step {step} of {total}
      </div>
      <h2>{title}</h2>
      {children}
    </div>
  )
}

export function Helper({ children }: { children: ReactNode }) {
  return (
    <div className="helper-callout">
      <span className="i">💡</span>
      <span>{children}</span>
    </div>
  )
}
