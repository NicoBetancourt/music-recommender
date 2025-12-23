export interface Song {
    track_id: string;
    track_name: string;
    track_artist: string;
    track_popularity: number;
    track_album_id: string;
    track_album_name: string;
    track_album_release_date: string;
    playlist_name?: string | null;
    playlist_id?: string | null;
    playlist_genre?: string | null;
    playlist_subgenre?: string | null;
    duration_ms: number;
    // Other fields present in DB but maybe optional for UI
    danceability: number;
    energy: number;
    key: number;
    loudness: number;
    mode: number;
    speechiness: number;
    acousticness: number;
    instrumentalness: number;
    liveness: number;
    valence: number;
    tempo: number;
}

export interface SongAudioResponse {
    track_id: string;
    preview_url: string | null;
    album_image: string | null;
    name?: string; // Sometimes returned
    artist?: string; // Sometimes returned
}

export interface RecommendationRequest {
    song_ids: string[];
    limit: number;
}
