import { StoreProvider } from './store/store'
import { NavProvider, useNav } from './store/nav'
import { Layout } from './components/Layout'
import { Dashboard } from './pages/Dashboard'
import { Wizard } from './pages/wizard/Wizard'
import { UXReviewList } from './pages/ux/UXReviewList'
import { UXReviewDetail } from './pages/ux/UXReviewDetail'
import { Settings } from './pages/Settings'

const TITLES: Record<string, { title: string; subtitle: string }> = {
  dashboard: { title: 'Briefs Dashboard', subtitle: 'Create better product context before UX starts designing.' },
  wizard: { title: 'PM Wizard', subtitle: 'Build a structured feature brief step by step.' },
  'ux-review': { title: 'UX Review', subtitle: 'Review submitted briefs and check design readiness.' },
  'ux-detail': { title: 'UX Review', subtitle: 'Review submitted briefs and check design readiness.' },
  settings: { title: 'Template Overview', subtitle: 'How to write a good Feature Brief.' },
}

function Router() {
  const { view } = useNav()
  const meta = TITLES[view] ?? TITLES.dashboard

  let page
  switch (view) {
    case 'wizard':
      page = <Wizard />
      break
    case 'ux-review':
      page = <UXReviewList />
      break
    case 'ux-detail':
      page = <UXReviewDetail />
      break
    case 'settings':
      page = <Settings />
      break
    case 'dashboard':
    default:
      page = <Dashboard />
  }

  return (
    <Layout title={meta.title} subtitle={meta.subtitle}>
      {page}
    </Layout>
  )
}

export default function App() {
  return (
    <StoreProvider>
      <NavProvider>
        <Router />
      </NavProvider>
    </StoreProvider>
  )
}
