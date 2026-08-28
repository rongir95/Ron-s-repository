import { useEffect, useState } from 'react'
import type { Settings } from '../types'

export type ResolvedTheme = 'light' | 'dark'

const QUERY = '(prefers-color-scheme: dark)'

function systemPrefersDark(): boolean {
  return typeof window !== 'undefined' && !!window.matchMedia && window.matchMedia(QUERY).matches
}

/**
 * The theme actually on screen right now.
 *
 * With the setting on "system" this follows the OS and keeps following it — the
 * listener matters because the header's toggle shows the theme you would switch
 * *to*, and that icon has to flip when the OS flips underneath us.
 */
export function useResolvedTheme(setting: Settings['theme']): ResolvedTheme {
  const [prefersDark, setPrefersDark] = useState(systemPrefersDark)

  useEffect(() => {
    if (typeof window === 'undefined' || !window.matchMedia) return
    const media = window.matchMedia(QUERY)
    const onChange = (event: MediaQueryListEvent) => setPrefersDark(event.matches)
    media.addEventListener('change', onChange)
    // Re-read on mount in case the OS changed before the listener attached.
    setPrefersDark(media.matches)
    return () => media.removeEventListener('change', onChange)
  }, [])

  if (setting === 'light' || setting === 'dark') return setting
  return prefersDark ? 'dark' : 'light'
}
