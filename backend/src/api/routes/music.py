from fastapi import APIRouter, Depends, HTTPException
from src.api.dependencies import get_music_service
from src.services.music_service import MusicService

router = APIRouter(prefix="/music", tags=["music"])


@router.get("/audio/{track_id}")
async def get_song_audio(
    track_id: str, service: MusicService = Depends(get_music_service)
):
    result = await service.get_song_audio(track_id)
    if "error" in result:
        status_code = 404 if "not found" in result["error"] else 400
        raise HTTPException(status_code=status_code, detail=result["error"])
    return result
