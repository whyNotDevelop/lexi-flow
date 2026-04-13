// ============================================
// LexiFlow Mobile - History Hook
// Uses the generated lexiflow-api-client
// ============================================

import { useState, useCallback, useMemo } from 'react'
import useSWR from 'swr'
import { history, analytics } from '@/api/compat'
import { isToday, isThisWeek } from '@/utils/dateFormatting'

interface HistoryItem {
  id: string
  word_id: string
  word: string
  looked_up_at: string
  is_saved: boolean
}

/**
 * Hook for lookup history management
 *
 * API Endpoints:
 * - GET /api/history/list/?since={datetime}
 * - GET /api/history/count/
 * - DELETE /api/history/clear/
 * - GET /api/analytics/lookups/
 */
export function useHistory() {
  const [items, setItems] = useState<HistoryItem[]>([])

  // Get date from 30 days ago for the since parameter
  const sinceDate = useMemo(() => {
    const date = new Date()
    date.setDate(date.getDate() - 30)
    return date.toISOString()
  }, [])

  // Fetch history with SWR
  const { error, isLoading, mutate } = useSWR(
    `/api/history/list?since=${sinceDate}`,
    async () => {
      // The API returns { count: number } according to OpenAPI spec
      // History list endpoint may return items differently
      const response = await history.getList(sinceDate)
      return response
    },
    {
      revalidateOnFocus: true,
      dedupingInterval: 5000,
      onSuccess: (data) => {
        // If the API returns items array, update local state
        if (Array.isArray(data)) {
          setItems(data)
        }
      },
    }
  )

  // Fetch lookup stats
  const { data: lookupStats } = useSWR('/api/analytics/lookups/', () => analytics.getLookupStats())

  // Stats computed from local items and API
  const stats = useMemo(() => {
    const today = items.filter((item) => isToday(item.looked_up_at)).length
    const thisWeek = items.filter((item) => isThisWeek(item.looked_up_at)).length
    const total = (lookupStats as { total?: number })?.total ?? items.length

    return {
      today,
      thisWeek,
      total,
    }
  }, [items, lookupStats])

  // Refresh history
  const refresh = useCallback(() => {
    setItems([])
    mutate()
  }, [mutate])

  // Clear all history (DELETE /api/history/clear/)
  const clearAll = useCallback(async () => {
    try {
      await history.clear()
      setItems([])
      mutate()
    } catch {
      throw new Error('Failed to clear history')
    }
  }, [mutate])

  // Mark item as saved (local update)
  const markAsSaved = useCallback((id: string) => {
    setItems((prevItems) =>
      prevItems.map((item) => (item.id === id ? { ...item, is_saved: true } : item))
    )
  }, [])

  return {
    items,
    stats,
    isLoading,
    error,
    refresh,
    clearAll,
    markAsSaved,
  }
}

export default useHistory
