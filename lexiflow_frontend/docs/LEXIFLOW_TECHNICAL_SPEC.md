# LexiFlow Technical Specification

> Complete technical specification for backend (Django/DRF) and mobile (React Native) developers to implement the LexiFlow reading assistant application.

---

## Table of Contents

1. [Stack Details](#1-stack-details)
2. [NPM Packages](#2-npm-packages)
3. [File Structure Explanation](#3-file-structure-explanation)
4. [Screen Flow](#4-screen-flow)
5. [API Contracts](#5-api-contracts)
6. [Data Models](#6-data-models)
7. [State Management Strategy](#7-state-management-strategy)
8. [Component Design Patterns](#8-component-design-patterns)
9. [Mobile Adaptation](#9-mobile-adaptation)
10. [Development Recommendations](#10-development-recommendations)

---

## 1. Stack Details

### UI Prototype Stack

| Layer | Technology | Version | Purpose |
|-------|------------|---------|---------|
| **Framework** | Next.js | 16.1.6 | React-based web framework for the UI prototype |
| **UI Library** | React | 19.2.4 | Core UI library with hooks and components |
| **Language** | TypeScript | 5.7.3 | Type-safe JavaScript for development |
| **Styling System** | Tailwind CSS | 4.2.0 | Utility-first CSS framework |
| **Component Library** | shadcn/ui | 4.0.0 | Pre-built accessible React components |
| **Icons** | Lucide React | 0.564.0 | Modern icon library |
| **State Management** | React useState | Built-in | Local component state (prototype only) |
| **Package Manager** | pnpm | Latest | Fast, disk-efficient package manager |
| **Build System** | Turbopack | Built into Next.js 16 | Fast bundler (default in Next.js 16) |

### Target Production Stack

| Layer | Technology | Version | Purpose |
|-------|------------|---------|---------|
| **Backend Framework** | Django | 4.2+ | Python web framework |
| **API Framework** | Django REST Framework | 3.14+ | REST API development |
| **Database** | PostgreSQL | 15+ | Primary relational database |
| **Cache** | Redis | 7+ | Caching and session storage |
| **Containerization** | Docker | Latest | Application containerization |
| **Mobile Framework** | React Native | 0.73+ | Cross-platform mobile development |

---

## 2. NPM Packages

### Core Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| `react` | 19.2.4 | Core React library for building UI components |
| `react-dom` | 19.2.4 | React DOM renderer for web applications |
| `next` | 16.1.6 | React framework with routing, SSR, and optimization |
| `typescript` | 5.7.3 | Type-safe JavaScript with static type checking |

### UI & Styling

| Package | Version | Purpose |
|---------|---------|---------|
| `tailwindcss` | 4.2.0 | Utility-first CSS framework for rapid styling |
| `tailwind-merge` | 3.3.1 | Merges Tailwind classes without conflicts |
| `class-variance-authority` | 0.7.1 | Type-safe component variant management |
| `clsx` | 2.1.1 | Conditional class name construction |
| `tw-animate-css` | 1.3.3 | Animation utilities for Tailwind |
| `lucide-react` | 0.564.0 | Modern SVG icon library with React components |

### Radix UI Primitives

| Package | Version | Purpose |
|---------|---------|---------|
| `@radix-ui/react-switch` | 1.2.6 | Accessible toggle switch component (used in Settings) |
| `@radix-ui/react-slot` | 1.2.4 | Polymorphic component composition |
| `@radix-ui/react-dialog` | 1.1.15 | Accessible modal dialog (potential use for popups) |
| `@radix-ui/react-label` | 2.1.8 | Accessible form labels |

### Form & Validation

| Package | Version | Purpose |
|---------|---------|---------|
| `react-hook-form` | 7.54.1 | Performant form state management |
| `@hookform/resolvers` | 3.9.1 | Validation schema resolvers for react-hook-form |
| `zod` | 3.24.1 | TypeScript-first schema validation |

### Utilities

| Package | Version | Purpose |
|---------|---------|---------|
| `date-fns` | 4.1.0 | Modern date utility library |
| `sonner` | 1.7.1 | Toast notifications |
| `vaul` | 1.1.2 | Drawer/bottom sheet component |
| `next-themes` | 0.4.6 | Theme management (light/dark mode) |

### Additional Packages for Production

These packages should be added for the production React Native implementation:

```json
{
  "dependencies": {
    "swr": "^2.2.0",
    "@tanstack/react-query": "^5.0.0",
    "zustand": "^4.4.0",
    "axios": "^1.6.0"
  }
}
```

| Package | Purpose |
|---------|---------|
| `swr` | Data fetching with caching and revalidation |
| `@tanstack/react-query` | Alternative to SWR for complex data fetching |
| `zustand` | Lightweight global state management |
| `axios` | HTTP client for API requests |

---

## 3. File Structure Explanation

```
/vercel/share/v0-project/
├── app/                          # Next.js App Router directory
├── components/                   # React components
│   ├── lexiflow/                # LexiFlow-specific components
│   └── ui/                      # shadcn/ui component library
├── hooks/                        # Custom React hooks
├── lib/                          # Utility functions
└── public/                       # Static assets
```

### `/app` - Next.js Application

The `app` directory contains the Next.js App Router structure:

| File | Purpose |
|------|---------|
| `layout.tsx` | Root layout with metadata, fonts, and global providers. Sets page title "LexiFlow - Intelligent Reading Assistant" and viewport settings. |
| `page.tsx` | Landing page that renders the phone mockup with the LexiFlow app prototype. Contains feature highlights and design showcase. |
| `globals.css` | Global styles including Tailwind imports, design tokens (colors, spacing), and dark mode CSS variables using OKLCH color space. |

### `/components/lexiflow` - Application Screens

This directory contains all LexiFlow-specific screen components:

| File | Purpose |
|------|---------|
| `lexiflow-app.tsx` | **Main App Container** - Manages global state (authentication, current screen, dark mode). Orchestrates navigation between screens and handles login flow. |
| `phone-mockup.tsx` | **Device Frame Wrapper** - Renders a realistic iPhone-style device frame around the app screens. Includes notch, status bar, and home indicator. |
| `login-screen.tsx` | **Authentication Screen** - Email/password login form with show/hide password toggle, social login buttons (Google, Apple), and sign up/sign in mode switching. |
| `reading-screen.tsx` | **Core Reading Interface** - The primary screen where users read text. Contains tappable words that trigger definition popups, header with dark mode toggle, and bottom navigation. |
| `word-definition-popup.tsx` | **Definition Modal** - Bottom sheet displaying word definition with pronunciation, audio button, save to vocabulary, numbered definitions with examples, and synonyms section. |
| `vocabulary-screen.tsx` | **Saved Words List** - Displays user's saved vocabulary with search functionality, word cards showing meaning and save date, delete capability, and weekly/total stats card. |
| `history-screen.tsx` | **Lookup History** - Chronological list of looked-up words with timestamps, save/delete actions per item, "Clear All" functionality, and today/week/total statistics grid. |
| `settings-screen.tsx` | **User Preferences** - Profile card, grouped settings (Account, Preferences, About), dark mode toggle switch, language selector, and logout button. |

### `/components/ui` - shadcn/ui Components

Pre-built, accessible UI primitives from shadcn/ui:

| File | Purpose |
|------|---------|
| `button.tsx` | Configurable button with variants (default, outline, ghost, destructive) and sizes |
| `input.tsx` | Styled text input with consistent design |
| `switch.tsx` | Toggle switch component (used for dark mode setting) |
| `card.tsx` | Container component for content sections |
| `dialog.tsx` | Modal dialog component |
| `toast.tsx` | Notification toast component |

### `/hooks` - Custom Hooks

| File | Purpose |
|------|---------|
| `use-mobile.ts` | Detects mobile viewport for responsive behavior |
| `use-toast.ts` | Toast notification management hook |

### `/lib` - Utilities

| File | Purpose |
|------|---------|
| `utils.ts` | Contains `cn()` function - combines `clsx` and `tailwind-merge` for conditional class names |

### `/public` - Static Assets

| Asset Type | Purpose |
|------------|---------|
| Images | App icons, logos, placeholder images |
| Fonts | Custom font files if needed |
| Favicons | Browser tab icons |

---

## 4. Screen Flow

### Navigation Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                      APP LAUNCH                              │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    LOGIN SCREEN                              │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  • Email/Password Form                               │   │
│  │  • Social Login (Google, Apple)                      │   │
│  │  • Sign Up / Sign In Toggle                          │   │
│  └─────────────────────────────────────────────────────┘   │
└────────────────────────┬────────────────────────────────────┘
                         │ On successful login
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                   READING SCREEN                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Header: [← Back] [Book Title] [☀/🌙 Theme Toggle]   │   │
│  │                                                      │   │
│  │  Reading Content with Tappable Words                 │   │
│  │  (Underlined words trigger definition popup)         │   │
│  │                                                      │   │
│  │  ┌────────────────────────────────────────────────┐ │   │
│  │  │  WORD DEFINITION POPUP (Bottom Sheet)          │ │   │
│  │  │  • Word + Pronunciation + Audio Button         │ │   │
│  │  │  • Save to Vocabulary Button                   │ │   │
│  │  │  • Numbered Definitions with Examples          │ │   │
│  │  │  • Synonyms Section                            │ │   │
│  │  │  • "Save to Vocabulary" CTA Button             │ │   │
│  │  └────────────────────────────────────────────────┘ │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                              │
│  BOTTOM NAVIGATION BAR:                                      │
│  [📖 Reading*] [🔖 Vocabulary] [🕒 History] [⚙ Settings]     │
└─────────────────────────────────────────────────────────────┘
         │                    │              │
         │                    │              │
         ▼                    ▼              ▼
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│  VOCABULARY     │  │    HISTORY      │  │   SETTINGS      │
│  SCREEN         │  │    SCREEN       │  │   SCREEN        │
│                 │  │                 │  │                 │
│  • Search Bar   │  │  • Clear All    │  │  • Profile Card │
│  • Word List    │  │  • History List │  │  • Dark Mode    │
│    with Delete  │  │    with Save/   │  │  • Language     │
│  • Weekly Stats │  │    Delete       │  │  • Logout       │
│  • Total Count  │  │  • Day/Week/    │  │                 │
│                 │  │    Total Stats  │  │                 │
└─────────────────┘  └─────────────────┘  └─────────────────┘
```

### User Flow Description

#### 1. Login → Reading Screen
- User launches app and sees the **Login Screen**
- Enters email/password OR taps Google/Apple social login
- On successful authentication, redirected to **Reading Screen**
- State changes: `isLoggedIn = true`, `currentScreen = "reading"`

#### 2. Reading Screen → Word Definition Popup
- User reads text content with underlined tappable words
- Tapping a word triggers the **Word Definition Popup** (bottom sheet)
- Popup slides up from bottom showing:
  - Word, pronunciation, audio playback button
  - Numbered definitions with example sentences
  - Synonyms section
  - "Save to Vocabulary" button
- Tapping backdrop or X button closes the popup
- Saving a word adds it to vocabulary and marks it as saved (filled bookmark icon)

#### 3. Reading Screen ↔ Vocabulary Screen
- User taps "Vocabulary" in bottom navigation
- **Vocabulary Screen** shows:
  - Search input to filter saved words
  - List of saved words with meaning preview and save date
  - Delete button per word
  - Statistics card (This Week / Total)
- User can tap any word to potentially view full definition
- Tapping "Reading" returns to Reading Screen

#### 4. Reading Screen ↔ History Screen
- User taps "History" in bottom navigation
- **History Screen** shows:
  - "Clear All" button in header
  - Chronological list of looked-up words
  - Each item shows: word, time ago, saved status
  - Unsaved words have bookmark button to save
  - All items have delete button
  - Statistics grid: Today / This Week / Total lookups
- Tapping "Reading" returns to Reading Screen

#### 5. Reading Screen ↔ Settings Screen
- User taps "Settings" in bottom navigation
- **Settings Screen** shows:
  - Profile card with avatar initials, name, email
  - Settings groups:
    - **Account**: Profile, Notifications
    - **Preferences**: Dark Mode toggle, Language selector
    - **About**: Privacy Policy, Help & Support
  - Logout button at bottom
- Dark Mode toggle immediately applies theme change
- Tapping "Reading" returns to Reading Screen

### State Transitions

```typescript
type Screen = "login" | "reading" | "vocabulary" | "history" | "settings"

// State variables
currentScreen: Screen      // Which screen is displayed
isLoggedIn: boolean        // Authentication status
isDarkMode: boolean        // Theme preference
selectedWord: WordData | null  // Currently selected word (for popup)
savedWords: string[]       // List of saved word IDs
```

---

## 5. API Contracts

### Authentication Endpoints

#### `POST /api/auth/register`

Create a new user account.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "SecurePassword123!",
  "full_name": "John Doe"
}
```

**Response (201 Created):**
```json
{
  "success": true,
  "data": {
    "user": {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "email": "user@example.com",
      "full_name": "John Doe",
      "avatar_url": null,
      "created_at": "2026-03-13T10:00:00Z"
    },
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "expires_in": 3600
  }
}
```

**Response (400 Bad Request):**
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input data",
    "details": {
      "email": ["Email already registered"],
      "password": ["Password must be at least 8 characters"]
    }
  }
}
```

---

#### `POST /api/auth/login`

Authenticate an existing user.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "SecurePassword123!"
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "user": {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "email": "user@example.com",
      "full_name": "John Doe",
      "avatar_url": "https://cdn.example.com/avatars/user123.jpg"
    },
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "expires_in": 3600
  }
}
```

**Response (401 Unauthorized):**
```json
{
  "success": false,
  "error": {
    "code": "INVALID_CREDENTIALS",
    "message": "Invalid email or password"
  }
}
```

---

#### `POST /api/auth/logout`

Invalidate the current session.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Successfully logged out"
}
```

---

#### `POST /api/auth/refresh`

Refresh an expired access token.

**Request Body:**
```json
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "expires_in": 3600
  }
}
```

---

#### `GET /api/auth/me`

Get the current authenticated user.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "user@example.com",
    "full_name": "John Doe",
    "avatar_url": "https://cdn.example.com/avatars/user123.jpg",
    "created_at": "2026-03-13T10:00:00Z",
    "preferences": {
      "is_dark_mode": false,
      "language": "en",
      "notifications_enabled": true
    }
  }
}
```

---

### Word Lookup Endpoints

#### `GET /api/words/{word}`

Look up a word definition.

**Path Parameters:**
- `word` (string): The word to look up (case-insensitive)

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "id": "word-550e8400-e29b-41d4-a716-446655440001",
    "word": "serendipitous",
    "phonetic": "/ˌser.ənˈdɪp.ɪ.təs/",
    "audio_url": "https://cdn.example.com/audio/serendipitous.mp3",
    "definitions": [
      {
        "id": "def-001",
        "part_of_speech": "adjective",
        "meaning": "Occurring or discovered by chance in a happy or beneficial way",
        "example": "Their meeting was entirely serendipitous.",
        "synonyms": ["fortunate", "lucky", "providential", "auspicious"],
        "order": 1
      }
    ],
    "is_saved": false
  },
  "meta": {
    "cached": true,
    "cache_expires_at": "2026-03-14T10:00:00Z"
  }
}
```

**Response (404 Not Found):**
```json
{
  "success": false,
  "error": {
    "code": "WORD_NOT_FOUND",
    "message": "Definition not found for 'xyz'"
  }
}
```

---

### Vocabulary Endpoints

#### `GET /api/vocabulary`

List all saved vocabulary words.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Query Parameters:**
- `page` (int, optional): Page number (default: 1)
- `limit` (int, optional): Items per page (default: 20, max: 100)
- `search` (string, optional): Search query to filter words

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "words": [
      {
        "id": "sv-001",
        "word_id": "word-001",
        "word": "serendipitous",
        "meaning": "Occurring by chance in a happy way",
        "saved_at": "2026-03-13T09:00:00Z",
        "review_count": 3,
        "last_reviewed_at": "2026-03-13T12:00:00Z"
      },
      {
        "id": "sv-002",
        "word_id": "word-002",
        "word": "ephemeral",
        "meaning": "Lasting for a very short time",
        "saved_at": "2026-03-13T08:30:00Z",
        "review_count": 1,
        "last_reviewed_at": null
      }
    ],
    "pagination": {
      "total": 47,
      "page": 1,
      "limit": 20,
      "total_pages": 3
    }
  }
}
```

---

#### `POST /api/vocabulary`

Save a word to vocabulary.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "word_id": "word-550e8400-e29b-41d4-a716-446655440001",
  "word": "serendipitous",
  "meaning": "Occurring by chance in a happy way"
}
```

**Response (201 Created):**
```json
{
  "success": true,
  "data": {
    "id": "sv-003",
    "word_id": "word-550e8400-e29b-41d4-a716-446655440001",
    "word": "serendipitous",
    "meaning": "Occurring by chance in a happy way",
    "saved_at": "2026-03-13T10:30:00Z",
    "review_count": 0
  }
}
```

**Response (409 Conflict):**
```json
{
  "success": false,
  "error": {
    "code": "ALREADY_SAVED",
    "message": "This word is already in your vocabulary"
  }
}
```

---

#### `DELETE /api/vocabulary/{id}`

Remove a word from vocabulary.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Path Parameters:**
- `id` (string): The saved vocabulary entry ID

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Word removed from vocabulary"
}
```

---

#### `GET /api/vocabulary/search?q={query}`

Search saved vocabulary words.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Query Parameters:**
- `q` (string, required): Search query (minimum 1 character)

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "words": [
      {
        "id": "sv-001",
        "word": "serendipitous",
        "meaning": "Occurring by chance in a happy way",
        "saved_at": "2026-03-13T09:00:00Z"
      }
    ],
    "total": 1,
    "query": "serend"
  }
}
```

---

### History Endpoints

#### `GET /api/history`

Get lookup history.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Query Parameters:**
- `page` (int, optional): Page number (default: 1)
- `limit` (int, optional): Items per page (default: 50, max: 100)
- `date` (string, optional): Filter by date (YYYY-MM-DD)

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "items": [
      {
        "id": "h-001",
        "word_id": "word-001",
        "word": "serendipitous",
        "looked_up_at": "2026-03-13T10:25:00Z",
        "is_saved": true
      },
      {
        "id": "h-002",
        "word_id": "word-002",
        "word": "ephemeral",
        "looked_up_at": "2026-03-13T10:20:00Z",
        "is_saved": true
      },
      {
        "id": "h-003",
        "word_id": "word-003",
        "word": "provincial",
        "looked_up_at": "2026-03-13T10:15:00Z",
        "is_saved": false
      }
    ],
    "pagination": {
      "total": 342,
      "page": 1,
      "limit": 50,
      "total_pages": 7
    }
  }
}
```

