// ============================================
// LexiFlow Mobile - Settings Screen
// ============================================

import React, { useCallback } from 'react'
import { View, Text, ScrollView, TouchableOpacity, Switch, Alert } from 'react-native'
import { SafeAreaView } from 'react-native-safe-area-context'

import { useAuth } from '@/hooks/useAuth'
import { usePreferencesStore } from '@/store/preferencesStore'
import {
  UserIcon,
  BellIcon,
  MoonIcon,
  GlobeIcon,
  ShieldIcon,
  HelpCircleIcon,
  LogOutIcon,
  ChevronRightIcon,
} from '@/components/icons'

interface SettingsItemProps {
  icon: React.ReactNode
  label: string
  value?: string
  onPress?: () => void
  rightElement?: React.ReactNode
  isDarkMode: boolean
}

function SettingsItem({
  icon,
  label,
  value,
  onPress,
  rightElement,
  isDarkMode,
}: SettingsItemProps) {
  const textColor = isDarkMode ? 'text-[#f5f4f2]' : 'text-[#1a1918]'
  const mutedColor = isDarkMode ? '#78746d' : '#78746d'

  return (
    <TouchableOpacity
      onPress={onPress}
      disabled={!onPress}
      className="flex-row items-center py-3"
    >
      <View className="w-8">{icon}</View>
      <Text className={`flex-1 ${textColor}`}>{label}</Text>
      {value && (
        <Text style={{ color: mutedColor }} className="mr-2">
          {value}
        </Text>
      )}
      {rightElement}
      {onPress && !rightElement && (
        <ChevronRightIcon size={18} color={mutedColor} />
      )}
    </TouchableOpacity>
  )
}

export default function SettingsScreen() {
  const { user, logout } = useAuth()
  const isDarkMode = usePreferencesStore((state) => state.is_dark_mode)
  const toggleDarkMode = usePreferencesStore((state) => state.toggleDarkMode)
  const language = usePreferencesStore((state) => state.language)

  // Handle logout
  const handleLogout = useCallback(() => {
    Alert.alert(
      'Log Out',
      'Are you sure you want to log out?',
      [
        { text: 'Cancel', style: 'cancel' },
        {
          text: 'Log Out',
          style: 'destructive',
          onPress: logout,
        },
      ]
    )
  }, [logout])

  // Get initials from name
  const getInitials = (name: string) => {
    return name
      .split(' ')
      .map((n) => n[0])
      .join('')
      .toUpperCase()
      .slice(0, 2)
  }

  // Dynamic styles
  const bgColor = isDarkMode ? 'bg-[#1a1918]' : 'bg-[#faf9f7]'
  const cardBg = isDarkMode ? 'bg-[#262524]' : 'bg-white'
  const textColor = isDarkMode ? 'text-[#f5f4f2]' : 'text-[#1a1918]'
  const mutedText = isDarkMode ? 'text-[#78746d]' : 'text-[#78746d]'
  const borderColor = isDarkMode ? 'border-[#3d3b38]' : 'border-[#e0ded9]'
  const iconColor = isDarkMode ? '#f5f4f2' : '#1a1918'
  const mutedIconColor = isDarkMode ? '#78746d' : '#78746d'

  // Get display language
  const getLanguageDisplay = () => {
    const languages: Record<string, string> = {
      en: 'English',
      es: 'Spanish',
      fr: 'French',
      de: 'German',
    }
    return languages[language] || 'English'
  }

  return (
    <SafeAreaView className={`flex-1 ${bgColor}`} edges={['top']}>
      {/* Header */}
      <View className="px-4 py-3">
        <Text className={`text-2xl font-bold ${textColor}`}>Settings</Text>
      </View>

      <ScrollView
        className="flex-1 px-4"
        showsVerticalScrollIndicator={false}
      >
        {/* Profile Card */}
        <View
          className={`${cardBg} rounded-2xl p-5 mb-6 border ${borderColor}`}
        >
          <View className="flex-row items-center">
            <View className="w-16 h-16 rounded-full bg-primary items-center justify-center">
              <Text className="text-white text-xl font-bold">
                {user?.full_name ? getInitials(user.full_name) : 'U'}
              </Text>
            </View>
            <View className="ml-4 flex-1">
              <Text className={`text-lg font-semibold ${textColor}`}>
                {user?.full_name || 'User'}
              </Text>
              <Text className={`text-sm ${mutedText}`}>
                {user?.email || 'user@example.com'}
              </Text>
            </View>
          </View>
        </View>

        {/* Account Section */}
        <View className="mb-6">
          <Text className={`text-xs font-semibold ${mutedText} mb-2 px-1`}>
            ACCOUNT
          </Text>
          <View
            className={`${cardBg} rounded-xl px-4 border ${borderColor}`}
          >
            <SettingsItem
              icon={<UserIcon size={20} color={iconColor} />}
              label="Profile"
              onPress={() => {}}
              isDarkMode={isDarkMode}
            />
            <View className={`h-px ${borderColor}`} />
            <SettingsItem
              icon={<BellIcon size={20} color={iconColor} />}
              label="Notifications"
              onPress={() => {}}
              isDarkMode={isDarkMode}
            />
          </View>
        </View>

        {/* Preferences Section */}
        <View className="mb-6">
          <Text className={`text-xs font-semibold ${mutedText} mb-2 px-1`}>
            PREFERENCES
          </Text>
          <View
            className={`${cardBg} rounded-xl px-4 border ${borderColor}`}
          >
            <SettingsItem
              icon={<MoonIcon size={20} color={iconColor} />}
              label="Dark Mode"
              isDarkMode={isDarkMode}
              rightElement={
                <Switch
                  value={isDarkMode}
                  onValueChange={toggleDarkMode}
                  trackColor={{ false: '#e0ded9', true: '#0d9488' }}
                  thumbColor="white"
                />
              }
            />
            <View className={`h-px ${borderColor}`} />
            <SettingsItem
              icon={<GlobeIcon size={20} color={iconColor} />}
              label="Language"
              value={getLanguageDisplay()}
              onPress={() => {}}
              isDarkMode={isDarkMode}
            />
          </View>
        </View>

        {/* About Section */}
        <View className="mb-6">
          <Text className={`text-xs font-semibold ${mutedText} mb-2 px-1`}>
            ABOUT
          </Text>
          <View
            className={`${cardBg} rounded-xl px-4 border ${borderColor}`}
          >
            <SettingsItem
              icon={<ShieldIcon size={20} color={iconColor} />}
              label="Privacy Policy"
              onPress={() => {}}
              isDarkMode={isDarkMode}
            />
            <View className={`h-px ${borderColor}`} />
            <SettingsItem
              icon={<HelpCircleIcon size={20} color={iconColor} />}
              label="Help & Support"
              onPress={() => {}}
              isDarkMode={isDarkMode}
            />
          </View>
        </View>

        {/* Logout Button */}
        <TouchableOpacity
          onPress={handleLogout}
          className={`${cardBg} rounded-xl p-4 flex-row items-center justify-center border border-destructive/30 mb-8`}
        >
          <LogOutIcon size={20} color="#dc2626" />
          <Text className="text-destructive font-semibold ml-2">Log Out</Text>
        </TouchableOpacity>

        {/* App Version */}
        <Text className={`text-center text-xs ${mutedText} mb-8`}>
          LexiFlow v1.0.0
        </Text>

        {/* Bottom padding */}
        <View className="h-20" />
      </ScrollView>
    </SafeAreaView>
  )
}
