from pydantic import BaseModel, ConfigDict, Field


class SongFeatures(BaseModel):
    danceability: float = Field(
        description="Danceability describes how suitable a track is for dancing based on a combination of musical elements including tempo, rhythm stability, beat strength, and overall regularity. A value of 0.0 is least danceable and 1.0 is most danceable."
    )

    energy: float = Field(
        description="Energy is a measure from 0.0 to 1.0 and represents a perceptual measure of intensity and activity. Typically, energetic tracks feel fast, loud, and noisy. For example, death metal has high energy, while a Bach prelude scores low on the scale."
    )

    key: int = Field(
        description="The key the track is in. Integers map to pitches using standard Pitch Class notation. E.g. 0 = C, 1 = C♯/D♭, 2 = D, and so on."
    )

    loudness: float = Field(
        description="The overall loudness of a track in decibels (dB). Loudness values are averaged across the entire track and are useful for comparing relative loudness of tracks. Values typical range between -60 and 0 db."
    )

    mode: int = Field(
        description="Mode indicates the modality (major or minor) of a track, the type of scale from which its melodic content is derived. Major is represented by 1 and minor is 0."
    )

    speechiness: float = Field(
        description="Speechiness detects the presence of spoken words in a track."
    )

    acousticness: float = Field(
        description="A confidence measure from 0.0 to 1.0 of whether the track is acoustic. 1.0 represents high confidence the track is acoustic."
    )

    instrumentalness: float = Field(
        description="Predicts whether a track contains no vocals. 'Ooh' and 'aah' sounds are treated as instrumental in this context."
    )

    liveness: float = Field(
        description="Detects the presence of an audience in the recording."
    )

    valence: float = Field(
        description="A measure from 0.0 to 1.0 describing the musical positiveness conveyed by a track."
    )

    mode: int = Field(
        description="Mode indicates the modality (major or minor) of a track, the type of scale from which its melodic content is derived. Major is represented by 1 and minor is 0."
    )

    speechiness: float = Field(
        description="Speechiness detects the presence of spoken words in a track."
    )

    acousticness: float = Field(
        description="A confidence measure from 0.0 to 1.0 of whether the track is acoustic. 1.0 represents high confidence the track is acoustic."
    )

    instrumentalness: float = Field(
        description="Predicts whether a track contains no vocals. 'Ooh' and 'aah' sounds are treated as instrumental in this context."
    )

    liveness: float = Field(
        description="Detects the presence of an audience in the recording."
    )

    valence: float = Field(
        description="A measure from 0.0 to 1.0 describing the musical positiveness conveyed by a track."
    )
    tempo: float = Field(
        description="BPM. Low (<80) for relax, High (>120) for workout/energy."
    )


class SongBase(SongFeatures):
    track_name: str
    track_artist: str
    track_popularity: int
    track_album_id: str
    track_album_name: str
    track_album_release_date: str
    playlist_name: str | None = None
    playlist_id: str | None = None
    playlist_genre: str | None = None
    playlist_subgenre: str | None = None

    tempo: float
    duration_ms: int


class SongCreate(SongBase):
    track_id: str


class SongUpdate(BaseModel):
    track_name: str | None = None
    track_artist: str | None = None
    track_popularity: int | None = None
    # Add other fields as optional for update if needed, keeping it simple for now


class SongResponse(SongBase):
    track_id: str

    model_config = ConfigDict(from_attributes=True)
