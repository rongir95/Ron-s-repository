import {
  useCallback,
  useEffect,
  useId,
  useRef,
  type ButtonHTMLAttributes,
  type CSSProperties,
  type InputHTMLAttributes,
  type ReactNode,
  type SelectHTMLAttributes,
  type TextareaHTMLAttributes,
} from 'react'
import { directionGlyph, signedMoney, signedPercent } from '../lib/format'

// --- Button ---------------------------------------------------------------

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'default' | 'primary' | 'danger' | 'ghost'
  size?: 'sm' | 'md'
  block?: boolean
  iconOnly?: boolean
}

export function Button({
  variant = 'default',
  size = 'md',
  block,
  iconOnly,
  className = '',
  type = 'button',
  ...rest
}: ButtonProps) {
  const cls = ['btn', variant !== 'default' && variant, size === 'sm' && 'sm', block && 'block', iconOnly && 'icon', className]
    .filter(Boolean)
    .join(' ')
  return <button type={type} className={cls} {...rest} />
}

// --- Card -----------------------------------------------------------------

export function Card({
  children,
  className = '',
  pad = true,
  style,
  as: Tag = 'div',
}: {
  children: ReactNode
  className?: string
  pad?: boolean
  style?: CSSProperties
  as?: 'div' | 'section'
}) {
  return (
    <Tag className={`card ${pad ? 'card-pad' : ''} ${className}`.trim()} style={style}>
      {children}
    </Tag>
  )
}

// --- Form controls --------------------------------------------------------

export function Field({
  label,
  hint,
  error,
  children,
  htmlFor,
}: {
  label: string
  hint?: string
  error?: string
  children: ReactNode
  htmlFor?: string
}) {
  return (
    <div className="field">
      <label className="field-label" htmlFor={htmlFor}>
        {label}
      </label>
      {children}
      {error ? (
        <span className="field-error" role="alert">
          {error}
        </span>
      ) : hint ? (
        <span className="field-hint">{hint}</span>
      ) : null}
    </div>
  )
}

export function Input({ className = '', ...rest }: InputHTMLAttributes<HTMLInputElement>) {
  return <input className={`input ${className}`.trim()} {...rest} />
}

export function Textarea({ className = '', ...rest }: TextareaHTMLAttributes<HTMLTextAreaElement>) {
  return <textarea className={`input ${className}`.trim()} {...rest} />
}

export function Select({ className = '', children, ...rest }: SelectHTMLAttributes<HTMLSelectElement>) {
  return (
    <select className={`select ${className}`.trim()} {...rest}>
      {children}
    </select>
  )
}

export function Segmented<T extends string>({
  value,
  options,
  onChange,
  label,
}: {
  value: T
  options: Array<{ value: T; label: string }>
  onChange: (value: T) => void
  label: string
}) {
  return (
    <div className="segmented" role="group" aria-label={label}>
      {options.map((option) => (
        <button
          key={option.value}
          type="button"
          aria-pressed={option.value === value}
          onClick={() => onChange(option.value)}
        >
          {option.label}
        </button>
      ))}
    </div>
  )
}

// --- Modal ----------------------------------------------------------------

export function Modal({
  title,
  subtitle,
  onClose,
  children,
  footer,
  wide,
}: {
  title: string
  subtitle?: string
  onClose: () => void
  children: ReactNode
  footer?: ReactNode
  wide?: boolean
}) {
  const panel = useRef<HTMLDivElement>(null)
  const titleId = useId()

  useEffect(() => {
    const previous = document.activeElement as HTMLElement | null
    // Focus the first control so keyboard users land inside the dialog.
    panel.current?.querySelector<HTMLElement>('input, select, textarea, button')?.focus()
    const onKeyDown = (event: KeyboardEvent) => {
      if (event.key === 'Escape') {
        event.stopPropagation()
        onClose()
        return
      }
      if (event.key !== 'Tab' || !panel.current) return
      const focusable = [
        ...panel.current.querySelectorAll<HTMLElement>(
          'a[href], button:not([disabled]), input:not([disabled]), select:not([disabled]), textarea:not([disabled]), [tabindex]:not([tabindex="-1"])',
        ),
      ].filter((element) => element.offsetParent !== null)
      if (!focusable.length) return
      const first = focusable[0]
      const last = focusable[focusable.length - 1]
      // Keep Tab inside the dialog.
      if (event.shiftKey && document.activeElement === first) {
        event.preventDefault()
        last.focus()
      } else if (!event.shiftKey && document.activeElement === last) {
        event.preventDefault()
        first.focus()
      }
    }
    document.addEventListener('keydown', onKeyDown, true)
    const { overflow } = document.body.style
    document.body.style.overflow = 'hidden'
    return () => {
      document.removeEventListener('keydown', onKeyDown, true)
      document.body.style.overflow = overflow
      previous?.focus?.()
    }
  }, [onClose])

  return (
    <div
      className="overlay"
      onMouseDown={(event) => {
        if (event.target === event.currentTarget) onClose()
      }}
    >
      <div
        className={`modal ${wide ? 'wide' : ''}`.trim()}
        role="dialog"
        aria-modal="true"
        aria-labelledby={titleId}
        ref={panel}
      >
        <div className="modal-head">
          <div>
            <h2 className="modal-title" id={titleId}>
              {title}
            </h2>
            {subtitle && <div className="modal-sub">{subtitle}</div>}
          </div>
          <Button variant="ghost" size="sm" iconOnly onClick={onClose} aria-label="Close">
            ✕
          </Button>
        </div>
        <div className="modal-body">{children}</div>
        {footer && <div className="modal-foot">{footer}</div>}
      </div>
    </div>
  )
}

