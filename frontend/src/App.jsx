import { useState } from 'react';
import { useSocket } from './hooks/useSocket';
import Lobby from './components/Lobby';
import GameBoard from './components/GameBoard';
import './index.css';

function App() {
  const { isConnected, emit, on } = useSocket();
  const [gameData, setGameData] = useState(null); // null = lobby, object = in game

  const handleGameStart = (data) => {
    setGameData(data);
  };

  // Trouver notre team dans les données de la partie
  const team = gameData
    ? Object.values(gameData.players).find(p => true)?.team // sera affiné quand on aura le sid
    : null;

  if (!gameData) {
    return (
      <Lobby
        emit={emit}
        on={on}
        isConnected={isConnected}
        onGameStart={handleGameStart}
      />
    );
  }

  return (
    <GameBoard
      emit={emit}
      on={on}
      roomId={gameData.room_id}
      team={team}
    />
  );
}

export default App;
