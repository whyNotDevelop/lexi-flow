# PatchedUserPreferences

Serializer for UserPreferences domain entity.  Handles user UI and reading preferences.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **string** |  | [optional] [readonly] [default to undefined]
**user_id** | **string** |  | [optional] [readonly] [default to undefined]
**is_dark_mode** | **boolean** |  | [optional] [default to false]
**language** | **string** |  | [optional] [default to 'en']
**notifications_enabled** | **boolean** |  | [optional] [default to true]
**font_size** | [**FontSizeEnum**](FontSizeEnum.md) |  | [optional] [default to undefined]
**reading_line_height** | **number** |  | [optional] [default to 1.6]

## Example

```typescript
import { PatchedUserPreferences } from 'lexiflow-api-client';

const instance: PatchedUserPreferences = {
    id,
    user_id,
    is_dark_mode,
    language,
    notifications_enabled,
    font_size,
    reading_line_height,
};
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
