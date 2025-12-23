from typing import Sequence

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from src.domain.models.song import SongModel


class SongRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, song: SongModel) -> SongModel:
        self.session.add(song)
        await self.session.commit()
        await self.session.refresh(song)
        return song

    async def get_all(self, limit: int = 100, offset: int = 0) -> Sequence[SongModel]:
        stmt = select(SongModel).limit(limit).offset(offset)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_by_id(self, track_id: str) -> SongModel | None:
        stmt = select(SongModel).where(SongModel.track_id == track_id)
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def update(self, track_id: str, song_data: dict) -> SongModel | None:
        # Check if exists first or update directly
        stmt = (
            update(SongModel)
            .where(SongModel.track_id == track_id)
            .values(**song_data)
            .returning(SongModel)
        )
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.scalars().first()

    async def delete(self, track_id: str) -> bool:
        stmt = delete(SongModel).where(SongModel.track_id == track_id)
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.rowcount > 0  # type: ignore

    async def bulk_create(self, songs: list[SongModel]):
        self.session.add_all(songs)
        await self.session.commit()