---

#### `POST /api/history`

Record a word lookup (called automatically when looking up a word).

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "word_id": "word-550e8400-e29b-41d4-a716-446655440001",
  "word": "serendipitous"
}
```

**Response (201 Created):**
```json
{
  "success": true,
  "data": {
    "id": "h-004",
    "word": "serendipitous",
    "looked_up_at": "2026-03-13T10:30:00Z"
  }
}
```

---

#### `DELETE /api/history/{id}`

Delete a single history item.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "History item deleted"
}
```

---

#### `DELETE /api/history`

Clear all history.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "All history cleared",
  "deleted_count": 342
}
```

---

### User Settings Endpoints

#### `GET /api/user/profile`

Get user profile.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "user@example.com",
    "full_name": "John Doe",
    "avatar_url": "https://cdn.example.com/avatars/user123.jpg",
    "created_at": "2026-03-13T10:00:00Z",
    "updated_at": "2026-03-13T12:00:00Z"
  }
}
```

---

#### `PATCH /api/user/profile`

Update user profile.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "full_name": "John Smith",
  "avatar_url": "https://cdn.example.com/avatars/new-avatar.jpg"
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "user@example.com",
    "full_name": "John Smith",
    "avatar_url": "https://cdn.example.com/avatars/new-avatar.jpg",
    "updated_at": "2026-03-13T14:00:00Z"
  }
}
```

---

#### `GET /api/user/preferences`

Get user preferences.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "is_dark_mode": false,
    "language": "en",
    "notifications_enabled": true,
    "font_size": "medium",
    "reading_line_height": 1.6
  }
}
```

