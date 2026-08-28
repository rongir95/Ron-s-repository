import { OTHER_SLOT } from '../store/store'

/**
 * Maps a holding's stable palette slot to its CSS custom property.
 *
 * Slots 0-7 are the eight validated categorical hues, assigned once per holding
 * and never recomputed, so a hue belongs to the entity rather than to its
 * current rank. Anything past the eighth holding shares the neutral "other"
 * grey — the palette is never cycled or extended with generated hues.
 */
export function seriesColor(slot: number): string {
  if (!Number.isInteger(slot) || slot < 0 || slot >= OTHER_SLOT) return 'var(--series-other)'
  return `var(--series-${slot + 1})`
}
