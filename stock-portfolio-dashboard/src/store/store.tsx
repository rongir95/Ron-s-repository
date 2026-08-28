/**
 * The single source of truth: portfolios, positions and settings, persisted to
 * localStorage on every change. Deliberately one React context and no state
 * library — the whole app is small enough that this stays readable, and the
 * persistence boundary is one function (`persist`) if a backend ever replaces it.
 */
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
import type { AppData, Lot, Portfolio, Position, Settings } from '../types'
import { createEmptyPortfolio, createSeedData, DEFAULT_SETTINGS } from '../data/seed'
import { newId } from '../lib/id'

const STORAGE_KEY = 'stock-portfolio-dashboard.v1'

/** Palette slots 0-7 are the validated categorical hues; 8 is the neutral
 *  "Other" grey that the tail of a long portfolio folds into. */
export const PALETTE_SLOTS = 8
export const OTHER_SLOT = 8

/**
 * Lowest palette slot not already taken, so a hue belongs to one holding and
 * only one, and is reused only once freed. Past the eighth holding everything
 * shares the neutral slot rather than cycling the palette.
 */
export function lowestFreeSlot(taken: Set<number>): number {
  for (let slot = 0; slot < PALETTE_SLOTS; slot++) if (!taken.has(slot)) return slot
  return OTHER_SLOT
}

// --- persistence ----------------------------------------------------------

function readStorage(): AppData | null {
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    if (!raw) return null
    return normalise(JSON.parse(raw))
  } catch {
    // Corrupt or unreadable (private mode, quota, hand-edited) — fall back to seed.
    return null
  }
}

function persist(data: AppData): void {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(data))
  } catch {
    /* storage unavailable or full — the app still works for this session */
  }
}

const str = (value: unknown, fallback = ''): string => (typeof value === 'string' ? value : fallback)
const posNum = (value: unknown): number => {
  const n = typeof value === 'number' ? value : Number.parseFloat(String(value))
  return Number.isFinite(n) ? n : 0
}

/** Rebuilds a valid AppData from anything — imported files included. */
export function normalise(raw: unknown): AppData | null {
  if (!raw || typeof raw !== 'object') return null
  const input = raw as Partial<AppData>
  const portfolios: Portfolio[] = (Array.isArray(input.portfolios) ? input.portfolios : [])
    .map((portfolio): Portfolio | null => {
      if (!portfolio || typeof portfolio !== 'object') return null
      // Colour slots are validated per portfolio: an imported or hand-edited
      // file must not end up with two holdings sharing a hue.
      const takenSlots = new Set<number>()
      const positions: Position[] = (Array.isArray(portfolio.positions) ? portfolio.positions : [])
        .map((position): Position | null => {
          if (!position || typeof position !== 'object') return null
          const symbol = str(position.symbol).trim().toUpperCase()
          if (!symbol) return null
          const lots: Lot[] = (Array.isArray(position.lots) ? position.lots : [])
            .map((lot): Lot | null => {
              if (!lot || typeof lot !== 'object') return null
              const shares = posNum(lot.shares)
              if (shares <= 0) return null
              return {
                id: str(lot.id) || newId('lot'),
                shares,
                price: Math.max(0, posNum(lot.price)),
                date: /^\d{4}-\d{2}-\d{2}$/.test(str(lot.date)) ? str(lot.date) : undefined,
              }
            })
            .filter((lot): lot is Lot => lot !== null)
          if (!lots.length) return null
          const stored = Number(position.colorSlot)
          const usable =
            Number.isInteger(stored) &&
            stored >= 0 &&
            stored <= OTHER_SLOT &&
            // The neutral slot is shared; the eight categorical ones are not.
            (stored === OTHER_SLOT || !takenSlots.has(stored))
          const colorSlot = usable ? stored : lowestFreeSlot(takenSlots)
          if (colorSlot < OTHER_SLOT) takenSlots.add(colorSlot)
          return {
            id: str(position.id) || newId('pos'),
            symbol,
            name: str(position.name) || undefined,
            lots,
            colorSlot,
            notes: str(position.notes) || undefined,
            createdAt: str(position.createdAt) || new Date().toISOString(),
          }
        })
        .filter((position): position is Position => position !== null)
      return {
        id: str(portfolio.id) || newId('pf'),
        name: str(portfolio.name) || 'Portfolio',
        baseCurrency: (str(portfolio.baseCurrency, 'USD') || 'USD').toUpperCase().slice(0, 3),
        positions,
        sample: portfolio.sample === true ? true : undefined,
        createdAt: str(portfolio.createdAt) || new Date().toISOString(),
      }
    })
    .filter((portfolio): portfolio is Portfolio => portfolio !== null)

  if (!portfolios.length) return null

  const settings: Settings = { ...DEFAULT_SETTINGS, ...(input.settings ?? {}) }
  if (!['yahoo', 'twelvedata', 'demo'].includes(settings.providerId)) settings.providerId = 'yahoo'
  if (!['system', 'light', 'dark'].includes(settings.theme)) settings.theme = 'system'
  settings.refreshSeconds = [0, 30, 60, 300, 900].includes(settings.refreshSeconds)
    ? settings.refreshSeconds
    : DEFAULT_SETTINGS.refreshSeconds
  settings.twelveDataKey = str(settings.twelveDataKey)
  settings.privacyMode = settings.privacyMode === true

  const activeId = str(input.activePortfolioId)
  return {
    version: 1,
    portfolios,
    activePortfolioId: portfolios.some((p) => p.id === activeId) ? activeId : portfolios[0].id,
    settings,
  }
}

