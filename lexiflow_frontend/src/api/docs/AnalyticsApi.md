# AnalyticsApi

All URIs are relative to *http://localhost*

|Method | HTTP request | Description|
|------------- | ------------- | -------------|
|[**analyticsLookupsRetrieve**](#analyticslookupsretrieve) | **GET** /api/analytics/lookups/ | Get lookup statistics|
|[**analyticsReadingSessionsRetrieve**](#analyticsreadingsessionsretrieve) | **GET** /api/analytics/reading-sessions/ | Get reading session statistics|
|[**analyticsStatsRetrieve**](#analyticsstatsretrieve) | **GET** /api/analytics/stats/ | Get user statistics|

# **analyticsLookupsRetrieve**
> { [key: string]: any; } analyticsLookupsRetrieve()

Get statistics about user\'s word lookups.

### Example

```typescript
import {
    AnalyticsApi,
    Configuration
} from 'lexiflow-api-client';

const configuration = new Configuration();
const apiInstance = new AnalyticsApi(configuration);

const { status, data } = await apiInstance.analyticsLookupsRetrieve();
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

# **analyticsReadingSessionsRetrieve**
> { [key: string]: any; } analyticsReadingSessionsRetrieve()

Get statistics about user\'s reading sessions.

### Example

```typescript
import {
    AnalyticsApi,
    Configuration
} from 'lexiflow-api-client';

const configuration = new Configuration();
const apiInstance = new AnalyticsApi(configuration);

const { status, data } = await apiInstance.analyticsReadingSessionsRetrieve();
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

# **analyticsStatsRetrieve**
> { [key: string]: any; } analyticsStatsRetrieve()

Get comprehensive statistics for the current user including reading sessions and lookups.

### Example

```typescript
import {
    AnalyticsApi,
    Configuration
} from 'lexiflow-api-client';

const configuration = new Configuration();
const apiInstance = new AnalyticsApi(configuration);

const { status, data } = await apiInstance.analyticsStatsRetrieve();
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

