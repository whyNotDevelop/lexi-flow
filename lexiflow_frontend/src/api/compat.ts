// src/api/compat.ts
import { WordsApi, VocabularyApi, HistoryApi, AnalyticsApi, AuthApi } from './api';
import type { Word, VocabularyEntry, UserRegistration } from './api';

const wordsApi = new WordsApi();
const vocabularyApi = new VocabularyApi();
const historyApi = new HistoryApi();
const analyticsApi = new AnalyticsApi();
const authApi = new AuthApi();

export const words = {
  lookup: (word: string) => wordsApi.wordsLookupRetrieve({ word }).then(res => res.data),
};

export const vocabulary = {
  getAll: () => vocabularyApi.vocabularyListList().then(res => res.data),
  search: () => vocabularyApi.vocabularySearchList().then(res => res.data),
  save: (wordId: string) => vocabularyApi.vocabularySaveCreate({ wordId }).then(res => res.data),
  remove: (wordId: string) => vocabularyApi.vocabularyRemoveDestroy({ wordId }),
  isSaved: (wordId: string) => vocabularyApi.vocabularyIsSavedRetrieve({ wordId }).then(res => res.data),
};

export const history = {
  getList: (since: string) => historyApi.historyListRetrieve({ since }).then(res => res.data),
  clear: () => historyApi.historyClearDestroy(),
  getCount: () => historyApi.historyCountRetrieve().then(res => res.data),
  getCountSince: (since: string) => historyApi.historyCountSinceRetrieve({ since }).then(res => res.data),
};

export const analytics = {
  getLookupStats: () => analyticsApi.analyticsLookupsRetrieve().then(res => res.data),
  getReadingStats: () => analyticsApi.analyticsReadingSessionsRetrieve().then(res => res.data),
  getUserStats: () => analyticsApi.analyticsStatsRetrieve().then(res => res.data),
};

export const auth = {
  register: (data: UserRegistration) => authApi.authRegisterCreate(data).then(res => res.data),
  getProfile: () => authApi.authProfileRetrieve().then(res => res.data),
  updatePreferences: (prefs: any) => authApi.authPreferencesPartialUpdate(prefs),
};