import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useRef,
  useState,
  type ReactNode,
} from 'react'
import type { FeatureBrief, Role } from '../types'
import { seedBriefs } from '../data/mockData'

const STORAGE_KEY = 'fbb.briefs.v1'
const ROLE_KEY = 'fbb.role.v1'
const SETTINGS_KEY = 'fbb.settings.v1'

export interface AppSettings {
  currentUserName: string
  organisation: string
}

const DEFAULT_SETTINGS: AppSettings = {
  currentUserName: 'You',
  organisation: 'Acme Product',
}

// ---- persistence helpers ---------------------------------------------------

function loadBriefs(): FeatureBrief[] {
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    if (!raw) return seedBriefs()
    const parsed = JSON.parse(raw) as FeatureBrief[]
    if (!Array.isArray(parsed) || parsed.length === 0) return seedBriefs()
    return parsed
  } catch {
    return seedBriefs()
  }
}

function loadRole(): Role {
  const r = localStorage.getItem(ROLE_KEY)
  return r === 'ux' ? 'ux' : 'pm'
}

function loadSettings(): AppSettings {
  try {
    const raw = localStorage.getItem(SETTINGS_KEY)
    if (!raw) return DEFAULT_SETTINGS
    return { ...DEFAULT_SETTINGS, ...(JSON.parse(raw) as Partial<AppSettings>) }
  } catch {
    return DEFAULT_SETTINGS
  }
}

// ---- toast system ----------------------------------------------------------

export interface Toast {
  id: number
  message: string
  variant: 'success' | 'info' | 'error'
}

// ---- context ---------------------------------------------------------------

interface StoreValue {
  briefs: FeatureBrief[]
  role: Role
  setRole: (r: Role) => void
  settings: AppSettings
  updateSettings: (patch: Partial<AppSettings>) => void
  getBrief: (id: string) => FeatureBrief | undefined
  saveBrief: (brief: FeatureBrief) => void
  deleteBrief: (id: string) => void
  addBrief: (brief: FeatureBrief) => void
  resetData: () => void
  toasts: Toast[]
  toast: (message: string, variant?: Toast['variant']) => void
  dismissToast: (id: number) => void
}

const StoreContext = createContext<StoreValue | null>(null)

export function StoreProvider({ children }: { children: ReactNode }) {
  const [briefs, setBriefs] = useState<FeatureBrief[]>(() => loadBriefs())
  const [role, setRoleState] = useState<Role>(() => loadRole())
  const [settings, setSettings] = useState<AppSettings>(() => loadSettings())
  const [toasts, setToasts] = useState<Toast[]>([])
  const toastId = useRef(0)

  // Persist briefs whenever they change.
  useEffect(() => {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(briefs))
    } catch {
      /* storage may be unavailable (private mode); ignore */
    }
  }, [briefs])

  useEffect(() => {
    localStorage.setItem(ROLE_KEY, role)
  }, [role])

  useEffect(() => {
    localStorage.setItem(SETTINGS_KEY, JSON.stringify(settings))
  }, [settings])

  const dismissToast = useCallback((id: number) => {
    setToasts((t) => t.filter((x) => x.id !== id))
  }, [])

  const toast = useCallback(
    (message: string, variant: Toast['variant'] = 'success') => {
      const id = ++toastId.current
      setToasts((t) => [...t, { id, message, variant }])
      setTimeout(() => dismissToast(id), 3200)
    },
    [dismissToast],
  )

  const setRole = useCallback((r: Role) => setRoleState(r), [])

  const updateSettings = useCallback((patch: Partial<AppSettings>) => {
    setSettings((s) => ({ ...s, ...patch }))
  }, [])

  const getBrief = useCallback((id: string) => briefs.find((b) => b.id === id), [briefs])

  const saveBrief = useCallback((brief: FeatureBrief) => {
    setBriefs((list) => {
      const idx = list.findIndex((b) => b.id === brief.id)
      if (idx === -1) return [...list, brief]
      const copy = [...list]
      copy[idx] = brief
      return copy
    })
  }, [])

  const addBrief = useCallback((brief: FeatureBrief) => {
    setBriefs((list) => [...list, brief])
  }, [])

  const deleteBrief = useCallback((id: string) => {
    setBriefs((list) => list.filter((b) => b.id !== id))
  }, [])

  const resetData = useCallback(() => {
    setBriefs(seedBriefs())
  }, [])

  const value = useMemo<StoreValue>(
    () => ({
      briefs,
      role,
      setRole,
      settings,
      updateSettings,
      getBrief,
      saveBrief,
      deleteBrief,
      addBrief,
      resetData,
      toasts,
      toast,
      dismissToast,
    }),
    [briefs, role, setRole, settings, updateSettings, getBrief, saveBrief, deleteBrief, addBrief, resetData, toasts, toast, dismissToast],
  )

  return <StoreContext.Provider value={value}>{children}</StoreContext.Provider>
}

// eslint-disable-next-line react-refresh/only-export-components
export function useStore(): StoreValue {
  const ctx = useContext(StoreContext)
  if (!ctx) throw new Error('useStore must be used within StoreProvider')
  return ctx
}
