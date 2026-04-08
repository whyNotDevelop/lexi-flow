## lexiflow-api-client@1.0.0

This generator creates TypeScript/JavaScript client that utilizes [axios](https://github.com/axios/axios). The generated Node module can be used in the following environments:

Environment
* Node.js
* Webpack
* Browserify

Language level
* ES5 - you must have a Promises/A+ library installed
* ES6

Module system
* CommonJS
* ES6 module system

It can be used in both TypeScript and JavaScript. In TypeScript, the definition will be automatically resolved via `package.json`. ([Reference](https://www.typescriptlang.org/docs/handbook/declaration-files/consumption.html))

### Building

To build and compile the typescript sources to javascript use:
```
npm install
npm run build
```

### Publishing

First build the package then run `npm publish`

### Consuming

navigate to the folder of your consuming project and run one of the following commands.

_published:_

```
npm install lexiflow-api-client@1.0.0 --save
```

_unPublished (not recommended):_

```
npm install PATH_TO_GENERATED_PACKAGE --save
```

### Documentation for API Endpoints

All URIs are relative to *http://localhost*

Class | Method | HTTP request | Description
------------ | ------------- | ------------- | -------------
*AnalyticsApi* | [**analyticsLookupsRetrieve**](docs/AnalyticsApi.md#analyticslookupsretrieve) | **GET** /api/analytics/lookups/ | Get lookup statistics
*AnalyticsApi* | [**analyticsReadingSessionsRetrieve**](docs/AnalyticsApi.md#analyticsreadingsessionsretrieve) | **GET** /api/analytics/reading-sessions/ | Get reading session statistics
*AnalyticsApi* | [**analyticsStatsRetrieve**](docs/AnalyticsApi.md#analyticsstatsretrieve) | **GET** /api/analytics/stats/ | Get user statistics
*AuthApi* | [**authPreferencesPartialUpdate**](docs/AuthApi.md#authpreferencespartialupdate) | **PATCH** /api/auth/preferences/ | Update user preferences
*AuthApi* | [**authPreferencesRetrieve**](docs/AuthApi.md#authpreferencesretrieve) | **GET** /api/auth/preferences/ | Get user preferences
*AuthApi* | [**authProfileRetrieve**](docs/AuthApi.md#authprofileretrieve) | **GET** /api/auth/profile/ | Get user profile
*AuthApi* | [**authRegisterCreate**](docs/AuthApi.md#authregistercreate) | **POST** /api/auth/register/ | Register new user
*AuthApi* | [**authUpdateProfilePartialUpdate**](docs/AuthApi.md#authupdateprofilepartialupdate) | **PATCH** /api/auth/update_profile/ | Update user profile
*HistoryApi* | [**historyClearDestroy**](docs/HistoryApi.md#historycleardestroy) | **DELETE** /api/history/clear/ | Clear lookup history
*HistoryApi* | [**historyCountRetrieve**](docs/HistoryApi.md#historycountretrieve) | **GET** /api/history/count/ | Get lookup count
*HistoryApi* | [**historyCountSinceRetrieve**](docs/HistoryApi.md#historycountsinceretrieve) | **GET** /api/history/count-since/ | Get lookup count since date
*HistoryApi* | [**historyListRetrieve**](docs/HistoryApi.md#historylistretrieve) | **GET** /api/history/list/ | Get lookup count since date
*VocabularyApi* | [**vocabularyIsSavedRetrieve**](docs/VocabularyApi.md#vocabularyissavedretrieve) | **GET** /api/vocabulary/is-saved/{word_id}/ | Check if word is saved
*VocabularyApi* | [**vocabularyListList**](docs/VocabularyApi.md#vocabularylistlist) | **GET** /api/vocabulary/list/ | Get user vocabulary
*VocabularyApi* | [**vocabularyRemoveDestroy**](docs/VocabularyApi.md#vocabularyremovedestroy) | **DELETE** /api/vocabulary/remove/{word_id}/ | Remove word from vocabulary
*VocabularyApi* | [**vocabularySaveCreate**](docs/VocabularyApi.md#vocabularysavecreate) | **POST** /api/vocabulary/save/{word_id}/ | Save word to vocabulary
*VocabularyApi* | [**vocabularySearchList**](docs/VocabularyApi.md#vocabularysearchlist) | **GET** /api/vocabulary/search/ | Search vocabulary
*WordsApi* | [**wordsLookupRetrieve**](docs/WordsApi.md#wordslookupretrieve) | **GET** /api/words/lookup/{word}/ | Look up a word


### Documentation For Models

 - [Definition](docs/Definition.md)
 - [FontSizeEnum](docs/FontSizeEnum.md)
 - [HistoryListRetrieve200Response](docs/HistoryListRetrieve200Response.md)
 - [PatchedUser](docs/PatchedUser.md)
 - [PatchedUserPreferences](docs/PatchedUserPreferences.md)
 - [User](docs/User.md)
 - [UserPreferences](docs/UserPreferences.md)
 - [UserRegistration](docs/UserRegistration.md)
 - [VocabularyEntry](docs/VocabularyEntry.md)
 - [Word](docs/Word.md)


<a id="documentation-for-authorization"></a>
## Documentation For Authorization


Authentication schemes defined for the API:
<a id="jwtAuth"></a>
### jwtAuth

- **Type**: Bearer authentication (JWT)

