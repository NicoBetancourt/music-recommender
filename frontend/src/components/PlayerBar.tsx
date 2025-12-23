import { useEffect, useRef } from 'react';
import { useMusicStore } from '../store/musicStore';

export const PlayerBar = () => {
    const { currentSong, currentAudio, isPlaying, togglePlayPause, volume, setVolume, nextSong, prevSong } = useMusicStore();
    const audioRef = useRef<HTMLAudioElement | null>(null);

    useEffect(() => {
        if (audioRef.current && currentAudio?.preview_url) {
            audioRef.current.src = currentAudio.preview_url;
            if (isPlaying) {
                audioRef.current.play().catch(e => console.error("Playback failed", e));
            }
        }
    }, [currentAudio]);

    useEffect(() => {
        if (audioRef.current) {
            if (isPlaying) {
                audioRef.current.play().catch(e => console.error("Playback failed", e));
            } else {
                audioRef.current.pause();
            }
        }
    }, [isPlaying]);

    useEffect(() => {
        if (audioRef.current) {
            audioRef.current.volume = volume;
        }
    }, [volume]);

    if (!currentSong) return null;

    return (
        <div className="fixed bottom-0 left-0 right-0 bg-card-light dark:bg-card-dark border-t border-slate-200 dark:border-[#222949] p-3 shadow-[0_-4px_6px_-1px_rgba(0,0,0,0.1)] z-40">
            <audio ref={audioRef} onEnded={nextSong} />
            <div className="max-w-[1280px] mx-auto flex items-center justify-between gap-4">
                <div className="flex items-center gap-3 w-1/3 min-w-0">
                    <div
                        className="size-12 rounded bg-cover bg-center shrink-0 hidden sm:flex items-center justify-center bg-slate-200 dark:bg-[#1e293b]"
                        style={{
                            backgroundImage: currentAudio?.album_image ? `url("${currentAudio.album_image}")` : 'none',
                        }}
                    >
                        {!currentAudio?.album_image && (
                            <span className="material-symbols-outlined text-slate-500 text-2xl">music_note</span>
                        )}
                    </div>
                    <div className="flex flex-col min-w-0">
                        <p className="text-sm font-bold text-slate-900 dark:text-white truncate">
                            {currentSong.track_name}
                        </p>
                        <p className="text-xs text-slate-500 dark:text-[#909acb] truncate">
                            {currentSong.track_artist}
                        </p>
                    </div>
                </div>
                <div className="flex flex-col items-center gap-1 flex-1">
                    <div className="flex items-center gap-4 text-slate-700 dark:text-white">
                        <button onClick={prevSong} className="text-slate-900 dark:text-white hover:text-primary transition-colors">
                            <span className="material-symbols-outlined text-3xl">skip_previous</span>
                        </button>
                        <button
                            onClick={togglePlayPause}
                            className="size-10 rounded-full bg-primary text-white flex items-center justify-center hover:scale-105 transition-transform shadow-md"
                        >
                            <span className="material-symbols-outlined fill-1">
                                {isPlaying ? 'pause' : 'play_arrow'}
                            </span>
                        </button>
                        <button onClick={nextSong} className="text-slate-900 dark:text-white hover:text-primary transition-colors">
                            <span className="material-symbols-outlined text-3xl">skip_next</span>
                        </button>
                    </div>
                    <div className="w-full max-w-md h-1 bg-slate-200 dark:bg-[#313a68] rounded-full overflow-hidden flex items-center">
                        <div className="h-full w-1/3 bg-primary rounded-full relative"></div>
                    </div>
                </div>
                <div className="hidden sm:flex items-center justify-end gap-3 w-1/3 text-slate-500 dark:text-[#909acb]">
                    <div className="flex items-center gap-2 group">
                        <span className="material-symbols-outlined">{volume === 0 ? 'volume_off' : 'volume_up'}</span>
                        <input
                            type="range"
                            min="0"
                            max="1"
                            step="0.01"
                            value={volume}
                            onChange={(e) => setVolume(parseFloat(e.target.value))}
                            className="w-24 h-1 bg-slate-200 dark:bg-[#313a68] rounded-full appearance-none cursor-pointer accent-primary"
                        />
                    </div>
                </div>
            </div>
        </div>
    );
};