---

#### `PATCH /api/user/preferences`

Update user preferences.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "is_dark_mode": true,
  "language": "es"
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "is_dark_mode": true,
    "language": "es",
    "notifications_enabled": true,
    "font_size": "medium",
    "reading_line_height": 1.6
  }
}
```

---

#### `GET /api/user/stats`

Get usage statistics.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "lookups": {
      "today": 23,
      "this_week": 89,
      "total": 342
    },
    "vocabulary": {
      "saved_today": 2,
      "saved_this_week": 12,
      "total_saved": 47
    },
    "reading": {
      "sessions_today": 3,
      "total_reading_time_minutes": 127
    },
    "streaks": {
      "current_streak_days": 7,
      "longest_streak_days": 14
    }
  }
}
```

---

## 6. Data Models

### User

Represents a registered user of the application.

```python
# Django Model
class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255, blank=True)
    avatar_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Django's AbstractUser provides: password, last_login, is_active, etc.
```

**Fields:**
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | UUID | Primary Key | Unique identifier |
| `email` | String | Unique, Required | User's email address |
| `password_hash` | String | Required | Bcrypt-hashed password |
| `full_name` | String | Optional | User's display name |
| `avatar_url` | URL | Optional | Profile picture URL |
| `created_at` | DateTime | Auto | Account creation timestamp |
| `updated_at` | DateTime | Auto | Last update timestamp |

