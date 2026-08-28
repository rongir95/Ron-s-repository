/**
 * First-run sample data, so the dashboard has something to show before any real
 * holdings are entered. Sample portfolios carry `sample: true`; the flag is
 * dropped the moment a portfolio is edited, and Settings → "Start fresh"
 * removes them entirely.
 */
import type { AppData, Portfolio, ProviderId } from '../types'

/**
 * Which provider a fresh install starts on. Yahoo Finance everywhere except the
 * standalone single-file build, which has no /yf proxy to reach it through and
 * so ships defaulted to offline demo prices. Settings overrides this at any time.
 */
function defaultProvider(): ProviderId {
  const configured = import.meta.env.VITE_DEFAULT_PROVIDER
  return configured === 'demo' || configured === 'twelvedata' ? configured : 'yahoo'
}

export const DEFAULT_SETTINGS: AppData['settings'] = {
  providerId: defaultProvider(),
  twelveDataKey: '',
  theme: 'system',
  refreshSeconds: 60,
  privacyMode: false,
}

function daysAgo(days: number): string {
  return new Date(Date.now() - days * 86_400_000).toISOString().slice(0, 10)
}

const samplePortfolios: Portfolio[] = [
  {
    id: 'sample-mine',
    name: 'My portfolio',
    baseCurrency: 'USD',
    cash: 1850,
    realisedPl: 0,
    sample: true,
    createdAt: new Date().toISOString(),
    positions: [
      {
        id: 'sample-aapl',
        symbol: 'AAPL',
        name: 'Apple Inc.',
        colorSlot: 0,
        createdAt: new Date().toISOString(),
        lots: [
          { id: 'sample-aapl-1', shares: 12, price: 171.4, date: daysAgo(420) },
          // A second buy at a different price — the average cost is share-weighted.
          { id: 'sample-aapl-2', shares: 6, price: 205.1, date: daysAgo(95) },
        ],
      },
      {
        id: 'sample-msft',
        symbol: 'MSFT',
        name: 'Microsoft Corporation',
        colorSlot: 1,
        createdAt: new Date().toISOString(),
        lots: [{ id: 'sample-msft-1', shares: 8, price: 352.9, date: daysAgo(300) }],
      },
      {
        id: 'sample-nvda',
        symbol: 'NVDA',
        name: 'NVIDIA Corporation',
        colorSlot: 2,
        createdAt: new Date().toISOString(),
        lots: [{ id: 'sample-nvda-1', shares: 40, price: 62.5, date: daysAgo(240) }],
      },
      {
        id: 'sample-voo',
        symbol: 'VOO',
        name: 'Vanguard S&P 500 ETF',
        colorSlot: 3,
        createdAt: new Date().toISOString(),
        lots: [{ id: 'sample-voo-1', shares: 9, price: 468.2, date: daysAgo(150) }],
      },
      {
        id: 'sample-nke',
        symbol: 'NKE',
        name: 'NIKE, Inc.',
        colorSlot: 4,
        createdAt: new Date().toISOString(),
        lots: [{ id: 'sample-nke-1', shares: 25, price: 98.75, date: daysAgo(200) }],
      },
    ],
  },
  {
    id: 'sample-brother',
    name: "Younger brother",
    baseCurrency: 'USD',
    cash: 420,
    realisedPl: 0,
    sample: true,
    createdAt: new Date().toISOString(),
    positions: [
      {
        id: 'sample-b-googl',
        symbol: 'GOOGL',
        name: 'Alphabet Inc.',
        colorSlot: 0,
        createdAt: new Date().toISOString(),
        lots: [{ id: 'sample-b-googl-1', shares: 10, price: 142.6, date: daysAgo(260) }],
      },
      {
        id: 'sample-b-qqq',
        symbol: 'QQQ',
        name: 'Invesco QQQ Trust',
        colorSlot: 1,
        createdAt: new Date().toISOString(),
        lots: [{ id: 'sample-b-qqq-1', shares: 6, price: 402.4, date: daysAgo(180) }],
      },
      {
        id: 'sample-b-dis',
        symbol: 'DIS',
        name: 'The Walt Disney Company',
        colorSlot: 2,
        createdAt: new Date().toISOString(),
        lots: [{ id: 'sample-b-dis-1', shares: 15, price: 104.3, date: daysAgo(120) }],
      },
    ],
  },
]

export function createSeedData(): AppData {
  return {
    version: 1,
    portfolios: samplePortfolios,
    activePortfolioId: samplePortfolios[0].id,
    settings: { ...DEFAULT_SETTINGS },
  }
}

export function createEmptyPortfolio(name: string, baseCurrency = 'USD'): Portfolio {
  return {
    id: `pf_${Math.random().toString(36).slice(2, 10)}`,
    name,
    baseCurrency,
    positions: [],
    cash: 0,
    realisedPl: 0,
    createdAt: new Date().toISOString(),
  }
}
