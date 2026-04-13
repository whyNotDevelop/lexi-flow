// ============================================
// LexiFlow Mobile - User Preferences Store (Zustand)
// Uses the generated lexiflow-api-client
// ============================================

import { create } from 'zustand'
import { persist, createJSONStorage } from 'zustand/middleware'
import AsyncStorage from '@react-native-async-storage/async-storage'
import { auth } from '@/api/compat'
import type { UserPreferences, FontSizeEnum } from 'lexiflow-api-client'

interface PreferencesState {
  // State from API
  id: string | null
  user_id: string | null
  is_dark_mode: boolean
  language: string
  notifications_enabled: boolean
  font_size: FontSizeEnum
  reading_line_height: number

  // Local state
  isLoading: boolean
  isSyncing: boolean

  // Actions
  toggleDarkMode: () => void
  setLanguage: (language: string) => void
  setFontSize: (size: FontSizeEnum) => void
  setLineHeight: (height: number) => void
  toggleNotifications: () => void
  syncWithServer: () => Promise<void>
  loadFromServer: () => Promise<void>
  setPreferences: (prefs: UserPreferences) => void
}

const defaultPreferences = {
  id: null,
  user_id: null,
  is_dark_mode: false,
  language: 'en',
  notifications_enabled: true,
  font_size: 'medium' as FontSizeEnum,
  reading_line_height: 1.6,
}

export const usePreferencesStore = create<PreferencesState>()(
  persist(
    (set, get) => ({
      // Initial state
      ...defaultPreferences,
      isLoading: false,
      isSyncing: false,

      // Toggle dark mode
      toggleDarkMode: () => {
        const newValue = !get().is_dark_mode
        set({ is_dark_mode: newValue })
        // Sync with server in background
        get().syncWithServer()
      },

      // Set language
      setLanguage: (language: string) => {
        set({ language })
        get().syncWithServer()
      },

      // Set font size
      setFontSize: (size: FontSizeEnum) => {
        set({ font_size: size })
        get().syncWithServer()
      },

      // Set reading line height
      setLineHeight: (height: number) => {
        // Clamp to valid range (1.0 - 2.0)
        const clampedHeight = Math.min(2.0, Math.max(1.0, height))
        set({ reading_line_height: clampedHeight })
        get().syncWithServer()
      },

      // Toggle notifications
      toggleNotifications: () => {
        const newValue = !get().notifications_enabled
        set({ notifications_enabled: newValue })
        get().syncWithServer()
      },

      // Sync preferences with server using generated client
      syncWithServer: async () => {
        const { is_dark_mode, language, notifications_enabled, font_size, reading_line_height } =
          get()
        set({ isSyncing: true })
        try {
          await auth.updatePreferences({
            is_dark_mode,
            language,
            notifications_enabled,
            font_size,
            reading_line_height,
          })
        } catch {
          // Silently fail - local state is authoritative
        } finally {
          set({ isSyncing: false })
        }
      },

      // Load preferences from server using generated client
      loadFromServer: async () => {
        set({ isLoading: true })
        try {
          const prefs = await auth.getPreferences()
          set({
            id: prefs.id,
            user_id: prefs.user_id,
            is_dark_mode: prefs.is_dark_mode ?? false,
            language: prefs.language ?? 'en',
            notifications_enabled: prefs.notifications_enabled ?? true,
            font_size: prefs.font_size ?? 'medium',
            reading_line_height: prefs.reading_line_height ?? 1.6,
            isLoading: false,
          })
        } catch {
          set({ isLoading: false })
        }
      },

      // Set preferences directly (used after login)
      setPreferences: (prefs: UserPreferences) => {
        set({
          id: prefs.id,
          user_id: prefs.user_id,
          is_dark_mode: prefs.is_dark_mode ?? false,
          language: prefs.language ?? 'en',
          notifications_enabled: prefs.notifications_enabled ?? true,
          font_size: prefs.font_size ?? 'medium',
          reading_line_height: prefs.reading_line_height ?? 1.6,
        })
      },
    }),
    {
      name: 'lexiflow-preferences-storage',
      storage: createJSONStorage(() => AsyncStorage),
      partialize: (state) => ({
        id: state.id,
        user_id: state.user_id,
        is_dark_mode: state.is_dark_mode,
        language: state.language,
        notifications_enabled: state.notifications_enabled,
        font_size: state.font_size,
        reading_line_height: state.reading_line_height,
      }),
    }
  )
)

export default usePreferencesStore
