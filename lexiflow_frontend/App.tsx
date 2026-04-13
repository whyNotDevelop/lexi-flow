// ============================================
// LexiFlow Mobile - App Entry Point
// ============================================

import React, { useEffect, useCallback } from 'react'
import { StatusBar, View, ActivityIndicator } from 'react-native'
import { SafeAreaProvider } from 'react-native-safe-area-context'
import { SWRConfig } from 'swr'

import { AppNavigator } from '@/navigation/AppNavigator'
import { useAuthStore } from '@/store/authStore'
import { usePreferencesStore } from '@/store/preferencesStore'
import { apiClient } from './api/client'

// Global SWR configuration
const swrConfig = {
  fetcher: (url: string) => apiClient.get(url).then((res) => res.data),
  revalidateOnFocus: true,
  dedupingInterval: 5000,
  errorRetryCount: 3,
}

export default function App() {
  const checkAuth = useAuthStore((state) => state.checkAuth)
  const isLoading = useAuthStore((state) => state.isLoading)
  const isDarkMode = usePreferencesStore((state) => state.is_dark_mode)
  const loadPreferences = usePreferencesStore((state) => state.loadFromServer)

  // Initialize app on mount
  useEffect(() => {
    const initializeApp = async () => {
      await checkAuth()
      // Load preferences from server if authenticated
      const isAuth = useAuthStore.getState().isAuthenticated
      if (isAuth) {
        await loadPreferences()
      }
    }
    initializeApp()
  }, [checkAuth, loadPreferences])

  // Show loading screen while checking auth
  if (isLoading) {
    return (
      <View
        style={{
          flex: 1,
          justifyContent: 'center',
          alignItems: 'center',
          backgroundColor: isDarkMode ? '#1a1918' : '#faf9f7',
        }}
      >
        <ActivityIndicator size="large" color="#0d9488" />
      </View>
    )
  }

  return (
    <SafeAreaProvider>
      <SWRConfig value={swrConfig}>
        <StatusBar
          barStyle={isDarkMode ? 'light-content' : 'dark-content'}
          backgroundColor={isDarkMode ? '#1a1918' : '#faf9f7'}
        />
        <AppNavigator />
      </SWRConfig>
    </SafeAreaProvider>
  )
}
