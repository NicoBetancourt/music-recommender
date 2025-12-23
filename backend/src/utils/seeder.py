import os

import pandas as pd
from src.core.database import AsyncSessionLocal
from src.domain.models.song import SongModel
from src.repositories.song_repository import SongRepository


async def seed_database():
    """Checks if the database is empty and seeds it from the Spotify CSV file."""
    print("Checking database...")
    async with AsyncSessionLocal() as session:
        repo = SongRepository(session)
        try:
            existing_songs = await repo.get_all(limit=1)
            if not existing_songs:
                csv_path = "src/resources/spotify_songs.csv"
                if not os.path.exists(csv_path):
                    print(f"CSV file not found at {csv_path}")
                    return

                print(f"Loading songs from {csv_path}...")
                try:
                    df = pd.read_csv(csv_path)
                    # Deduplicate by track_id
                    df = df.drop_duplicates(subset=["track_id"], keep="first")
                    # Handle NaNs: convert NaN to None for object columns
                    df = df.where(pd.notnull(df), None)

                    songs_to_create = []
                    for _, row in df.iterrows():
                        try:
                            song = SongModel(
                                track_id=str(row["track_id"]),
                                track_name=str(row["track_name"]),
                                track_artist=str(row["track_artist"]),
                                track_popularity=int(row["track_popularity"]),
                                track_album_id=str(row["track_album_id"]),
                                track_album_name=str(row["track_album_name"]),
                                track_album_release_date=str(
                                    row["track_album_release_date"]
                                ),
                                playlist_name=str(row["playlist_name"])
                                if row["playlist_name"] is not None
                                else None,
                                playlist_id=str(row["playlist_id"])
                                if row["playlist_id"] is not None
                                else None,
                                playlist_genre=str(row["playlist_genre"])
                                if row["playlist_genre"] is not None
                                else None,
                                playlist_subgenre=str(row["playlist_subgenre"])
                                if row["playlist_subgenre"] is not None
                                else None,
                                danceability=float(row["danceability"]),
                                energy=float(row["energy"]),
                                key=int(row["key"]),
                                loudness=float(row["loudness"]),
                                mode=int(row["mode"]),
                                speechiness=float(row["speechiness"]),
                                acousticness=float(row["acousticness"]),
                                instrumentalness=float(row["instrumentalness"]),
                                liveness=float(row["liveness"]),
                                valence=float(row["valence"]),
                                tempo=float(row["tempo"]),
                                duration_ms=int(row["duration_ms"]),
                            )
                            songs_to_create.append(song)
                        except ValueError as ve:
                            print(f"Skipping row due to value error: {ve}")
                            continue

                    batch_size = 1000
                    total_songs = len(songs_to_create)
                    if total_songs > 0:
                        print(f"Found {total_songs} songs to insert.")
                        for i in range(0, total_songs, batch_size):
                            batch = songs_to_create[i : i + batch_size]
                            await repo.bulk_create(batch)
                            print(
                                f"Loaded {min(i + batch_size, total_songs)}/{total_songs} songs"
                            )
                        print("Data loading completed.")
                    else:
                        print("No songs found in CSV.")

                except Exception as e:
                    print(f"Error loading CSV: {e}")
            else:
                print("Songs already loaded in database.")
        except Exception as e:
            print(f"Error during seeding: {e}")
