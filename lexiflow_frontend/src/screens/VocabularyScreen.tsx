// ============================================
// LexiFlow Mobile - Vocabulary Screen
// ============================================

import React, { useCallback } from 'react'
import {
  View,
  Text,
  TextInput,
  FlatList,
  TouchableOpacity,
  RefreshControl,
  ActivityIndicator,
} from 'react-native'
import { SafeAreaView } from 'react-native-safe-area-context'

import { useVocabulary } from '@/hooks/useVocabulary'
import { usePreferencesStore } from '@/store/preferencesStore'
import { formatShortDate } from '@/utils/dateFormatting'
import type { VocabularyEntry } from '../api'
import { SearchIcon, TrashIcon, BookmarkFilledIcon } from '@/components/icons'

export default function VocabularyScreen() {
  const {
    words,
    stats,
    isLoading,
    isRefreshing,
    searchQuery,
    setSearchQuery,
    removeWord,
    refresh,
    loadMore,
    hasMore,
  } = useVocabulary()

  const isDarkMode = usePreferencesStore((state) => state.is_dark_mode)

  // Handle delete word
  const handleDelete = useCallback(
    async (id: string) => {
      try {
        await removeWord(id)
      } catch {
        // Error handled by hook
      }
    },
    [removeWord]
  )

  // Dynamic styles
  const bgColor = isDarkMode ? 'bg-[#1a1918]' : 'bg-[#faf9f7]'
  const cardBg = isDarkMode ? 'bg-[#262524]' : 'bg-white'
  const textColor = isDarkMode ? 'text-[#f5f4f2]' : 'text-[#1a1918]'
  const mutedText = isDarkMode ? 'text-[#78746d]' : 'text-[#78746d]'
  const borderColor = isDarkMode ? 'border-[#3d3b38]' : 'border-[#e0ded9]'
  const inputBg = isDarkMode ? 'bg-[#2e2d2b]' : 'bg-[#f0eeeb]'
  const iconColor = isDarkMode ? '#78746d' : '#78746d'

  // Render word card (uses VocabularyEntry from generated client)
  const renderWordCard = useCallback(
    ({ item }: { item: VocabularyEntry }) => (
      <View
        className={`${cardBg} rounded-xl p-4 mb-3 border ${borderColor}`}
      >
        <View className="flex-row items-start justify-between">
          <View className="flex-1 pr-3">
            <View className="flex-row items-center gap-2 mb-1">
              <Text className={`font-semibold ${textColor} capitalize`}>
                {item.word_text}
              </Text>
              <View className="px-2 py-0.5 rounded-full bg-primary/10">
                <Text className="text-primary text-xs">
                  {formatShortDate(item.saved_at)}
                </Text>
              </View>
            </View>
            <Text
              className={`text-sm ${mutedText} leading-5`}
              numberOfLines={2}
            >
              {item.meaning}
            </Text>
          </View>
          <TouchableOpacity
            onPress={() => handleDelete(item.word_id)}
            className="w-9 h-9 rounded-full items-center justify-center"
            style={{ backgroundColor: isDarkMode ? '#2e2d2b' : '#f0eeeb' }}
          >
            <TrashIcon size={16} color={iconColor} />
          </TouchableOpacity>
        </View>
      </View>
    ),
    [cardBg, borderColor, textColor, mutedText, iconColor, isDarkMode, handleDelete]
  )

  // Render empty state
  const renderEmptyState = () => (
    <View className="flex-1 items-center justify-center py-20">
      <View
        className="w-16 h-16 rounded-2xl items-center justify-center mb-4"
        style={{ backgroundColor: isDarkMode ? '#2e2d2b' : '#f0eeeb' }}
      >
        <BookmarkFilledIcon size={28} color={iconColor} />
      </View>
      <Text className={`text-lg font-semibold ${textColor}`}>
        {searchQuery ? 'No matches found' : 'No saved words yet'}
      </Text>
      <Text className={`text-sm ${mutedText} mt-2 text-center px-8`}>
        {searchQuery
          ? `No words match "${searchQuery}"`
          : 'Tap on any word while reading to look it up and save it to your vocabulary'}
      </Text>
    </View>
  )

  // Render footer (loading more)
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
      <View className="px-4 py-3">
        <Text className={`text-2xl font-bold ${textColor}`}>Vocabulary</Text>
      </View>

      {/* Search Bar */}
      <View className="px-4 mb-4">
        <View className={`flex-row items-center ${inputBg} rounded-xl px-4 h-12`}>
          <SearchIcon size={18} color={iconColor} />
          <TextInput
            className={`flex-1 ml-3 ${textColor}`}
            placeholder="Search your vocabulary..."
            placeholderTextColor={iconColor}
            value={searchQuery}
            onChangeText={setSearchQuery}
            autoCapitalize="none"
          />
        </View>
      </View>

      {/* Stats Card */}
      <View className="px-4 mb-4">
        <View
          className={`${cardBg} rounded-xl p-4 flex-row border ${borderColor}`}
        >
          <View className="flex-1 items-center">
            <Text className="text-2xl font-bold text-primary">
              {stats.thisWeek}
            </Text>
            <Text className={`text-xs ${mutedText}`}>This Week</Text>
          </View>
          <View className={`w-px ${borderColor}`} />
          <View className="flex-1 items-center">
            <Text className={`text-2xl font-bold ${textColor}`}>
              {stats.total}
            </Text>
            <Text className={`text-xs ${mutedText}`}>Total Saved</Text>
          </View>
        </View>
      </View>

      {/* Words List */}
      {isLoading && words.length === 0 ? (
        <View className="flex-1 items-center justify-center">
          <ActivityIndicator size="large" color="#0d9488" />
        </View>
      ) : (
        <FlatList
          data={words}
          keyExtractor={(item) => item.id}
          renderItem={renderWordCard}
          contentContainerStyle={{
            paddingHorizontal: 16,
            paddingBottom: 100,
            flexGrow: words.length === 0 ? 1 : undefined,
          }}
          ListEmptyComponent={renderEmptyState}
          ListFooterComponent={renderFooter}
          onEndReached={loadMore}
          onEndReachedThreshold={0.5}
          refreshControl={
            <RefreshControl
              refreshing={isRefreshing}
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
