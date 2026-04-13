// ============================================
// LexiFlow Mobile - Auth Hook
// Uses the generated lexiflow-api-client
// ============================================

import { useCallback, useEffect } from 'react'
import { useAuthStore } from '@/store/authStore'
import type { UserRegistration } from 'lexiflow-api-client'

interface LoginCredentials {
  email: string
  password: string
}

/**
 * Hook for authentication operations
 * Wraps the auth store with convenient methods
 *
 * API Endpoints:
 * - POST /api/auth/token/ (Simple JWT - not in OpenAPI)
 * - POST /api/auth/register/
 * - GET /api/auth/profile/
 * - PATCH /api/auth/update_profile/
 * - GET /api/auth/preferences/
 * - PATCH /api/auth/preferences/
 */
export function useAuth() {
  const {
    user,
    isAuthenticated,
    isLoading,
    error,
    login: storeLogin,
    register: storeRegister,
    logout: storeLogout,
    checkAuth,
    clearError,
    refreshProfile,
  } = useAuthStore()

  // Check authentication status on mount
  useEffect(() => {
    checkAuth()
  }, [checkAuth])

  // Login handler
  const login = useCallback(
    async (credentials: LoginCredentials) => {
      await storeLogin(credentials)
    },
    [storeLogin]
  )

  // Register handler
  const register = useCallback(
    async (credentials: UserRegistration) => {
      await storeRegister(credentials)
    },
    [storeRegister]
  )

  // Logout handler
  const logout = useCallback(async () => {
    await storeLogout()
  }, [storeLogout])

  return {
    user,
    isAuthenticated,
    isLoading,
    error,
    login,
    register,
    logout,
    clearError,
    refreshProfile,
  }
}

export default useAuth
