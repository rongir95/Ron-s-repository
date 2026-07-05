import { useState, type ReactNode } from 'react'
import { Button, IconButton } from './ui'

// A labelled field wrapper with optional required marker and helper hint.
export function Field({
  label,
  required,
  hint,
  children,
}: {
  label?: string
  required?: boolean
  hint?: string
  children: ReactNode
}) {
  return (
    <div className="field">
      {label && (
        <label className="field-label">
          {label}
          {required && <span className="req" title="Required">*</span>}
        </label>
      )}
      {hint && <div className="field-hint">{hint}</div>}
      {children}
    </div>
  )
}

export function Input({
  value,
  onChange,
  placeholder,
  type = 'text',
}: {
  value: string
  onChange: (v: string) => void
  placeholder?: string
  type?: string
}) {
  return (
    <input
      className="input"
      type={type}
      value={value}
      placeholder={placeholder}
      onChange={(e) => onChange(e.target.value)}
    />
  )
}

export function Textarea({
  value,
  onChange,
  placeholder,
  rows = 3,
}: {
  value: string
  onChange: (v: string) => void
  placeholder?: string
  rows?: number
}) {
  return (
    <textarea
      className="textarea"
      value={value}
      rows={rows}
      placeholder={placeholder}
      onChange={(e) => onChange(e.target.value)}
    />
  )
}

export function Select<T extends string>({
  value,
  onChange,
  options,
  placeholder,
}: {
  value: T | ''
  onChange: (v: T) => void
  options: readonly T[]
  placeholder?: string
}) {
  return (
    <select className="select" value={value} onChange={(e) => onChange(e.target.value as T)}>
      {placeholder && <option value="">{placeholder}</option>}
      {options.map((o) => (
        <option key={o} value={o}>
          {o}
        </option>
      ))}
    </select>
  )
}

export function Checkbox({
  checked,
  onChange,
  label,
}: {
  checked: boolean
  onChange: (v: boolean) => void
  label: ReactNode
}) {
  return (
    <label className="checkbox-row">
      <input type="checkbox" checked={checked} onChange={(e) => onChange(e.target.checked)} />
      <span>{label}</span>
    </label>
  )
}

// A multi-select rendered as toggleable chips. With `allowCustom`, the user can
// also type and add their own values, which appear as selected chips and can be
// toggled off (removed) like any other.
export function ChipSelect({
  options,
  selected,
  onToggle,
  allowCustom,
  customPlaceholder = 'Add your own…',
}: {
  options: string[]
  selected: string[]
  onToggle: (value: string) => void
  allowCustom?: boolean
  customPlaceholder?: string
}) {
  const [custom, setCustom] = useState('')
  // Show the fixed options plus any selected values that aren't in the list
  // (i.e. custom entries the user added).
  const extras = selected.filter((s) => !options.includes(s))
  const all = [...options, ...extras]

  const add = () => {
    const v = custom.trim()
    if (v && !selected.includes(v)) onToggle(v)
    setCustom('')
  }

  return (
    <div>
      <div className="chip-select">
        {all.map((o) => (
          <button
            key={o}
            type="button"
            className={`chip-toggle ${selected.includes(o) ? 'on' : ''}`}
            onClick={() => onToggle(o)}
          >
            {selected.includes(o) ? '✓ ' : ''}
            {o}
          </button>
        ))}
      </div>
      {allowCustom && (
        <div className="row" style={{ marginTop: 10, maxWidth: 380 }}>
          <input
            className="input"
            value={custom}
            placeholder={customPlaceholder}
            onChange={(e) => setCustom(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === 'Enter') {
                e.preventDefault()
                add()
              }
            }}
          />
          <Button size="sm" type="button" onClick={add} disabled={!custom.trim()}>
            Add
          </Button>
        </div>
      )}
    </div>
  )
}

// Quick-add suggestion chips (clicking adds an item, not a toggle).
export function SuggestionChips({
  options,
  onPick,
}: {
  options: string[]
  onPick: (value: string) => void
}) {
  return (
    <div className="chip-select" style={{ marginBottom: 14 }}>
      {options.map((o) => (
        <button key={o} type="button" className="chip-toggle" onClick={() => onPick(o)}>
          + {o}
        </button>
      ))}
    </div>
  )
}

// A generic add/remove list of cards. Renders each item via a render prop.
export function RepeatableList<T extends { id: string }>({
  items,
  onAdd,
  onRemove,
  renderItem,
  addLabel = 'Add item',
  itemLabel = 'Item',
  emptyHint,
}: {
  items: T[]
  onAdd: () => void
  onRemove: (id: string) => void
  renderItem: (item: T, index: number) => ReactNode
  addLabel?: string
  itemLabel?: string
  emptyHint?: string
}) {
  return (
    <div>
      {items.length === 0 && emptyHint && (
        <p className="muted text-sm" style={{ marginTop: 0 }}>
          {emptyHint}
        </p>
      )}
      {items.map((item, i) => (
        <div className="repeat-item" key={item.id}>
          <div className="repeat-item-head">
            <span className="idx">
              {itemLabel} {i + 1}
            </span>
            <span className="spacer" />
            <IconButton onClick={() => onRemove(item.id)} title={`Remove ${itemLabel.toLowerCase()}`} />
          </div>
          {renderItem(item, i)}
        </div>
      ))}
      <Button variant="ghost" onClick={onAdd} style={{ borderStyle: 'dashed', borderColor: 'var(--border-strong)', borderWidth: 1 }}>
        + {addLabel}
      </Button>
    </div>
  )
}
