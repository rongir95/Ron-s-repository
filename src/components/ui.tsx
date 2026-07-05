import {
  useState,
  type ButtonHTMLAttributes,
  type CSSProperties,
  type ReactNode,
} from 'react'

// --- Button ---------------------------------------------------------------

type ButtonVariant = 'default' | 'primary' | 'danger' | 'ghost'
interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: ButtonVariant
  size?: 'sm' | 'md' | 'lg'
  block?: boolean
}

export function Button({
  variant = 'default',
  size = 'md',
  block,
  className = '',
  children,
  ...rest
}: ButtonProps) {
  const cls = [
    'btn',
    variant !== 'default' ? variant : '',
    size !== 'md' ? size : '',
    block ? 'block' : '',
    className,
  ]
    .filter(Boolean)
    .join(' ')
  return (
    <button className={cls} {...rest}>
      {children}
    </button>
  )
}

// --- Card -----------------------------------------------------------------

export function Card({
  children,
  className = '',
  pad = true,
  onClick,
  style,
}: {
  children: ReactNode
  className?: string
  pad?: boolean
  onClick?: () => void
  style?: CSSProperties
}) {
  return (
    <div className={`card ${pad ? 'card-pad' : ''} ${className}`} onClick={onClick} style={style}>
      {children}
    </div>
  )
}

// --- Progress bar ---------------------------------------------------------

export function ProgressBar({ value, tone }: { value: number; tone?: 'green' | 'orange' | 'red' }) {
  return (
    <div className="progress" role="progressbar" aria-valuenow={Math.round(value)} aria-valuemin={0} aria-valuemax={100}>
      <div className={`progress-fill ${tone ?? ''}`} style={{ width: `${Math.min(100, Math.max(0, value))}%` }} />
    </div>
  )
}

// --- Readiness ring -------------------------------------------------------

export function ReadinessRing({ score }: { score: number }) {
  const col = score >= 80 ? 'var(--green)' : score >= 50 ? 'var(--orange)' : 'var(--red)'
  return (
    <div
      className="readiness-ring"
      style={{ ['--pct' as string]: String(score), ['--col' as string]: col }}
      aria-label={`Readiness ${score}%`}
    >
      <div className="inner">{score}%</div>
    </div>
  )
}

// --- Empty state ----------------------------------------------------------

export function EmptyState({
  icon = '📄',
  title,
  children,
  action,
}: {
  icon?: string
  title: string
  children?: ReactNode
  action?: ReactNode
}) {
  return (
    <div className="empty">
      <div className="icon">{icon}</div>
      <h4>{title}</h4>
      {children && <p>{children}</p>}
      {action && <div style={{ marginTop: 14 }}>{action}</div>}
    </div>
  )
}

// --- Icon (delete) button -------------------------------------------------

export function IconButton({ onClick, title = 'Remove', children = '✕' }: { onClick: () => void; title?: string; children?: ReactNode }) {
  return (
    <button type="button" className="icon-btn" onClick={onClick} title={title} aria-label={title}>
      {children}
    </button>
  )
}

// --- Collapsible section --------------------------------------------------

export function Collapsible({
  title,
  defaultOpen = false,
  right,
  children,
}: {
  title: ReactNode
  defaultOpen?: boolean
  right?: ReactNode
  children: ReactNode
}) {
  const [open, setOpen] = useState(defaultOpen)
  return (
    <div className="section-card">
      <div className={`collapse-head ${open ? 'open' : ''}`} onClick={() => setOpen((o) => !o)}>
        <span className="caret">▶</span>
        <h3>{title}</h3>
        <span className="spacer" />
        {right}
      </div>
      {open && <div className="collapse-body">{children}</div>}
    </div>
  )
}

// --- Modal ----------------------------------------------------------------

export function Modal({
  title,
  children,
  onClose,
  actions,
}: {
  title: string
  children: ReactNode
  onClose: () => void
  actions: ReactNode
}) {
  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal" onClick={(e) => e.stopPropagation()}>
        <h3>{title}</h3>
        <div>{children}</div>
        <div className="modal-actions">{actions}</div>
      </div>
    </div>
  )
}

export function ConfirmModal({
  title,
  message,
  confirmLabel = 'Confirm',
  danger,
  onConfirm,
  onCancel,
}: {
  title: string
  message: string
  confirmLabel?: string
  danger?: boolean
  onConfirm: () => void
  onCancel: () => void
}) {
  return (
    <Modal
      title={title}
      onClose={onCancel}
      actions={
        <>
          <Button variant="ghost" onClick={onCancel}>
            Cancel
          </Button>
          <Button variant={danger ? 'danger' : 'primary'} onClick={onConfirm}>
            {confirmLabel}
          </Button>
        </>
      }
    >
      <p style={{ margin: 0 }}>{message}</p>
    </Modal>
  )
}
