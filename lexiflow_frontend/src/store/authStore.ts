// ============================================
// LexiFlow Mobile - Authentication Store (Zustand)
// Uses the generated lexiflow-api-client
// ============================================

import { create } from 'zustand'
import { persist, createJSONStorage } from 'zustand/middleware'
import AsyncStorage from '@react-native-async-storage/async-storage'
import axios from 'axios'
import { auth, tokenStorage } from '@/api/compat'
import type { User, UserRegistration } from 'lexiflow-api-client'

// API base URL for token endpoints
const API_BASE_URL = process.env.EXPO_PUBLIC_API_URL || 'https://api.lexiflow.app'

interface LoginCredentials {
  email: string
  password: string
}

interface AuthState {
  // State
  user: User | null
  isAuthenticated: boolean
  isLoading: boolean
  error: string | null

  // Actions
  login: (credentials: LoginCredentials) => Promise<void>
  register: (credentials: UserRegistration) => Promise<void>
  logout: () => Promise<void>
  setUser: (user: User) => void
  clearError: () => void
  checkAuth: () => Promise<void>
  refreshProfile: () => Promise<void>
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set, get) => ({
      // Initial state
      user: null,
      isAuthenticated: false,
      isLoading: false,
      error: null,

      // Login action - uses JWT token endpoint
      login: async (credentials: LoginCredentials) => {
        set({ isLoading: true, error: null })
        try {
          // Call the JWT token endpoint (Simple JWT)
          const tokenResponse = await axios.post(`${API_BASE_URL}/api/auth/token/`, {
            email: credentials.email,
            password: credentials.password,
          })

          const { access, refresh } = tokenResponse.data

          // Store tokens
          await auth.setTokens(access, refresh)

          // Fetch user profile using the generated client
          const user = await auth.getProfile()

          set({
            user,
            isAuthenticated: true,
            isLoading: false,
          })
        } catch (error: unknown) {
          const message =
            axios.isAxiosError(error) && error.response?.data?.detail
              ? error.response.data.detail
              : error instanceof Error
                ? error.message
                : 'Login failed'
          set({ error: message, isLoading: false })
          throw error
        }
      },

      // Register action - uses generated client
      register: async (credentials: UserRegistration) => {
        set({ isLoading: true, error: null })
        try {
          // Register using the generated client
          const registerResponse = await auth.register(credentials)

          // The response should include tokens or we need to login after
          // Assuming the backend returns tokens on registration
          if (registerResponse && 'access' in registerResponse && 'refresh' in registerResponse) {
            const { access, refresh } = registerResponse as { access: string; refresh: string }
            await auth.setTokens(access, refresh)
          } else {
            // If not, login with the credentials
            const tokenResponse = await axios.post(`${API_BASE_URL}/api/auth/token/`, {
              email: credentials.email,
              password: credentials.password,
            })
            const { access, refresh } = tokenResponse.data
            await auth.setTokens(access, refresh)
          }

          // Fetch user profile
          const user = await auth.getProfile()

          set({
            user,
            isAuthenticated: true,
            isLoading: false,
          })
        } catch (error: unknown) {
          const message =
            axios.isAxiosError(error) && error.response?.data
              ? JSON.stringify(error.response.data)
              : error instanceof Error
                ? error.message
                : 'Registration failed'
          set({ error: message, isLoading: false })
          throw error
        }
      },

      // Logout action
      logout: async () => {
        await auth.clearTokens()
        set({
          user: null,
          isAuthenticated: false,
          error: null,
        })
      },

      // Update user data
      setUser: (user: User) => {
        set({ user })
      },

      // Clear error message
      clearError: () => {
        set({ error: null })
      },

      // Check if user is still authenticated
      checkAuth: async () => {
        const token = await tokenStorage.getAccessToken()
        if (!token) {
          set({ isAuthenticated: false, user: null })
          return
        }

        try {
          const user = await auth.getProfile()
          set({ user, isAuthenticated: true })
        } catch {
          // Token expired or invalid
          await auth.clearTokens()
          set({
            user: null,
            isAuthenticated: false,
          })
        }
      },

      // Refresh user profile from server
      refreshProfile: async () => {
        const { isAuthenticated } = get()
        if (!isAuthenticated) return

        try {
          const user = await auth.getProfile()
          set({ user })
        } catch {
          // Ignore errors - user data will remain stale
        }
      },
    }),
    {
      name: 'lexiflow-auth-storage',
      storage: createJSONStorage(() => AsyncStorage),
      partialize: (state) => ({
        user: state.user,
        isAuthenticated: state.isAuthenticated,
      }),
    }
  )
)

export default useAuthStore
