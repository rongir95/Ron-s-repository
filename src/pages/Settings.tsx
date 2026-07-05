import { useState } from 'react'
import { useStore } from '../store/store'
import { Card, Button, ConfirmModal } from '../components/ui'
import { Field, Input } from '../components/forms'
import { REQUIRED_FIELDS, READINESS_CRITERIA } from '../utils/readiness'

export function Settings() {
  const { settings, updateSettings, resetData, toast } = useStore()
  const [confirmReset, setConfirmReset] = useState(false)

  return (
    <div>
      {confirmReset && (
        <ConfirmModal
          title="Reset all data?"
          message="This clears every brief and restores the sample data. This cannot be undone."
          confirmLabel="Reset data"
          danger
          onCancel={() => setConfirmReset(false)}
          onConfirm={() => {
            resetData()
            setConfirmReset(false)
            toast('Data reset to samples', 'info')
          }}
        />
      )}

      <div className="page-head">
        <div>
          <h1>How to write a good Feature Brief</h1>
          <p>Template overview and workspace settings.</p>
        </div>
      </div>

      <Card className="card-pad" style={{ marginBottom: 18 }}>
        <div className="callout blue">
          This brief is <strong>not meant to replace a full PRD</strong>. It is meant to give UX enough
          context to start thinking, asking the right questions, and identifying missing information early.
        </div>
      </Card>

      <div className="field-row" style={{ alignItems: 'start' }}>
        <Card className="card-pad">
          <h3 className="mb-8" style={{ fontSize: 15 }}>What this tool is for</h3>
          <p className="text-sm muted mt-0">
            PMs often ask UX to start on features without enough context — no clear problem, intent, users,
            or constraints. Feature Brief Builder guides you through a structured brief so UX can review the
            product intent, spot gaps, and ask better questions before design starts.
          </p>
        </Card>

        <Card className="card-pad">
          <h3 className="mb-8" style={{ fontSize: 15 }}>What PMs should prepare first</h3>
          <ul className="text-sm" style={{ margin: 0, paddingLeft: 18, color: 'var(--text-2)' }}>
            <li>The user and business problem you are solving</li>
            <li>Evidence or signal that the problem is real</li>
            <li>Who the target users are, and their state</li>
            <li>Which platforms and markets are in scope</li>
            <li>Known dependencies, risks, and open questions</li>
          </ul>
        </Card>
      </div>

      <div className="field-row" style={{ alignItems: 'start', marginTop: 0 }}>
        <Card className="card-pad">
          <h3 className="mb-8" style={{ fontSize: 15 }}>What makes a brief ready for UX</h3>
          <p className="text-sm muted mt-0">A brief is ready when these readiness checks pass:</p>
          <ul className="text-sm" style={{ margin: 0, paddingLeft: 18, color: 'var(--text-2)' }}>
            {READINESS_CRITERIA.map((c) => (
              <li key={c.key}>{c.label}</li>
            ))}
          </ul>
        </Card>

        <Card className="card-pad">
          <h3 className="mb-8" style={{ fontSize: 15 }}>Feature Brief vs. detailed PRD</h3>
          <p className="text-sm muted mt-0">
            A <strong>Feature Brief</strong> captures intent, context, and enough structure for UX to start
            exploring. A <strong>PRD</strong> comes later and specifies detailed behavior, acceptance
            criteria, and edge-case handling in full. Think of the brief as the shared starting point that
            makes the eventual PRD faster and better.
          </p>
          <h4 style={{ margin: '14px 0 6px', fontSize: 13 }}>What UX needs before designing</h4>
          <p className="text-sm muted mt-0">
            A clear problem, defined users, confirmed platforms, the core flow, must-have requirements, an
            explicit out-of-scope, and awareness of blocking questions and dependencies.
          </p>
        </Card>
      </div>

      <Card className="card-pad" style={{ marginTop: 18 }}>
        <h3 className="mb-8" style={{ fontSize: 15 }}>Minimum required fields before submitting</h3>
        <div className="row wrap" style={{ gap: 8 }}>
          {REQUIRED_FIELDS.map((f) => (
            <span key={f.label} className="chip brand">
              <span className="dot" />
              {f.label}
            </span>
          ))}
        </div>
      </Card>

      <Card className="card-pad" style={{ marginTop: 18 }}>
        <h3 className="mb-16" style={{ fontSize: 15 }}>Workspace settings</h3>
        <div className="field-row">
          <Field label="Your name" hint="Used when you add UX notes or reviews.">
            <Input value={settings.currentUserName} onChange={(v) => updateSettings({ currentUserName: v })} />
          </Field>
          <Field label="Organisation">
            <Input value={settings.organisation} onChange={(v) => updateSettings({ organisation: v })} />
          </Field>
        </div>
        <div className="divider" />
        <div className="row" style={{ justifyContent: 'space-between' }}>
          <div className="text-sm muted">Reset local data and restore the built-in sample briefs.</div>
          <Button variant="danger" onClick={() => setConfirmReset(true)}>Reset all data</Button>
        </div>
      </Card>
    </div>
  )
}
