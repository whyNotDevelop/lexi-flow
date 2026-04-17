// ============================================
// LexiFlow Mobile - App Navigator
// ============================================

import React from 'react'
import { NavigationContainer } from '@react-navigation/native'
import { createNativeStackNavigator } from '@react-navigation/native-stack'
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs'
import { View, Text } from 'react-native'

import { useAuthStore } from '@/store/authStore'
import { usePreferencesStore } from '@/store/preferencesStore'
import { RootStackParamList, MainTabParamList } from '@/types'

// Screens
import LoginScreen from '@/screens/LoginScreen'
import ReadingScreen from '@/screens/ReadingScreen'
import VocabularyScreen from '@/screens/VocabularyScreen'
import HistoryScreen from '@/screens/HistoryScreen'
import SettingsScreen from '@/screens/SettingsScreen'

// Icons (using simple text for now - replace with actual icons)
import { BookIcon, BookmarkIcon, ClockIcon, SettingsIcon } from '@/components/icons'

const Stack = createNativeStackNavigator<RootStackParamList>()
const Tab = createBottomTabNavigator<MainTabParamList>()

/**
 * Main tab navigator for authenticated users
 */
function MainTabs() {
  const isDarkMode = usePreferencesStore((state) => state.is_dark_mode)

  return (
    <Tab.Navigator
      screenOptions={{
        headerShown: false,
        tabBarStyle: {
          backgroundColor: isDarkMode ? '#262524' : '#ffffff',
          borderTopColor: isDarkMode ? '#3d3b38' : '#e0ded9',
          paddingBottom: 8,
          paddingTop: 8,
          height: 64,
        },
        tabBarActiveTintColor: '#0d9488',
        tabBarInactiveTintColor: isDarkMode ? '#78746d' : '#78746d',
        tabBarLabelStyle: {
          fontSize: 11,
          fontWeight: '500',
        },
      }}
    >
      <Tab.Screen
        name="Reading"
        component={ReadingScreen}
        options={{
          tabBarLabel: 'Reading',
          tabBarIcon: ({ color, size }) => <BookIcon color={color} size={size} />,
        }}
      />
      <Tab.Screen
        name="Vocabulary"
        component={VocabularyScreen}
        options={{
          tabBarLabel: 'Vocabulary',
          tabBarIcon: ({ color, size }) => <BookmarkIcon color={color} size={size} />,
        }}
      />
      <Tab.Screen
        name="History"
        component={HistoryScreen}
        options={{
          tabBarLabel: 'History',
          tabBarIcon: ({ color, size }) => <ClockIcon color={color} size={size} />,
        }}
      />
      <Tab.Screen
        name="Settings"
        component={SettingsScreen}
        options={{
          tabBarLabel: 'Settings',
          tabBarIcon: ({ color, size }) => <SettingsIcon color={color} size={size} />,
        }}
      />
    </Tab.Navigator>
  )
}

/**
 * Root navigator - handles auth state
 */
export function AppNavigator() {
  const isAuthenticated = useAuthStore((state) => state.isAuthenticated)
  const isDarkMode = usePreferencesStore((state) => state.is_dark_mode)

  return (
    // Inside AppNavigator, replace the theme object:
<NavigationContainer
  theme={{
    dark: isDarkMode,
    colors: {
      primary: '#0d9488',
      background: isDarkMode ? '#1a1918' : '#faf9f7',
      card: isDarkMode ? '#262524' : '#ffffff',
      text: isDarkMode ? '#f5f4f2' : '#1a1918',
      border: isDarkMode ? '#3d3b38' : '#e0ded9',
      notification: '#0d9488',
    },
    fonts: {
      regular: {
        fontFamily: 'System',
        fontWeight: 'bold'
      },
      medium: {
        fontFamily: 'System',
        fontWeight: 'bold'
      },
      bold: {
        fontFamily: 'System',
        fontWeight: 'bold'
      },
      heavy: {
        fontFamily: 'System',
        fontWeight: 'bold'
      },
    },
  }}
>
      <Stack.Navigator screenOptions={{ headerShown: false }}>
        {!isAuthenticated ? (
          <Stack.Screen
            name="Login"
            component={LoginScreen}
            options={{
              animationTypeForReplace: 'pop',
            }}
          />
        ) : (
          <Stack.Screen name="Main" component={MainTabs} />
        )}
      </Stack.Navigator>
    </NavigationContainer>
  )
}

export default AppNavigator