**Relationships:**
- One-to-One with `UserPreferences`
- One-to-Many with `SavedWord`
- One-to-Many with `LookupHistory`
- One-to-Many with `ReadingSession`

---

### Word

Represents a dictionary word entry.

```python
class Word(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    word = models.CharField(max_length=255, unique=True, db_index=True)
    phonetic = models.CharField(max_length=255, blank=True)
    audio_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['word']),
        ]
```

**Fields:**
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | UUID | Primary Key | Unique identifier |
| `word` | String | Unique, Indexed | The word itself |
| `phonetic` | String | Optional | IPA pronunciation |
| `audio_url` | URL | Optional | Audio pronunciation URL |
| `created_at` | DateTime | Auto | First lookup timestamp |

**Relationships:**
- One-to-Many with `Definition`

---

### Definition

Represents a single definition for a word.

```python
class Definition(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    word = models.ForeignKey(Word, on_delete=models.CASCADE, related_name='definitions')
    part_of_speech = models.CharField(max_length=50)  # noun, verb, adjective, etc.
    meaning = models.TextField()
    example = models.TextField(blank=True)
    synonyms = ArrayField(models.CharField(max_length=100), blank=True, default=list)
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order']
```

**Fields:**
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | UUID | Primary Key | Unique identifier |
| `word_id` | UUID | Foreign Key | Reference to Word |
| `part_of_speech` | String | Required | noun, verb, adjective, etc. |
| `meaning` | Text | Required | The definition text |
| `example` | Text | Optional | Example sentence |
| `synonyms` | Array[String] | Optional | List of similar words |
| `order` | Integer | Default 0 | Display order |

---

### VocabularyEntry (SavedWord)

Represents a word saved to user's vocabulary.

```python
class VocabularyEntry(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='vocabulary')
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    meaning = models.TextField()  # Cached primary meaning
    saved_at = models.DateTimeField(auto_now_add=True)
    review_count = models.IntegerField(default=0)
    last_reviewed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        unique_together = ['user', 'word']
        ordering = ['-saved_at']
```

**Fields:**
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | UUID | Primary Key | Unique identifier |
| `user_id` | UUID | Foreign Key | Reference to User |
| `word_id` | UUID | Foreign Key | Reference to Word |
| `meaning` | Text | Required | Cached primary definition |
| `saved_at` | DateTime | Auto | When word was saved |
| `review_count` | Integer | Default 0 | Times reviewed |
| `last_reviewed_at` | DateTime | Optional | Last review timestamp |

**Constraints:**
- Unique together: (user_id, word_id) - user cannot save same word twice

---

### SearchHistory (LookupHistory)

Records each word lookup by a user.

```python
class SearchHistory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lookup_history')
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    looked_up_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-looked_up_at']
        indexes = [
            models.Index(fields=['user', '-looked_up_at']),
            models.Index(fields=['looked_up_at']),
        ]
```

**Fields:**
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | UUID | Primary Key | Unique identifier |
| `user_id` | UUID | Foreign Key | Reference to User |
| `word_id` | UUID | Foreign Key | Reference to Word |
| `looked_up_at` | DateTime | Auto, Indexed | Lookup timestamp |

**Note:** Unlike VocabularyEntry, the same word can appear multiple times in history.

---

### ReadingSession

Tracks user reading sessions for analytics.

```python
class ReadingSession(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reading_sessions')
    book_id = models.CharField(max_length=255, blank=True)  # External book reference
    book_title = models.CharField(max_length=500, blank=True)
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    duration_seconds = models.IntegerField(default=0)
    words_looked_up = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['-started_at']
```

**Fields:**
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | UUID | Primary Key | Unique identifier |
| `user_id` | UUID | Foreign Key | Reference to User |
| `book_id` | String | Optional | External book identifier |
| `book_title` | String | Optional | Book title for display |
| `started_at` | DateTime | Auto | Session start time |
| `ended_at` | DateTime | Optional | Session end time |
| `duration_seconds` | Integer | Default 0 | Total reading time |
| `words_looked_up` | Integer | Default 0 | Words looked up in session |

---

### UserPreferences

Stores user settings and preferences.

```python
class UserPreferences(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='preferences')
    is_dark_mode = models.BooleanField(default=False)
    language = models.CharField(max_length=10, default='en')
    notifications_enabled = models.BooleanField(default=True)
    font_size = models.CharField(max_length=20, default='medium')  # small, medium, large
    reading_line_height = models.FloatField(default=1.6)
```

**Fields:**
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | UUID | Primary Key | Unique identifier |
| `user_id` | UUID | Foreign Key, Unique | Reference to User |
| `is_dark_mode` | Boolean | Default False | Dark theme preference |
| `language` | String | Default 'en' | Preferred language |
| `notifications_enabled` | Boolean | Default True | Push notifications |
| `font_size` | String | Default 'medium' | Reading font size |
| `reading_line_height` | Float | Default 1.6 | Text line height |

