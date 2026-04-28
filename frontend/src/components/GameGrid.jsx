import './GameGrid.css';

/**
 * Icônes des entités pour le rendu dans la grille.
 */
const TOWER_ICONS = {
  ARCHER: '🏹',
  CANNON: '💣',
  FREEZE: '❄️',
};

const UNIT_ICONS = {
  MAGE: '🧙',
  SOLDAT: '⚔️',
};

/**
 * GameGrid — Affiche la grille 2D du jeu.
 *
 * Attend un `grid` sous cette forme (envoyé par le backend) :
 * [
 *   [{ "type": "grass" }, { "type": "path" }, { "type": "grass" }],
 *   [{ "type": "grass" }, { "type": "path", "entity": { "kind": "tower", "type": "ARCHER", "hp": 50, "max_hp": 50 } }, ...]
 * ]
 *
 * Si `grid` est null/undefined, affiche un placeholder.
 * 
 * Props: grid, towers, units, onCellClick, selectedTower
 */
export default function GameGrid({ grid, towers, units, onCellClick, selectedTower }) {

  // Si pas de grille reçue du backend, afficher un placeholder
  if (!grid || grid.length === 0) {
    return (
      <div className="glass glow-border grid-placeholder">
        <span className="icon">🗺️</span>
        <p>En attente de la grille du serveur...</p>
        <p style={{ fontSize: '0.8rem' }}>La carte sera générée par le backend</p>
      </div>
    );
  }

  const cols = grid[0].length;

  // Mapper les entités (tours + unités) sur la grille pour un accès rapide
  const entityMap = {};

  if (towers) {
    for (const tower of towers) {
      entityMap[`${tower.x}-${tower.y}`] = { kind: 'tower', ...tower };
    }
  }

  if (units) {
    for (const unit of units) {
      // Les unités peuvent avoir des positions flottantes, on arrondit
      const rx = Math.round(unit.x);
      const ry = Math.round(unit.y);
      entityMap[`${rx}-${ry}`] = { kind: 'unit', ...unit };
    }
  }

  return (
    <div
      className="game-grid"
      style={{ gridTemplateColumns: `repeat(${cols}, 48px)` }}
    >
      {grid.map((row, y) =>
        row.map((cell, x) => {
          const entity = entityMap[`${x}-${y}`];
          const cellType = cell.type || 'empty';

          // Déterminer si on peut placer ici
          const canPlace = selectedTower && cellType === 'grass' && !entity;

          return (
            <div
              key={`${x}-${y}`}
              className={`grid-cell ${cellType} ${canPlace ? 'placeable' : ''} ${selectedTower && !canPlace ? 'not-placeable' : ''}`}
              onClick={() => onCellClick && onCellClick(x, y, cellType)}
            >
              {/* Entité sur la case */}
              {entity && (
                <>
                  <span className="cell-entity">
                    {entity.kind === 'tower'
                      ? TOWER_ICONS[entity.type] || '🏗️'
                      : UNIT_ICONS[entity.type] || '👤'
                    }
                  </span>

                  {/* Barre de vie */}
                  {entity.hp != null && entity.max_hp != null && (
                    <div className="cell-healthbar">
                      <div
                        className={`cell-healthbar-fill ${entity.hp / entity.max_hp < 0.3 ? 'low' : ''}`}
                        style={{ width: `${(entity.hp / entity.max_hp) * 100}%` }}
                      />
                    </div>
                  )}
                </>
              )}
            </div>
          );
        })
      )}
    </div>
  );
}
