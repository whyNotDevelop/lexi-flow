# VocabularyApi

All URIs are relative to *http://localhost*

|Method | HTTP request | Description|
|------------- | ------------- | -------------|
|[**vocabularyIsSavedRetrieve**](#vocabularyissavedretrieve) | **GET** /api/vocabulary/is-saved/{word_id}/ | Check if word is saved|
|[**vocabularyListList**](#vocabularylistlist) | **GET** /api/vocabulary/list/ | Get user vocabulary|
|[**vocabularyRemoveDestroy**](#vocabularyremovedestroy) | **DELETE** /api/vocabulary/remove/{word_id}/ | Remove word from vocabulary|
|[**vocabularySaveCreate**](#vocabularysavecreate) | **POST** /api/vocabulary/save/{word_id}/ | Save word to vocabulary|
|[**vocabularySearchList**](#vocabularysearchlist) | **GET** /api/vocabulary/search/ | Search vocabulary|

# **vocabularyIsSavedRetrieve**
> { [key: string]: any; } vocabularyIsSavedRetrieve()

Check if a specific word is saved in user\'s vocabulary.

### Example

```typescript
import {
    VocabularyApi,
    Configuration
} from 'lexiflow-api-client';

const configuration = new Configuration();
const apiInstance = new VocabularyApi(configuration);

let wordId: string; // (default to undefined)

const { status, data } = await apiInstance.vocabularyIsSavedRetrieve(
    wordId
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **wordId** | [**string**] |  | defaults to undefined|


### Return type

**{ [key: string]: any; }**

### Authorization

[jwtAuth](../README.md#jwtAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **vocabularyListList**
> Array<VocabularyEntry> vocabularyListList()

Get all words saved by the user.

### Example

```typescript
import {
    VocabularyApi,
    Configuration
} from 'lexiflow-api-client';

const configuration = new Configuration();
const apiInstance = new VocabularyApi(configuration);

const { status, data } = await apiInstance.vocabularyListList();
```

### Parameters
This endpoint does not have any parameters.


### Return type

**Array<VocabularyEntry>**

### Authorization

[jwtAuth](../README.md#jwtAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **vocabularyRemoveDestroy**
> vocabularyRemoveDestroy()

Remove a word from the user\'s personal vocabulary list.

### Example

```typescript
import {
    VocabularyApi,
    Configuration
} from 'lexiflow-api-client';

const configuration = new Configuration();
const apiInstance = new VocabularyApi(configuration);

let wordId: string; // (default to undefined)

const { status, data } = await apiInstance.vocabularyRemoveDestroy(
    wordId
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **wordId** | [**string**] |  | defaults to undefined|


### Return type

void (empty response body)

### Authorization

[jwtAuth](../README.md#jwtAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**204** | No response body |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **vocabularySaveCreate**
> VocabularyEntry vocabularySaveCreate()

Save a word to the user\'s personal vocabulary list.

### Example

```typescript
import {
    VocabularyApi,
    Configuration
} from 'lexiflow-api-client';

const configuration = new Configuration();
const apiInstance = new VocabularyApi(configuration);

let wordId: string; // (default to undefined)

const { status, data } = await apiInstance.vocabularySaveCreate(
    wordId
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **wordId** | [**string**] |  | defaults to undefined|


### Return type

**VocabularyEntry**

### Authorization

[jwtAuth](../README.md#jwtAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**201** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **vocabularySearchList**
> Array<VocabularyEntry> vocabularySearchList()

Search user\'s saved vocabulary by word text.

### Example

```typescript
import {
    VocabularyApi,
    Configuration
} from 'lexiflow-api-client';

const configuration = new Configuration();
const apiInstance = new VocabularyApi(configuration);

const { status, data } = await apiInstance.vocabularySearchList();
```

### Parameters
This endpoint does not have any parameters.


### Return type

**Array<VocabularyEntry>**

### Authorization

[jwtAuth](../README.md#jwtAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