// --- toasts ---------------------------------------------------------------

export interface Toast {
  id: string
  message: string
  tone: 'info' | 'success' | 'error'
}

// --- context --------------------------------------------------------------

export interface NewPositionInput {
  symbol: string
  name?: string
  shares: number
  price: number
  date?: string
  notes?: string
}

interface StoreValue {
  data: AppData
  portfolio: Portfolio
  settings: Settings
  toasts: Toast[]
  toast: (message: string, tone?: Toast['tone']) => void
  dismissToast: (id: string) => void

  setActivePortfolio: (id: string) => void
  addPortfolio: (name: string, baseCurrency?: string) => string
  renamePortfolio: (id: string, name: string) => void
  setPortfolioCurrency: (id: string, currency: string) => void
  deletePortfolio: (id: string) => void

  addPosition: (input: NewPositionInput) => void
  /** Replaces the whole position — used by the edit form. */
  savePosition: (positionId: string, patch: Pick<Position, 'symbol' | 'name' | 'lots' | 'notes'>) => void
  removePosition: (positionId: string) => void

  updateSettings: (patch: Partial<Settings>) => void
  replaceAll: (data: AppData) => void
  startFresh: (name: string) => void
}

const StoreContext = createContext<StoreValue | null>(null)

export function StoreProvider({ children }: { children: ReactNode }) {
  const [data, setData] = useState<AppData>(() => readStorage() ?? createSeedData())
  const [toasts, setToasts] = useState<Toast[]>([])
  const timers = useRef<number[]>([])

  useEffect(() => {
    persist(data)
  }, [data])

  useEffect(
    () => () => {
      for (const timer of timers.current) clearTimeout(timer)
    },
    [],
  )

  const dismissToast = useCallback((id: string) => {
    setToasts((current) => current.filter((t) => t.id !== id))
  }, [])

  const toast = useCallback(
    (message: string, tone: Toast['tone'] = 'info') => {
      const id = newId('toast')
      setToasts((current) => [...current.slice(-2), { id, message, tone }])
      timers.current.push(
        window.setTimeout(() => setToasts((current) => current.filter((t) => t.id !== id)), 4200),
      )
    },
    [],
  )

  /** Applies `fn` to the active portfolio and drops its "sample" badge. */
  const editActive = useCallback((fn: (portfolio: Portfolio) => Portfolio) => {
    setData((current) => ({
      ...current,
      portfolios: current.portfolios.map((portfolio) =>
        portfolio.id === current.activePortfolioId ? { ...fn(portfolio), sample: undefined } : portfolio,
      ),
    }))
  }, [])

  const value = useMemo<StoreValue>(() => {
    const portfolio =
      data.portfolios.find((p) => p.id === data.activePortfolioId) ?? data.portfolios[0]

    return {
      data,
      portfolio,
      settings: data.settings,
      toasts,
      toast,
      dismissToast,

      setActivePortfolio: (id) => setData((current) => ({ ...current, activePortfolioId: id })),

      addPortfolio: (name, baseCurrency) => {
        const created = createEmptyPortfolio(name.trim() || 'New portfolio', baseCurrency)
        setData((current) => ({
          ...current,
          portfolios: [...current.portfolios, created],
          activePortfolioId: created.id,
        }))
        return created.id
      },

      renamePortfolio: (id, name) =>
        setData((current) => ({
          ...current,
          portfolios: current.portfolios.map((p) =>
            p.id === id ? { ...p, name: name.trim() || p.name } : p,
          ),
        })),

      setPortfolioCurrency: (id, currency) =>
        setData((current) => ({
          ...current,
          portfolios: current.portfolios.map((p) =>
            p.id === id ? { ...p, baseCurrency: currency.toUpperCase().slice(0, 3) } : p,
          ),
        })),

      deletePortfolio: (id) =>
        setData((current) => {
          // Never leave the app with no portfolio at all.
          if (current.portfolios.length <= 1) {
            const replacement = createEmptyPortfolio('My portfolio')
            return { ...current, portfolios: [replacement], activePortfolioId: replacement.id }
          }
          const portfolios = current.portfolios.filter((p) => p.id !== id)
          return {
            ...current,
            portfolios,
            activePortfolioId:
              current.activePortfolioId === id ? portfolios[0].id : current.activePortfolioId,
          }
        }),

      addPosition: (input) => {
        const symbol = input.symbol.trim().toUpperCase()
        editActive((current) => {
          const existing = current.positions.find((p) => p.symbol === symbol)
          const lot: Lot = {
            id: newId('lot'),
            shares: input.shares,
            price: input.price,
            date: input.date || undefined,
          }
          // Buying more of something already held adds a lot rather than a
          // duplicate row, so the average cost stays correct automatically.
          if (existing) {
            return {
              ...current,
              positions: current.positions.map((p) =>
                p.id === existing.id
                  ? { ...p, lots: [...p.lots, lot], name: p.name || input.name, notes: input.notes ?? p.notes }
                  : p,
              ),
            }
          }
          const position: Position = {
            id: newId('pos'),
            symbol,
            name: input.name,
            lots: [lot],
            colorSlot: lowestFreeSlot(new Set(current.positions.map((entry) => entry.colorSlot))),
            notes: input.notes,
            createdAt: new Date().toISOString(),
          }
          return { ...current, positions: [...current.positions, position] }
        })
      },

      savePosition: (positionId, patch) =>
        editActive((current) => ({
          ...current,
          positions: current.positions.map((p) =>
            p.id === positionId
              ? {
                  ...p,
                  symbol: patch.symbol.trim().toUpperCase() || p.symbol,
                  name: patch.name,
                  lots: patch.lots,
                  notes: patch.notes,
                }
              : p,
          ),
        })),

      removePosition: (positionId) =>
        editActive((current) => ({
          ...current,
          positions: current.positions.filter((p) => p.id !== positionId),
        })),

      updateSettings: (patch) =>
        setData((current) => ({ ...current, settings: { ...current.settings, ...patch } })),

      replaceAll: (next) => setData(next),

      startFresh: (name) => {
        const replacement = createEmptyPortfolio(name.trim() || 'My portfolio')
        setData((current) => ({
          version: 1,
          portfolios: [replacement],
          activePortfolioId: replacement.id,
          settings: current.settings,
        }))
      },
    }
  }, [data, toasts, toast, dismissToast, editActive])

  return <StoreContext.Provider value={value}>{children}</StoreContext.Provider>
}

export function useStore(): StoreValue {
  const value = useContext(StoreContext)
  if (!value) throw new Error('useStore must be used inside <StoreProvider>')
  return value
}

export { STORAGE_KEY }
