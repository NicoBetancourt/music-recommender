from src.agents.song_feature_agent import SongFeaturesAgent
from src.domain.schemas.song import SongResponse
from src.services.recommender_service import RecommenderService


class TextStructureService:
    def __init__(
        self, agent: SongFeaturesAgent, recommender_service: RecommenderService
    ):
        self.agent = agent
        self.recommender_service = recommender_service

    async def text_structure(self, text: str, limit: int) -> list[SongResponse]:
        text_feature = await self.agent(text)
        songs = await self.recommender_service.recommend_from_features(
            text_feature, limit
        )
        return songs
