import pandas as pd
from sklearn.neighbors import NearestNeighbors  # type: ignore
from sklearn.preprocessing import MinMaxScaler  # type: ignore

from src.domain.schemas.song import SongFeatures, SongResponse
from src.repositories.song_repository import SongRepository


class RecommenderService:
    _FEATURES = [
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

    def __init__(self, song_repository: SongRepository):
        self._song_repository = song_repository

    def _songs_to_dataframe(self, all_songs_models) -> tuple[pd.DataFrame, dict]:
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
            }
            for s in all_songs_models
        ]

        songs_map = {s.track_id: s for s in all_songs_models}
        df_songs = pd.DataFrame(list_of_songs)
        return df_songs, songs_map

    def _build_nn_model(
        self,
        df_songs: pd.DataFrame,
        n_songs: int,
    ) -> tuple[MinMaxScaler, NearestNeighbors, int]:
        scaler = MinMaxScaler()
        df_songs[self._FEATURES] = scaler.fit_transform(df_songs[self._FEATURES])

        k_neighbors = n_songs
        if k_neighbors > len(df_songs):
            k_neighbors = len(df_songs)
        if k_neighbors <= 0:
            k_neighbors = 0

        nn_model = NearestNeighbors(
            n_neighbors=max(k_neighbors, 1), algorithm="ball_tree"
        )
        nn_model.fit(df_songs[self._FEATURES])
        return scaler, nn_model, k_neighbors

    def _responses_from_neighbor_indices(
        self,
        df_songs: pd.DataFrame,
        songs_map: dict,
        neighbor_indices,
        n_songs: int,
    ) -> list[SongResponse]:
        recommended_songs: list[SongResponse] = []
        for idx in neighbor_indices:
            track_id = df_songs.iloc[idx]["track_id"]
            original_song = songs_map.get(track_id)
            if original_song:
                recommended_songs.append(SongResponse.model_validate(original_song))
        return recommended_songs[:n_songs]

    def _song_to_raw_feature_row(self, song_model) -> list:
        data = {
            "danceability": song_model.danceability,
            "energy": song_model.energy,
            "key": song_model.key,
            "loudness": song_model.loudness,
            "speechiness": song_model.speechiness,
            "acousticness": song_model.acousticness,
            "instrumentalness": song_model.instrumentalness,
            "liveness": song_model.liveness,
            "valence": song_model.valence,
            "tempo": song_model.tempo,
        }
        return [data[f] for f in self._FEATURES]

    def _song_features_to_row(self, song_features: SongFeatures) -> list:
        return [getattr(song_features, f) for f in self._FEATURES]

    def _song_features_has_all_required(self, song_features: SongFeatures) -> bool:
        return all(getattr(song_features, f) is not None for f in self._FEATURES)

    async def recommend_from_features(
        self,
        features_json: SongFeatures | dict,
        n_songs: int,
    ) -> list[SongResponse]:
        all_songs_models = await self._song_repository.get_all(limit=100000)
        if not all_songs_models:
            return []

        df_songs, songs_map = self._songs_to_dataframe(all_songs_models)

        song_features = (
            features_json
            if isinstance(features_json, SongFeatures)
            else SongFeatures.model_validate(features_json)
        )
        if not self._song_features_has_all_required(song_features):
            return []

        scaler, nn_model, k_neighbors = self._build_nn_model(df_songs, n_songs)
        if k_neighbors <= 0:
            return []

        query_row = pd.DataFrame(
            [self._song_features_to_row(song_features)], columns=self._FEATURES
        )
        query_normalized = scaler.transform(query_row)
        distances, indices = nn_model.kneighbors(query_normalized)

        neighbor_indices = indices[0]
        return self._responses_from_neighbor_indices(
            df_songs=df_songs,
            songs_map=songs_map,
            neighbor_indices=neighbor_indices,
            n_songs=n_songs,
        )

    async def recommend(self, song_ids: list[str], n_songs: int) -> list[SongResponse]:
        # Fetch all songs to build the model.
        # Note: In a production system, we would cache the model or train it offline.
        # For this exercise, we build it on the fly as requested.
        all_songs_models = await self._song_repository.get_all(
            limit=100000
        )  # Assuming < 100k songs
        if not all_songs_models:
            return []

        df_songs, songs_map = self._songs_to_dataframe(all_songs_models)
        scaler, nn_model, k_neighbors = self._build_nn_model(df_songs, n_songs)
        # Ensure k_neighbors <= number of samples
        if k_neighbors <= 0:
            return []

        features = self._FEATURES

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
            raw_values.append(self._song_to_raw_feature_row(s))

        if not raw_values:
            return []

        reference_songs_normalized = scaler.transform(
            pd.DataFrame(raw_values, columns=self._FEATURES)
        )
        combined_features = reference_songs_normalized.mean(axis=0).tolist()

        distances, indices = nn_model.kneighbors([combined_features])

        # Indices is list of lists [[idx1, idx2...]]
        neighbor_indices = indices[0]

        # Limit to n_songs just in case
        return self._responses_from_neighbor_indices(
            df_songs=df_songs,
            songs_map=songs_map,
            neighbor_indices=neighbor_indices,
            n_songs=n_songs,
        )
