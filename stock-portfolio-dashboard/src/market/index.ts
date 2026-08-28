import type { ProviderId, Settings } from '../types'
import { demoProvider } from './providers/demo'
import { createTwelveDataProvider } from './providers/twelvedata'
import { yahooProvider, yahooRelayProvider } from './providers/yahoo'
import type { MarketDataProvider } from './types'

export const PROVIDER_CHOICES: Array<{ id: ProviderId; label: string; blurb: string }> = [
  {
    id: 'yahoo',
    label: 'Yahoo Finance',
    blurb:
      'Default. No API key or sign-up. Needs the app served with its /yf proxy — that means npm run dev, npm run preview, or a Vercel/Netlify deploy.',
  },
  {
    id: 'yahoo-relay',
    label: 'Yahoo Finance via a public relay',
    blurb:
      'The same Yahoo prices with no API key and no deploy — works from a plain static host or a file opened straight from disk. Requests are relayed by a free third-party service (only ticker symbols are sent), so availability is best-effort.',
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
    case 'yahoo-relay':
      return yahooRelayProvider
    case 'demo':
      return demoProvider
    case 'yahoo':
    default:
      return yahooProvider
  }
}

export * from './types'
