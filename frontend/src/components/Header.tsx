export const Header = () => {
    return (
        <header className="sticky top-0 z-50 w-full bg-card-light/90 dark:bg-card-dark/90 backdrop-blur-md border-b border-slate-200 dark:border-[#222949]">
            <div className="max-w-[1280px] mx-auto px-4 sm:px-10 py-3 flex items-center justify-between">
                <div className="flex items-center gap-3">
                    <div className="size-8 text-primary flex items-center justify-center">
                        <span className="material-symbols-outlined text-3xl">equalizer</span>
                    </div>
                    <h1 className="text-lg font-bold tracking-tight">Sound Recommender</h1>
                </div>
                <div className="flex items-center gap-4">
                    <button className="flex items-center justify-center size-10 overflow-hidden rounded-full bg-slate-200 dark:bg-[#222949] border-2 border-transparent hover:border-primary transition-colors">
                        <span className="material-symbols-outlined text-slate-500 dark:text-white text-xl">
                            person
                        </span>
                    </button>
                </div>
            </div>
        </header>
    );
};
