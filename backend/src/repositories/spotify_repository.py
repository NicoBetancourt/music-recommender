import httpx
from src.core.config import settings


class SpotifyRepository:
    def __init__(self):
        self.base_url = settings.URL_SPOTIFY
        self.account_url = settings.URL_SPOTIFY_ACCOUNT
        self.basic_auth = settings.SPOTIFY_BASIC_AUTHENTICATION

    async def create_token(self) -> str:
        async with httpx.AsyncClient() as client:
            headers = {"Authorization": f"Basic {self.basic_auth}"}
            data = {"grant_type": "client_credentials"}
            response = await client.post(self.account_url, headers=headers, data=data)
            response.raise_for_status()
            data = response.json()
            return data["access_token"]

    async def search_song(self, name: str, artist: str, token: str) -> dict:
        async with httpx.AsyncClient() as client:
            path = f"{self.base_url}/search"
            query = f"track:{name} artist:{artist}"
            params = {"q": query, "type": "track", "limit": 1}
            headers = {"Authorization": f"Bearer {token}"}
            response = await client.get(path, params=params, headers=headers)
            response.raise_for_status()
            return response.json()
