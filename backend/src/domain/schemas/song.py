from pydantic import BaseModel, ConfigDict

class SongBase(BaseModel):
    track_name: str
    track_artist: str
    track_popularity: int
    track_album_id: str
    track_album_name: str
    track_album_release_date: str
    playlist_name: str | None = None
    playlist_id: str | None = None
    playlist_genre: str | None = None
    playlist_subgenre: str | None = None
    
    danceability: float
    energy: float
    key: int
    loudness: float
    mode: int
    speechiness: float
    acousticness: float
    instrumentalness: float
    liveness: float
    valence: float
    tempo: float
    duration_ms: int

class SongCreate(SongBase):
    track_id: str

class SongUpdate(BaseModel):
    track_name: str | None = None
    track_artist: str | None = None
    track_popularity: int | None = None
    # Add other fields as optional for update if needed, keeping it simple for now

class SongResponse(SongBase):
    track_id: str

    model_config = ConfigDict(from_attributes=True)
