import type { ProviderId, Settings } from '../types'
import { demoProvider } from './providers/demo'
import { createTwelveDataProvider } from './providers/twelvedata'
import { yahooProvider } from './providers/yahoo'
import type { MarketDataProvider } from './types'

export const PROVIDER_CHOICES: Array<{ id: ProviderId; label: string; blurb: string }> = [
  {
    id: 'yahoo',
    label: 'Yahoo Finance',
    blurb:
      'Default. No API key or sign-up. Needs the app served with its /yf proxy — that means npm run dev, npm run preview, or a Vercel/Netlify deploy.',
  },
  {
    id: 'twelvedata',
    label: 'Twelve Data',
    blurb:
      'Works from any static host (no proxy needed) with a free API key. Free tier: 8 requests/min, 800/day.',
  },
  {
    id: 'demo',
    label: 'Demo data (offline)',
    blurb: 'Synthetic prices generated locally. Use it to try the dashboard out without any network access.',
  },
]

export function getProvider(settings: Settings): MarketDataProvider {
  switch (settings.providerId) {
    case 'twelvedata':
      return createTwelveDataProvider(settings.twelveDataKey)
    case 'demo':
      return demoProvider
    case 'yahoo':
    default:
      return yahooProvider
  }
}

export * from './types'
