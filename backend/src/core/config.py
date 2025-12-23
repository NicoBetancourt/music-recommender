from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "Music Recommender"
    API_V1_STR: str = "/api/v1"
    DATABASE_URL: str = "sqlite+aiosqlite:///./src/core/storage/music.db"

    # Spotify API Configuration
    URL_SPOTIFY: str = "https://api.spotify.com/v1"
    URL_SPOTIFY_ACCOUNT: str = "https://accounts.spotify.com/api/token"
    SPOTIFY_BASIC_AUTHENTICATION: str = ""

    # Deezer API Configuration
    URL_DEEZER: str = "https://api.deezer.com"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore",
    )


settings = Settings()
