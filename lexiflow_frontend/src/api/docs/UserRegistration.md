# UserRegistration

Serializer for user registration.  Includes password field for registration (not returned in responses).

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**email** | **string** |  | [default to undefined]
**password** | **string** |  | [default to undefined]
**full_name** | **string** |  | [optional] [default to undefined]

## Example

```typescript
import { UserRegistration } from 'lexiflow-api-client';

const instance: UserRegistration = {
    email,
    password,
    full_name,
};
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
