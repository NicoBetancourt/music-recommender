from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.agents.song_feature_agent import SongFeaturesAgent
from src.core.database import get_db_session
from src.repositories.deezer_repository import DeezerRepository
from src.repositories.song_repository import SongRepository
from src.repositories.spotify_repository import SpotifyRepository
from src.services.music_service import MusicService
from src.services.recommender_service import RecommenderService
from src.services.song_service import SongService
from src.services.text_structure import TextStructureService


async def get_repository(
    session: AsyncSession = Depends(get_db_session),
) -> SongRepository:
    return SongRepository(session)


async def get_song_service(
    repo: SongRepository = Depends(get_repository),
) -> SongService:
    return SongService(repo)


async def get_recommender_service(
    repo: SongRepository = Depends(get_repository),
) -> RecommenderService:
    return RecommenderService(repo)


async def get_spotify_repository() -> SpotifyRepository:
    return SpotifyRepository()


async def get_deezer_repository() -> DeezerRepository:
    return DeezerRepository()


async def get_music_service(
    song_repo: SongRepository = Depends(get_repository),
    deezer_repo: DeezerRepository = Depends(get_deezer_repository),
    spotify_repo: SpotifyRepository = Depends(get_spotify_repository),
) -> MusicService:
    return MusicService(song_repo, deezer_repo, spotify_repo)


async def get_song_feature_agent() -> SongFeaturesAgent:
    return SongFeaturesAgent()


async def get_text_structure_service(
    agent: SongFeaturesAgent = Depends(get_song_feature_agent),
    recommender_service: RecommenderService = Depends(get_recommender_service),
) -> TextStructureService:
    return TextStructureService(agent, recommender_service)