---

### Entity Relationship Diagram

```
┌──────────────────┐       ┌──────────────────┐
│      User        │       │  UserPreferences │
├──────────────────┤       ├──────────────────┤
│ id (PK)          │───────│ user_id (FK, UK) │
│ email            │   1:1 │ is_dark_mode     │
│ password_hash    │       │ language         │
│ full_name        │       │ notifications    │
│ avatar_url       │       │ font_size        │
│ created_at       │       │ line_height      │
│ updated_at       │       └──────────────────┘
└────────┬─────────┘
         │
         │ 1:N
         ▼
┌──────────────────┐       ┌──────────────────┐
│ VocabularyEntry  │       │  SearchHistory   │
├──────────────────┤       ├──────────────────┤
│ id (PK)          │       │ id (PK)          │
│ user_id (FK)     │       │ user_id (FK)     │
│ word_id (FK)     │       │ word_id (FK)     │
│ meaning          │       │ looked_up_at     │
│ saved_at         │       └────────┬─────────┘
│ review_count     │                │
│ last_reviewed_at │                │
└────────┬─────────┘                │
         │                          │
         │ N:1                      │ N:1
         ▼                          ▼
┌──────────────────────────────────────────────┐
│                    Word                       │
├──────────────────────────────────────────────┤
│ id (PK)                                      │
│ word (UK, IDX)                               │
│ phonetic                                     │
│ audio_url                                    │
│ created_at                                   │
└────────────────────────┬─────────────────────┘
                         │
                         │ 1:N
                         ▼
                ┌──────────────────┐
                │   Definition     │
                ├──────────────────┤
                │ id (PK)          │
                │ word_id (FK)     │
                │ part_of_speech   │
                │ meaning          │
                │ example          │
                │ synonyms[]       │
                │ order            │
                └──────────────────┘

┌──────────────────┐
│  ReadingSession  │
├──────────────────┤
│ id (PK)          │
│ user_id (FK)     │ ──► User
│ book_id          │
│ book_title       │
│ started_at       │
│ ended_at         │
│ duration_seconds │
│ words_looked_up  │
└──────────────────┘
```

---

## 7. State Management Strategy

### Current Prototype (Local State)

The prototype uses React's `useState` for simplicity:

```typescript
// LexiFlowApp.tsx - Root state
const [currentScreen, setCurrentScreen] = useState<Screen>("login")
const [isLoggedIn, setIsLoggedIn] = useState(false)
const [isDarkMode, setIsDarkMode] = useState(false)

// ReadingScreen.tsx - Screen-level state
const [selectedWord, setSelectedWord] = useState<WordData | null>(null)
const [savedWords, setSavedWords] = useState<string[]>([])
```

### Recommended Production Strategy

For the production React Native app, use a layered state management approach:

#### Layer 1: Global State (Zustand)

For app-wide state that persists across screens:

```typescript
// stores/useAppStore.ts
import { create } from 'zustand'
import { persist, createJSONStorage } from 'zustand/middleware'
import AsyncStorage from '@react-native-async-storage/async-storage'

interface AppState {
  // Authentication
  user: User | null
  accessToken: string | null
  isAuthenticated: boolean
  
  // UI State
  isDarkMode: boolean
  currentScreen: Screen
  
  // Actions
  login: (credentials: LoginCredentials) => Promise<void>
  logout: () => void
  setScreen: (screen: Screen) => void
  toggleDarkMode: () => void
}

export const useAppStore = create<AppState>()(
  persist(
    (set, get) => ({
      user: null,
      accessToken: null,
      isAuthenticated: false,
      isDarkMode: false,
      currentScreen: 'login',
      
      login: async (credentials) => {
        const response = await authApi.login(credentials)
        set({
          user: response.user,
          accessToken: response.access_token,
          isAuthenticated: true,
          currentScreen: 'reading'
        })
      },
      
      logout: () => {
        set({
          user: null,
          accessToken: null,
          isAuthenticated: false,
          currentScreen: 'login'
        })
      },
      
      setScreen: (screen) => set({ currentScreen: screen }),
      toggleDarkMode: () => set((state) => ({ isDarkMode: !state.isDarkMode }))
    }),
    {
      name: 'lexiflow-app-storage',
      storage: createJSONStorage(() => AsyncStorage),
      partialize: (state) => ({
        user: state.user,
        accessToken: state.accessToken,
        isDarkMode: state.isDarkMode
      })
    }
  )
)
```

#### Layer 2: Server State (SWR or React Query)

For data that comes from the API:

```typescript
// hooks/useVocabulary.ts
import useSWR from 'swr'
import { vocabularyApi } from '@/api/vocabulary'

export function useVocabulary() {
  const { data, error, isLoading, mutate } = useSWR(
    '/api/vocabulary',
    vocabularyApi.getAll,
    {
      revalidateOnFocus: true,
      dedupingInterval: 5000,
    }
  )
  
  const saveWord = async (word: SaveWordRequest) => {
    await vocabularyApi.save(word)
    mutate() // Revalidate the cache
  }
  
  const removeWord = async (id: string) => {
    await vocabularyApi.remove(id)
    mutate()
  }
  
  return {
    words: data?.words ?? [],
    total: data?.total ?? 0,
    isLoading,
    error,
    saveWord,
    removeWord
  }
}

// hooks/useWordDefinition.ts
export function useWordDefinition(word: string | null) {
  const { data, error, isLoading } = useSWR(
    word ? `/api/words/${word}` : null,
    () => word ? wordsApi.lookup(word) : null,
    {
      revalidateOnFocus: false,
      dedupingInterval: 60000, // Cache definitions for 1 minute
    }
  )
  
  return {
    definition: data,
    isLoading,
    error,
    notFound: error?.code === 'WORD_NOT_FOUND'
  }
}
```

#### Layer 3: Local UI State (useState)

For component-specific, ephemeral state:

```typescript
// Inside a component
const [showPassword, setShowPassword] = useState(false)
const [searchQuery, setSearchQuery] = useState('')
const [isPopupVisible, setIsPopupVisible] = useState(false)
```

