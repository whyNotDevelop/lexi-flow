// ============================================
// LexiFlow Mobile - Reading Screen
// ============================================

import React, { useState, useRef, useCallback } from 'react'
import { View, Text, ScrollView, TouchableOpacity } from 'react-native'
import { SafeAreaView } from 'react-native-safe-area-context'
import { GestureHandlerRootView } from 'react-native-gesture-handler'

import { TappableText } from '@/components/TappableText'
import { WordDefinitionSheet, WordDefinitionSheetRef } from '@/components/WordDefinitionSheet'
import { usePreferencesStore } from '@/store/preferencesStore'
import { ChevronLeftIcon, SunIcon, MoonIcon } from '@/components/icons'

// Sample reading content
const SAMPLE_TEXT = `The afternoon sun cast long shadows across the garden as Elena walked slowly between the rows of flowers. She had always found a peculiar sense of tranquility in this secluded corner of the estate, where the ephemeral beauty of nature seemed to exist in harmonious contrast with the permanence of the old stone walls.

Her grandmother had been serendipitous in discovering this property decades ago, stumbling upon it during a provincial journey through the countryside. The verdant landscape had captivated her immediately, its bucolic charm reminiscent of paintings she had admired in distant museums.

Elena paused beside a cluster of resplendent roses, their crimson petals still damp with morning dew. The mellifluous song of a nightingale drifted from somewhere in the adjacent woodland, adding another layer to the symphony of natural sounds that filled this sanctuary.

She contemplated the transient nature of moments like these—how quickly they pass, how precious they become in memory. The ineffable feeling of peace that washed over her was something she yearned to preserve, though she knew such attempts were ultimately futile.

As the sun began its inexorable descent toward the horizon, Elena made her way back toward the house, carrying with her the contemplative mood that this sacred space always seemed to evoke.`

// Words that should be definable (in a real app, this might come from an API)
const DEFINABLE_WORDS = [
  'peculiar',
  'tranquility',
  'secluded',
  'ephemeral',
  'harmonious',
  'permanence',
  'serendipitous',
  'provincial',
  'verdant',
  'captivated',
  'bucolic',
  'reminiscent',
  'resplendent',
  'crimson',
  'mellifluous',
  'adjacent',
  'symphony',
  'sanctuary',
  'contemplated',
  'transient',
  'ineffable',
  'yearned',
  'futile',
  'inexorable',
  'contemplative',
  'evoke',
]

export default function ReadingScreen() {
  const [selectedWord, setSelectedWord] = useState<string | null>(null)
  const sheetRef = useRef<WordDefinitionSheetRef>(null)

  const isDarkMode = usePreferencesStore((state) => state.is_dark_mode)
  const toggleDarkMode = usePreferencesStore((state) => state.toggleDarkMode)

  // Handle word tap
  const handleWordPress = useCallback((word: string) => {
    setSelectedWord(word)
    sheetRef.current?.open()
  }, [])

  // Handle sheet close
  const handleSheetClose = useCallback(() => {
    setSelectedWord(null)
  }, [])

  // Dynamic styles
  const bgColor = isDarkMode ? 'bg-[#1a1918]' : 'bg-[#faf9f7]'
  const cardBg = isDarkMode ? 'bg-[#262524]' : 'bg-white'
  const textColor = isDarkMode ? 'text-[#f5f4f2]' : 'text-[#1a1918]'
  const mutedText = isDarkMode ? 'text-[#78746d]' : 'text-[#78746d]'
  const borderColor = isDarkMode ? 'border-[#3d3b38]' : 'border-[#e0ded9]'
  const iconColor = isDarkMode ? '#f5f4f2' : '#1a1918'

  return (
    <GestureHandlerRootView style={{ flex: 1 }}>
      <SafeAreaView className={`flex-1 ${bgColor}`}>
        {/* Header */}
        <View
          className={`flex-row items-center justify-between px-4 py-3 border-b ${borderColor}`}
        >
          <TouchableOpacity className="w-10 h-10 items-center justify-center">
            <ChevronLeftIcon size={24} color={iconColor} />
          </TouchableOpacity>

          <View className="flex-1 items-center">
            <Text className={`font-semibold ${textColor}`}>The Silent Garden</Text>
            <Text className={`text-xs ${mutedText}`}>Chapter 1</Text>
          </View>

          <TouchableOpacity
            onPress={toggleDarkMode}
            className="w-10 h-10 items-center justify-center"
          >
            {isDarkMode ? (
              <SunIcon size={20} color={iconColor} />
            ) : (
              <MoonIcon size={20} color={iconColor} />
            )}
          </TouchableOpacity>
        </View>

        {/* Reading Content */}
        <ScrollView
          className="flex-1 px-5 py-6"
          showsVerticalScrollIndicator={false}
        >
          <TappableText
            text={SAMPLE_TEXT}
            definableWords={DEFINABLE_WORDS}
            selectedWord={selectedWord}
            onWordPress={handleWordPress}
          />

          {/* Reading hint */}
          <View
            className={`mt-8 p-4 rounded-xl border ${borderColor}`}
            style={{ backgroundColor: isDarkMode ? '#262524' : '#f0eeeb' }}
          >
            <Text className={`text-xs text-center ${mutedText}`}>
              Tap on any underlined word to see its definition
            </Text>
          </View>

          {/* Bottom padding for scroll */}
          <View className="h-20" />
        </ScrollView>

        {/* Word Definition Bottom Sheet */}
        <WordDefinitionSheet
          ref={sheetRef}
          word={selectedWord}
          onClose={handleSheetClose}
        />
      </SafeAreaView>
    </GestureHandlerRootView>
  )
}
