from fastapi import APIRouter, Depends
from pydantic import BaseModel
from src.api.dependencies import get_recommender_service
from src.domain.schemas.song import SongResponse
from src.services.recommender_service import RecommenderService


class RecommendationRequest(BaseModel):
    song_ids: list[str]
    limit: int = 10


router = APIRouter(prefix="/recommend", tags=["recommendations"])


@router.post("/", response_model=list[SongResponse])
async def recommend_songs(
    request: RecommendationRequest,
    service: RecommenderService = Depends(get_recommender_service),
):
    return await service.recommend(request.song_ids, request.limit)
