// ============================================
// LexiFlow Mobile - Vocabulary Hook
// Uses the generated lexiflow-api-client
// ============================================

import { useCallback, useEffect, useMemo } from 'react'
import { useVocabularyStore } from '@/store/vocabularyStore'

/**
 * Hook for vocabulary management
 * Provides filtered words and CRUD operations
 *
 * API Endpoints:
 * - GET /api/vocabulary/list/
 * - GET /api/vocabulary/search/
 * - POST /api/vocabulary/save/{word_id}/
 * - DELETE /api/vocabulary/remove/{word_id}/
 * - GET /api/vocabulary/is-saved/{word_id}/
 */
export function useVocabulary() {
  const {
    words,
    isLoading,
    isRefreshing,
    searchQuery,
    error,
    fetchWords,
    refreshWords,
    saveWord: storeSaveWord,
    removeWord: storeRemoveWord,
    setSearchQuery,
    isWordSaved,
    clearError,
  } = useVocabularyStore()

  // Fetch words on mount
  useEffect(() => {
    fetchWords()
  }, [fetchWords])

  // Filter words based on search query (client-side for immediate feedback)
  const filteredWords = useMemo(() => {
    if (!searchQuery) return words
    const query = searchQuery.toLowerCase()
    return words.filter(
      (w) =>
        w.word_text.toLowerCase().includes(query) || w.meaning.toLowerCase().includes(query)
    )
  }, [words, searchQuery])

  // Save a word (POST /api/vocabulary/save/{word_id}/)
  const saveWord = useCallback(
    async (wordId: string) => {
      return await storeSaveWord(wordId)
    },
    [storeSaveWord]
  )

  // Remove a word (DELETE /api/vocabulary/remove/{word_id}/)
  const removeWord = useCallback(
    async (wordId: string) => {
      await storeRemoveWord(wordId)
    },
    [storeRemoveWord]
  )

  // Stats
  const stats = useMemo(() => {
    const now = new Date()
    const weekAgo = new Date(now.getTime() - 7 * 24 * 60 * 60 * 1000)

    const thisWeek = words.filter((w) => new Date(w.saved_at) >= weekAgo).length

    return {
      thisWeek,
      total: words.length,
    }
  }, [words])

  return {
    words: filteredWords,
    allWords: words,
    totalCount: words.length,
    isLoading,
    isRefreshing,
    searchQuery,
    error,
    stats,
    setSearchQuery,
    saveWord,
    removeWord,
    refresh: refreshWords,
    isWordSaved,
    clearError,
  }
}

export default useVocabulary
