// src/hooks/useVocabulary.ts
import { useCallback, useEffect, useMemo } from 'react';
import { useVocabularyStore } from '@/store/vocabularyStore';

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
  } = useVocabularyStore();

  useEffect(() => {
    fetchWords();
  }, [fetchWords]);

  const filteredWords = useMemo(() => {
    if (!searchQuery) return words;
    const query = searchQuery.toLowerCase();
    return words.filter((w: { word_text: string; meaning: string; }) => w.word_text.toLowerCase().includes(query) || w.meaning.toLowerCase().includes(query));
  }, [words, searchQuery]);

  const saveWord = useCallback(async (wordId: string) => {
    return await storeSaveWord(wordId);
  }, [storeSaveWord]);

  const removeWord = useCallback(async (wordId: string) => {
    await storeRemoveWord(wordId);
  }, [storeRemoveWord]);

  const stats = useMemo(() => {
    const now = new Date();
    const weekAgo = new Date(now.getTime() - 7 * 24 * 60 * 60 * 1000);
    const thisWeek = words.filter((w: { saved_at: string | number | Date; }) => new Date(w.saved_at) >= weekAgo).length;
    return { thisWeek, total: words.length };
  }, [words]);

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
    loadMore: () => {},      // placeholder
    hasMore: false,          // placeholder
  };
}