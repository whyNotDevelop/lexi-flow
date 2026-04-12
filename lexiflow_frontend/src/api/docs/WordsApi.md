# WordsApi

All URIs are relative to *http://localhost*

|Method | HTTP request | Description|
|------------- | ------------- | -------------|
|[**wordsLookupRetrieve**](#wordslookupretrieve) | **GET** /api/words/lookup/{word}/ | Look up a word|

# **wordsLookupRetrieve**
> Word wordsLookupRetrieve()

Look up a word definition with caching and external API fallback. Records lookup in history.

### Example

```typescript
import {
    WordsApi,
    Configuration
} from 'lexiflow-api-client';

const configuration = new Configuration();
const apiInstance = new WordsApi(configuration);

let word: string; // (default to undefined)

const { status, data } = await apiInstance.wordsLookupRetrieve(
    word
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **word** | [**string**] |  | defaults to undefined|


### Return type

**Word**

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

