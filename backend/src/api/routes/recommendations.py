from fastapi import APIRouter, Depends
from pydantic import BaseModel

from src.api.dependencies import get_recommender_service, get_text_structure_service
from src.domain.schemas.song import SongResponse
from src.services.recommender_service import RecommenderService
from src.services.text_structure import TextStructureService


class RecommendationRequest(BaseModel):
    song_ids: list[str]
    limit: int = 10


class TextRecommendationRequest(BaseModel):
    text_input: str
    limit: int = 10


router = APIRouter(prefix="/recommend", tags=["recommendations"])


@router.post("/", response_model=list[SongResponse])
async def recommend_songs(
    request: RecommendationRequest,
    service: RecommenderService = Depends(get_recommender_service),
):
    return await service.recommend(request.song_ids, request.limit)


@router.post("/text", response_model=list[SongResponse])
async def recommend_by_text(
    request: TextRecommendationRequest,
    service: TextStructureService = Depends(get_text_structure_service),
):
    return await service.text_structure(request.text_input, request.limit)
