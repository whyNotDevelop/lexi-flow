// ============================================
// LexiFlow Mobile - Utilities Exports
// ============================================

export * from './wordDetection'
export * from './dateFormatting'

/**
 * Classname utility for NativeWind
 * Combines class names conditionally
 */
export function cn(...classes: (string | undefined | null | false)[]): string {
  return classes.filter(Boolean).join(' ')
}
