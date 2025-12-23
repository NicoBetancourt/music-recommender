import { useEffect } from 'react';
import { useMusicStore } from '../store/musicStore';

export const SongList = () => {
    const { songs, isLoading, fetchSongs, playSong, toggleSelection, selectedSongIds, page, hasMore, getRecommendations } = useMusicStore();

    useEffect(() => {
        fetchSongs();
    }, [fetchSongs]);

    const handleLoadMore = () => {
        fetchSongs((page + 1) * 10, 10);
    };

    return (
        <section className="px-4 sm:px-10 pb-28 flex-1 flex flex-col gap-6">
            <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
                <h3 className="text-xl font-bold text-slate-900 dark:text-white flex items-center gap-2">
                    <span className="material-symbols-outlined text-primary">queue_music</span>
                    Resultados de búsqueda
                </h3>
                <button
                    onClick={() => getRecommendations()}
                    disabled={selectedSongIds.length === 0}
                    className={`w-full sm:w-auto px-6 py-3 bg-primary hover:bg-blue-700 active:bg-blue-800 text-white font-bold rounded-xl shadow-lg hover:shadow-primary/25 transition-all flex items-center justify-center gap-2 group ${selectedSongIds.length === 0 ? 'opacity-50 cursor-not-allowed' : ''}`}
                >
                    <span className="material-symbols-outlined group-hover:animate-pulse">
                        auto_awesome
                    </span>
                    Recomendar Canciones Similares
                </button>
            </div>

            <div className="bg-card-light dark:bg-card-dark rounded-2xl shadow-sm border border-slate-200 dark:border-[#222949] overflow-hidden flex flex-col">
                <div className="flex items-center gap-4 px-6 py-3 bg-slate-50 dark:bg-[#1f253e] border-b border-slate-200 dark:border-[#313a68] text-xs font-bold text-slate-500 dark:text-[#909acb] uppercase tracking-wider">
                    <div className="w-5 text-center">#</div>
                    <div className="flex-1">Título / Artista</div>
                    <div className="hidden sm:block">Acción</div>
                </div>
                <div className="divide-y divide-slate-100 dark:divide-[#222949]">
                    {songs.map((song) => (
                        <div
                            key={song.track_id}
                            className="group flex items-center gap-4 px-4 sm:px-6 py-4 hover:bg-slate-50 dark:hover:bg-[#1f253e] transition-colors"
                        >
                            <div className="flex items-center justify-center h-full">
                                <input
                                    aria-label="Seleccionar canción"
                                    className="size-5 rounded border-slate-300 dark:border-slate-600 text-primary focus:ring-primary bg-transparent cursor-pointer transition-colors"
                                    type="checkbox"
                                    checked={selectedSongIds.includes(song.track_id)}
                                    onChange={() => toggleSelection(song.track_id)}
                                />
                            </div>
                            <div
                                className="flex-1 min-w-0 cursor-pointer"
                                role="button"
                                title="Haz clic para reproducir"
                                onClick={() => playSong(song)}
                            >
                                <div className="flex flex-col sm:flex-row sm:items-center gap-1 sm:gap-3">
                                    <span className="text-base sm:text-lg font-bold text-slate-900 dark:text-white truncate group-hover:text-primary transition-colors">
                                        {song.track_name}
                                    </span>
                                    <span className="hidden sm:inline text-slate-300 dark:text-slate-600">
                                        •
                                    </span>
                                    <span className="text-sm font-medium text-slate-500 dark:text-[#909acb] truncate">
                                        {song.track_artist}
                                    </span>
                                </div>
                            </div>
                            <button
                                onClick={() => playSong(song)}
                                className="size-10 rounded-full text-slate-300 dark:text-slate-600 group-hover:text-primary group-hover:bg-primary/10 flex items-center justify-center transition-all opacity-0 group-hover:opacity-100"
                            >
                                <span className="material-symbols-outlined text-2xl">play_circle</span>
                            </button>
                        </div>
                    ))}
                    {isLoading && (
                        <div className="p-4 text-center text-slate-500">Cargando...</div>
                    )}
                    {!isLoading && hasMore && (
                        <div className="p-4 flex justify-center">
                            <button onClick={handleLoadMore} className="text-primary hover:underline">
                                Cargar más
                            </button>
                        </div>
                    )}
                </div>
            </div>
        </section>
    );
};
