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