### State Flow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                     ZUSTAND STORE                            │
│  (Persisted to AsyncStorage)                                 │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ • user: User | null                                  │   │
│  │ • accessToken: string | null                         │   │
│  │ • isAuthenticated: boolean                           │   │
│  │ • isDarkMode: boolean                                │   │
│  │ • currentScreen: Screen                              │   │
│  └─────────────────────────────────────────────────────┘   │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           │ useAppStore()
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                    SWR / REACT QUERY                         │
│  (Cached API responses)                                      │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ • /api/vocabulary → words[], total                   │   │
│  │ • /api/history → items[], total                      │   │
│  │ • /api/words/{word} → definition                     │   │
│  │ • /api/user/stats → statistics                       │   │
│  └─────────────────────────────────────────────────────┘   │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           │ useSWR(), useQuery()
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                   COMPONENT STATE                            │
│  (Ephemeral UI state)                                        │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ • selectedWord: WordData | null                      │   │
│  │ • searchQuery: string                                │   │
│  │ • showPassword: boolean                              │   │
│  │ • isPopupVisible: boolean                            │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

---

## 8. Component Design Patterns

### Pattern 1: Container vs Presentational Components

**Container Components** handle logic and state:

```typescript
// containers/VocabularyContainer.tsx
export function VocabularyContainer() {
  const { words, isLoading, removeWord } = useVocabulary()
  const [searchQuery, setSearchQuery] = useState('')
  
  const filteredWords = useMemo(() => 
    words.filter(w => w.word.toLowerCase().includes(searchQuery.toLowerCase())),
    [words, searchQuery]
  )
  
  const handleDelete = async (id: string) => {
    await removeWord(id)
    // Show toast notification
  }
  
  return (
    <VocabularyScreen
      words={filteredWords}
      isLoading={isLoading}
      searchQuery={searchQuery}
      onSearchChange={setSearchQuery}
      onDelete={handleDelete}
    />
  )
}
```

**Presentational Components** are pure UI:

```typescript
// screens/VocabularyScreen.tsx
interface VocabularyScreenProps {
  words: SavedWord[]
  isLoading: boolean
  searchQuery: string
  onSearchChange: (query: string) => void
  onDelete: (id: string) => void
}

export function VocabularyScreen({ 
  words, 
  isLoading, 
  searchQuery, 
  onSearchChange, 
  onDelete 
}: VocabularyScreenProps) {
  return (
    <View>
      <SearchInput value={searchQuery} onChange={onSearchChange} />
      {isLoading ? (
        <LoadingSpinner />
      ) : (
        <WordList words={words} onDelete={onDelete} />
      )}
    </View>
  )
}
```

### Pattern 2: Reusable UI Primitives

Create atomic components that can be composed:

```typescript
// components/ui/Card.tsx
interface CardProps {
  children: React.ReactNode
  className?: string
  onPress?: () => void
}

export function Card({ children, className, onPress }: CardProps) {
  const Component = onPress ? TouchableOpacity : View
  return (
    <Component 
      onPress={onPress}
      className={cn(
        "bg-card rounded-xl border border-border p-3",
        className
      )}
    >
      {children}
    </Component>
  )
}

// components/ui/IconButton.tsx
interface IconButtonProps {
  icon: React.ComponentType<IconProps>
  onPress: () => void
  variant?: 'default' | 'ghost' | 'destructive'
  size?: 'sm' | 'md' | 'lg'
}

export function IconButton({ icon: Icon, onPress, variant = 'ghost', size = 'md' }: IconButtonProps) {
  return (
    <TouchableOpacity
      onPress={onPress}
      className={cn(
        "items-center justify-center rounded-lg",
        sizeStyles[size],
        variantStyles[variant]
      )}
    >
      <Icon className={iconSizeStyles[size]} />
    </TouchableOpacity>
  )
}
```

### Pattern 3: Component Composition

Compose complex components from primitives:

```typescript
// components/WordCard.tsx
interface WordCardProps {
  word: SavedWord
  onDelete: () => void
  onPress?: () => void
}

export function WordCard({ word, onDelete, onPress }: WordCardProps) {
  return (
    <Card onPress={onPress} className="flex-row items-center justify-between">
      <View className="flex-1 min-w-0">
        <View className="flex-row items-center gap-2">
          <Text className="font-medium text-foreground">{word.word}</Text>
          <Badge variant="muted">{word.savedAt}</Badge>
        </View>
        <Text className="text-xs text-muted-foreground mt-0.5 truncate">
          {word.meaning}
        </Text>
      </View>
      <IconButton 
        icon={Trash2} 
        onPress={onDelete}
        variant="ghost"
      />
    </Card>
  )
}

// Usage
<WordCard 
  word={word} 
  onDelete={() => handleDelete(word.id)}
  onPress={() => showDefinition(word)}
/>
```

### Pattern 4: Render Props for Flexible Layouts

```typescript
// components/BottomNavigation.tsx
interface BottomNavigationProps {
  activeScreen: Screen
  onNavigate: (screen: Screen) => void
}

export function BottomNavigation({ activeScreen, onNavigate }: BottomNavigationProps) {
  return (
    <View className="flex-row items-center justify-around py-3 border-t border-border bg-card">
      <NavItem 
        icon={Book} 
        label="Reading" 
        isActive={activeScreen === 'reading'}
        onPress={() => onNavigate('reading')}
      />
      <NavItem 
        icon={Bookmark} 
        label="Vocabulary" 
        isActive={activeScreen === 'vocabulary'}
        onPress={() => onNavigate('vocabulary')}
      />
      <NavItem 
        icon={Clock} 
        label="History" 
        isActive={activeScreen === 'history'}
        onPress={() => onNavigate('history')}
      />
      <NavItem 
        icon={Settings} 
        label="Settings" 
        isActive={activeScreen === 'settings'}
        onPress={() => onNavigate('settings')}
      />
    </View>
  )
}
```

### Pattern 5: Custom Hooks for Reusable Logic

```typescript
// hooks/useTappableText.ts
export function useTappableText(
  text: string,
  definableWords: string[],
  onWordTap: (word: string) => void
) {
  const segments = useMemo(() => {
    const words = text.split(/(\s+)/)
    return words.map((word, index) => {
      const cleanWord = word.replace(/[.,!?;:'"]/g, '')
      const isTappable = definableWords.some(
        w => w.toLowerCase() === cleanWord.toLowerCase()
      )
      return { text: word, isTappable, index }
    })
  }, [text, definableWords])
  
  return { segments, onWordTap }
}

// Usage in component
const { segments, onWordTap } = useTappableText(
  sampleText,
  definableWords,
  (word) => setSelectedWord(word)
)
```

---

## 9. Mobile Adaptation

### React Native Component Mapping

| Web (Next.js/React) | React Native | Notes |
|---------------------|--------------|-------|
| `<div>` | `<View>` | Container component |
| `<span>` | `<Text>` | Text must be in Text component |
| `<p>` | `<Text>` | Paragraphs are Text components |
| `<button>` | `<TouchableOpacity>` | Pressable wrapper |
| `<input>` | `<TextInput>` | Form input |
| `<img>` | `<Image>` | Image component |
| `<svg>` | `react-native-svg` | SVG library needed |
| `onClick` | `onPress` | Touch handler |
| CSS classes | NativeWind or StyleSheet | Styling approach |

