# VocabularyEntry


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **string** |  | [readonly] [default to undefined]
**user_id** | **string** |  | [readonly] [default to undefined]
**word_id** | **string** |  | [default to undefined]
**word_text** | **string** |  | [readonly] [default to undefined]
**meaning** | **string** |  | [default to undefined]
**saved_at** | **string** |  | [readonly] [default to undefined]
**review_count** | **number** |  | [readonly] [default to 0]
**last_reviewed_at** | **string** |  | [readonly] [default to undefined]

## Example

```typescript
import { VocabularyEntry } from 'lexiflow-api-client';

const instance: VocabularyEntry = {
    id,
    user_id,
    word_id,
    word_text,
    meaning,
    saved_at,
    review_count,
    last_reviewed_at,
};
```

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)
