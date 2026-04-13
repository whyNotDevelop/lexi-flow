// ============================================
// LexiFlow Mobile - History Screen
// ============================================

import React, { useCallback, useState } from 'react'
import {
  View,
  Text,
  FlatList,
  TouchableOpacity,
  RefreshControl,
  ActivityIndicator,
  Alert,
} from 'react-native'
import { SafeAreaView } from 'react-native-safe-area-context'

import { useHistory } from '@/hooks/useHistory'
import { useVocabulary } from '@/hooks/useVocabulary'
import { usePreferencesStore } from '@/store/preferencesStore'
import { formatRelativeTime } from '@/utils/dateFormatting'
import { HistoryItem } from '@/types'
import {
  TrashIcon,
  BookmarkIcon,
  BookmarkFilledIcon,
  ClockIcon,
} from '@/components/icons'

export default function HistoryScreen() {
  const {
    items,
    stats,
    isLoading,
    hasMore,
    loadMore,
    refresh,
    deleteItem,
    clearAll,
    markAsSaved,
  } = useHistory()

  const { saveWord, isWordSaved } = useVocabulary()
  const isDarkMode = usePreferencesStore((state) => state.is_dark_mode)
  const [savingIds, setSavingIds] = useState<Set<string>>(new Set())

  // Handle save word
  const handleSave = useCallback(
    async (item: HistoryItem) => {
      setSavingIds((prev) => new Set(prev).add(item.id))
      try {
        await saveWord(item.word_id, item.word, '')
        markAsSaved(item.id)
      } catch {
        // Error handled by hook
      } finally {
        setSavingIds((prev) => {
          const next = new Set(prev)
          next.delete(item.id)
          return next
        })
      }
    },
    [saveWord, markAsSaved]
  )

  // Handle delete item
  const handleDelete = useCallback(
    async (id: string) => {
      try {
        await deleteItem(id)
      } catch {
        Alert.alert('Error', 'Failed to delete history item')
      }
    },
    [deleteItem]
  )

  // Handle clear all
  const handleClearAll = useCallback(() => {
    Alert.alert(
      'Clear History',
      'Are you sure you want to clear all lookup history? This cannot be undone.',
      [
        { text: 'Cancel', style: 'cancel' },
        {
          text: 'Clear All',
          style: 'destructive',
          onPress: async () => {
            try {
              await clearAll()
            } catch {
              Alert.alert('Error', 'Failed to clear history')
            }
          },
        },
      ]
    )
  }, [clearAll])

  // Dynamic styles
  const bgColor = isDarkMode ? 'bg-[#1a1918]' : 'bg-[#faf9f7]'
  const cardBg = isDarkMode ? 'bg-[#262524]' : 'bg-white'
  const textColor = isDarkMode ? 'text-[#f5f4f2]' : 'text-[#1a1918]'
  const mutedText = isDarkMode ? 'text-[#78746d]' : 'text-[#78746d]'
  const borderColor = isDarkMode ? 'border-[#3d3b38]' : 'border-[#e0ded9]'
  const iconColor = isDarkMode ? '#78746d' : '#78746d'

  // Render history item
  const renderHistoryItem = useCallback(
    ({ item }: { item: HistoryItem }) => {
      const isSaved = item.is_saved || isWordSaved(item.word)
      const isSaving = savingIds.has(item.id)

      return (
        <View
          className={`${cardBg} rounded-xl p-4 mb-3 border ${borderColor}`}
        >
          <View className="flex-row items-center justify-between">
            <View className="flex-1">
              <Text className={`font-semibold ${textColor} capitalize`}>
                {item.word}
              </Text>
              <Text className={`text-xs ${mutedText} mt-0.5`}>
                {formatRelativeTime(item.looked_up_at)}
              </Text>
            </View>
            <View className="flex-row items-center gap-2">
              <TouchableOpacity
                onPress={() => !isSaved && handleSave(item)}
                disabled={isSaved || isSaving}
                className="w-9 h-9 rounded-full items-center justify-center"
                style={{ backgroundColor: isDarkMode ? '#2e2d2b' : '#f0eeeb' }}
              >
                {isSaving ? (
                  <ActivityIndicator size="small" color="#0d9488" />
                ) : isSaved ? (
                  <BookmarkFilledIcon size={16} color="#0d9488" />
                ) : (
                  <BookmarkIcon size={16} color={iconColor} />
                )}
              </TouchableOpacity>
              <TouchableOpacity
                onPress={() => handleDelete(item.id)}
                className="w-9 h-9 rounded-full items-center justify-center"
                style={{ backgroundColor: isDarkMode ? '#2e2d2b' : '#f0eeeb' }}
              >
                <TrashIcon size={16} color={iconColor} />
              </TouchableOpacity>
            </View>
          </View>
        </View>
      )
    },
    [
      cardBg,
      borderColor,
      textColor,
      mutedText,
      iconColor,
      isDarkMode,
      isWordSaved,
      savingIds,
      handleSave,
      handleDelete,
    ]
  )

  // Render empty state
  const renderEmptyState = () => (
    <View className="flex-1 items-center justify-center py-20">
      <View
        className="w-16 h-16 rounded-2xl items-center justify-center mb-4"
        style={{ backgroundColor: isDarkMode ? '#2e2d2b' : '#f0eeeb' }}
      >
        <ClockIcon size={28} color={iconColor} />
      </View>
      <Text className={`text-lg font-semibold ${textColor}`}>
        No lookup history
      </Text>
      <Text className={`text-sm ${mutedText} mt-2 text-center px-8`}>
        Words you look up while reading will appear here
      </Text>
    </View>
  )

  // Render footer
  const renderFooter = () => {
    if (!hasMore || isLoading) return null
    return (
      <View className="py-4 items-center">
        <ActivityIndicator color="#0d9488" />
      </View>
    )
  }

  return (
    <SafeAreaView className={`flex-1 ${bgColor}`} edges={['top']}>
      {/* Header */}
      <View className="flex-row items-center justify-between px-4 py-3">
        <Text className={`text-2xl font-bold ${textColor}`}>History</Text>
        {items.length > 0 && (
          <TouchableOpacity onPress={handleClearAll}>
            <Text className="text-destructive font-medium">Clear All</Text>
          </TouchableOpacity>
        )}
      </View>

      {/* Stats Grid */}
      <View className="px-4 mb-4">
        <View
          className={`${cardBg} rounded-xl p-4 flex-row border ${borderColor}`}
        >
          <View className="flex-1 items-center">
            <Text className="text-2xl font-bold text-primary">
              {stats.today}
            </Text>
            <Text className={`text-xs ${mutedText}`}>Today</Text>
          </View>
          <View className={`w-px ${borderColor}`} />
          <View className="flex-1 items-center">
            <Text className={`text-2xl font-bold ${textColor}`}>
              {stats.thisWeek}
            </Text>
            <Text className={`text-xs ${mutedText}`}>This Week</Text>
          </View>
          <View className={`w-px ${borderColor}`} />
          <View className="flex-1 items-center">
            <Text className={`text-2xl font-bold ${textColor}`}>
              {stats.total}
            </Text>
            <Text className={`text-xs ${mutedText}`}>Total</Text>
          </View>
        </View>
      </View>

      {/* History List */}
      {isLoading && items.length === 0 ? (
        <View className="flex-1 items-center justify-center">
          <ActivityIndicator size="large" color="#0d9488" />
        </View>
      ) : (
        <FlatList
          data={items}
          keyExtractor={(item) => item.id}
          renderItem={renderHistoryItem}
          contentContainerStyle={{
            paddingHorizontal: 16,
            paddingBottom: 100,
            flexGrow: items.length === 0 ? 1 : undefined,
          }}
          ListEmptyComponent={renderEmptyState}
          ListFooterComponent={renderFooter}
          onEndReached={loadMore}
          onEndReachedThreshold={0.5}
          refreshControl={
            <RefreshControl
              refreshing={false}
              onRefresh={refresh}
              tintColor="#0d9488"
            />
          }
          showsVerticalScrollIndicator={false}
        />
      )}
    </SafeAreaView>
  )
}
