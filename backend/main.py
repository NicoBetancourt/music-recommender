from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.routes import music, recommendations, songs
from src.core.config import settings
from src.utils.seeder import seed_database


@asynccontextmanager
async def lifespan(app: FastAPI):
    await seed_database()
    yield


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan,
)

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(songs.router, prefix=settings.API_V1_STR)
app.include_router(recommendations.router, prefix=settings.API_V1_STR)
app.include_router(music.router, prefix=settings.API_V1_STR)


@app.get("/")
def root():
    return {"message": "Welcome to Music Recommender API"}
