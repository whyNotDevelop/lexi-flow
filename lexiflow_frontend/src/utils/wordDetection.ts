// ============================================
// LexiFlow Mobile - Word Detection Utility
// ============================================
// Pure utility functions for extracting words from text
// No DOM dependencies - works with React Native touch handling

/**
 * Punctuation characters to strip from words
 */
const PUNCTUATION_REGEX = /^[.,!?;:'"()\[\]{}—–-]+|[.,!?;:'"()\[\]{}—–-]+$/g

/**
 * Extract a clean word from raw text
 * Removes surrounding punctuation while preserving internal characters
 */
export function cleanWord(rawWord: string): string {
  return rawWord.replace(PUNCTUATION_REGEX, '').toLowerCase().trim()
}

/**
 * Check if a string represents a valid word (not just numbers or symbols)
 */
export function isValidWord(word: string): boolean {
  if (!word || word.length < 2) return false
  // Must contain at least one letter
  return /[a-zA-Z]/.test(word)
}

/**
 * Split text into segments (words and whitespace)
 * Each segment includes its position for touch handling
 */
export interface TextSegment {
  text: string
  startIndex: number
  endIndex: number
  isWord: boolean
  cleanedWord: string | null
}

export function splitTextIntoSegments(text: string): TextSegment[] {
  const segments: TextSegment[] = []
  const regex = /(\S+|\s+)/g
  let match: RegExpExecArray | null

  while ((match = regex.exec(text)) !== null) {
    const segment = match[0]
    const isWhitespace = /^\s+$/.test(segment)
    const cleanedWord = isWhitespace ? null : cleanWord(segment)
    const isWord = !isWhitespace && cleanedWord !== null && isValidWord(cleanedWord)

    segments.push({
      text: segment,
      startIndex: match.index,
      endIndex: match.index + segment.length,
      isWord,
      cleanedWord: isWord ? cleanedWord : null,
    })
  }

  return segments
}

/**
 * Find which word was tapped based on character index
 * Used when the component knows which character position was touched
 */
export function getWordAtIndex(text: string, charIndex: number): string | null {
  const segments = splitTextIntoSegments(text)
  const segment = segments.find(
    (s) => charIndex >= s.startIndex && charIndex < s.endIndex && s.isWord
  )
  return segment?.cleanedWord ?? null
}

/**
 * Check if a word should be highlighted as "definable"
 * Used to pre-mark words that have definitions available
 */
export function isDefinableWord(
  word: string,
  definableWords: string[]
): boolean {
  const cleaned = cleanWord(word)
  return definableWords.some(
    (dw) => dw.toLowerCase() === cleaned.toLowerCase()
  )
}

/**
 * Extract all unique words from text
 * Useful for prefetching definitions or analytics
 */
export function extractUniqueWords(text: string): string[] {
  const segments = splitTextIntoSegments(text)
  const words = segments
    .filter((s) => s.isWord && s.cleanedWord)
    .map((s) => s.cleanedWord as string)
  
  return [...new Set(words)]
}

/**
 * Get word boundaries for a specific word in text
 * Returns all occurrences of the word with their positions
 */
export interface WordBoundary {
  word: string
  start: number
  end: number
}

export function getWordBoundaries(text: string, targetWord: string): WordBoundary[] {
  const boundaries: WordBoundary[] = []
  const segments = splitTextIntoSegments(text)
  const targetCleaned = cleanWord(targetWord)

  for (const segment of segments) {
    if (segment.cleanedWord === targetCleaned) {
      boundaries.push({
        word: segment.text,
        start: segment.startIndex,
        end: segment.endIndex,
      })
    }
  }

  return boundaries
}

export default {
  cleanWord,
  isValidWord,
  splitTextIntoSegments,
  getWordAtIndex,
  isDefinableWord,
  extractUniqueWords,
  getWordBoundaries,
}
