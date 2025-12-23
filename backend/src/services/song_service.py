from src.domain.models.song import SongModel
from src.domain.schemas.song import SongCreate, SongResponse, SongUpdate
from src.repositories.song_repository import SongRepository


class SongService:
    def __init__(self, repo: SongRepository):
        self.repo = repo

    async def create_song(self, song_in: SongCreate) -> SongResponse:
        song = SongModel(**song_in.model_dump())
        created = await self.repo.create(song)
        return SongResponse.model_validate(created)

    async def get_songs(self, limit: int = 100, offset: int = 0) -> list[SongResponse]:
        songs = await self.repo.get_all(limit, offset)
        return [SongResponse.model_validate(s) for s in songs]

    async def get_song_by_id(self, track_id: str) -> SongResponse | None:
        song = await self.repo.get_by_id(track_id)
        if song:
            return SongResponse.model_validate(song)
        return None

    async def update_song(
        self, track_id: str, song_in: SongUpdate
    ) -> SongResponse | None:
        song_data = song_in.model_dump(exclude_unset=True)
        updated = await self.repo.update(track_id, song_data)
        if updated:
            return SongResponse.model_validate(updated)
        return None

    async def delete_song(self, track_id: str) -> bool:
        return await self.repo.delete(track_id)
