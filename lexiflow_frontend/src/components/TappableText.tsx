// ============================================
// LexiFlow Mobile - Tappable Text Component
// ============================================

import React, { useMemo } from 'react'
import { Text, View } from 'react-native'
import { splitTextIntoSegments, isDefinableWord } from '@/utils/wordDetection'
import { usePreferencesStore } from '@/store/preferencesStore'

interface TappableTextProps {
  text: string
  definableWords?: string[]
  selectedWord?: string | null
  onWordPress: (word: string) => void
}

/**
 * Renders text with tappable words
 * Underlines words that have definitions available
 */
export function TappableText({
  text,
  definableWords = [],
  selectedWord,
  onWordPress,
}: TappableTextProps) {
  const isDarkMode = usePreferencesStore((state) => state.is_dark_mode)
  const lineHeight = usePreferencesStore((state) => state.reading_line_height)
  const fontSize = usePreferencesStore((state) => state.font_size)

  // Get font size based on preference
  const getFontSize = () => {
    switch (fontSize) {
      case 'small':
        return 14
      case 'large':
        return 18
      default:
        return 16
    }
  }

  // Parse text into segments
  const segments = useMemo(() => splitTextIntoSegments(text), [text])

  // Dynamic styles
  const textColor = isDarkMode ? '#f5f4f2' : '#1a1918'
  const highlightColor = '#0d9488'
  const selectedBg = isDarkMode ? 'rgba(13, 148, 136, 0.2)' : 'rgba(13, 148, 136, 0.15)'

  return (
    <Text
      style={{
        fontSize: getFontSize(),
        lineHeight: getFontSize() * lineHeight,
        color: textColor,
      }}
    >
      {segments.map((segment, index) => {
        const isDefinable =
          segment.isWord &&
          segment.cleanedWord &&
          (definableWords.length === 0 || isDefinableWord(segment.text, definableWords))

        const isSelected =
          segment.cleanedWord &&
          selectedWord?.toLowerCase() === segment.cleanedWord.toLowerCase()

        if (isDefinable && segment.cleanedWord) {
          return (
            <Text
              key={index}
              onPress={() => onWordPress(segment.cleanedWord!)}
              style={{
                textDecorationLine: 'underline',
                textDecorationColor: highlightColor,
                textDecorationStyle: 'dotted',
                backgroundColor: isSelected ? selectedBg : 'transparent',
                color: isSelected ? highlightColor : textColor,
              }}
            >
              {segment.text}
            </Text>
          )
        }

        return <Text key={index}>{segment.text}</Text>
      })}
    </Text>
  )
}

export default TappableText
