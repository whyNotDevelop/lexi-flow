# LexiFlow API Contract v1.0

**Base URL:** `https://lexiflow-backend.onrender.com/api/`  
**Authentication:** JWT (Bearer token) – obtained via `/api/auth/register/` (returns tokens) or future login endpoint.

---

## Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register/` | Register new user (returns tokens) |
| GET | `/api/auth/profile/` | Get current user profile |
| PATCH | `/api/auth/update-profile/` | Update profile (full_name, avatar_url) |
| GET | `/api/auth/preferences/` | Get user preferences |
| PATCH | `/api/auth/preferences/` | Update preferences |

---

## Word Lookup

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/words/lookup/{word}/` | Look up a word (cached, external API fallback) |

### Response (200)
```json
{
  "id": "uuid",
  "text": "serendipity",
  "phonetic": "/ˌserənˈdɪpɪti/",
  "audio_url": "https://...",
  "definitions": [
    {
      "id": "uuid",
      "part_of_speech": "noun",
      "meaning": "the occurrence of events by chance...",
      "example": "A fortunate stroke of serendipity.",
      "synonyms": ["luck", "chance"],
      "order": 0
    }
  ],
  "is_saved": false
}

### Vocabulary

| Method | Endpoint                              | Description                 |
| ------ | ------------------------------------- | --------------------------- |
| POST   | `/api/vocabulary/save/{word_id}/`     | Save word to vocabulary     |
| DELETE | `/api/vocabulary/remove/{word_id}/`   | Remove word from vocabulary |
| GET    | `/api/vocabulary/list/`               | List all saved words        |
| GET    | `/api/vocabulary/search/?q={query}`   | Search saved words          |
| GET    | `/api/vocabulary/is-saved/{word_id}/` | Check if word is saved      |

### Vocabulary Entry Response
{
  "id": "uuid",
  "user_id": "uuid",
  "word_id": "uuid",
  "word_text": "serendipity",
  "meaning": "the occurrence of events by chance...",
  "saved_at": "2026-04-05T12:00:00Z",
  "review_count": 0,
  "last_reviewed_at": null
}

### History
| Method | Endpoint                                     | Description                            |
| ------ | -------------------------------------------- | -------------------------------------- |
| GET    | `/api/history/list/`                         | Get lookup history (most recent first) |
| DELETE | `/api/history/clear/`                        | Clear all history                      |
| GET    | `/api/history/count/`                        | Total lookup count                     |
| GET    | `/api/history/count-since/?since={ISO_DATE}` | Lookups since given date               |

### History List Response
[
  {
    "id": "uuid",
    "user_id": "uuid",
    "word_id": "uuid",
    "looked_up_at": "2026-04-05T12:00:00Z"
  }
]

### Analytics
| Method | Endpoint                           | Description                                            |
| ------ | ---------------------------------- | ------------------------------------------------------ |
| GET    | `/api/analytics/stats/`            | Comprehensive user stats                               |
| GET    | `/api/analytics/reading-sessions/` | Reading session stats                                  |
| GET    | `/api/analytics/lookups/`          | Lookup stats (today, last 7 days, last 30 days, total) |

### Stats Response Example
{
  "total_sessions": 5,
  "active_sessions": 1,
  "reading_time_seconds": 3600,
  "average_session_duration_seconds": 720,
  "total_words_looked_up": 42,
  "lookups_total": 100,
  "lookups_today": 10,
  "lookups_last_7_days": 45,
  "lookups_last_30_days": 100
}

### Status Codes
| Code                      | Meaning                                    |
| ------------------------- | ------------------------------------------ |
| 200 OK                    | Successful request                         |
| 201 Created               | Resource created                           |
| 204 No Content            | Deletion successful                        |
| 400 Bad Request           | Invalid input                              |
| 401 Unauthorized          | Missing or invalid token                   |
| 404 Not Found             | Resource not found                         |
| 409 Conflict              | Duplicate entry (e.g., word already saved) |
| 500 Internal Server Error | Server error                               |
