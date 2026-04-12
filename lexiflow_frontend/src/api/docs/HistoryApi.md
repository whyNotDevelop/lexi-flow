# HistoryApi

All URIs are relative to *http://localhost*

|Method | HTTP request | Description|
|------------- | ------------- | -------------|
|[**historyClearDestroy**](#historycleardestroy) | **DELETE** /api/history/clear/ | Clear lookup history|
|[**historyCountRetrieve**](#historycountretrieve) | **GET** /api/history/count/ | Get lookup count|
|[**historyCountSinceRetrieve**](#historycountsinceretrieve) | **GET** /api/history/count-since/ | Get lookup count since date|
|[**historyListRetrieve**](#historylistretrieve) | **GET** /api/history/list/ | Get lookup count since date|

# **historyClearDestroy**
> { [key: string]: any; } historyClearDestroy()

Delete all lookup history for the current user.

### Example

```typescript
import {
    HistoryApi,
    Configuration
} from 'lexiflow-api-client';

const configuration = new Configuration();
const apiInstance = new HistoryApi(configuration);

const { status, data } = await apiInstance.historyClearDestroy();
```

### Parameters
This endpoint does not have any parameters.


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

# **historyCountRetrieve**
> { [key: string]: any; } historyCountRetrieve()

Get total number of word lookups for the user.

### Example

```typescript
import {
    HistoryApi,
    Configuration
} from 'lexiflow-api-client';

const configuration = new Configuration();
const apiInstance = new HistoryApi(configuration);

const { status, data } = await apiInstance.historyCountRetrieve();
```

### Parameters
This endpoint does not have any parameters.


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

# **historyCountSinceRetrieve**
> { [key: string]: any; } historyCountSinceRetrieve()

Get number of lookups since a specific date.

### Example

```typescript
import {
    HistoryApi,
    Configuration
} from 'lexiflow-api-client';

const configuration = new Configuration();
const apiInstance = new HistoryApi(configuration);

const { status, data } = await apiInstance.historyCountSinceRetrieve();
```

### Parameters
This endpoint does not have any parameters.


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

# **historyListRetrieve**
> HistoryListRetrieve200Response historyListRetrieve()

Get number of lookups since a specific date.

### Example

```typescript
import {
    HistoryApi,
    Configuration
} from 'lexiflow-api-client';

const configuration = new Configuration();
const apiInstance = new HistoryApi(configuration);

let since: string; //ISO 8601 datetime (e.g., 2024-01-01T00:00:00Z) (default to undefined)

const { status, data } = await apiInstance.historyListRetrieve(
    since
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **since** | [**string**] | ISO 8601 datetime (e.g., 2024-01-01T00:00:00Z) | defaults to undefined|


### Return type

**HistoryListRetrieve200Response**

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

