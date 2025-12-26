# Music Recommender - Frontend

A modern and elegant user interface for the intelligent music recommendation system. Built with React, TypeScript, and Vite, it offers a premium experience with both traditional search and AI-powered magic search.

## Table of Contents

- [Core Features](#core-features)
- [Tech Stack](#tech-stack)
- [Installation and Configuration](#installation-and-configuration)
- [Running the Project](#running-the-project)
- [Component Architecture](#component-architecture)
- [Main Functionalities](#main-functionalities)
- [State Management](#state-management)
- [Backend Integration](#backend-integration)
- [Design and Styles](#design-and-styles)

---

## Core Features

- **Dual Search**:
  - **Traditional Search**: Search songs by name or artist.
  - **Magic Search ✨**: Describe the type of music you're looking for in natural language, and AI will find the perfect songs.

- **Integrated Audio Player**: 
  - Plays 30-second previews from Deezer.
  - Play/Pause controls.
  - Visual playback indicator.

- **Personalized Recommendations**:
  - Select multiple favorite songs.
  - Get recommendations based on musical similarity.
  - ML algorithm that analyzes 10+ audio features.

- **Premium Design**:
  - Automatic Dark/Light mode.
  - Smooth animations and micro-interactions.
  - Responsive design (mobile-first).
  - Modern gradients.

- **Optimized Performance**:
  - Lazy loading for songs.
  - Efficient state management with Zustand.
  - Hot Module Replacement (HMR) during development.

---

## Tech Stack

### Core
- **React 19.2**: UI library with the latest features.
- **TypeScript 5.9**: Static typing for increased robustness.
- **Vite 7.2**: Ultra-fast build tool with HMR.

### State Management
- **Zustand 5.0**: Lightweight and simple state management.

### Styling
- **TailwindCSS 3.4**: Utility-first CSS framework.
- **PostCSS + Autoprefixer**: CSS processing.
- **CSS Custom Properties**: Variables for dynamic themes.

### HTTP Client
- **Axios 1.13**: HTTP client with interceptors.

### Utilities
- **clsx**: Conditional CSS class composition.
- **tailwind-merge**: Intelligent merging for Tailwind classes.

### Development
- **ESLint**: Linter with rules for React and TypeScript.
- **Vite Plugin React**: Support for Fast Refresh.

---

## Installation and Configuration

### Prerequisites

- **Node.js 18+** or **Bun 1.0+**
- **npm**, **yarn**, **pnpm**, or **bun**

### 1. Clone the repository

```bash
git clone <repository-url>
cd music-recommender/frontend
```

### 2. Install dependencies

With **bun** (recommended):
```bash
bun install
```

With **npm**:
```bash
npm install
```

With **yarn**:
```bash
yarn install
```

With **pnpm**:
```bash
pnpm install
```

### 3. Configure environment variables (optional)

Create a `.env` file in the `frontend/` root directory if you need to customize the backend URL:

```env
VITE_API_URL=http://localhost:8000/api/v1
```

By default, the application points to `http://localhost:8000/api/v1`.

---

##  Running the Project

### Development Mode

With **bun**:
```bash
bun run dev
```

With **npm**:
```bash
npm run dev
```

The application will be available at: **http://localhost:5173**

### Build for Production

```bash
bun run build
# or
npm run build
```

The optimized files will be generated in the `dist/` directory.

### Preview the Build

```bash
bun run preview
# or
npm run preview
```

### Linting

```bash
bun run lint
# or
npm run lint
```

---

## Component Architecture

```
src/
├── components/           # React Components
│   ├── Header.tsx        # Top navigation bar
│   ├── Hero.tsx          # Hero section with search
│   ├── SongList.tsx      # Song list with selection
│   └── PlayerBar.tsx     # Fixed audio player
│
├── store/                # State management
│   └── musicStore.ts     # Main Zustand store
│
├── api/                  # HTTP Services
│   └── musicApi.ts       # Axios client and endpoints
│
├── types/                # TypeScript Definitions
│   └── song.ts           # Song interfaces
│
├── resources/            # Static resources
│   └── music.svg         # Icons and assets
│
├── App.tsx               # Root component
├── main.tsx              # Entry point
├── index.css             # Global styles and Tailwind
└── App.css               # App-specific styles
```

### Data Flow

```
User interacts with UI
    ↓
[React Component]
    ↓
[Zustand Store] (dispatch action)
    ↓
[API Service] (Axios)
    ↓
[Backend API]
    ↓
[Store updates state]
    ↓
[Component re-renders]
```

---

## Main Functionalities

### 1. Header

**Component**: `Header.tsx`

**Features**:
- App logo and title.
- Responsive design with gradient.
- Sticky header with backdrop blur.

### 2. Hero Section (Search)

**Component**: `Hero.tsx`

**Search Modes**:

#### Normal Mode (Traditional Search)
- **Input**: Song name or artist.
- **Action**: Searches in the database.
- **Endpoint**: `GET /songs/?search={query}`
- **Usage**: Explore the existing catalog.

#### Magic Mode ✨ (AI-powered Search)
- **Input**: Natural language description.
  - Examples:
    - "relaxing music to study"
    - "happy summer songs"
    - "energetic music for the gym"
    - "sad songs to cry to"
- **Action**: The LLM extracts musical features and searches for similar songs.
- **Endpoint**: `POST /recommend/text`
- **Process**:
  1. User writes a description.
  2. Backend uses Gemini to extract features (danceability, energy, valence, etc.).
  3. KNN algorithm searches for songs with those characteristics.
  4. Returns top 10 recommendations.

**Magic Toggle**:
- Button with `auto_awesome` (✨) icon.
- Pulse animation when active.
- Changes placeholder and input behavior.

**Loading Indicator**:
- Spinner in search button.
- "Sparkles" animation when in magic mode.
- Message: "Generating magic recommendations..."

### 3. Song List

**Component**: `SongList.tsx`

**Features**:
- **Multiple selection**: Click on songs to select them.
- **Visual indicator**: Blue border and checkmark on selected songs.
- **Displayed Information**:
  - Song name
  - Artist
  - Album
  - Popularity (progress bar)
  - Musical features (danceability, energy, valence)
- **Recommendation button**: Appears when there are selected songs.
- **Lazy loading**: Loads more songs on scroll.

**Interactions**:
1. **Click on song**: Select/deselect.
2. **Click on "Get Recommendations"**: 
   - Sends selected song IDs to the backend.
   - Endpoint: `POST /recommend/`
   - Receives similar songs based on ML.

### 4. Player Bar

**Component**: `PlayerBar.tsx`

**Features**:
- **Fixed position**: Always visible at the bottom.
- **Current song info**:
  - Album cover (placeholder)
  - Song name
  - Artist
- **Controls**:
  - Play/Pause
  - Playback indicator
- **Spotify Integration**:
  - Uses 30-second previews.
  - Endpoint: `GET /music/audio/{track_id}`

**States**:
- No song: Shows placeholder.
- Loading: Spinner.
- Playing: Pause button.
- Paused: Play button.

---

## State Management

### Zustand Store

**File**: `src/store/musicStore.ts`

**Global State**:

```typescript
interface MusicStore {
  // Data
  songs: Song[];              // Current song list
  selectedSongs: Song[];      // Selected songs
  currentSong: Song | null;   // Song currently playing
  
  // UI State
  isPlaying: boolean;         // Player state
  isLoading: boolean;         // Loading indicator
  isMagicMode: boolean;       // Active search mode
  
  // Actions
  fetchSongs: (offset, limit, search?) => Promise<void>;
  toggleSongSelection: (song: Song) => void;
  getRecommendations: () => Promise<void>;
  getMagicRecommendations: (text: string) => Promise<void>;
  playSong: (song: Song) => Promise<void>;
  togglePlayPause: () => void;
  toggleMagicMode: () => void;
}
```

**Benefits of Zustand**:
- Zero boilerplate (no actions, reducers, providers).
- TypeScript-first.
- Integrated DevTools.
- Optimized performance (minimal re-renders).

### Action Flow

#### Normal Search
```typescript
fetchSongs(0, 10, "Beatles")
  ↓
GET /songs/?search=Beatles
  ↓
songs = response.data
```

#### Magic Search
```typescript
getMagicRecommendations("concentration music")
  ↓
POST /recommend/text { text_input: "concentration music" }
  ↓
LLM extracts features → KNN searches for similar
  ↓
songs = recommendations
```

#### Recommendations by Song
```typescript
getRecommendations()
  ↓
song_ids = selectedSongs.map(s => s.track_id)
  ↓
POST /recommend/ { song_ids: [...], limit: 10 }
  ↓
songs = recommendations
```

---

## Backend Integration

### API Client

**File**: `src/api/client.ts`

**Axios Configuration**:

```typescript
const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});
```

### Used Endpoints

| Method | Endpoint | Description | Used in |
|--------|----------|-------------|----------|
| GET | `/songs/` | Search songs | `fetchSongs()` |
| POST | `/recommend/` | Recommendations by song | `getRecommendations()` |
| POST | `/recommend/text` | Recommendations by text (AI) | `getMagicRecommendations()` |
| GET | `/music/audio/{track_id}` | Spotify audio preview | `playSong()` |

### Error Handling

```typescript
try {
  const response = await api.post('/recommend/text', { text_input });
  return response.data;
} catch (error) {
  console.error('Error getting magic recommendations:', error);
  // UI shows error message
  throw error;
}
```

---

## Design and Styles

### Design System

**Main Colors**:
- **Primary**: `#0d33f2` (Vibrant blue)
- **Purple**: `#a855f7` (Purple accent)
- **Gradients**: Combinations of primary and purple.

**Dark Mode**:
- Background: `#0a0e1a` (Deep dark blue)
- Cards: `#101322` (Medium dark blue)
- Borders: `#222949` (Grayish blue)
- Text: `#ffffff` / `#909acb` (White / Bluish gray)

**Light Mode**:
- Background: `#f8fafc` (Very light gray)
- Cards: `#ffffff` (White)
- Borders: `#e2e8f0` (Light gray)
- Text: `#0f172a` / `#64748b` (Dark blue / Gray)

### Typography

- **Font Family**: System fonts (`-apple-system`, `BlinkMacSystemFont`, `Segoe UI`, etc.).
- **Weights**: 400 (normal), 500 (medium), 600 (semibold), 700 (bold), 900 (black).

### Icons

**Google Material Symbols**:
```html
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined" rel="stylesheet" />
```

Icons used:
- `search`: Search
- `auto_awesome`: Magic mode
- `play_arrow`: Play
- `pause`: Pause
- `check_circle`: Selected song
- `progress_activity`: Loading

### Animations

**Custom Animations** (in `index.css`):

```css
@keyframes pulse-glow {
  0%, 100% { box-shadow: 0 0 20px rgba(13, 51, 242, 0.5); }
  50% { box-shadow: 0 0 30px rgba(168, 85, 247, 0.8); }
}

@keyframes sparkle {
  0%, 100% { transform: scale(0); opacity: 0; }
  50% { transform: scale(1); opacity: 1; }
}
```

**Transitions**:
- `transition-all`: Smooth changes for colors, sizes, etc.
- `hover:scale-105`: Hover effect on buttons.
- `active:scale-95`: Tactile feedback on clicks.

### Responsive Design

**Breakpoints** (Tailwind):
- `sm`: 640px
- `md`: 768px
- `lg`: 1024px
- `xl`: 1280px

**Mobile-First Strategy**:
```tsx
<h2 className="text-2xl sm:text-4xl">
  // Mobile: 2xl, Desktop: 4xl
</h2>
```

---

## Enjoy the Music

Explore, discover, and enjoy personalized AI-powered music recommendations! 🎧✨
