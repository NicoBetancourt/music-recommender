from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Float, Integer

class Base(DeclarativeBase):
    pass

class SongModel(Base):
    __tablename__ = "songs"

    track_id: Mapped[str] = mapped_column(String, primary_key=True)
    track_name: Mapped[str] = mapped_column(String, nullable=False)
    track_artist: Mapped[str] = mapped_column(String, nullable=False)
    track_popularity: Mapped[int] = mapped_column(Integer)
    track_album_id: Mapped[str] = mapped_column(String)
    track_album_name: Mapped[str] = mapped_column(String)
    track_album_release_date: Mapped[str] = mapped_column(String)
    playlist_name: Mapped[str | None] = mapped_column(String, nullable=True)
    playlist_id: Mapped[str | None] = mapped_column(String, nullable=True)
    playlist_genre: Mapped[str | None] = mapped_column(String, nullable=True)
    playlist_subgenre: Mapped[str | None] = mapped_column(String, nullable=True)
    
    danceability: Mapped[float] = mapped_column(Float)
    energy: Mapped[float] = mapped_column(Float)
    key: Mapped[int] = mapped_column(Integer)
    loudness: Mapped[float] = mapped_column(Float)
    mode: Mapped[int] = mapped_column(Integer)
    speechiness: Mapped[float] = mapped_column(Float)
    acousticness: Mapped[float] = mapped_column(Float)
    instrumentalness: Mapped[float] = mapped_column(Float)
    liveness: Mapped[float] = mapped_column(Float)
    valence: Mapped[float] = mapped_column(Float)
    tempo: Mapped[float] = mapped_column(Float)
    duration_ms: Mapped[int] = mapped_column(Integer)
