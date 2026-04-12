# User

Serializer for User domain entity.  Handles user profile data for registration and profile updates.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **string** |  | [readonly] [default to undefined]
**email** | **string** |  | [default to undefined]
**full_name** | **string** |  | [optional] [default to undefined]
**avatar_url** | **string** |  | [optional] [default to undefined]
**created_at** | **string** |  | [readonly] [default to undefined]
**updated_at** | **string** |  | [readonly] [default to undefined]

## Example

```typescript
import { User } from 'lexiflow-api-client';

const instance: User = {
    id,
    email,
    full_name,
    avatar_url,
    created_at,
    updated_at,
};
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
