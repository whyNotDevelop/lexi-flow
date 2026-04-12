# Word

Serializer for Word domain entity.  Handles serialization of complete word entries including definitions, pronunciation, and metadata.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **string** |  | [readonly] [default to undefined]
**text** | **string** |  | [default to undefined]
**language** | **string** |  | [default to undefined]
**phonetic** | **string** |  | [optional] [default to undefined]
**audio_url** | **string** |  | [optional] [default to undefined]
**created_at** | **string** |  | [readonly] [default to undefined]
**definitions** | [**Array&lt;Definition&gt;**](Definition.md) |  | [readonly] [default to undefined]

## Example

```typescript
import { Word } from 'lexiflow-api-client';

const instance: Word = {
    id,
    text,
    language,
    phonetic,
    audio_url,
    created_at,
    definitions,
};
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
