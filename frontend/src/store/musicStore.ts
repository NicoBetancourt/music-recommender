import { create } from 'zustand';
import { api } from '../api/client';
import type { Song, SongAudioResponse } from '../types';
// @ts-ignore
import duckSong from '../resources/duck-song.mp3';

interface MusicState {
    // Song List
    songs: Song[];
    isLoading: boolean;
    error: string | null;
    page: number;
    hasMore: boolean;

    // Search state
    currentSearchQuery: string;
    isMagicMode: boolean;

    // Selection
    selectedSongIds: string[];
    toggleSelection: (trackId: string) => void;
    clearSelection: () => void;

    // Player
    currentSong: Song | null;
    currentAudio: SongAudioResponse | null;
    isPlaying: boolean;
    volume: number;

    // Actions
    fetchSongs: (skip?: number, limit?: number, query?: string) => Promise<void>;
    playSong: (song: Song) => Promise<void>;
    togglePlayPause: () => void;
    setVolume: (vol: number) => void;
    nextSong: () => void;
    prevSong: () => void;
    getRecommendations: () => Promise<void>;
    getMagicRecommendations: (text: string) => Promise<void>;
    toggleMagicMode: () => void;
    setSearchQuery: (query: string) => void;
}

export const useMusicStore = create<MusicState>((set, get) => ({
    songs: [],
    isLoading: false,
    error: null,
    page: 0,
    hasMore: true,
    currentSearchQuery: '',
    isMagicMode: false,

    selectedSongIds: [],
    toggleSelection: (trackId) => {
        set((state) => {
            const isSelected = state.selectedSongIds.includes(trackId);
            return {
                selectedSongIds: isSelected
                    ? state.selectedSongIds.filter((id) => id !== trackId)
                    : [...state.selectedSongIds, trackId],
            };
        });
    },
    clearSelection: () => set({ selectedSongIds: [] }),

    currentSong: null,
    currentAudio: null,
    isPlaying: false,
    volume: 0.5,

    setSearchQuery: (query) => set({ currentSearchQuery: query }),

    fetchSongs: async (skip = 0, limit = 10, query) => {
        set({ isLoading: true, error: null });
        const searchQuery = query !== undefined ? query : get().currentSearchQuery;

        if (skip === 0 && query !== undefined) {
            set({ currentSearchQuery: query });
        }

        try {
            const newSongs = await api.getSongs(skip, limit, searchQuery);
            set((state) => ({
                songs: skip === 0 ? newSongs : [...state.songs, ...newSongs],
                page: skip / limit,
                hasMore: newSongs.length === limit,
                isLoading: false,
            }));
        } catch (err: any) {
            set({ isLoading: false, error: err.message || 'Failed to fetch songs' });
        }
    },

    playSong: async (song) => {
        const { currentSong, isPlaying } = get();
        if (currentSong?.track_id === song.track_id) {
            set({ isPlaying: !isPlaying });
            return;
        }

        set({ currentSong: song, isPlaying: true, isLoading: true });
        try {
            const audioData = await api.getSongAudio(song.track_id);
            set({ currentAudio: audioData, isLoading: false });
        } catch (err: any) {
            console.error("Failed to load audio", err);
            // Handle 404 with duck song
            if (err.response?.status === 404) {
                set({
                    currentAudio: {
                        track_id: song.track_id,
                        preview_url: duckSong,
                        album_image: null
                    },
                    isLoading: false
                });
            } else {
                set({ isLoading: false, isPlaying: false });
            }
        }
    },

    togglePlayPause: () => {
        set((state) => ({ isPlaying: !state.isPlaying }));
    },

    setVolume: (vol) => set({ volume: vol }),

    nextSong: () => {
        const { songs, currentSong } = get();
        if (!currentSong) return;
        const idx = songs.findIndex(s => s.track_id === currentSong.track_id);
        if (idx !== -1 && idx < songs.length - 1) {
            get().playSong(songs[idx + 1]);
        }
    },

    prevSong: () => {
        const { songs, currentSong } = get();
        if (!currentSong) return;
        const idx = songs.findIndex(s => s.track_id === currentSong.track_id);
        if (idx > 0) {
            get().playSong(songs[idx - 1]);
        }
    },

    getRecommendations: async () => {
        const { selectedSongIds } = get();
        if (selectedSongIds.length === 0) return;

        set({ isLoading: true, error: null });
        try {
            const recommendations = await api.getRecommendations(selectedSongIds);
            set({ songs: recommendations, isLoading: false, selectedSongIds: [] });
        } catch (err: any) {
            set({ isLoading: false, error: err.message });
        }
    },

    getMagicRecommendations: async (text: string) => {
        if (!text.trim()) return;

        set({ isLoading: true, error: null });
        try {
            const recommendations = await api.getTextRecommendations(text);
            set({ songs: recommendations, isLoading: false, page: 0, hasMore: false });
        } catch (err: any) {
            set({ isLoading: false, error: err.message });
        }
    },

    toggleMagicMode: () => {
        set((state) => ({ isMagicMode: !state.isMagicMode }));
    }
}));