### Styling with NativeWind

NativeWind brings Tailwind CSS to React Native:

```typescript
// Install: npm install nativewind tailwindcss

// Before (Web)
<div className="flex items-center justify-between p-4 bg-card rounded-xl">
  <span className="text-sm font-medium text-foreground">Hello</span>
</div>

// After (React Native with NativeWind)
<View className="flex-row items-center justify-between p-4 bg-card rounded-xl">
  <Text className="text-sm font-medium text-foreground">Hello</Text>
</View>
```

### Key Differences

#### 1. Flexbox Direction

```typescript
// Web: flex-direction is row by default
<div className="flex items-center">

// React Native: flex-direction is column by default
<View className="flex-row items-center">
```

#### 2. Text Handling

```typescript
// Web: Text can be inline
<span>Hello <span className="font-bold">world</span></span>

// React Native: Nested Text required
<Text>Hello <Text className="font-bold">world</Text></Text>
```

#### 3. Scrolling

```typescript
// Web: div with overflow-y-auto
<div className="flex-1 overflow-y-auto">

// React Native: ScrollView or FlatList
<ScrollView className="flex-1">
<FlatList data={items} renderItem={...} />
```

#### 4. Input Components

```typescript
// Web
<input 
  type="email"
  placeholder="Email"
  className="pl-10 h-12"
  onChange={(e) => setEmail(e.target.value)}
/>

// React Native
<TextInput
  keyboardType="email-address"
  placeholder="Email"
  className="pl-10 h-12"
  onChangeText={setEmail}
/>
```

### Screen Conversion Example

**Web (reading-screen.tsx):**
```tsx
export function ReadingScreen({ onNavigate }: Props) {
  return (
    <div className="h-full flex flex-col bg-background">
      <div className="flex items-center justify-between px-4 py-3 border-b border-border">
        <button onClick={() => {}}>
          <ChevronLeft className="h-5 w-5" />
        </button>
        <span className="text-sm font-medium">The Silent Garden</span>
      </div>
      <div className="flex-1 overflow-y-auto px-5 py-6">
        <p className="text-sm leading-relaxed">{text}</p>
      </div>
    </div>
  )
}
```

**React Native (ReadingScreen.tsx):**
```tsx
export function ReadingScreen({ onNavigate }: Props) {
  return (
    <View className="flex-1 bg-background">
      <View className="flex-row items-center justify-between px-4 py-3 border-b border-border">
        <TouchableOpacity onPress={() => {}}>
          <ChevronLeft className="h-5 w-5" />
        </TouchableOpacity>
        <Text className="text-sm font-medium">The Silent Garden</Text>
      </View>
      <ScrollView className="flex-1 px-5 py-6">
        <Text className="text-sm leading-relaxed">{text}</Text>
      </ScrollView>
    </View>
  )
}
```

### Navigation Setup

Use React Navigation for screen management:

```typescript
// navigation/AppNavigator.tsx
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs'
import { createNativeStackNavigator } from '@react-navigation/native-stack'

const Tab = createBottomTabNavigator()
const Stack = createNativeStackNavigator()

function MainTabs() {
  return (
    <Tab.Navigator>
      <Tab.Screen name="Reading" component={ReadingScreen} />
      <Tab.Screen name="Vocabulary" component={VocabularyScreen} />
      <Tab.Screen name="History" component={HistoryScreen} />
      <Tab.Screen name="Settings" component={SettingsScreen} />
    </Tab.Navigator>
  )
}

export function AppNavigator() {
  const { isAuthenticated } = useAppStore()
  
  return (
    <Stack.Navigator screenOptions={{ headerShown: false }}>
      {!isAuthenticated ? (
        <Stack.Screen name="Login" component={LoginScreen} />
      ) : (
        <Stack.Screen name="Main" component={MainTabs} />
      )}
    </Stack.Navigator>
  )
}
```

### Bottom Sheet for Word Definition

Use `@gorhom/bottom-sheet` for the word definition popup:

```typescript
import BottomSheet, { BottomSheetView } from '@gorhom/bottom-sheet'

export function WordDefinitionSheet({ word, onClose }: Props) {
  const bottomSheetRef = useRef<BottomSheet>(null)
  const snapPoints = useMemo(() => ['50%', '80%'], [])
  
  return (
    <BottomSheet
      ref={bottomSheetRef}
      snapPoints={snapPoints}
      enablePanDownToClose
      onClose={onClose}
    >
      <BottomSheetView className="p-5">
        <View className="flex-row items-center justify-between mb-4">
          <Text className="text-xl font-semibold capitalize">{word.word}</Text>
          <TouchableOpacity onPress={onClose}>
            <X className="h-5 w-5" />
          </TouchableOpacity>
        </View>
        {/* Definition content */}
      </BottomSheetView>
    </BottomSheet>
  )
}
```

---

## 10. Development Recommendations

### Frontend Architecture

1. **Use Feature-Based Folder Structure**
   ```
   src/
   ├── features/
   │   ├── auth/
   │   │   ├── components/
   │   │   ├── hooks/
   │   │   ├── screens/
   │   │   └── api.ts
   │   ├── reading/
   │   ├── vocabulary/
   │   └── settings/
   ├── shared/
   │   ├── components/
   │   ├── hooks/
   │   └── utils/
   └── navigation/
   ```

2. **Implement Proper TypeScript Types**
   - Define strict types for all API responses
   - Use Zod schemas for runtime validation
   - Create type-safe API client

3. **Use Absolute Imports**
   ```json
   // tsconfig.json
   {
     "compilerOptions": {
       "baseUrl": ".",
       "paths": {
         "@/*": ["src/*"],
         "@components/*": ["src/shared/components/*"],
         "@features/*": ["src/features/*"]
       }
     }
   }
   ```

### API Consumption

1. **Create Type-Safe API Client**
   ```typescript
   // api/client.ts
   import axios from 'axios'
   import { useAppStore } from '@/stores/useAppStore'
   
   const apiClient = axios.create({
     baseURL: 'https://api.lexiflow.app',
     timeout: 10000,
   })
   
   apiClient.interceptors.request.use((config) => {
     const token = useAppStore.getState().accessToken
     if (token) {
       config.headers.Authorization = `Bearer ${token}`
     }
     return config
   })
   
   apiClient.interceptors.response.use(
     (response) => response,
     async (error) => {
       if (error.response?.status === 401) {
         // Handle token refresh or logout
       }
       return Promise.reject(error)
     }
   )
   
   export { apiClient }
   ```

