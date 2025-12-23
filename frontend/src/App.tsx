import { Header } from './components/Header';
import { Hero } from './components/Hero';
import { SongList } from './components/SongList';
import { PlayerBar } from './components/PlayerBar';

function App() {
  return (
    <>
      <Header />
      <main className="flex-grow w-full max-w-[1280px] mx-auto flex flex-col">
        <Hero />
        <SongList />
      </main>
      <PlayerBar />
    </>
  );
}

export default App;
