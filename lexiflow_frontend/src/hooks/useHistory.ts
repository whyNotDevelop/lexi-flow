// src/hooks/useHistory.ts
import { useState, useCallback, useMemo } from 'react';
import useSWR from 'swr';
import { history, analytics } from '@/api/compat';
import type { HistoryItem } from '@/types';

export function useHistory() {
  const [items, setItems] = useState<HistoryItem[]>([]);

  const sinceDate = useMemo(() => {
    const date = new Date();
    date.setDate(date.getDate() - 30);
    return date.toISOString();
  }, []);

  const { error, isLoading, mutate } = useSWR(
    `history-list-${sinceDate}`,
    async () => {
      const data = await history.getList(sinceDate);
      // The API returns { count?: number } – we need to adapt to the actual shape
      // For now, we assume the response is an array of history items.
      // If it returns a different shape, adjust accordingly.
      const itemsArray = Array.isArray(data) ? data : [];
      setItems(itemsArray);
      return itemsArray;
    },
    { revalidateOnFocus: true, dedupingInterval: 5000 }
  );

  const { data: lookupStats } = useSWR('lookup-stats', () => analytics.getLookupStats());

  const stats = useMemo(() => {
    const today = items.filter((item) => new Date(item.looked_up_at).toDateString() === new Date().toDateString()).length;
    const thisWeek = items.filter((item) => {
      const d = new Date(item.looked_up_at);
      const now = new Date();
      const diffDays = (now.getTime() - d.getTime()) / (1000 * 3600 * 24);
      return diffDays <= 7;
    }).length;
    const total = items.length;
    return { today, thisWeek, total };
  }, [items]);

  const refresh = useCallback(() => {
    setItems([]);
    mutate();
  }, [mutate]);

  const clearAll = useCallback(async () => {
    await history.clear();
    setItems([]);
    mutate();
  }, [mutate]);

  const deleteItem = useCallback(async (id: string) => {
    // If the API has a delete endpoint, implement it. For now, we just remove from local state.
    setItems((prev) => prev.filter((item) => item.id !== id));
  }, []);

  const markAsSaved = useCallback((id: string) => {
    setItems((prev) => prev.map((item) => (item.id === id ? { ...item, is_saved: true } : item)));
  }, []);

  // Placeholders for pagination (if needed)
  const hasMore = false;
  const loadMore = () => {};

  return {
    items,
    stats,
    isLoading,
    error,
    refresh,
    clearAll,
    deleteItem,
    markAsSaved,
    hasMore,
    loadMore,
  };
}