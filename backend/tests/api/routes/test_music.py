from unittest.mock import AsyncMock, MagicMock

import pytest
from httpx import AsyncClient
from main import app
from src.api.dependencies import get_deezer_repository, get_spotify_repository
from src.core.config import settings


@pytest.fixture
def mock_music_services():
    # Mock Spotify Repo
    mock_spotify = MagicMock()
    mock_spotify.get_track = AsyncMock(
        return_value={
            "preview_url": "http://preview.url",
            "external_url": "http://spotify.url",
            "name": "Mock Song",
            "artists": ["Mock Artist"],
            "album": "Mock Album",
            "duration_ms": 200000,
            "popularity": 80,
            "album_images": [{"url": "http://image.url"}],
        }
    )

    # Mock Deezer Repo
    mock_deezer = MagicMock()
    mock_deezer.search_song = AsyncMock(
        return_value={
            "data": [
                {
                    "id": 123,
                    "preview": "http://deezer.preview",
                    "link": "http://deezer.link",
                    "album": {"cover_xl": "http://deezer.image"},
                    "artist": {"picture_xl": "http://deezer.artist"},
                }
            ]
        }
    )

    app.dependency_overrides[get_spotify_repository] = lambda: mock_spotify
    app.dependency_overrides[get_deezer_repository] = lambda: mock_deezer

    yield

    # Cleanup
    if get_spotify_repository in app.dependency_overrides:
        del app.dependency_overrides[get_spotify_repository]
    if get_deezer_repository in app.dependency_overrides:
        del app.dependency_overrides[get_deezer_repository]


@pytest.mark.asyncio
async def test_get_audio_preview(async_client: AsyncClient, mock_music_services):
    # Depending on implementation, it might check DB first or go straight to API
    # Usually strictly fetches from Spotify/Deezer given a track_id

    track_id = "spotify_id_123"

    # Create song in DB first because MusicService checks existence
    song_data = {
        "track_id": track_id,
        "track_name": "Mock Song",
        "track_artist": "Mock Artist",
        "track_popularity": 80,
        "danceability": 0.5,
        "energy": 0.5,
        "key": 0,
        "loudness": -5,
        "mode": 1,
        "speechiness": 0.0,
        "acousticness": 0.0,
        "instrumentalness": 0.0,
        "liveness": 0.0,
        "valence": 0.0,
        "tempo": 120.0,
        "duration_ms": 200000,
        "track_album_id": "album_1",
        "track_album_name": "Mock Album",
        "track_album_release_date": "2023-01-01",
    }
    await async_client.post(f"{settings.API_V1_STR}/songs/", json=song_data)

    response = await async_client.get(f"{settings.API_V1_STR}/music/audio/{track_id}")

    assert response.status_code == 200
    data = response.json()
    assert data["track_name"] == "Mock Song"
    assert data["preview_url"] == "http://deezer.preview"
