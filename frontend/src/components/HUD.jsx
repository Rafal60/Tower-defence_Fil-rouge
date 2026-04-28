import './HUD.css';

/**
 * HUD — Affiche l'or, les vies, la vague en cours et l'équipe.
 */
export default function HUD({ gameState, team }) {
  const gold = team === 'defender' ? gameState?.defender_gold : gameState?.attacker_gold;

  return (
    <div className="hud-container glass">
      <div className="hud-left">
        <span className={`hud-team ${team}`}>
          {team === 'defender' ? '🛡️ Défenseur' : '⚔️ Attaquant'}
        </span>

        <div className="hud-stat">
          <span className="icon">💰</span>
          <span className="value gold">{gold ?? 0}</span>
        </div>

        <div className="hud-stat">
          <span className="icon">❤️</span>
          <span className="value lives">
            {gameState?.base_hp ?? 0} / {gameState?.base_max_hp ?? 0}
          </span>
        </div>
      </div>

      <div className="hud-right">
        <div className="hud-stat">
          <span className="icon">🌊</span>
          <span className="value wave">
            Vague {gameState?.round ?? 1} / {gameState?.max_round ?? '?'}
          </span>
        </div>
      </div>
    </div>
  );
}
