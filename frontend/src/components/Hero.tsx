import { useMusicStore } from '../store/musicStore';
import { useState } from 'react';

export const Hero = () => {
    const { fetchSongs, getMagicRecommendations, isMagicMode, toggleMagicMode, isLoading } = useMusicStore();
    const [query, setQuery] = useState('');

    const handleSearch = (e: React.FormEvent) => {
        e.preventDefault();
        if (isMagicMode) {
            // Use magic search (text-based recommendations)
            getMagicRecommendations(query);
        } else {
            // Use normal search
            fetchSongs(0, 10, query);
        }
    };

    return (
        <section className="px-4 sm:px-10 py-8">
            <div className="relative w-full rounded-2xl overflow-hidden min-h-[260px] flex flex-col items-center justify-center p-6 text-center shadow-xl border border-slate-200 dark:border-[#222949] bg-card-light dark:bg-card-dark">
                <div
                    className="absolute inset-0 bg-cover bg-center z-0 opacity-40 dark:opacity-30"
                    style={{
                        backgroundImage: "linear-gradient(135deg, #0d33f2 0%, #a855f7 100%)",
                    }}
                ></div>
                <div className="relative z-10 flex flex-col gap-6 max-w-2xl w-full items-center">
                    <div className="flex flex-col gap-1">
                        <h2 className="text-2xl sm:text-4xl font-black text-slate-900 dark:text-white tracking-tight">
                            {isMagicMode ? '✨ Búsqueda Mágica' : 'Explora y Descubre'}
                        </h2>
                        <p className="text-sm sm:text-base text-slate-700 dark:text-slate-300 font-medium">
                            {isMagicMode
                                ? 'Describe el tipo de música que buscas y deja que la IA encuentre las canciones perfectas.'
                                : 'Selecciona tus canciones favoritas para recibir recomendaciones personalizadas.'}
                        </p>
                    </div>
                    <div className="w-full max-w-[600px] relative group">
                        <form onSubmit={handleSearch} className="relative flex items-center w-full h-14 bg-white dark:bg-[#101322] rounded-full border-2 border-slate-200 dark:border-[#313a68] shadow-lg overflow-hidden focus-within:border-primary dark:focus-within:border-primary transition-colors">
                            <div className="pl-5 pr-3 text-slate-400 dark:text-[#909acb]">
                                <span className="material-symbols-outlined text-2xl">search</span>
                            </div>
                            <input
                                className="flex-1 bg-transparent border-none focus:ring-0 text-slate-900 dark:text-white placeholder:text-slate-400 dark:placeholder:text-[#909acb] text-base h-full font-medium outline-none"
                                placeholder={isMagicMode ? "Ej: canciones alegres de verano..." : "Buscar canción o artista..."}
                                type="text"
                                value={query}
                                onChange={(e) => setQuery(e.target.value)}
                            />
                            <button
                                type="button"
                                onClick={toggleMagicMode}
                                title={isMagicMode ? "Desactivar búsqueda mágica" : "Activar búsqueda mágica"}
                                className={`mr-2 size-9 rounded-full flex items-center justify-center transition-all ${isMagicMode
                                        ? 'bg-gradient-to-br from-primary to-purple-600 text-white animate-pulse-glow'
                                        : 'bg-slate-100 dark:bg-[#222949] text-slate-400 dark:text-[#909acb] hover:text-primary dark:hover:text-primary'
                                    }`}
                            >
                                <span className="material-symbols-outlined text-xl">auto_awesome</span>
                            </button>
                            <div className="pr-1.5">
                                <button
                                    type="submit"
                                    disabled={isLoading}
                                    className="size-11 rounded-full bg-primary hover:bg-blue-700 text-white flex items-center justify-center transition-all shadow-md transform active:scale-95 disabled:opacity-50 disabled:cursor-not-allowed"
                                >
                                    {isLoading ? (
                                        <span className="material-symbols-outlined animate-spin">progress_activity</span>
                                    ) : (
                                        <span className="material-symbols-outlined">arrow_forward</span>
                                    )}
                                </button>
                            </div>
                        </form>

                        {/* Magic Loading Animation */}
                        {isLoading && isMagicMode && (
                            <div className="absolute -bottom-12 left-0 right-0 flex items-center justify-center gap-2">
                                <div className="flex gap-1">
                                    <span className="w-2 h-2 bg-primary rounded-full animate-sparkle" style={{ animationDelay: '0s' }}></span>
                                    <span className="w-2 h-2 bg-purple-500 rounded-full animate-sparkle" style={{ animationDelay: '0.3s' }}></span>
                                    <span className="w-2 h-2 bg-primary rounded-full animate-sparkle" style={{ animationDelay: '0.6s' }}></span>
                                </div>
                                <p className="text-sm font-medium text-primary dark:text-purple-400 animate-pulse">
                                    Generando recomendaciones mágicas...
                                </p>
                            </div>
                        )}
                    </div>
                </div>
            </div>
        </section>
    );
};
