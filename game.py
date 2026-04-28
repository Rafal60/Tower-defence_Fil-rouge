from enums import State
from typing import List
from models import MapObject, UnitObject, TowerObject
from models import BaseObject
from models.player import AttackerPlayer, DefenderPlayer
import math


class GameObject:
    def __init__(self,
                 _round: int,
                 _max_round: int,
                 _attacker: AttackerPlayer,
                 _defender: DefenderPlayer,
                 _map: MapObject,
                 _base: BaseObject,
                 _tick_rate: float
                 ):
        self.state = State.WAITING
        self.round = _round
        self.max_round = _max_round
        self.attacker = _attacker
        self.defender = _defender
        self.map = _map
        self.base = _base
        self.tick_rate = _tick_rate
        self.current_round_obj = None  # RoundObject de la vague en cours

    def start(self) -> None:
        self.state = State.PLAYING

    def game_loop(self, dt: float) -> None:
        if self.state != State.PLAYING:
            return

        self.update_units(dt)
        self.update_towers(dt)
        self.attacker.collect_income(dt)
        self.check_round_end()
        self.check_game_over()
        self.broadcast_state()

    def update_units(self, dt: float) -> None:
        """Déplace chaque unité le long du chemin."""
        for unit in list(self.map.units):
            unit.move(unit.waypoint_index)
            # TODO: implémenter le déplacement progressif avec dt et speed

    def update_towers(self, dt: float) -> None:
        """Chaque tour cherche une cible dans sa portée et attaque."""
        for tower in self.map.towers:
            tower.cooldown_remaining -= dt
            if tower.cooldown_remaining <= 0:
                # Chercher les unités dans la portée
                units_in_range = []
                for unit in self.map.units:
                    dist = math.hypot(unit.x - tower.x, unit.y - tower.y)
                    if dist <= tower.attack_range:
                        units_in_range.append(unit)

                if units_in_range:
                    tower.attack(units_in_range)
                    tower.cooldown_remaining = tower.attack_speed

    def check_round_end(self) -> None:
        """Vérifie si la vague est terminée (plus d'unités vivantes et queue vide)."""
        if self.current_round_obj is None:
            return

        all_spawned = len(self.current_round_obj.spawn_queue) == 0
        no_units_alive = len(self.map.units) == 0

        if all_spawned and no_units_alive:
            self.current_round_obj.is_finished = True
            self.next_round()

    def check_game_over(self) -> None:
        """Vérifie si la partie est terminée."""
        # L'attaquant gagne si la base est détruite
        if self.base.hp <= 0:
            self.end_game("attacker")
            return

        # Le défenseur gagne si toutes les vagues sont passées
        if self.round > self.max_round and len(self.map.units) == 0:
            self.end_game("defender")

    def broadcast_state(self) -> None:
        """Envoie l'état du jeu à tous les joueurs via WebSocket."""
        # TODO: implémenter avec Flask-SocketIO
        # socketio.emit('game_state_update', self.to_dict(), room=self.room_id)
        pass

    def next_round(self) -> None:
        """Passe à la vague suivante et accorde un bonus d'or."""
        self.round += 1
        # Bonus d'or entre les vagues
        self.attacker.earn(50)
        self.defender.earn(50)

    def end_game(self, winner: str) -> None:
        """Termine la partie."""
        self.state = State.GAME_OVER
        # TODO: émettre l'événement 'game_over' via WebSocket
        # socketio.emit('game_over', {'winner': winner}, room=self.room_id)

    def to_dict(self) -> dict:
        """Sérialise l'état complet du jeu pour envoi WebSocket."""
        return {
            "state": self.state.value,
            "round": self.round,
            "max_round": self.max_round,
            "base_hp": self.base.hp,
            "base_max_hp": self.base.max_hp,
            "attacker_gold": self.attacker.gold,
            "defender_gold": self.defender.gold,
            "units": [u.to_dict() for u in self.map.units],
            "towers": [t.to_dict() for t in self.map.towers],
        }