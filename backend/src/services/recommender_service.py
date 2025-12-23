import pandas as pd
from sklearn.neighbors import NearestNeighbors  # type: ignore
from sklearn.preprocessing import MinMaxScaler  # type: ignore
from src.domain.schemas.song import SongResponse
from src.repositories.song_repository import SongRepository


class RecommenderService:
    def __init__(self, song_repository: SongRepository):
        self._song_repository = song_repository

    async def recommend(self, song_ids: list[str], n_songs: int) -> list[SongResponse]:
        # Fetch all songs to build the model.
        # Note: In a production system, we would cache the model or train it offline.
        # For this exercise, we build it on the fly as requested.
        all_songs_models = await self._song_repository.get_all(
            limit=100000
        )  # Assuming < 100k songs
        if not all_songs_models:
            return []

        list_of_songs = [
            {
                "track_id": s.track_id,
                "danceability": s.danceability,
                "energy": s.energy,
                "key": s.key,
                "loudness": s.loudness,
                "mode": s.mode,
                "speechiness": s.speechiness,
                "acousticness": s.acousticness,
                "instrumentalness": s.instrumentalness,
                "liveness": s.liveness,
                "valence": s.valence,
                "tempo": s.tempo,
                "duration_ms": s.duration_ms,
                # Add other fields if needed for output mapping later, but features are subset
                # actually we need full dict to map back to response if we want full details
                # reusing the model object directly later might be better
            }
            for s in all_songs_models
        ]

        # We need a way to look up the full song object by id later efficiently
        songs_map = {s.track_id: s for s in all_songs_models}

        df_songs = pd.DataFrame(list_of_songs)

        features = [
            "danceability",
            "energy",
            "key",
            "loudness",
            "speechiness",
            "acousticness",
            "instrumentalness",
            "liveness",
            "valence",
            "tempo",
        ]

        scaler = MinMaxScaler()
        df_songs[features] = scaler.fit_transform(df_songs[features])

        k_neighbors = n_songs
        # Ensure k_neighbors <= number of samples
        if k_neighbors > len(df_songs):
            k_neighbors = len(df_songs)

        nn_model = NearestNeighbors(n_neighbors=k_neighbors, algorithm="ball_tree")
        nn_model.fit(df_songs[features])

        list_values = []
        for song_id in song_ids:
            if song_id not in songs_map:
                continue

            # Find the row in df_songs for this song_id
            # Or just extract from map and normalize using the same scaler?
            # Easiest is to pick from df_songs

            song_row = df_songs[df_songs["track_id"] == song_id]
            if song_row.empty:
                continue

            features_values = song_row[features].values.flatten().tolist()
            list_values.append(features_values)

        if not list_values:
            return []

        # reference_songs_normalized = scaler.transform(pd.DataFrame(list_values))
        # Wait, df_songs is already scaled. So picking from it gives scaled values.
        # The user snippet did:
        # chosen_track_id = ...to_dict()
        # features_values = [chosen_track_id[feature] for feature in features]
        # list_values.append(features_values)
        # reference_songs_normalized = scaler.transform(pd.DataFrame(list_values))
        #
        # This implies user snippet picked RAW values then transformed.
        # My approach picked SCALED values from df_songs.

        # Let's stick to the user logic: pick raw, then transform.
        # So I need raw values map.

        raw_values = []
        for song_id in song_ids:
            s = songs_map.get(song_id)
            if not s:
                continue
            # Extract raw features from model
            data = {
                "danceability": s.danceability,
                "energy": s.energy,
                "key": s.key,
                "loudness": s.loudness,
                "speechiness": s.speechiness,
                "acousticness": s.acousticness,
                "instrumentalness": s.instrumentalness,
                "liveness": s.liveness,
                "valence": s.valence,
                "tempo": s.tempo,
            }
            raw_values.append([data[f] for f in features])

        if not raw_values:
            return []

        reference_songs_normalized = scaler.transform(
            pd.DataFrame(raw_values, columns=features)
        )
        combined_features = reference_songs_normalized.mean(axis=0).tolist()

        distances, indices = nn_model.kneighbors([combined_features])

        # Indices is list of lists [[idx1, idx2...]]
        neighbor_indices = indices[0]

        recommended_songs = []
        for idx in neighbor_indices:
            # df_songs has track_id.
            track_id = df_songs.iloc[idx]["track_id"]
            original_song = songs_map.get(track_id)
            if original_song:
                recommended_songs.append(SongResponse.model_validate(original_song))

        # Limit to n_songs just in case
        return recommended_songs[:n_songs]
