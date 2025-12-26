import pytest
from httpx import AsyncClient
from src.core.config import settings


@pytest.mark.asyncio
async def test_create_song(async_client: AsyncClient):
    song_data = {
        "track_id": "test_track_1",
        "track_name": "Test Song",
        "track_artist": "Test Artist",
        "track_popularity": 50,
        "danceability": 0.5,
        "energy": 0.5,
        "key": 1,
        "loudness": -10.0,
        "mode": 1,
        "speechiness": 0.1,
        "acousticness": 0.2,
        "instrumentalness": 0.0,
        "liveness": 0.1,
        "valence": 0.5,
        "tempo": 100.0,
        "duration_ms": 200000,
        "track_album_id": "album_1",
        "track_album_name": "Test Album",
        "track_album_release_date": "2023-01-01",
        "playlist_name": "Test Playlist",
        "playlist_id": "playlist_1",
        "playlist_genre": "Test Genre",
        "playlist_subgenre": "Test Subgenre",
    }

    response = await async_client.post(f"{settings.API_V1_STR}/songs/", json=song_data)
    assert response.status_code == 200
    data = response.json()
    assert data["track_id"] == song_data["track_id"]
    assert data["track_name"] == song_data["track_name"]


@pytest.mark.asyncio
async def test_get_song(async_client: AsyncClient):
    # First create a song
    song_data = {
        "track_id": "test_track_2",
        "track_name": "Test Song 2",
        "track_artist": "Test Artist",
        "track_popularity": 50,
        "danceability": 0.5,
        "energy": 0.5,
        "key": 1,
        "loudness": -10.0,
        "mode": 1,
        "speechiness": 0.1,
        "acousticness": 0.2,
        "instrumentalness": 0.0,
        "liveness": 0.1,
        "valence": 0.5,
        "tempo": 100.0,
        "duration_ms": 200000,
        "track_album_id": "album_1",
        "track_album_name": "Test Album",
        "track_album_release_date": "2023-01-01",
    }
    await async_client.post(f"{settings.API_V1_STR}/songs/", json=song_data)

    # Get it
    response = await async_client.get(f"{settings.API_V1_STR}/songs/test_track_2")
    assert response.status_code == 200
    data = response.json()
    assert data["track_id"] == "test_track_2"


@pytest.mark.asyncio
async def test_list_songs(async_client: AsyncClient):
    # Create a couple of songs
    for i in range(3):
        song_data = {
            "track_id": f"list_track_{i}",
            "track_name": f"List Song {i}",
            "track_artist": "Test Artist",
            "track_popularity": 50,
            "danceability": 0.5,
            "energy": 0.5,
            "key": 1,
            "loudness": -10.0,
            "mode": 1,
            "speechiness": 0.1,
            "acousticness": 0.2,
            "instrumentalness": 0.0,
            "liveness": 0.1,
            "valence": 0.5,
            "tempo": 100.0,
            "duration_ms": 200000,
            "track_album_id": f"album_{i}",
            "track_album_name": "Test Album",
            "track_album_release_date": "2023-01-01",
        }
        res = await async_client.post(f"{settings.API_V1_STR}/songs/", json=song_data)
        assert res.status_code == 200

    response = await async_client.get(f"{settings.API_V1_STR}/songs/?limit=2")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2


@pytest.mark.asyncio
async def test_update_song(async_client: AsyncClient):
    # Create
    song_data = {
        "track_id": "update_track",
        "track_name": "Original Name",
        "track_artist": "Original Artist",
        "track_popularity": 50,
        "danceability": 0.5,
        "energy": 0.5,
        "key": 1,
        "loudness": -10.0,
        "mode": 1,
        "speechiness": 0.1,
        "acousticness": 0.2,
        "instrumentalness": 0.0,
        "liveness": 0.1,
        "valence": 0.5,
        "tempo": 100.0,
        "duration_ms": 200000,
        "track_album_id": "album_1",
        "track_album_name": "Test Album",
        "track_album_release_date": "2023-01-01",
    }
    await async_client.post(f"{settings.API_V1_STR}/songs/", json=song_data)

    # Update
    update_data = {"track_name": "Updated Name"}
    response = await async_client.put(
        f"{settings.API_V1_STR}/songs/update_track", json=update_data
    )
    assert response.status_code == 200
    data = response.json()
    assert data["track_name"] == "Updated Name"
    # Artist should remain same
    assert data["track_artist"] == "Original Artist"


@pytest.mark.asyncio
async def test_delete_song(async_client: AsyncClient):
    # Create
    song_data = {
        "track_id": "delete_track",
        "track_name": "To Delete",
        "track_artist": "Test Artist",
        "track_popularity": 50,
        "danceability": 0.5,
        "energy": 0.5,
        "key": 1,
        "loudness": -10.0,
        "mode": 1,
        "speechiness": 0.1,
        "acousticness": 0.2,
        "instrumentalness": 0.0,
        "liveness": 0.1,
        "valence": 0.5,
        "tempo": 100.0,
        "duration_ms": 200000,
        "track_album_id": "album_1",
        "track_album_name": "Test Album",
        "track_album_release_date": "2023-01-01",
    }
    await async_client.post(f"{settings.API_V1_STR}/songs/", json=song_data)

    # Delete
    response = await async_client.delete(f"{settings.API_V1_STR}/songs/delete_track")
    assert (
        response.status_code == 200
    )  # Or 204 depending on implementation, usually delete returns object or status

    # Verify gone
    response = await async_client.get(f"{settings.API_V1_STR}/songs/delete_track")
    assert response.status_code == 404
