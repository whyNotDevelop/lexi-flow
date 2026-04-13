// ============================================
// LexiFlow Mobile - Login Screen
// ============================================

import React, { useState } from 'react'
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  KeyboardAvoidingView,
  Platform,
  ScrollView,
  ActivityIndicator,
} from 'react-native'
import { SafeAreaView } from 'react-native-safe-area-context'

import { useAuth } from '@/hooks/useAuth'
import { usePreferencesStore } from '@/store/preferencesStore'
import { MailIcon, LockIcon, EyeIcon, EyeOffIcon, UserIcon } from '@/components/icons'

export default function LoginScreen() {
  const { login, register, isLoading, error, clearError } = useAuth()
  const isDarkMode = usePreferencesStore((state) => state.is_dark_mode)

  // Form state
  const [isSignUp, setIsSignUp] = useState(false)
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [fullName, setFullName] = useState('')
  const [showPassword, setShowPassword] = useState(false)

  // Form validation
  const isValidEmail = email.includes('@') && email.includes('.')
  const isValidPassword = password.length >= 8
  const isValidName = fullName.trim().length >= 2
  const canSubmit = isValidEmail && isValidPassword && (!isSignUp || isValidName)

  // Handle form submission
  const handleSubmit = async () => {
    if (!canSubmit) return
    clearError()

    try {
      if (isSignUp) {
        await register({ email, password, full_name: fullName })
      } else {
        await login({ email, password })
      }
    } catch {
      // Error is handled by the hook
    }
  }

  // Toggle between sign in and sign up
  const toggleMode = () => {
    setIsSignUp(!isSignUp)
    clearError()
  }

  // Dynamic styles based on dark mode
  const bgColor = isDarkMode ? 'bg-[#1a1918]' : 'bg-[#faf9f7]'
  const cardBg = isDarkMode ? 'bg-[#262524]' : 'bg-white'
  const textColor = isDarkMode ? 'text-[#f5f4f2]' : 'text-[#1a1918]'
  const mutedText = isDarkMode ? 'text-[#78746d]' : 'text-[#78746d]'
  const inputBg = isDarkMode ? 'bg-[#2e2d2b]' : 'bg-[#f0eeeb]'
  const borderColor = isDarkMode ? 'border-[#3d3b38]' : 'border-[#e0ded9]'
  const iconColor = isDarkMode ? '#78746d' : '#78746d'

  return (
    <SafeAreaView className={`flex-1 ${bgColor}`}>
      <KeyboardAvoidingView
        behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
        className="flex-1"
      >
        <ScrollView
          contentContainerStyle={{ flexGrow: 1, justifyContent: 'center', padding: 24 }}
          keyboardShouldPersistTaps="handled"
        >
          {/* Logo and Title */}
          <View className="items-center mb-10">
            <View className="w-16 h-16 rounded-2xl bg-primary items-center justify-center mb-4">
              <Text className="text-white text-2xl font-bold">L</Text>
            </View>
            <Text className={`text-2xl font-bold ${textColor}`}>LexiFlow</Text>
            <Text className={`text-sm ${mutedText} mt-1`}>
              {isSignUp ? 'Create your account' : 'Welcome back'}
            </Text>
          </View>

          {/* Error Message */}
          {error && (
            <View className="bg-red-100 border border-red-300 rounded-xl p-3 mb-4">
              <Text className="text-red-700 text-center text-sm">{error}</Text>
            </View>
          )}

          {/* Form Card */}
          <View className={`${cardBg} rounded-2xl p-5 ${borderColor} border`}>
            {/* Full Name (Sign Up only) */}
            {isSignUp && (
              <View className="mb-4">
                <Text className={`text-sm font-medium ${textColor} mb-2`}>Full Name</Text>
                <View className={`flex-row items-center ${inputBg} rounded-xl px-4 h-12`}>
                  <UserIcon size={18} color={iconColor} />
                  <TextInput
                    className={`flex-1 ml-3 ${textColor}`}
                    placeholder="John Doe"
                    placeholderTextColor={iconColor}
                    value={fullName}
                    onChangeText={setFullName}
                    autoCapitalize="words"
                    autoComplete="name"
                  />
                </View>
              </View>
            )}

            {/* Email Input */}
            <View className="mb-4">
              <Text className={`text-sm font-medium ${textColor} mb-2`}>Email</Text>
              <View className={`flex-row items-center ${inputBg} rounded-xl px-4 h-12`}>
                <MailIcon size={18} color={iconColor} />
                <TextInput
                  className={`flex-1 ml-3 ${textColor}`}
                  placeholder="you@example.com"
                  placeholderTextColor={iconColor}
                  value={email}
                  onChangeText={setEmail}
                  keyboardType="email-address"
                  autoCapitalize="none"
                  autoComplete="email"
                />
              </View>
            </View>

            {/* Password Input */}
            <View className="mb-6">
              <Text className={`text-sm font-medium ${textColor} mb-2`}>Password</Text>
              <View className={`flex-row items-center ${inputBg} rounded-xl px-4 h-12`}>
                <LockIcon size={18} color={iconColor} />
                <TextInput
                  className={`flex-1 ml-3 ${textColor}`}
                  placeholder="Enter your password"
                  placeholderTextColor={iconColor}
                  value={password}
                  onChangeText={setPassword}
                  secureTextEntry={!showPassword}
                  autoCapitalize="none"
                  autoComplete={isSignUp ? 'new-password' : 'current-password'}
                />
                <TouchableOpacity onPress={() => setShowPassword(!showPassword)}>
                  {showPassword ? (
                    <EyeOffIcon size={18} color={iconColor} />
                  ) : (
                    <EyeIcon size={18} color={iconColor} />
                  )}
                </TouchableOpacity>
              </View>
              {isSignUp && (
                <Text className={`text-xs ${mutedText} mt-1`}>
                  Password must be at least 8 characters
                </Text>
              )}
            </View>

            {/* Submit Button */}
            <TouchableOpacity
              onPress={handleSubmit}
              disabled={!canSubmit || isLoading}
              className={`h-12 rounded-xl items-center justify-center ${
                canSubmit && !isLoading ? 'bg-primary' : 'bg-primary/50'
              }`}
            >
              {isLoading ? (
                <ActivityIndicator color="white" />
              ) : (
                <Text className="text-white font-semibold">
                  {isSignUp ? 'Create Account' : 'Sign In'}
                </Text>
              )}
            </TouchableOpacity>

            {/* Divider */}
            <View className="flex-row items-center my-6">
              <View className={`flex-1 h-px ${borderColor}`} />
              <Text className={`px-4 text-sm ${mutedText}`}>or continue with</Text>
              <View className={`flex-1 h-px ${borderColor}`} />
            </View>

            {/* Social Login Buttons */}
            <View className="flex-row gap-3">
              <TouchableOpacity
                className={`flex-1 h-12 rounded-xl items-center justify-center border ${borderColor}`}
              >
                <Text className={textColor}>Google</Text>
              </TouchableOpacity>
              <TouchableOpacity
                className={`flex-1 h-12 rounded-xl items-center justify-center border ${borderColor}`}
              >
                <Text className={textColor}>Apple</Text>
              </TouchableOpacity>
            </View>
          </View>

          {/* Toggle Sign In / Sign Up */}
          <View className="flex-row justify-center mt-6">
            <Text className={mutedText}>
              {isSignUp ? 'Already have an account? ' : "Don't have an account? "}
            </Text>
            <TouchableOpacity onPress={toggleMode}>
              <Text className="text-primary font-semibold">
                {isSignUp ? 'Sign In' : 'Sign Up'}
              </Text>
            </TouchableOpacity>
          </View>
        </ScrollView>
      </KeyboardAvoidingView>
    </SafeAreaView>
  )
}
