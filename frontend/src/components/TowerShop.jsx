import { useState } from 'react';
import { EMIT } from '../utils/socketEvents';
import './TowerShop.css';

/**
 * Données des tours et unités (miroir de enums.py).
 */
const TOWERS = [
  { type: 'ARCHER', icon: '🏹', name: 'Archer', price: 10 },
  { type: 'CANNON', icon: '💣', name: 'Canon', price: 20 },
  { type: 'FREEZE', icon: '❄️', name: 'Gel', price: 25 },
];

const UNITS = [
  { type: 'MAGE', icon: '🧙', name: 'Mage', price: 10 },
  { type: 'SOLDAT', icon: '⚔️', name: 'Soldat', price: 30 },
];

/**
 * TowerShop — Barre de sélection des tours (défenseur) ou unités (attaquant).
 * Props: emit, roomId, team, gold, selectedTower, onSelectTower
 */
export default function TowerShop({ emit, roomId, team, gold, selectedTower, onSelectTower }) {

  const handleSendUnit = (unitType) => {
    emit(EMIT.SEND_UNIT, { room_id: roomId, type: unitType });
  };

  if (team === 'defender') {
    return (
      <div className="tower-shop glass">
        <span className="tower-shop-title">🛡️ Tours</span>
        {TOWERS.map((tower) => (
          <div
            key={tower.type}
            className={`tower-card ${selectedTower === tower.type ? 'selected' : ''} ${gold < tower.price ? 'disabled' : ''}`}
            onClick={() => gold >= tower.price && onSelectTower(tower.type)}
          >
            <span className="tower-icon">{tower.icon}</span>
            <span className="tower-name">{tower.name}</span>
            <span className="tower-price">💰 {tower.price}</span>
          </div>
        ))}
      </div>
    );
  }

  // Attacker view
  return (
    <div className="tower-shop glass">
      <span className="tower-shop-title">⚔️ Unités</span>
      {UNITS.map((unit) => (
        <div
          key={unit.type}
          className={`unit-card ${gold < unit.price ? 'disabled' : ''}`}
          onClick={() => gold >= unit.price && handleSendUnit(unit.type)}
        >
          <span className="tower-icon">{unit.icon}</span>
          <span className="tower-name">{unit.name}</span>
          <span className="tower-price">💰 {unit.price}</span>
        </div>
      ))}
    </div>
  );
}
