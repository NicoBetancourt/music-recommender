# Music Recommender API - Backend

An intelligent music recommendation system that combines Machine Learning with natural language processing via LLM to offer personalized recommendations based on musical features and textual descriptions.

## 📋 Table of Contents

- [Core Features](#-core-features)
- [Tech Stack](#-tech-stack)
- [Project Architecture](#-project-architecture)
- [Installation and Configuration](#-installation-and-configuration)
- [Running the Service](#-running-the-service)
- [API Endpoints](#-api-endpoints)
- [Recommendation System](#-recommendation-system)
- [LLM Agent for Feature Extraction](#-llm-agent-for-feature-extraction)
- [Machine Learning Model](#-machine-learning-model)

---

## 🚀 Core Features

- **Song-based recommendations**: Get similar recommendations based on one or more reference songs.
- **Natural language recommendations**: Describe the type of music you're looking for in natural language ("music for focus", "happy party songs", etc.).
- **Full song CRUD**: Complete management of the musical catalog.
- **Spotify API Integration**: Fetch audio previews and metadata.
- **Database of 30,000+ songs**: Pre-loaded dataset from Spotify.
- **Clean and scalable architecture**: Following Clean Architecture principles.

---

## 🛠 Tech Stack

### Core
- **Python**: 3.13+
- **FastAPI**: High-performance asynchronous web framework.
- **Uvicorn**: ASGI server for FastAPI.

### Dependency Management
- **uv** (Astral): Ultra-fast package and virtual environment manager.

### Validation and Typing
- **Pydantic V2**: Data validation and serialization.
- **Pydantic Settings**: Configuration management via environment variables.

### Database
- **SQLAlchemy 2.0**: Asynchronous ORM.
- **Alembic**: Migration system.
- **SQLite**: Database (development/light production).
- **aiosqlite**: Asynchronous driver for SQLite.

### Machine Learning
- **scikit-learn**: Nearest Neighbors algorithm for recommendations.
- **pandas**: Data manipulation and analysis.
- **NumPy**: Numerical operations (scikit-learn dependency).

### Artificial Intelligence
- **Pydantic AI**: Framework for LLM agents.
- **Google Gemini**: Language model for musical feature extraction.

### Monitoring
- **Logfire**: Observability and logging (optional).

### HTTP Client
- **httpx**: Asynchronous HTTP client for Spotify API integration.

---

## 🏗 Project Architecture

The project follows a simplified **Clean Architecture**, separating responsibilities into well-defined layers:

```
backend/
├── src/
│   ├── api/                      # HTTP Presentation Layer
│   │   ├── routes/               # Endpoint definitions
│   │   │   ├── songs.py          # Song CRUD
│   │   │   ├── recommendations.py # Recommendation endpoints
│   │   │   └── music.py          # Spotify integration
│   │   ├── middleware/           # Custom middlewares
│   │   └── dependencies.py       # Dependency injection
│   │
│   ├── core/                     # Framework Configuration
│   │   ├── config.py             # Settings and environment variables
│   │   ├── database.py           # SQLAlchemy setup
│   │   └── logging.py            # Log setup
│   │
│   ├── domain/                   # Domain Layer (Contracts)
│   │   ├── schemas/              # Pydantic Models (DTOs)
│   │   │   └── song.py           # Song and feature schemas
│   │   └── models/               # SQLAlchemy Models (Entities)
│   │       └── song.py           # Database model
│   │
│   ├── repositories/             # Data Access Layer
│   │   ├── song_repository.py    # CRUD DB operations
│   │   └── music_repository.py   # Spotify API integration
│   │
│   ├── services/                 # Business Logic Layer
│   │   ├── song_service.py       # Song management logic
│   │   ├── recommender_service.py # ML recommendation system
│   │   ├── text_structure.py     # Orchestration: text → features → recommendation
│   │   └── music_service.py      # Spotify integration logic
│   │
│   ├── agents/                   # LLM Agents
│   │   ├── song_feature_agent.py # Feature extraction agent
│   │   └── prompts.py            # Agent system prompts
│   │
│   ├── utils/                    # Shared Utilities
│   │   └── seeder.py             # Initial data loading
│   │
│   └── resources/                # Static Resources
│       └── spotify_songs.csv     # Song dataset
│
├── alembic/                      # Database Migrations
├── main.py                       # Application entry point
├── pyproject.toml                # Dependency config (uv)
└── .env                          # Environment variables (not versioned)
```

### Data Flow

```
HTTP Client
    ↓
[API Routes] (FastAPI endpoints)
    ↓
[Services] (Business logic)
    ↓
[Repositories] (Data access)
    ↓
[Database / External APIs]
```

---

## 📦 Installation and Configuration

### Prerequisites

- **Python 3.13+**
- **uv** installed ([Installation instructions](https://github.com/astral-sh/uv))

### 1. Clone the repository

```bash
git clone <repository-url>
cd music-recommender/backend
```

### 2. Create virtual environment with uv

```bash
uv venv
```

### 3. Install dependencies

```bash
uv sync
```

### 4. Configure environment variables

Create a `.env` file in the `backend/` root directory:

```env
# App Configuration
PROJECT_NAME="Music Recommender API"
API_V1_STR="/api/v1"

# Database
DATABASE_URL="sqlite+aiosqlite:///./music_recommender.db"

# Spotify API (to fetch audio previews)
SPOTIFY_CLIENT_ID="your_client_id"
SPOTIFY_CLIENT_SECRET="your_client_secret"

# Google Gemini API (for the LLM agent)
GOOGLE_API_KEY="your_google_api_key"
MODEL="gemini-2.0-flash-exp"

# Logfire (optional, for monitoring)
LOGFIRE=false
```

### 5. Run migrations

```bash
uv run alembic upgrade head
```

---

## ▶️ Running the Service

### Development Mode (with hot-reload)

```bash
fastapi dev
```

Or using uv explicitly:

```bash
uv run fastapi dev
```

The server will be available at: **http://localhost:8000**

### Production Mode

```bash
uv run uvicorn main:app --host 0.0.0.0 --port 8000
```

### Interactive Documentation

Once the service is running, you can access:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/api/v1/openapi.json

---

## 🔌 API Endpoints

### Base URL
```
http://localhost:8000/api/v1
```

### 1. Songs (Song Management)

#### `POST /songs/`
Create a new song in the database.

**Request Body:**
```json
{
  "track_id": "spotify_track_id",
  "track_name": "Song Name",
  "track_artist": "Artist Name",
  "track_popularity": 85,
  "danceability": 0.75,
  "energy": 0.82,
  "key": 5,
  "loudness": -5.2,
  "mode": 1,
  "speechiness": 0.05,
  "acousticness": 0.12,
  "instrumentalness": 0.0,
  "liveness": 0.1,
  "valence": 0.68,
  "tempo": 128.0,
  "duration_ms": 210000,
  "track_album_id": "album_id",
  "track_album_name": "Album Name",
  "track_album_release_date": "2023-01-01",
  "playlist_name": "Playlist",
  "playlist_id": "playlist_id",
  "playlist_genre": "pop",
  "playlist_subgenre": "dance pop"
}
```

#### `GET /songs/`
List songs with pagination and search.

**Query Parameters:**
- `skip` (int, default: 0): Offset for pagination.
- `limit` (int, default: 100): Maximum number of results.
- `search` (string, optional): Search by song name or artist.

**Example:**
```
GET /api/v1/songs/?limit=20&search=Beatles
```

#### `GET /songs/{track_id}`
Retrieve a specific song by its ID.

#### `PUT /songs/{track_id}`
Update information for an existing song.

#### `DELETE /songs/{track_id}`
Remove a song from the database.

---

### 2. Recommendations (Recommendation System)

#### `POST /recommend/`
**Method 1: Recommendations based on reference songs**

Fetch recommendations similar to one or more provided songs.

**Request Body:**
```json
{
  "song_ids": ["track_id_1", "track_id_2"],
  "limit": 10
}
```

**Response:**
```json
[
  {
    "track_id": "recommended_track_1",
    "track_name": "Recommended Song 1",
    "track_artist": "Artist Name",
    "danceability": 0.72,
    "energy": 0.80,
    // ... other features
  },
  // ... more recommended songs
]
```

**How it works:**
1. Extracts musical features of the reference songs.
2. Calculates the average of their features.
3. Finds the most similar songs using Nearest Neighbors.
4. Returns the top N recommendations.

---

#### `POST /recommend/text`
**Method 2: Recommendations based on textual description**

Fetch recommendations starting from a natural language description.

**Request Body:**
```json
{
  "text_input": "relaxing music to concentrate while studying",
  "limit": 10
}
```

**Response:**
```json
[
  {
    "track_id": "recommended_track_1",
    "track_name": "Calm Piano Study",
    "track_artist": "Study Music",
    "instrumentalness": 0.95,
    "energy": 0.25,
    "valence": 0.45,
    // ... other features
  },
  // ... more recommended songs
]
```

**How it works:**
1. Sends the text to the LLM agent (Gemini).
2. The agent extracts numerical musical features from the text.
3. Uses those features to search for similar songs with Nearest Neighbors.
4. Returns the top N recommendations.

---

### 3. Music (Spotify Integration)

#### `GET /music/audio/{track_id}`
Fetches audio preview and metadata for a song from Spotify.

**Response:**
```json
{
  "preview_url": "https://p.scdn.co/mp3-preview/...",
  "external_url": "https://open.spotify.com/track/...",
  "name": "Song Name",
  "artists": ["Artist 1", "Artist 2"],
  "album": "Album Name",
  "duration_ms": 210000,
  "popularity": 85
}
```

---

## 🎯 Recommendation System

The system implements **two complementary methods** for music recommendation:

### Method 1: Recommendation by Song Similarity

**Algorithm**: K-Nearest Neighbors (KNN) with Ball Tree

**Used Features** (10 features):
- `danceability`: Track suitability for dancing (0.0 - 1.0).
- `energy`: Perceived intensity and activity (0.0 - 1.0).
- `key`: Musical pitch class (0-11, where 0=C, 1=C#, etc.).
- `loudness`: Volume in decibels (-60 to 0 dB).
- `speechiness`: Presence of spoken words (0.0 - 1.0).
- `acousticness`: Acoustic vs. electronic level (0.0 - 1.0).
- `instrumentalness`: Absence of vocals (0.0 - 1.0).
- `liveness`: Presence of a live audience (0.0 - 1.0).
- `valence`: Musical positivity (0.0 - 1.0).
- `tempo`: Speed in BPM.

**Detailed Process:**

1. **Data Loading**: All songs are retrieved from the database.
2. **Normalization**: Features are normalized using MinMaxScaler (0-1).
3. **Model Building**: A KNN model is trained with Ball Tree.
4. **Reference Feature Extraction**: Characteristics of selected songs are obtained.
5. **Averaging**: If there are multiple songs, their features are averaged.
6. **Neighbor Search**: The algorithm finds the K closest songs in the 10-dimensional space.
7. **Ranking**: Returns songs sorted by similarity.

**Advantages:**
- Fast and efficient (Ball Tree optimizes searches in multidimensional spaces).
- No extensive prior training required.
- Interpretable and consistent results.

---

### Method 2: Recommendation by Textual Description

**Complete Flow:**

```
User Text
    ↓
[LLM Agent - Gemini]
    ↓
Extracted Numerical Features
    ↓
[Recommender Service]
    ↓
Recommended Songs
```

**Transformation Example:**

**User Input:**
```
"energetic music for a gym workout"
```

**LLM Extracted Features:**
```json
{
  "danceability": 0.75,
  "energy": 0.95,
  "valence": 0.80,
  "tempo": 140.0,
  "acousticness": 0.10,
  "instrumentalness": 0.05,
  "speechiness": 0.15,
  "key": null,
  "loudness": null,
  "mode": 1,
  "liveness": 0.1
}
```

**Process:**
1. Text is sent to `TextStructureService`.
2. Service invokes `SongFeaturesAgent`.
3. Agent uses Gemini to interpret text and extract features.
4. Features are passed to `RecommenderService`.
5. The same KNN algorithm as in Method 1 is executed.
6. Most similar songs to the extracted features are returned.

**Advantages:**
- Natural interface for non-technical users.
- Captures complex intentions ("sad but hopeful music").
- Combines the best of NLP and traditional ML.

---

## 🤖 LLM Agent for Feature Extraction

### Agent Architecture

**Location**: `src/agents/song_feature_agent.py`

**Framework**: Pydantic AI

**Model**: Google Gemini 2.0 Flash Exp

### Internal Operation

The agent is designed as an **expert musicologist** that translates natural language into technical audio parameters.

```python
class SongFeaturesAgent:
    def __init__(self):
        provider = GoogleProvider(api_key=settings.GOOGLE_API_KEY)
        model = GoogleModel(settings.MODEL, provider=provider)
        self.agent = Agent(
            system_prompt=system_prompt,
            model=model,
            output_type=SongFeatures,  # Structured output
        )

    async def __call__(self, input: str) -> SongFeatures:
        answer = await self.agent.run(input)
        return answer.output
```

### System Prompt (Prompt Engineering)

The prompt is carefully designed to:

1. **Define the role**: "Expert musicologist translating descriptions to numerical features".
2. **Specify each feature**: Precise definitions with ranges and examples.
3. **Provide heuristics**: Common mappings (e.g., "gym" → high energy + high tempo).
4. **Establish inference rules**: Only fill relevant fields, leave others as null.

**Included Mapping Examples:**

| User Description | Key Extracted Features |
|------------------|------------------------|
| "Concentration / Study" | `instrumentalness`: 0.8-1.0<br>`energy`: 0.0-0.4<br>`speechiness`: 0.0-0.1 |
| "Party / Club" | `danceability`: 0.7-1.0<br>`energy`: 0.7-1.0<br>`valence`: 0.6-1.0 |
| "Sad / Heartbreak" | `valence`: 0.0-0.2<br>`mode`: 0 (minor)<br>`energy`: 0.0-0.4 |
| "Gym / Workout" | `energy`: 0.8-1.0<br>`tempo`: >125<br>`acousticness`: 0.0-0.2 |
| "Relaxation / Sleep" | `energy`: 0.0-0.2<br>`danceability`: low<br>`tempo`: low |

### Validation with Pydantic

The LLM output is automatically validated against the `SongFeatures` schema:

```python
class SongFeatures(BaseModel):
    danceability: float = Field(description="...")
    energy: float = Field(description="...")
    key: int = Field(description="...")
    # ... other fields with detailed descriptions
```

**Benefits:**
- **Type safety**: Ensures the LLM returns the correct format.
- **Automatic validation**: Ranges and types are automatically checked.
- **Integrated documentation**: Descriptions guide the model.

### Ambiguity Handling

The agent is trained to:
- **Leave fields as `null`** when not relevant (e.g., don't infer `key` unless mentioned).
- **Use appropriate ranges** instead of exact values.
- **Prioritize semantic features** over technical ones when there's a conflict.

---

## 🧠 Machine Learning Model

### Algorithm: K-Nearest Neighbors (KNN)

**Implementation**: `sklearn.neighbors.NearestNeighbors`

**Algorithm Structure**: Ball Tree

### Why KNN?

1. **No supervised training needed**: We don't need "similarity" labels.
2. **Interpretable**: Distance in feature space is intuitive.
3. **Efficient for searches**: Ball Tree optimizes searches in high-dimensional spaces.
4. **Flexible**: Works with both reference songs and synthetic features from the LLM.

### Data Preprocessing

**Normalization with MinMaxScaler:**

```python
scaler = MinMaxScaler()
df_songs[features] = scaler.fit_transform(df_songs[features])
```

**Why normalize?**
- Features have very different scales:
  - `tempo`: 50-200 BPM
  - `danceability`: 0.0-1.0
  - `loudness`: -60 to 0 dB
- Without normalization, features with larger ranges would dominate the distance.
- MinMaxScaler scales everything to the [0, 1] range.

### Similarity Calculation

**Distance Metric**: Euclidean (KNN default)

For two songs A and B:

```
distance = √(Σ(feature_A_i - feature_B_i)²)
```

Where i iterates through the 10 normalized features.

### Model Construction

```python
nn_model = NearestNeighbors(
    n_neighbors=k,  # Desired number of recommendations
    algorithm='ball_tree'  # Optimized data structure
)
nn_model.fit(df_songs[features])
```

**Ball Tree:**
- Partitions the space into nested hyperspheres.
- Reduces search complexity from O(n) to O(log n).
- Ideal for medium-large datasets (our case: 30k+ songs).

### Neighbor Search

```python
# Normalize the query with the same scaler
query_normalized = scaler.transform(query_features)

# Find the K closest neighbors
distances, indices = nn_model.kneighbors(query_normalized)
```

**Output:**
- `distances`: Array of Euclidean distances to each neighbor.
- `indices`: Indices of the closest songs in the dataset.

### Feature Averaging (Multiple Songs)

When the user selects multiple songs:

```python
# Extract features for each reference song
reference_features = [extract_features(song) for song in selected_songs]

# Average features
combined_features = np.mean(reference_features, axis=0)

# Search for neighbors of the average
distances, indices = nn_model.kneighbors([combined_features])
```

**Justification:**
- Captures the "center of gravity" of user preferences.
- More robust than using a single song.
- Allows mixing genres/styles.

### Limitations and Considerations

1. **Cold Start**: Requires songs to be in the DB.
2. **Scalability**: For millions of songs, consider:
   - Approximate Nearest Neighbors (ANN) with FAISS or Annoy.
   - Pre-computed indices.
3. **Dataset Bias**: Recommendations are limited to the available catalog.
4. **Fixed Features**: Doesn't learn user preferences over time (no feedback loop).

### Possible Future Improvements

- **Collaborative Filtering**: Incorporate preferences of similar users.
- **Deep Embeddings**: Use audio models (e.g., Spotify's Audio Features API).
- **Hybrid Approach**: Combine current content-based with collaborative filtering.
- **Feedback Loop**: Adjust feature weights according to user interactions.

---

## 🗄️ Database

### Data Model

**Main Table**: `songs`

**Fields**:
- `track_id` (PK): Unique Spotify identifier.
- Metadata: `track_name`, `track_artist`, `track_album_name`, etc.
- Audio Features: `danceability`, `energy`, `valence`, etc.
- Playlist Information: `playlist_genre`, `playlist_subgenre`.

### Initial Seeding

The seeder runs automatically when the application starts:

```python
# main.py
@asynccontextmanager
async def lifespan(app: FastAPI):
    await seed_database()  # Loads CSV if DB is empty
    yield
```

**Dataset**: `src/resources/spotify_songs.csv` (~30,000 songs)

---

## 🔧 Advanced Configuration

### Complete Environment Variables

```env
# App
PROJECT_NAME="Music Recommender API"
API_V1_STR="/api/v1"

# Database
DATABASE_URL="sqlite+aiosqlite:///./music_recommender.db"

# Spotify
SPOTIFY_CLIENT_ID="your_client_id"
SPOTIFY_CLIENT_SECRET="your_client_secret"

# Google Gemini
GOOGLE_API_KEY="your_api_key"
MODEL="gemini-2.0-flash-exp"

# Monitoring
LOGFIRE=false
```

### CORS

By default, the API accepts requests from any origin:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Production Recommendation**: Explicitly specify allowed origins.

---

## 📚 Additional Resources

- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **Pydantic AI**: https://ai.pydantic.dev/
- **scikit-learn KNN**: https://scikit-learn.org/stable/modules/neighbors.html
- **Spotify Web API**: https://developer.spotify.com/documentation/web-api/
- **Google Gemini**: https://ai.google.dev/

---

## 📄 License

This project is open-source and available under the MIT License.
