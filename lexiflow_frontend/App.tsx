// App.tsx
import React, { useEffect } from 'react';
import { StatusBar, View, ActivityIndicator } from 'react-native';
import { SafeAreaProvider } from 'react-native-safe-area-context';
import { SWRConfig } from 'swr';
import { AppNavigator } from '@/navigation/AppNavigator';
import { useAuthStore } from '@/store/authStore';
import { usePreferencesStore } from '@/store/preferencesStore';
import { wordsApi } from '@/api/compat';  // use compat for fetcher

const swrConfig = {
  fetcher: (url: string) => {
    // Simple fetcher – you can implement based on your needs
    // For now, we'll use the wordsApi as a placeholder
    return wordsApi.wordsLookupRetrieve(url).then(res => res.data);
  },
  revalidateOnFocus: true,
  dedupingInterval: 5000,
  errorRetryCount: 3,
};

export default function App() {
  const checkAuth = useAuthStore((state) => state.checkAuth);
  const isLoading = useAuthStore((state) => state.isLoading);
  const isDarkMode = usePreferencesStore((state) => state.is_dark_mode);
  const loadPreferences = usePreferencesStore((state) => state.loadFromServer);

  useEffect(() => {
    const initializeApp = async () => {
      await checkAuth();
      const isAuth = useAuthStore.getState().isAuthenticated;
      if (isAuth) {
        await loadPreferences();
      }
    };
    initializeApp();
  }, [checkAuth, loadPreferences]);

  if (isLoading) {
    return (
      <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center', backgroundColor: isDarkMode ? '#1a1918' : '#faf9f7' }}>
        <ActivityIndicator size="large" color="#0d9488" />
      </View>
    );
  }

  return (
    <SafeAreaProvider>
      <SWRConfig value={swrConfig}>
        <StatusBar barStyle={isDarkMode ? 'light-content' : 'dark-content'} backgroundColor={isDarkMode ? '#1a1918' : '#faf9f7'} />
        <AppNavigator />
      </SWRConfig>
    </SafeAreaProvider>
  );
}