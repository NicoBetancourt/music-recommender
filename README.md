# Music Recommender

An intelligent music recommendation system that combines **Machine Learning** with **Generative Artificial Intelligence** to offer personalized recommendations based on musical features and natural language descriptions.

## Key Features

- ** Dual Recommendations**:
  - **Traditional ML**: Based on musical feature similarity (K-Nearest Neighbors).
  - **Generative AI**: Natural language description → Musical features → Recommendations.

- ** Premium Interface**: Modern design with dark mode, smooth animations, and micro-interactions.

- ** Intelligent Search**: 
  - Traditional search by name/artist.
  - Magic search utilizing natural language processing.

- ** Integrated Player**: Spotify audio previews directly within the application.

- ** 30,000+ Songs**: Comprehensive Spotify dataset with detailed audio features available [here](https://www.kaggle.com/datasets/bricevergnou/spotify-recommendation).

---

##  Project Architecture

```
music-recommender/
├── backend/              # FastAPI API + ML + LLM
│   ├── src/
│   │   ├── api/         # REST Endpoints
│   │   ├── services/    # Business logic
│   │   ├── agents/      # LLM Agent (Gemini)
│   │   ├── repositories/# Data access
│   │   └── domain/      # Models and schemas
│   └── README.md        # Detailed backend documentation
│
└── frontend/            # React + TypeScript + Vite
    ├── src/
    │   ├── components/  # UI Components
    │   ├── store/       # State management (Zustand)
    │   └── api/         # HTTP Client
    └── README.md        # Detailed frontend documentation
```

---

## Quick Start

### Prerequisites

- **Backend**:
  - Python 3.13+
  - uv (package manager)
  - Google Gemini API Key
  - Deezer API Credentials (optional, for previews)

- **Frontend**:
  - Node.js 18+ or Bun 1.0+
  - npm/yarn/pnpm/bun

### 1. Clone the Repository

```bash
git clone <repository-url>
cd music-recommender
```

### 2. Configure Backend

```bash
cd backend

# Create virtual environment
uv venv

# Install dependencies
uv sync

# Configure environment variables
cp .env.example .env
# Edit .env with your API keys

# Run migrations
uv run alembic upgrade head

# Start development server
fastapi dev
```

The backend will be available at: **http://localhost:8000**

### 3. Configure Frontend

```bash
cd frontend

# Install dependencies
bun install
# or npm install

# Start development server
bun run dev
# or npm run dev
```

The frontend will be available at: **http://localhost:5173**

---

## Detailed Documentation

### Backend
Refer to [`backend/README.md`](./backend/README.md) for:
- Clean Architecture breakdown.
- API Endpoint details.
- ML Recommendation System (KNN).
- LLM Agent for feature extraction.
- Machine Learning model explanation.
- Advanced configuration.

### Frontend
Refer to [`frontend/README.md`](./frontend/README.md) for:
- Component architecture.
- Dual search functionality details.
- State management with Zustand.
- Backend integration.
- Design system and styles.

---

## Use Cases

### 1. Recommendation by Similar Songs

**Scenario**: You have favorite songs and want to discover similar music.

**Flow**:
1. Search for your favorite songs in the application.
2. Select multiple songs (click on them).
3. Click on "Get Recommendations".
4. The system analyzes musical features (danceability, energy, valence, etc.).
5. KNN algorithm finds the 10 most similar songs.
6. Play and discover new music.

**Technology**: K-Nearest Neighbors with 10 audio features.

---

### 2. Recommendation by Natural Description

**Scenario**: You know what type of music you want but don't know specific songs.

**Flow**:
1. Activate "Magic Search" (✨) mode.
2. Describe in natural language:
   - "relaxing music to concentrate while studying"
   - "happy summer songs for a party"
   - "energetic music for a gym workout"
   - "sad but hopeful songs"
3. The LLM (Gemini) extracts musical features from the text.
4. The system searches for songs matching those features.
5. Get recommendations perfectly aligned with your description.

**Technology**: Google Gemini + Pydantic AI + K-Nearest Neighbors.

---

## How It Works

### Hybrid Recommendation System

```
┌─────────────────────────────────────────────────────────┐
│                      USER                               │
└────────────┬───────────────────────────┬─-──────────────┘
             │                           │
             │                           │
    ┌────────▼────────┐          ┌───────▼────────┐
    │  Select         │          │  Describe in   │
    │  Songs          │          │  Natural Text  │
    └────────┬────────┘          └───────┬────────┘
             │                           │
             │                           │
    ┌────────▼────────┐          ┌───────▼────────┐
    │  Extract        │          │  LLM (Gemini)  │
    │  Musical        │          │  Extract       │
    │  Features       │          │  Features      │
    └────────┬────────┘          └───────┬────────┘
             │                           │
             └────────────┬──────────────┘
                          │
                 ┌────────▼────────┐
                 │  Numerical      │
                 │  Features       │
                 │  (10 dims)      │
                 └────────┬────────┘
                          │
                 ┌────────▼────────┐
                 │  K-Nearest      │
                 │  Neighbors      │
                 │  (Ball Tree)    │
                 └────────┬────────┘
                          │
                 ┌────────▼────────┐
                 │  Recommended    │
                 │  Songs          │
                 └─────────────────┘
```

### Musical Features Utilized

The system analyzes **10 attributes** for each song:

| Feature | Description | Range |
|---------|-------------|-------|
| **danceability** | How suitable a track is for dancing | 0.0 - 1.0 |
| **energy** | Perceived intensity and activity | 0.0 - 1.0 |
| **key** | Musical pitch class (C, C#, D, etc.) | 0 - 11 |
| **loudness** | Overall volume in decibels | -60 to 0 dB |
| **speechiness** | Presence of spoken words | 0.0 - 1.0 |
| **acousticness** | Acoustic vs. electronic level | 0.0 - 1.0 |
| **instrumentalness** | Absence of vocals | 0.0 - 1.0 |
| **liveness** | Presence of a live audience | 0.0 - 1.0 |
| **valence** | Musical positivity (happy/sad) | 0.0 - 1.0 |
| **tempo** | Speed in BPM | 50 - 200+ |

---

## Full Tech Stack

### Backend
- **Framework**: FastAPI (Python 3.13)
- **ORM**: SQLAlchemy 2.0 (Async)
- **Database**: SQLite (via aiosqlite)
- **ML**: scikit-learn (K-Nearest Neighbors)
- **LLM**: Google Gemini 2.0 Flash
- **AI Framework**: Pydantic AI
- **Validation**: Pydantic V2
- **Migrations**: Alembic
- **HTTP Client**: httpx
- **Package Manager**: uv (Astral)

### Frontend
- **Framework**: React 19.2
- **Language**: TypeScript 5.9
- **Build Tool**: Vite 7.2
- **State Management**: Zustand 5.0
- **Styles**: TailwindCSS 3.4
- **HTTP Client**: Axios 1.13
- **Runtime**: Bun (optional, compatible with Node.js)

---

## LLM Usage Examples

### User Input → Extracted Features

| Description | Key Features |
|-------------|--------------|
| "music for concentration" | `instrumentalness`: 0.9<br>`energy`: 0.3<br>`speechiness`: 0.05 |
| "summer party" | `danceability`: 0.85<br>`energy`: 0.8<br>`valence`: 0.9 |
| "sad songs" | `valence`: 0.1<br>`mode`: 0 (minor)<br>`energy`: 0.3 |
| "gym workout" | `energy`: 0.95<br>`tempo`: 140<br>`acousticness`: 0.1 |
| "relaxing music" | `energy`: 0.15<br>`tempo`: 60<br>`valence`: 0.5 |

---

## Screenshots

### Normal Search
<img width="2558" height="1434" alt="image" src="https://github.com/user-attachments/assets/6ea4ef46-5a9c-4fdb-882d-db6e87e3b325" />

### Magic Search
<img width="2558" height="1434" alt="image" src="https://github.com/user-attachments/assets/b27e55e6-b1a0-4fde-a7be-5ada4ac52172" />

---

<img width="2558" height="1434" alt="image" src="https://github.com/user-attachments/assets/ad7a2953-d732-432d-88ac-0fa2b051653e" />


### Recommendations
<img width="2558" height="1434" alt="image" src="https://github.com/user-attachments/assets/7f631974-2da1-4ea9-ae95-b60a49e3f2b4" />


### Player
<img width="2628" height="768" alt="image" src="https://github.com/user-attachments/assets/0091eff8-5c06-4d1c-8edc-ead8bbf5fddb" />


---

## Environment Variables

### Backend (`.env`)

```env
# App
PROJECT_NAME="Music Recommender API"
API_V1_STR="/api/v1"

# Database
DATABASE_URL="sqlite+aiosqlite:///./music_recommender.db"

# Spotify API (deprecated)
SPOTIFY_BASIC_AUTHENTICATION="your_spotify_basic_auth"

# Google Gemini
GOOGLE_API_KEY="your_api_key"
MODEL="gemini-2.5-flash"

# Monitoring (optional)
LOGFIRE=false
```

### Frontend (`.env`)

```env
VITE_API_URL=http://localhost:8000/api/v1
```

---

## Testing

### Backend

```bash
cd backend
uv run pytest
```

### Frontend

```bash
cd frontend
bun test
# or npm test
```

---

## Deployment

### Backend (Docker)

```bash
cd backend
docker build -t music-recommender-api .
docker run -p 8000:8000 music-recommender-api
```

### Frontend (Vercel/Netlify)

```bash
cd frontend
bun run build
# Upload dist/ folder to Vercel/Netlify
```

---

## Resources and References

- **FastAPI**: https://fastapi.tiangolo.com/
- **Pydantic AI**: https://ai.pydantic.dev/
- **scikit-learn**: https://scikit-learn.org/
- **React**: https://react.dev/
- **Vite**: https://vitejs.dev/
- **TailwindCSS**: https://tailwindcss.com/
- **Spotify Web API**: https://developer.spotify.com/documentation/web-api/
- **Deezer Web API**: https://developers.deezer.com/api/
- **Google Gemini**: https://ai.google.dev/

---

## Acknowledgments

- Spotify dataset provided by the Kaggle community.
- Google for Gemini API access.
- Spotify and Deezer for their music API.
- The open-source community for incredible tools.

---

## Author

**Nico Betancourt**
