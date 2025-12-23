import httpx
from src.core.config import settings


class DeezerRepository:
    def __init__(self):
        self.base_url = settings.URL_DEEZER

    async def search_song(self, name: str, artist: str) -> dict:
        async with httpx.AsyncClient() as client:
            path = f"{self.base_url}/search"
            query = f'track:"{name}" artist:"{artist}"'
            params = {"q": query, "limit": 1}
            response = await client.get(path, params=params)
            response.raise_for_status()
            return response.json()
