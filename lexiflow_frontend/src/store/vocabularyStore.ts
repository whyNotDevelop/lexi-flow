// ============================================
// LexiFlow Mobile - Vocabulary Store (Zustand)
// Uses the generated lexiflow-api-client
// ============================================

import { create } from 'zustand'
import { vocabulary } from '@/api/compat'
import type { VocabularyEntry } from 'lexiflow-api-client'

interface VocabularyState {
  // State
  words: VocabularyEntry[]
  isLoading: boolean
  isRefreshing: boolean
  searchQuery: string
  error: string | null

  // Actions
  fetchWords: () => Promise<void>
  refreshWords: () => Promise<void>
  searchWords: () => Promise<void>
  saveWord: (wordId: string) => Promise<VocabularyEntry>
  removeWord: (wordId: string) => Promise<void>
  checkIfSaved: (wordId: string) => Promise<boolean>
  setSearchQuery: (query: string) => void
  isWordSaved: (wordId: string) => boolean
  clearError: () => void
}

export const useVocabularyStore = create<VocabularyState>((set, get) => ({
  // Initial state
  words: [],
  isLoading: false,
  isRefreshing: false,
  searchQuery: '',
  error: null,

  // Fetch all words from API
  // GET /api/vocabulary/list/
  fetchWords: async () => {
    set({ isLoading: true, error: null })
    try {
      const words = await vocabulary.getAll()
      set({
        words,
        isLoading: false,
      })
    } catch (error: unknown) {
      const message = error instanceof Error ? error.message : 'Failed to load vocabulary'
      set({ error: message, isLoading: false })
    }
  },

  // Refresh words (pull-to-refresh)
  refreshWords: async () => {
    set({ isRefreshing: true })
    try {
      const words = await vocabulary.getAll()
      set({
        words,
        isRefreshing: false,
      })
    } catch (error: unknown) {
      const message = error instanceof Error ? error.message : 'Failed to refresh vocabulary'
      set({ error: message, isRefreshing: false })
    }
  },

  // Search vocabulary
  // GET /api/vocabulary/search/
  searchWords: async () => {
    set({ isLoading: true, error: null })
    try {
      const words = await vocabulary.search()
      set({
        words,
        isLoading: false,
      })
    } catch (error: unknown) {
      const message = error instanceof Error ? error.message : 'Failed to search vocabulary'
      set({ error: message, isLoading: false })
    }
  },

  // Save a word to vocabulary
  // POST /api/vocabulary/save/{word_id}/
  saveWord: async (wordId: string) => {
    try {
      const savedWord = await vocabulary.save(wordId)
      set((state) => ({
        words: [savedWord, ...state.words],
      }))
      return savedWord
    } catch (error: unknown) {
      const message = error instanceof Error ? error.message : 'Failed to save word'
      set({ error: message })
      throw error
    }
  },

  // Remove a word from vocabulary
  // DELETE /api/vocabulary/remove/{word_id}/
  removeWord: async (wordId: string) => {
    const previousWords = get().words
    // Optimistic update
    set((state) => ({
      words: state.words.filter((w) => w.word_id !== wordId),
    }))
    try {
      await vocabulary.remove(wordId)
    } catch (error: unknown) {
      // Revert on error
      set({ words: previousWords })
      const message = error instanceof Error ? error.message : 'Failed to remove word'
      set({ error: message })
      throw error
    }
  },

  // Check if a word is saved
  // GET /api/vocabulary/is-saved/{word_id}/
  checkIfSaved: async (wordId: string) => {
    try {
      const response = await vocabulary.isSaved(wordId)
      return response?.is_saved ?? false
    } catch {
      return false
    }
  },

  // Set search query
  setSearchQuery: (query: string) => {
    set({ searchQuery: query })
  },

  // Check if a word is saved (local check)
  isWordSaved: (wordId: string) => {
    return get().words.some((w) => w.word_id === wordId)
  },

  // Clear error
  clearError: () => {
    set({ error: null })
  },
}))

export default useVocabularyStore
