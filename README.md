# Feature Brief Builder

> Create better product context before UX starts designing.

An interactive prototype that guides Product Managers through a structured
wizard to produce a clear **Product / UX Feature Brief**, and gives the UX team
a read-only review dashboard to assess design readiness, surface missing
information, and raise questions back to the PM.

Built with **React + TypeScript + Vite**, persisted entirely in
**localStorage** (no backend required).

---

## How to run

```bash
npm install
npm run dev        # start the dev server (http://localhost:5173)
```

Other scripts:

```bash
npm run build      # type-check + production build to dist/
npm run preview    # preview the production build
npm run typecheck  # type-check only
```

On first load the app seeds two sample briefs (including the fully-populated
*Post-Signup Social Profile Onboarding* example). Use **Settings → Reset all
data** to restore the samples at any time.

### Trying it out

- Use the **PM View / UX View** role switcher at the bottom of the sidebar.
- **PM View** → open a brief (or *+ New Brief*) to edit it in the 24-step
  wizard; progress autosaves. The final *Submit / Share* step shows readiness,
  missing required fields, and lets you submit for UX review.
- **UX View** → *UX Review* lists submitted briefs; open one to see the
  readiness summary, missing information, the design-readiness checklist,
  add UX notes / questions, browse the full collapsible brief, and export
  (Copy as Markdown / Export JSON / Print).
- When UX marks a brief **Needs More Info**, the UX questions appear back in the
  PM wizard for the PM to answer.

---

## Project structure

```
src/
  types.ts                 # The complete FeatureBrief data model
  main.tsx / App.tsx       # Entry point + view router
  index.css                # Design system (light internal-tool theme)

  store/
    store.tsx              # Briefs + role + settings + toasts, localStorage persistence
    nav.tsx                # Lightweight in-memory navigation (no router dependency)

  data/
    factory.ts             # createBlankBrief(), ids, platform/checklist defaults
    options.ts             # Shared option lists & selectable suggestions
    mockData.ts            # Seed briefs (the social-onboarding example)

  utils/
    readiness.ts           # Readiness scoring + required-field validation
    export.ts              # Markdown / JSON export + clipboard helpers

  components/
    ui.tsx                 # Button, Card, Modal, ProgressBar, ReadinessRing, Collapsible…
    forms.tsx              # Field, Input, Textarea, Select, Checkbox, ChipSelect, RepeatableList
    chips.tsx              # Status / priority / MoSCoW / readiness chips
    Layout.tsx             # Sidebar + header + role switcher + toast stack
    BriefDocument.tsx      # Read-only, collapsible full-brief renderer (UX side)

  pages/
    Dashboard.tsx          # Central briefs dashboard (search / filter / sort)
    Settings.tsx           # Template overview + workspace settings
    wizard/                # PM side — 24-step wizard (one file per group of steps)
      Wizard.tsx           # Container: stepper, autosave, completion %, submit
      steps.ts             # Step registry (title + completion predicate)
      Steps*.tsx           # The individual step forms
      ReviewStep.tsx       # Final submit / share screen
    ux/
      UXReviewList.tsx     # UX review inbox
      UXReviewDetail.tsx   # Full UX review experience
```

---

## Key design decisions & assumptions

- **No router / no state library.** Navigation is a tiny in-memory context
  (`store/nav.tsx`) and state is a single React context (`store/store.tsx`).
  This keeps the prototype dependency-light; both are isolated so they can be
  swapped for `react-router` / a real data layer without touching the pages.
- **One `FeatureBrief` shape** holds both PM content and the `uxReview` layer,
  and is a plain serialisable object so it round-trips cleanly through
  localStorage (and later, any backend).
- **Readiness is computed, not stored.** `computeReadiness()` derives the score,
  status, and missing-information list live from the brief, so it is always in
  sync. The stored `readinessScore` field is left for a future backend to cache.
- **Autosave** debounces writes (500ms) into the store, which persists to
  localStorage on every change.
- **Roles are cosmetic.** The PM/UX switch only changes navigation and
  permissions in the UI — there is no real auth.
- **Mock users** (Maya Chen, Priya Desai, …) are illustrative sample data.

---

## Extending into a real product

- **Backend / persistence:** replace the localStorage read/write in
  `store/store.tsx` with API calls. The `FeatureBrief` type is the API contract.
- **Auth & roles:** swap the prototype role switch for real authentication;
  gate the UX-only mutations (review status, checklist, notes) server-side.
- **Routing & deep links:** replace `store/nav.tsx` with `react-router` so briefs
  have shareable URLs (`/briefs/:id`, `/review/:id`).
- **Real-time collaboration:** the flat, section-based model is amenable to
  per-section optimistic updates or CRDT-based sync.
- **Templates:** the wizard is config-driven via `pages/wizard/steps.ts`, so
  alternative brief templates can be added by defining new step registries.
- **PDF/export:** `utils/export.ts` already produces Markdown/JSON; add a proper
  PDF library or server-side render for branded exports.
