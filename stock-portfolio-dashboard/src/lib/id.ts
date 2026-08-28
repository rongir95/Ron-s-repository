/** Short, collision-resistant ids that survive JSON round-trips. */
export function newId(prefix = ''): string {
  const random =
    typeof crypto !== 'undefined' && 'randomUUID' in crypto
      ? crypto.randomUUID().replace(/-/g, '').slice(0, 12)
      : Math.random().toString(36).slice(2, 10) + Date.now().toString(36).slice(-4)
  return prefix ? `${prefix}_${random}` : random
}