2. **Use SWR for Data Fetching**
   ```typescript
   // Configure SWR globally
   <SWRConfig
     value={{
       fetcher: (url) => apiClient.get(url).then(res => res.data),
       onError: (error) => {
         // Global error handling
         if (error.code === 'NETWORK_ERROR') {
           showToast('Network error. Please check your connection.')
         }
       },
       revalidateOnFocus: true,
       dedupingInterval: 5000,
     }}
   >
   ```

### Error Handling

1. **Create Error Boundary**
   ```typescript
   import { ErrorBoundary } from 'react-error-boundary'
   
   function ErrorFallback({ error, resetErrorBoundary }) {
     return (
       <View className="flex-1 items-center justify-center p-6">
         <Text className="text-destructive text-lg font-semibold mb-2">
           Something went wrong
         </Text>
         <Text className="text-muted-foreground text-center mb-4">
           {error.message}
         </Text>
         <Button onPress={resetErrorBoundary}>Try Again</Button>
       </View>
     )
   }
   ```

2. **Handle API Errors Gracefully**
   ```typescript
   const { data, error, isLoading } = useSWR(...)
   
   if (error) {
     if (error.code === 'WORD_NOT_FOUND') {
       return <NotFoundMessage word={searchedWord} />
     }
     if (error.code === 'NETWORK_ERROR') {
       return <OfflineMessage onRetry={refetch} />
     }
     return <GenericError error={error} />
   }
   ```

### Loading States

1. **Use Skeleton Loaders**
   ```typescript
   function WordCardSkeleton() {
     return (
       <Card className="flex-row items-center">
         <View className="flex-1">
           <View className="h-4 w-24 bg-muted rounded animate-pulse" />
           <View className="h-3 w-40 bg-muted rounded mt-2 animate-pulse" />
         </View>
       </Card>
     )
   }
   
   // Usage
   {isLoading ? (
     Array(5).fill(0).map((_, i) => <WordCardSkeleton key={i} />)
   ) : (
     words.map(word => <WordCard key={word.id} word={word} />)
   )}
   ```

2. **Optimistic Updates**
   ```typescript
   const saveWord = async (word: SaveWordRequest) => {
     // Optimistically update UI
     mutate(
       (current) => ({
         ...current,
         words: [...current.words, { ...word, id: 'temp-id', saving: true }]
       }),
       false // Don't revalidate yet
     )
     
     try {
       await vocabularyApi.save(word)
       mutate() // Revalidate after success
     } catch (error) {
       mutate() // Revert on error
       throw error
     }
   }
   ```

### Offline Support

1. **Cache API Responses**
   ```typescript
   import AsyncStorage from '@react-native-async-storage/async-storage'
   
   const offlineCache = {
     get: async (key: string) => {
       const data = await AsyncStorage.getItem(`cache:${key}`)
       return data ? JSON.parse(data) : null
     },
     set: async (key: string, data: any, ttl: number = 3600000) => {
       await AsyncStorage.setItem(`cache:${key}`, JSON.stringify({
         data,
         expiresAt: Date.now() + ttl
       }))
     }
   }
   ```

2. **Queue Offline Actions**
   ```typescript
   import NetInfo from '@react-native-community/netinfo'
   
   const actionQueue = create((set, get) => ({
     queue: [],
     addAction: (action) => set(state => ({
       queue: [...state.queue, action]
     })),
     processQueue: async () => {
       const { isConnected } = await NetInfo.fetch()
       if (isConnected) {
         for (const action of get().queue) {
           await action.execute()
         }
         set({ queue: [] })
       }
     }
   }))
   ```

3. **Show Offline Indicator**
   ```typescript
   function useNetworkStatus() {
     const [isOnline, setIsOnline] = useState(true)
     
     useEffect(() => {
       const unsubscribe = NetInfo.addEventListener(state => {
         setIsOnline(state.isConnected ?? true)
       })
       return unsubscribe
     }, [])
     
     return { isOnline }
   }
   
   // In app root
   {!isOnline && (
     <View className="bg-destructive/10 px-4 py-2">
       <Text className="text-destructive text-xs text-center">
         You are offline. Some features may be unavailable.
       </Text>
     </View>
   )}
   ```

### Performance Optimizations

1. **Memoize Expensive Computations**
   ```typescript
   const filteredWords = useMemo(
     () => words.filter(w => w.word.includes(searchQuery)),
     [words, searchQuery]
   )
   ```

2. **Use FlatList for Long Lists**
   ```typescript
   <FlatList
     data={words}
     keyExtractor={(item) => item.id}
     renderItem={({ item }) => <WordCard word={item} />}
     initialNumToRender={10}
     maxToRenderPerBatch={10}
     windowSize={5}
     getItemLayout={(data, index) => ({
       length: 72, // Item height
       offset: 72 * index,
       index
     })}
   />
   ```

3. **Lazy Load Heavy Components**
   ```typescript
   const WordDefinitionPopup = lazy(() => import('./WordDefinitionPopup'))
   
   // Usage
   <Suspense fallback={<LoadingSpinner />}>
     {selectedWord && <WordDefinitionPopup word={selectedWord} />}
   </Suspense>
   ```

---

## Appendix: Quick Reference

### Common Commands

```bash
# Development
pnpm dev                    # Start dev server
pnpm build                  # Production build
pnpm lint                   # Run ESLint

# React Native
npx react-native start      # Start Metro bundler
npx react-native run-ios    # Run on iOS simulator
npx react-native run-android # Run on Android emulator

# Django
python manage.py runserver  # Start dev server
python manage.py migrate    # Run migrations
python manage.py createsuperuser # Create admin user
```

### Environment Variables

```env
# Frontend (.env.local)
NEXT_PUBLIC_API_URL=https://api.lexiflow.app
NEXT_PUBLIC_SENTRY_DSN=...

# Backend (.env)
DATABASE_URL=postgres://user:pass@localhost:5432/lexiflow
REDIS_URL=redis://localhost:6379
SECRET_KEY=your-secret-key
JWT_SECRET=your-jwt-secret
```

### API Response Format

All API responses follow this format:

```typescript
interface ApiResponse<T> {
  success: boolean
  data?: T
  error?: {
    code: string
    message: string
    details?: Record<string, string[]>
  }
  meta?: {
    cached?: boolean
    cache_expires_at?: string
  }
}

interface PaginatedResponse<T> extends ApiResponse<{ items: T[] }> {
  data: {
    items: T[]
    pagination: {
      total: number
      page: number
      limit: number
      total_pages: number
    }
  }
}
```

---

*Document Version: 1.0.0*
*Last Updated: March 13, 2026*
*Generated for: LexiFlow Reading Assistant*
