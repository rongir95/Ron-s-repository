import {
  createContext,
  useCallback,
  useContext,
  useMemo,
  useState,
  type ReactNode,
} from 'react'

// A deliberately tiny navigation layer. Keeping it in-memory (rather than
// pulling in a router) keeps the prototype dependency-light; swapping in
// react-router later only touches this file and the sidebar links.

export type View = 'dashboard' | 'wizard' | 'ux-review' | 'ux-detail' | 'settings'

interface NavState {
  view: View
  briefId: string | null
}

interface NavValue extends NavState {
  navigate: (view: View, briefId?: string | null) => void
  openWizard: (briefId: string) => void
  openUxDetail: (briefId: string) => void
}

const NavContext = createContext<NavValue | null>(null)

export function NavProvider({ children }: { children: ReactNode }) {
  const [state, setState] = useState<NavState>({ view: 'dashboard', briefId: null })

  const navigate = useCallback((view: View, briefId: string | null = null) => {
    setState({ view, briefId })
    window.scrollTo({ top: 0 })
  }, [])

  const openWizard = useCallback((briefId: string) => navigate('wizard', briefId), [navigate])
  const openUxDetail = useCallback((briefId: string) => navigate('ux-detail', briefId), [navigate])

  const value = useMemo<NavValue>(
    () => ({ ...state, navigate, openWizard, openUxDetail }),
    [state, navigate, openWizard, openUxDetail],
  )

  return <NavContext.Provider value={value}>{children}</NavContext.Provider>
}

// eslint-disable-next-line react-refresh/only-export-components
export function useNav(): NavValue {
  const ctx = useContext(NavContext)
  if (!ctx) throw new Error('useNav must be used within NavProvider')
  return ctx
}
