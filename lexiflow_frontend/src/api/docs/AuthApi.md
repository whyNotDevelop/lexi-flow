# AuthApi

All URIs are relative to *http://localhost*

|Method | HTTP request | Description|
|------------- | ------------- | -------------|
|[**authPreferencesPartialUpdate**](#authpreferencespartialupdate) | **PATCH** /api/auth/preferences/ | Update user preferences|
|[**authPreferencesRetrieve**](#authpreferencesretrieve) | **GET** /api/auth/preferences/ | Get user preferences|
|[**authProfileRetrieve**](#authprofileretrieve) | **GET** /api/auth/profile/ | Get user profile|
|[**authRegisterCreate**](#authregistercreate) | **POST** /api/auth/register/ | Register new user|
|[**authUpdateProfilePartialUpdate**](#authupdateprofilepartialupdate) | **PATCH** /api/auth/update_profile/ | Update user profile|

# **authPreferencesPartialUpdate**
> UserPreferences authPreferencesPartialUpdate()

Update the current user\'s preferences.

### Example

```typescript
import {
    AuthApi,
    Configuration,
    PatchedUserPreferences
} from 'lexiflow-api-client';

const configuration = new Configuration();
const apiInstance = new AuthApi(configuration);

let patchedUserPreferences: PatchedUserPreferences; // (optional)

const { status, data } = await apiInstance.authPreferencesPartialUpdate(
    patchedUserPreferences
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **patchedUserPreferences** | **PatchedUserPreferences**|  | |


### Return type

**UserPreferences**

### Authorization

[jwtAuth](../README.md#jwtAuth)

### HTTP request headers

 - **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **authPreferencesRetrieve**
> UserPreferences authPreferencesRetrieve()

Get the current user\'s preferences.

### Example

```typescript
import {
    AuthApi,
    Configuration
} from 'lexiflow-api-client';

const configuration = new Configuration();
const apiInstance = new AuthApi(configuration);

const { status, data } = await apiInstance.authPreferencesRetrieve();
```

### Parameters
This endpoint does not have any parameters.


### Return type

**UserPreferences**

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

# **authProfileRetrieve**
> User authProfileRetrieve()

Get the current user\'s profile information.

### Example

```typescript
import {
    AuthApi,
    Configuration
} from 'lexiflow-api-client';

const configuration = new Configuration();
const apiInstance = new AuthApi(configuration);

const { status, data } = await apiInstance.authProfileRetrieve();
```

### Parameters
This endpoint does not have any parameters.


### Return type

**User**

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

# **authRegisterCreate**
> { [key: string]: any; } authRegisterCreate(userRegistration)

Create a new user account and return authentication tokens.

### Example

```typescript
import {
    AuthApi,
    Configuration,
    UserRegistration
} from 'lexiflow-api-client';

const configuration = new Configuration();
const apiInstance = new AuthApi(configuration);

let userRegistration: UserRegistration; //

const { status, data } = await apiInstance.authRegisterCreate(
    userRegistration
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **userRegistration** | **UserRegistration**|  | |


### Return type

**{ [key: string]: any; }**

### Authorization

[jwtAuth](../README.md#jwtAuth)

### HTTP request headers

 - **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**201** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **authUpdateProfilePartialUpdate**
> User authUpdateProfilePartialUpdate()

Update the current user\'s profile information.

### Example

```typescript
import {
    AuthApi,
    Configuration,
    PatchedUser
} from 'lexiflow-api-client';

const configuration = new Configuration();
const apiInstance = new AuthApi(configuration);

let patchedUser: PatchedUser; // (optional)

const { status, data } = await apiInstance.authUpdateProfilePartialUpdate(
    patchedUser
);
```

### Parameters

|Name | Type | Description  | Notes|
|------------- | ------------- | ------------- | -------------|
| **patchedUser** | **PatchedUser**|  | |


### Return type

**User**

### Authorization

[jwtAuth](../README.md#jwtAuth)

### HTTP request headers

 - **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
 - **Accept**: application/json


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
|**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

