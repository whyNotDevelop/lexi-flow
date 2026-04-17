// ============================================
// LexiFlow Mobile - Word Lookup Hook
// Uses the generated lexiflow-api-client
// ============================================

import { useState, useCallback } from 'react'
import useSWR from 'swr'
import { words, vocabulary } from '@/api/compat'
import type { Word } from '../api'

interface WordWithSavedStatus extends Word {
  is_saved?: boolean
}

/**
 * Hook for looking up word definitions
 * Uses SWR for caching and deduplication
 *
 * API: GET /api/words/lookup/{word}/
 */
export function useWordLookup(word: string | null) {
  const [isSaving, setIsSaving] = useState(false)
  const key = word ? `/api/words/lookup/${word.toLowerCase()}` : null

  // Fetch word definition with SWR
  const { data, error, isLoading, mutate } = useSWR<WordWithSavedStatus | null>(
    key,
    async (_key: string | null) => {
      const wordData = await words.lookup(word!)

      // Check if word is saved in vocabulary
      let is_saved = false
      if (wordData?.id) {
        try {
          const savedCheck = await vocabulary.isSaved(wordData.id)
          is_saved = (savedCheck as { is_saved?: boolean })?.is_saved ?? false
        } catch {
          // Ignore - assume not saved
        }
      }

      return { ...wordData, is_saved }
    },
    {
      revalidateOnFocus: false,
      dedupingInterval: 60000, // Cache for 1 minute
    }
  )

  // Mark word as saved (updates local cache)
  const markAsSaved = useCallback(() => {
    if (data) {
      mutate({ ...data, is_saved: true }, false)
    }
  }, [data, mutate])

  // Mark word as unsaved
  const markAsUnsaved = useCallback(() => {
    if (data) {
      mutate({ ...data, is_saved: false }, false)
    }
  }, [data, mutate])

  return {
    definition: data ?? null,
    isLoading,
    error: error as { code: string; message: string } | null,
    notFound: error?.response?.status === 404,
    isSaved: data?.is_saved ?? false,
    isSaving,
    setIsSaving,
    markAsSaved,
    markAsUnsaved,
    refetch: mutate,
  }
}

export default useWordLookup
