import { useState, useEffect } from 'react';
import { EMIT, ON } from '../utils/socketEvents';
import HUD from './HUD';
import GameGrid from './GameGrid';
import TowerShop from './TowerShop';
import './GameBoard.css';

/**
 * GameBoard — Conteneur principal du jeu.
 * Reçoit et affiche l'état du jeu depuis le serveur via WebSocket.
 *
 * Props: emit, on, roomId, team
 */
export default function GameBoard({ emit, on, roomId, team }) {
  const [gameState, setGameState] = useState(null);
  const [selectedTower, setSelectedTower] = useState(null);
  const [gameOver, setGameOver] = useState(null);

  useEffect(() => {
    const cleanups = [];

    // Écouter les mises à jour de l'état du jeu
    cleanups.push(on(ON.GAME_STATE_UPDATE, (state) => {
      setGameState(state);
    }));

    // Écouter la fin de partie
    cleanups.push(on(ON.GAME_OVER, (data) => {
      setGameOver(data);
    }));

    return () => cleanups.forEach(fn => fn && fn());
  }, [on]);

  /**
   * Clic sur une case de la grille.
   */
  const handleCellClick = (x, y, cellType) => {
    // Défenseur : placer une tour
    if (team === 'defender' && selectedTower && cellType === 'grass') {
      emit(EMIT.PLACE_TOWER, {
        room_id: roomId,
        type: selectedTower,
        x,
        y,
      });
      setSelectedTower(null);
    }
  };

  const gold = team === 'defender'
    ? gameState?.defender_gold ?? 0
    : gameState?.attacker_gold ?? 0;

  return (
    <div className="gameboard-container">
      {/* HUD en haut */}
      <HUD gameState={gameState} team={team} />

      {/* Grille de jeu au centre */}
      <div className="gameboard-main">
        <GameGrid
          grid={gameState?.grid ?? null}
          towers={gameState?.towers ?? []}
          units={gameState?.units ?? []}
          onCellClick={handleCellClick}
          selectedTower={selectedTower}
        />
      </div>

      {/* Shop en bas */}
      <div className="gameboard-footer">
        <TowerShop
          emit={emit}
          roomId={roomId}
          team={team}
          gold={gold}
          selectedTower={selectedTower}
          onSelectTower={setSelectedTower}
        />
      </div>

      {/* Overlay Game Over */}
      {gameOver && (
        <div className="gameover-overlay">
          <div className="gameover-card glass glow-border">
            <div className="trophy">🏆</div>
            <h2>Partie terminée !</h2>
            <p className="winner">
              {gameOver.winner === team ? '🎉 Victoire !' : '💀 Défaite...'}
            </p>
            <button
              className="btn btn-primary"
              onClick={() => window.location.reload()}
            >
              Retour au lobby
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
