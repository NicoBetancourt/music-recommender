from src.repositories.deezer_repository import DeezerRepository
from src.repositories.song_repository import SongRepository
from src.repositories.spotify_repository import SpotifyRepository


class MusicService:
    def __init__(
        self,
        song_repo: SongRepository,
        deezer_repo: DeezerRepository,
        spotify_repo: SpotifyRepository,
    ):
        self.song_repo = song_repo
        self.deezer_repo = deezer_repo
        self.spotify_repo = spotify_repo

    async def get_song_audio(self, track_id: str) -> dict:
        # 1. Fetch song from database repository
        song = await self.song_repo.get_by_id(track_id)
        if not song:
            return {"error": "Song not found in database"}

        # 2. Search song on Deezer (no auth required)
        try:
            deezer_result = await self.deezer_repo.search_song(
                song.track_name, song.track_artist
            )

            tracks = deezer_result.get("data", [])
            if not tracks:
                return {"error": "Song not found on Deezer"}

            # Pick the first result
            track_info = tracks[0]

            return {
                "track_id": track_id,
                "track_name": song.track_name,
                "track_artist": song.track_artist,
                "deezer_id": track_info.get("id"),
                "preview_url": track_info.get("preview"),
                "external_url": track_info.get("link"),
                "album_image": track_info.get("album", {}).get("cover_xl")
                or track_info.get("artist", {}).get("picture_xl"),
            }
        except Exception as e:
            return {"error": f"Failed to search song on Deezer: {str(e)}"}

    async def get_song_audio_spotify(self, track_id: str) -> dict:
        # Keeping spotify logic just in case or if needed as fallback
        song = await self.song_repo.get_by_id(track_id)
        if not song:
            return {"error": "Song not found in database"}

        try:
            token = await self.spotify_repo.create_token()
            spotify_result = await self.spotify_repo.search_song(
                song.track_name, song.track_artist, token
            )
            tracks = spotify_result.get("tracks", {}).get("items", [])
            if not tracks:
                return {"error": "Song not found on Spotify"}
            track_info = tracks[0]
            return {
                "track_id": track_id,
                "track_name": song.track_name,
                "track_artist": song.track_artist,
                "spotify_id": track_info.get("id"),
                "preview_url": track_info.get("preview_url"),
                "external_url": track_info.get("external_urls", {}).get("spotify"),
                "album_image": track_info.get("album", {})
                .get("images", [{}])[0]
                .get("url"),
            }
        except Exception as e:
            return {"error": f"Failed to search song on Spotify: {str(e)}"}