export function ConfirmDialog({
  title,
  message,
  confirmLabel = 'Confirm',
  destructive,
  onConfirm,
  onCancel,
}: {
  title: string
  message: ReactNode
  confirmLabel?: string
  destructive?: boolean
  onConfirm: () => void
  onCancel: () => void
}) {
  return (
    <Modal
      title={title}
      onClose={onCancel}
      footer={
        <>
          <Button onClick={onCancel}>Cancel</Button>
          <Button variant={destructive ? 'danger' : 'primary'} onClick={onConfirm}>
            {confirmLabel}
          </Button>
        </>
      }
    >
      <div style={{ color: 'var(--text-2)' }}>{message}</div>
    </Modal>
  )
}

// --- Value display --------------------------------------------------------

export function toneClass(value: number): string {
  if (value > 0) return 'v-gain'
  if (value < 0) return 'v-loss'
  return 'v-flat'
}

/**
 * A signed money or percentage value.
 *
 * Direction is carried by the sign and the arrow as well as the colour —
 * green/red alone would not be distinguishable to every reader.
 */
export function Value({
  amount,
  currency,
  percent,
  arrow = true,
  bold,
  masked,
}: {
  amount: number
  currency?: string
  /** Render as a percentage (amount is then a fraction). */
  percent?: boolean
  arrow?: boolean
  bold?: boolean
  masked?: boolean
}) {
  const text = percent ? signedPercent(amount) : signedMoney(amount, currency)
  return (
    <span className={toneClass(amount)} style={bold ? { fontWeight: 650 } : undefined}>
      {arrow && (
        <span className="arrow" aria-hidden="true">
          {directionGlyph(amount)}
        </span>
      )}
      {arrow && ' '}
      <span className={masked ? 'privacy-mask' : undefined}>{text}</span>
    </span>
  )
}

// --- Chips, banners, empty states ----------------------------------------

export function Chip({
  children,
  tone = 'default',
  large,
  title,
}: {
  children: ReactNode
  tone?: 'default' | 'gain' | 'loss' | 'accent' | 'warn'
  large?: boolean
  title?: string
}) {
  return (
    <span
      className={`chip ${tone !== 'default' ? tone : ''} ${large ? 'lg' : ''}`.trim()}
      title={title}
    >
      {children}
    </span>
  )
}

export function Swatch({ color }: { color: string }) {
  return <span className="swatch" style={{ background: color }} aria-hidden="true" />
}

export function Banner({
  tone = 'default',
  title,
  children,
  action,
}: {
  tone?: 'default' | 'error' | 'info'
  title?: string
  children: ReactNode
  action?: ReactNode
}) {
  return (
    <div className={`banner ${tone !== 'default' ? tone : ''}`.trim()} role={tone === 'error' ? 'alert' : undefined}>
      <div className="banner-body">
        {title && <div className="banner-title">{title}</div>}
        <div>{children}</div>
      </div>
      {action}
    </div>
  )
}

export function EmptyState({
  icon,
  title,
  children,
  action,
}: {
  icon?: ReactNode
  title: string
  children?: ReactNode
  action?: ReactNode
}) {
  return (
    <div className="empty">
      {icon && <div className="empty-icon">{icon}</div>}
      <h3>{title}</h3>
      {children && <p>{children}</p>}
      {action}
    </div>
  )
}

export function Skeleton({ width = '100%', height = 14 }: { width?: number | string; height?: number }) {
  return <span className="skeleton" style={{ display: 'inline-block', width, height }} aria-hidden="true" />
}

// --- Icons ----------------------------------------------------------------
// Inline SVG rather than emoji: emoji render differently per platform and can
// come out as full-colour glyphs that clash with the row they sit in.

export function IconPencil() {
  return (
    <svg width="14" height="14" viewBox="0 0 16 16" fill="none" stroke="currentColor" strokeWidth="1.4" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M11.3 2.4a1.4 1.4 0 0 1 2 2L5.6 12.1l-2.8.7.7-2.8 7.8-7.6Z" />
      <path d="M10.2 3.5 12.5 5.8" />
    </svg>
  )
}

export function IconTrash() {
  return (
    <svg width="14" height="14" viewBox="0 0 16 16" fill="none" stroke="currentColor" strokeWidth="1.4" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M2.8 4.4h10.4M6.3 4.4V3.1h3.4v1.3M4.2 4.4l.6 8.2a1 1 0 0 0 1 .9h4.4a1 1 0 0 0 1-.9l.6-8.2" />
      <path d="M6.7 7v3.8M9.3 7v3.8" />
    </svg>
  )
}

// --- Hooks ----------------------------------------------------------------

/** Closes a popover on outside click or Escape. */
export function useDismiss(open: boolean, onClose: () => void) {
  const ref = useRef<HTMLDivElement>(null)
  const close = useCallback(onClose, [onClose])
  useEffect(() => {
    if (!open) return
    const onPointerDown = (event: MouseEvent) => {
      if (ref.current && !ref.current.contains(event.target as Node)) close()
    }
    const onKeyDown = (event: KeyboardEvent) => {
      if (event.key === 'Escape') close()
    }
    document.addEventListener('mousedown', onPointerDown)
    document.addEventListener('keydown', onKeyDown)
    return () => {
      document.removeEventListener('mousedown', onPointerDown)
      document.removeEventListener('keydown', onKeyDown)
    }
  }, [open, close])
  return ref
}
