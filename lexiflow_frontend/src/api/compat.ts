// src/api/compat.ts
import { WordsApi, VocabularyApi, HistoryApi, AnalyticsApi, AuthApi } from './api';
import type { Word, VocabularyEntry, UserRegistration, UserPreferences } from './api';
import AsyncStorage from '@react-native-async-storage/async-storage';

export const wordsApi = new WordsApi();
const vocabularyApi = new VocabularyApi();
const historyApi = new HistoryApi();
const analyticsApi = new AnalyticsApi();
const authApi = new AuthApi();

// ========== Words ==========
export const words = {
  lookup: (word: string) => wordsApi.wordsLookupRetrieve(word).then(res => res.data),
};

// ========== Vocabulary ==========
export const vocabulary = {
  getAll: () => vocabularyApi.vocabularyListList().then(res => res.data),
  search: () => vocabularyApi.vocabularySearchList().then(res => res.data),
  save: (wordId: string) => vocabularyApi.vocabularySaveCreate(wordId).then(res => res.data),
  remove: (wordId: string) => vocabularyApi.vocabularyRemoveDestroy(wordId),
  isSaved: (wordId: string) => vocabularyApi.vocabularyIsSavedRetrieve(wordId).then(res => res.data),
};

// ========== History ==========
export const history = {
  getList: (since: string) => historyApi.historyListRetrieve(since).then(res => res.data),
  clear: () => historyApi.historyClearDestroy(),
  getCount: () => historyApi.historyCountRetrieve().then(res => res.data),
  getCountSince: (since: string) => historyApi.historyCountSinceRetrieve({ params: { since } }).then(res => res.data),
};

// ========== Analytics ==========
export const analytics = {
  getLookupStats: () => analyticsApi.analyticsLookupsRetrieve().then(res => res.data),
  getReadingStats: () => analyticsApi.analyticsReadingSessionsRetrieve().then(res => res.data),
  getUserStats: () => analyticsApi.analyticsStatsRetrieve().then(res => res.data),
};

// ========== Auth Helpers ==========
export const tokenStorage = {
  getAccessToken: () => AsyncStorage.getItem('access_token'),
  setAccessToken: (token: string) => AsyncStorage.setItem('access_token', token),
  getRefreshToken: () => AsyncStorage.getItem('refresh_token'),
  setRefreshToken: (token: string) => AsyncStorage.setItem('refresh_token', token),
  clearTokens: () => Promise.all([
    AsyncStorage.removeItem('access_token'),
    AsyncStorage.removeItem('refresh_token'),
  ]),
};

export const auth = {
  setTokens: async (access: string, refresh: string) => {
    await tokenStorage.setAccessToken(access);
    await tokenStorage.setRefreshToken(refresh);
  },
  clearTokens: tokenStorage.clearTokens,
  getProfile: () => authApi.authProfileRetrieve().then(res => res.data),
  getPreferences: () => authApi.authPreferencesRetrieve().then(res => res.data),
  updatePreferences: (prefs: any) => authApi.authPreferencesPartialUpdate(prefs),
  register: (data: UserRegistration) => authApi.authRegisterCreate(data).then(res => res.data),
};