import pytest
from httpx import AsyncClient
from src.core.config import settings


@pytest.mark.asyncio
async def test_recommend_by_songs(async_client: AsyncClient):
    # 1. Create reference songs
    song1 = {
        "track_id": "ref_1",
        "track_name": "Reference 1",
        "track_artist": "Ref Artist",
        "track_popularity": 50,
        "danceability": 0.8,
        "energy": 0.8,
        "key": 1,
        "loudness": -5.0,
        "mode": 1,
        "speechiness": 0.05,
        "acousticness": 0.1,
        "instrumentalness": 0.0,
        "liveness": 0.1,
        "valence": 0.8,
        "tempo": 120.0,
        "duration_ms": 200000,
        "track_album_id": "album_1",
        "track_album_name": "Ref Album",
        "track_album_release_date": "2023-01-01",
    }
    await async_client.post(f"{settings.API_V1_STR}/songs/", json=song1)

    # 2. Create potential match (similar features)
    match = {
        "track_id": "match_1",
        "track_name": "Match 1",
        "track_artist": "Match Artist",
        "track_popularity": 50,
        "danceability": 0.79,  # Very close
        "energy": 0.81,  # Very close
        "key": 1,
        "loudness": -5.1,
        "mode": 1,
        "speechiness": 0.05,
        "acousticness": 0.11,
        "instrumentalness": 0.01,
        "liveness": 0.11,
        "valence": 0.79,
        "tempo": 121.0,
        "duration_ms": 200000,
        "track_album_id": "album_2",
        "track_album_name": "Match Album",
        "track_album_release_date": "2023-01-01",
    }
    await async_client.post(f"{settings.API_V1_STR}/songs/", json=match)

    # 3. Create different song
    diff = {
        "track_id": "diff_1",
        "track_name": "Different",
        "track_artist": "Diff Artist",
        "track_popularity": 50,
        "danceability": 0.1,  # Far away
        "energy": 0.1,
        "key": 1,
        "loudness": -20.0,
        "mode": 1,
        "speechiness": 0.05,
        "acousticness": 0.9,
        "instrumentalness": 0.9,
        "liveness": 0.1,
        "valence": 0.1,
        "tempo": 60.0,
        "duration_ms": 200000,
        "track_album_id": "album_3",
        "track_album_name": "Diff Album",
        "track_album_release_date": "2023-01-01",
    }
    await async_client.post(f"{settings.API_V1_STR}/songs/", json=diff)

    # Request recommendation
    payload = {"song_ids": ["ref_1"], "limit": 5}
    response = await async_client.post(
        f"{settings.API_V1_STR}/recommend/", json=payload
    )
    assert response.status_code == 200
    data = response.json()

    # Should find at least the match
    # Note: Logic usually excludes the input song itself, so check for match_1
    found_ids = [s["track_id"] for s in data]
    assert "match_1" in found_ids


@pytest.mark.asyncio
async def test_recommend_by_text(async_client: AsyncClient):
    # Depending on conftest mock, the agent returns fixed features
    # features = {danceability: 0.5, energy: 0.5, ...}

    # Create a song that matches those mock features
    perfect_match = {
        "track_id": "text_match",
        "track_name": "Text Match",
        "track_artist": "Artist",
        "track_popularity": 50,
        "danceability": 0.5,
        "energy": 0.5,
        "key": 0,
        "loudness": -5.0,
        "mode": 1,
        "speechiness": 0.05,
        "acousticness": 0.1,
        "instrumentalness": 0.0,
        "liveness": 0.1,
        "valence": 0.5,
        "tempo": 120.0,
        "duration_ms": 200000,
        "track_album_id": "album_4",
        "track_album_name": "Text Album",
        "track_album_release_date": "2023-01-01",
    }
    await async_client.post(f"{settings.API_V1_STR}/songs/", json=perfect_match)

    payload = {"text_input": "some prompt (mocked anyway)", "limit": 5}
    response = await async_client.post(
        f"{settings.API_V1_STR}/recommend/text", json=payload
    )
    assert response.status_code == 200
    data = response.json()

    found_ids = [s["track_id"] for s in data]
    assert "text_match" in found_ids
