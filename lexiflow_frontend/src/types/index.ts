// ============================================
// LexiFlow Mobile - TypeScript Type Definitions
// These types mirror the generated lexiflow-api-client models
// ============================================

// Re-export generated types from the API client
// Note: When using the generated client, import directly from 'lexiflow-api-client'
// These are provided for reference and for use when the client isn't available

// ----- Enums -----
export type FontSizeEnum = 'small' | 'medium' | 'large'

// ----- User Types -----
export interface User {
  id: string // uuid
  email: string
  full_name?: string | null
  avatar_url?: string | null
  created_at: string // ISO datetime
  updated_at: string // ISO datetime
}

export interface PatchedUser {
  id?: string
  email?: string
  full_name?: string | null
  avatar_url?: string | null
  created_at?: string
  updated_at?: string
}

export interface UserPreferences {
  id: string // uuid, readonly
  user_id: string // uuid, readonly
  is_dark_mode: boolean
  language: string
  notifications_enabled: boolean
  font_size: FontSizeEnum
  reading_line_height: number // 1.0 - 2.0
}

export interface PatchedUserPreferences {
  id?: string
  user_id?: string
  is_dark_mode?: boolean
  language?: string
  notifications_enabled?: boolean
  font_size?: FontSizeEnum
  reading_line_height?: number
}

export interface UserRegistration {
  email: string
  password: string // writeOnly, minLength 8
  full_name?: string | null
}

// ----- Word Types -----
export interface Definition {
  id: string // uuid, readonly
  meaning: string
  part_of_speech: string
  example?: string | null
  synonyms?: string[]
  order?: number
}

export interface Word {
  id: string // uuid, readonly
  text: string
  language: string
  phonetic?: string | null
  audio_url?: string | null
  created_at: string // ISO datetime, readonly
  definitions: Definition[] // readonly
}

// ----- Vocabulary Types -----
export interface VocabularyEntry {
  id: string // uuid, readonly
  user_id: string // uuid, readonly
  word_id: string // uuid
  word_text: string // readonly
  meaning: string
  saved_at: string // ISO datetime, readonly
  review_count: number // readonly, default 0
  last_reviewed_at: string // ISO datetime, readonly
}

// ----- History Types -----
export interface HistoryListRetrieve200Response {
  count?: number
}

// ----- Auth Types (for local use) -----
export interface LoginCredentials {
  email: string
  password: string
}

export interface RegisterCredentials {
  email: string
  password: string
  full_name?: string
}

export interface AuthTokens {
  access: string
  refresh: string
}

export interface AuthResponse {
  user: User
  tokens: AuthTokens
}

// ----- Stats Types -----
export interface LookupStats {
  today: number
  this_week: number
  total: number
}

export interface ReadingSessionStats {
  sessions_today: number
  total_reading_time_minutes: number
}

export interface UserStats {
  lookups: LookupStats
  reading_sessions: ReadingSessionStats
}

// ----- API Response Types -----
export interface ApiError {
  code: string
  message: string
  details?: Record<string, string[]>
}

export interface ApiResponse<T> {
  success: boolean
  data?: T
  error?: ApiError
  meta?: Record<string, unknown>
}

// ----- Navigation Types -----
export type RootStackParamList = {
  Login: undefined
  Main: undefined
}

export type MainTabParamList = {
  Reading: undefined
  Vocabulary: undefined
  History: undefined
  Settings: undefined
}

export type Screen = 'login' | 'reading' | 'vocabulary' | 'history' | 'settings'

// ----- Utility Types -----
export interface Pagination {
  total: number
  page: number
  limit: number
  total_pages: number
}
