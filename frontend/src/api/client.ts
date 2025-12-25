import axios from 'axios';
import type { Song, SongAudioResponse } from '../types';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

export const apiClient = axios.create({
    baseURL: API_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

export const api = {
    getSongs: async (skip: number = 0, limit: number = 10, search?: string): Promise<Song[]> => {
        const params: any = { skip, limit };
        if (search) params.search = search;
        const response = await apiClient.get<Song[]>('/songs/', { params });
        return response.data;
    },

    getSongById: async (trackId: string): Promise<Song> => {
        const response = await apiClient.get<Song>(`/songs/${trackId}`);
        return response.data;
    },

    getSongAudio: async (trackId: string): Promise<SongAudioResponse> => {
        const response = await apiClient.get<SongAudioResponse>(`/music/audio/${trackId}`);
        return response.data;
    },

    getRecommendations: async (songIds: string[], limit: number = 10): Promise<Song[]> => {
        const response = await apiClient.post<Song[]>('/recommend/', { song_ids: songIds, limit });
        return response.data;
    },

    getTextRecommendations: async (text: string, limit: number = 10): Promise<Song[]> => {
        const response = await apiClient.post<Song[]>('/recommend/text', { text_input: text, limit });
        return response.data;
    },
};
