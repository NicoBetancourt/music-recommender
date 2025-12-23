from fastapi import APIRouter, Depends, HTTPException
from src.api.dependencies import get_song_service
from src.domain.schemas.song import SongCreate, SongResponse, SongUpdate
from src.services.song_service import SongService

router = APIRouter(prefix="/songs", tags=["songs"])


@router.post("/", response_model=SongResponse)
async def create_song(
    song_in: SongCreate, service: SongService = Depends(get_song_service)
):
    return await service.create_song(song_in)


@router.get("/", response_model=list[SongResponse])
async def read_songs(
    skip: int = 0,
    limit: int = 100,
    search: str | None = None,
    service: SongService = Depends(get_song_service),
):
    return await service.get_songs(limit=limit, offset=skip, search=search)


@router.get("/{track_id}", response_model=SongResponse)
async def read_song(track_id: str, service: SongService = Depends(get_song_service)):
    song = await service.get_song_by_id(track_id)
    if not song:
        raise HTTPException(status_code=404, detail="Song not found")
    return song


@router.put("/{track_id}", response_model=SongResponse)
async def update_song(
    track_id: str, song_in: SongUpdate, service: SongService = Depends(get_song_service)
):
    song = await service.update_song(track_id, song_in)
    if not song:
        raise HTTPException(status_code=404, detail="Song not found")
    return song


@router.delete("/{track_id}", response_model=bool)
async def delete_song(track_id: str, service: SongService = Depends(get_song_service)):
    success = await service.delete_song(track_id)
    if not success:
        raise HTTPException(status_code=404, detail="Song not found")
    return success
