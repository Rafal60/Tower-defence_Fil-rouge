import { useState, useEffect } from 'react';
import { EMIT, ON } from '../utils/socketEvents';
import './Lobby.css';

/**
 * Lobby — Créer ou rejoindre une room.
 * Props: emit, on, isConnected, onGameStart
 */
export default function Lobby({ emit, on, isConnected, onGameStart }) {
  const [username, setUsername] = useState('');
  const [roomId, setRoomId] = useState('');
  const [team, setTeam] = useState(null);       // 'attacker' | 'defender'
  const [waiting, setWaiting] = useState(false);
  const [playerCount, setPlayerCount] = useState(0);
  const [isReady, setIsReady] = useState(false);

  useEffect(() => {
    const cleanups = [];

    cleanups.push(on(ON.ROOM_CREATED, (data) => {
      setTeam(data.team);
      setRoomId(data.room_id);
      setWaiting(true);
      setPlayerCount(1);
    }));

    cleanups.push(on(ON.ROOM_JOINED, (data) => {
      setTeam(data.team);
      setRoomId(data.room_id);
      setWaiting(true);
      setPlayerCount(2);
    }));

    cleanups.push(on(ON.PLAYER_JOINED, (data) => {
      setPlayerCount(data.player_count);
    }));

    cleanups.push(on(ON.GAME_START, (data) => {
      onGameStart({ ...data, myTeam: team });
    }));

    return () => cleanups.forEach(fn => fn && fn());
  }, [on, onGameStart, team]);

  const handleCreate = (e) => {
    e.preventDefault();
    if (!username.trim() || !roomId.trim()) return;
    emit(EMIT.CREATE_ROOM, { room_id: roomId, username });
  };

  const handleJoin = (e) => {
    e.preventDefault();
    if (!username.trim() || !roomId.trim()) return;
    emit(EMIT.JOIN_ROOM, { room_id: roomId, username });
  };

  const handleReady = () => {
    emit(EMIT.PLAYER_READY, { room_id: roomId });
    setIsReady(true);
  };

  return (
    <div className="lobby-container">
      <h1 className="lobby-title">TOWER DEFENSE</h1>
      <p className="lobby-subtitle">Défends ta base ou envoie tes troupes</p>

      <div className="lobby-status">
        <span className={`status-dot ${isConnected ? 'online' : 'offline'}`} />
        {isConnected ? 'Connecté au serveur' : 'Connexion en cours...'}
      </div>

      {!waiting ? (
        <div className="lobby-card glass glow-border">
          <h2>🏰 Rejoindre une partie</h2>
          <form className="lobby-form" onSubmit={handleJoin}>
            <input
              className="input"
              type="text"
              placeholder="Ton pseudo"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
            />
            <input
              className="input"
              type="text"
              placeholder="Code de la room"
              value={roomId}
              onChange={(e) => setRoomId(e.target.value)}
              required
            />
            <button className="btn btn-primary" type="submit" disabled={!isConnected}>
              Rejoindre
            </button>
          </form>

          <div className="lobby-divider">ou</div>

          <button
            className="btn btn-outline"
            style={{ width: '100%' }}
            onClick={handleCreate}
            disabled={!isConnected || !username.trim() || !roomId.trim()}
          >
            Créer une room
          </button>
        </div>
      ) : (
        <div className="lobby-card glass glow-border">
          <div className="lobby-waiting">
            <p>Room</p>
            <div className="room-code">{roomId}</div>
            <p>
              <span className={`lobby-team-badge ${team}`}>
                {team === 'defender' ? '🛡️ Défenseur' : '⚔️ Attaquant'}
              </span>
            </p>
            <p style={{ marginTop: '1rem' }}>
              {playerCount < 2 ? (
                <span className="animate-pulse">En attente d'un adversaire...</span>
              ) : !isReady ? (
                <button className="btn btn-gold" onClick={handleReady}>
                  ✅ Prêt !
                </button>
              ) : (
                <span className="animate-pulse">En attente de l'adversaire...</span>
              )}
            </p>
            <p style={{ marginTop: '0.5rem', fontSize: '0.8rem', color: 'var(--text-muted)' }}>
              {playerCount}/2 joueurs
            </p>
          </div>
        </div>
      )}
    </div>
  );
}
