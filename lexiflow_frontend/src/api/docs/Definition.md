# Definition

Serializer for Definition domain entity.  Handles serialization of word definitions including part of speech, meaning, examples, and synonyms.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **string** |  | [readonly] [default to undefined]
**meaning** | **string** |  | [default to undefined]
**part_of_speech** | **string** |  | [default to undefined]
**example** | **string** |  | [optional] [default to undefined]
**synonyms** | **Array&lt;string&gt;** |  | [optional] [default to undefined]
**order** | **number** |  | [optional] [default to 0]

## Example

```typescript
import { Definition } from 'lexiflow-api-client';

const instance: Definition = {
    id,
    meaning,
    part_of_speech,
    example,
    synonyms,
    order,
};
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
