import asyncio
import os
import sys
from typing import AsyncGenerator, Generator
from unittest.mock import MagicMock

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from main import app
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from src.agents.song_feature_agent import SongFeaturesAgent
from src.api.dependencies import get_db_session, get_song_feature_agent
from src.domain.models.song import Base
from src.domain.schemas.song import SongFeatures

# Use file-based SQLite database for testing to avoid in-memory persistence issues
TEST_DATABASE_URL = "sqlite+aiosqlite:///./test.db"


@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="function")
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """Create a fresh database session for each test."""

    engine = create_async_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
    )

    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    session_local = async_sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )

    async with session_local() as session:
        yield session
        # Cleanup
        await session.rollback()

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()

    # Remove file
    if os.path.exists("./test.db"):
        os.remove("./test.db")


@pytest_asyncio.fixture(scope="function")
async def async_client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """Create a test client with a database override."""

    async def override_get_db_session():
        yield db_session

    app.dependency_overrides[get_db_session] = override_get_db_session

    # We will also mock the agent by default to avoid API calls
    async def override_get_agent():
        # The service calls agent(input). This invokes __call__.
        # We need an object where object(input) is a coroutine returning SongFeatures.
        mock_agent = MagicMock(spec=SongFeaturesAgent)

        # Define the async function that __call__ will behave like
        async def mock_call(input: str):
            return SongFeatures(
                danceability=0.5,
                energy=0.5,
                valence=0.5,
                tempo=120.0,
                acousticness=0.1,
                instrumentalness=0.0,
                speechiness=0.05,
                liveness=0.1,
                loudness=-5.0,
                key=0,
                mode=1,
                duration_ms=200000,
            )

        mock_agent.side_effect = mock_call
        return mock_agent

    app.dependency_overrides[get_song_feature_agent] = override_get_agent

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        yield client

    app.dependency_overrides.clear()
