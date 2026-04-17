// ============================================
// LexiFlow Mobile - Word Definition Bottom Sheet
// ============================================

import React, { useCallback, useMemo, useRef, forwardRef, useImperativeHandle } from 'react'
import { View, Text, TouchableOpacity, ActivityIndicator, ScrollView } from 'react-native'
import BottomSheet, { BottomSheetView, BottomSheetBackdrop } from '@gorhom/bottom-sheet'
import { useWordLookup } from '@/hooks/useWordLookup'
import { useVocabulary } from '@/hooks/useVocabulary'
import { usePreferencesStore } from '@/store/preferencesStore'
import {
  XIcon,
  VolumeIcon,
  BookmarkIcon,
  BookmarkFilledIcon,
} from '@/components/icons'

interface WordDefinitionSheetProps {
  word: string | null
  onClose: () => void
}

export interface WordDefinitionSheetRef {
  open: () => void
  close: () => void
}

export const WordDefinitionSheet = forwardRef<WordDefinitionSheetRef, WordDefinitionSheetProps>(
  ({ word, onClose }, ref) => {
    const bottomSheetRef = useRef<BottomSheet>(null)
    const isDarkMode = usePreferencesStore((state) => state.is_dark_mode)

    // Fetch word definition
    const {
      definition,
      isLoading,
      error,
      notFound,
      isSaved,
      setIsSaving,
      isSaving,
      markAsSaved,
    } = useWordLookup(word)

    // Vocabulary actions
    const { saveWord, isWordSaved } = useVocabulary()

    // Snap points for bottom sheet
    const snapPoints = useMemo(() => ['50%', '80%'], [])

    // Imperative handle for parent control
    useImperativeHandle(ref, () => ({
      open: () => bottomSheetRef.current?.snapToIndex(0),
      close: () => bottomSheetRef.current?.close(),
    }))

    // Handle save to vocabulary
    const handleSave = useCallback(async () => {
      if (!definition || isSaving) return
      setIsSaving(true)
      try {
        // Use word_id for saving (API: POST /api/vocabulary/save/{word_id}/)
        await saveWord(definition.id)
        markAsSaved()
      } catch {
        // Error handled by hook
      } finally {
        setIsSaving(false)
      }
    }, [definition, isSaving, setIsSaving, saveWord, markAsSaved])

    // Handle audio playback
    const handlePlayAudio = useCallback(() => {
      if (definition?.audio_url) {
        // Audio playback would be implemented with expo-av
        console.log('Play audio:', definition.audio_url)
      }
    }, [definition?.audio_url])

    // Render backdrop
    const renderBackdrop = useCallback(
      (props: any) => (
        <BottomSheetBackdrop
          {...props}
          disappearsOnIndex={-1}
          appearsOnIndex={0}
          opacity={0.5}
        />
      ),
      []
    )

    // Dynamic colors
    const bgColor = isDarkMode ? '#262524' : '#ffffff'
    const textColor = isDarkMode ? '#f5f4f2' : '#1a1918'
    const mutedColor = isDarkMode ? '#78746d' : '#78746d'
    const borderColor = isDarkMode ? '#3d3b38' : '#e0ded9'
    const cardBg = isDarkMode ? '#2e2d2b' : '#f0eeeb'

    // Aggregate synonyms from all returned definitions
    const synonyms = useMemo(() => {
      if (!definition?.definitions?.length) return []
      return Array.from(
        new Set(definition.definitions.flatMap((def) => def.synonyms ?? []))
      )
    }, [definition])

    // Check if word is already saved (using word_id from definition)
    const wordIsSaved = definition?.id ? isWordSaved(definition.id) || isSaved : false

    return (
      <BottomSheet
        ref={bottomSheetRef}
        index={word ? 0 : -1}
        snapPoints={snapPoints}
        enablePanDownToClose
        onClose={onClose}
        backdropComponent={renderBackdrop}
        backgroundStyle={{ backgroundColor: bgColor }}
        handleIndicatorStyle={{ backgroundColor: mutedColor }}
      >
        <BottomSheetView style={{ flex: 1, padding: 20 }}>
          {/* Header */}
          <View className="flex-row items-center justify-between mb-4">
            <View className="flex-row items-center gap-3">
              <Text
                style={{ color: textColor }}
                className="text-2xl font-bold capitalize"
              >
                {word}
              </Text>
              {definition?.audio_url && (
                <TouchableOpacity
                  onPress={handlePlayAudio}
                  className="w-8 h-8 rounded-full items-center justify-center"
                  style={{ backgroundColor: cardBg }}
                >
                  <VolumeIcon size={16} color={mutedColor} />
                </TouchableOpacity>
              )}
            </View>
            <View className="flex-row items-center gap-2">
              <TouchableOpacity
                onPress={handleSave}
                disabled={wordIsSaved || isSaving}
                className="w-10 h-10 rounded-full items-center justify-center"
                style={{ backgroundColor: cardBg }}
              >
                {isSaving ? (
                  <ActivityIndicator size="small" color="#0d9488" />
                ) : wordIsSaved ? (
                  <BookmarkFilledIcon size={20} color="#0d9488" />
                ) : (
                  <BookmarkIcon size={20} color={mutedColor} />
                )}
              </TouchableOpacity>
              <TouchableOpacity
                onPress={onClose}
                className="w-10 h-10 rounded-full items-center justify-center"
                style={{ backgroundColor: cardBg }}
              >
                <XIcon size={20} color={mutedColor} />
              </TouchableOpacity>
            </View>
          </View>

          {/* Pronunciation */}
          {definition?.phonetic && (
            <Text style={{ color: mutedColor }} className="text-sm mb-4">
              {definition.phonetic}
            </Text>
          )}

          {/* Loading State */}
          {isLoading && (
            <View className="flex-1 items-center justify-center">
              <ActivityIndicator size="large" color="#0d9488" />
              <Text style={{ color: mutedColor }} className="mt-3">
                Looking up definition...
              </Text>
            </View>
          )}

          {/* Error State */}
          {error && !isLoading && (
            <View className="flex-1 items-center justify-center">
              <Text style={{ color: textColor }} className="text-lg font-medium">
                {notFound ? 'Word not found' : 'Error loading definition'}
              </Text>
              <Text style={{ color: mutedColor }} className="mt-2 text-center">
                {notFound
                  ? `We couldn't find a definition for "${word}"`
                  : error.message}
              </Text>
            </View>
          )}

          {/* Definitions */}
          {definition && !isLoading && (
            <ScrollView showsVerticalScrollIndicator={false} className="flex-1">
              {definition.definitions.map((def, index) => (
                <View key={def.id} className="mb-5">
                  {/* Part of Speech & Number */}
                  <View className="flex-row items-center gap-2 mb-2">
                    <View
                      className="w-6 h-6 rounded-full items-center justify-center"
                      style={{ backgroundColor: '#0d9488' }}
                    >
                      <Text className="text-white text-xs font-medium">
                        {index + 1}
                      </Text>
                    </View>
                    <Text style={{ color: mutedColor }} className="text-sm italic">
                      {def.part_of_speech}
                    </Text>
                  </View>

                  {/* Meaning */}
                  <Text style={{ color: textColor }} className="text-base leading-6 mb-2">
                    {def.meaning}
                  </Text>

                  {/* Example */}
                  {def.example && (
                    <View
                      className="rounded-lg p-3 mt-2"
                      style={{ backgroundColor: cardBg }}
                    >
                      <Text style={{ color: mutedColor }} className="text-sm italic">
                        &quot;{def.example}&quot;
                      </Text>
                    </View>
                  )}
                </View>
              ))}

              {/* Synonyms */}
              {synonyms.length > 0 && (
                <View
                  className="rounded-xl p-4 mt-2"
                  style={{ borderColor, borderWidth: 1 }}
                >
                  <Text
                    style={{ color: textColor }}
                    className="text-sm font-semibold mb-3"
                  >
                    Synonyms
                  </Text>
                  <View className="flex-row flex-wrap gap-2">
                    {synonyms.map((syn, idx) => (
                      <View
                        key={idx}
                        className="px-3 py-1.5 rounded-full"
                        style={{ backgroundColor: cardBg }}
                      >
                        <Text style={{ color: textColor }} className="text-sm">
                          {syn}
                        </Text>
                      </View>
                    ))}
                  </View>
                </View>
              )}

              {/* Save Button */}
              {!wordIsSaved && (
                <TouchableOpacity
                  onPress={handleSave}
                  disabled={isSaving}
                  className="mt-6 mb-4 py-3 rounded-xl items-center"
                  style={{ backgroundColor: '#0d9488' }}
                >
                  {isSaving ? (
                    <ActivityIndicator color="white" />
                  ) : (
                    <Text className="text-white font-semibold">
                      Save to Vocabulary
                    </Text>
                  )}
                </TouchableOpacity>
              )}
            </ScrollView>
          )}
        </BottomSheetView>
      </BottomSheet>
    )
  }
)

WordDefinitionSheet.displayName = 'WordDefinitionSheet'

export default WordDefinitionSheet
