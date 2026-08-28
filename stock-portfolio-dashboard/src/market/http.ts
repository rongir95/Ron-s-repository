import { MarketDataError } from './types'

/** JSON fetch with a timeout and error messages that are safe to show a user. */
export async function fetchJson<T>(url: string, timeoutMs = 12_000): Promise<T> {
  const controller = new AbortController()
  const timer = setTimeout(() => controller.abort(), timeoutMs)
  let response: Response
  try {
    response = await fetch(url, { signal: controller.signal, headers: { accept: 'application/json' } })
  } catch (err) {
    if ((err as Error).name === 'AbortError') {
      throw new MarketDataError('The market-data request timed out.', err)
    }
    throw new MarketDataError('Could not reach the market-data service.', err)
  } finally {
    clearTimeout(timer)
  }

  if (!response.ok) {
    if (response.status === 404) {
      throw new MarketDataError(
        'Market-data proxy not found (404). The /yf proxy is only available via `npm run dev`, ' +
          '`npm run preview`, or a Vercel/Netlify deploy — on other hosts switch provider in Settings.',
      )
    }
    if (response.status === 429) {
      throw new MarketDataError('Rate limit reached. Wait a moment, or slow the refresh rate in Settings.')
    }
    if (response.status === 401 || response.status === 403) {
      throw new MarketDataError('The market-data service rejected the request — check your API key in Settings.')
    }
    throw new MarketDataError(`Market data unavailable (HTTP ${response.status}).`)
  }

  try {
    return (await response.json()) as T
  } catch (err) {
    throw new MarketDataError('The market-data service returned a malformed response.', err)
  }
}

/** Runs tasks with bounded concurrency so we never flood a rate-limited API. */
export async function mapLimit<In, Out>(
  items: In[],
  limit: number,
  worker: (item: In) => Promise<Out>,
): Promise<Out[]> {
  const results = new Array<Out>(items.length)
  let cursor = 0
  const runners = Array.from({ length: Math.min(limit, items.length) }, async () => {
    while (cursor < items.length) {
      const index = cursor++
      results[index] = await worker(items[index])
    }
  })
  await Promise.all(runners)
  return results
}
