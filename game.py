from enums import State, Team
from typing import List, Dict
from models import MapObject, AttackObject, DefenseObject
from models import BaseObject


class GameObject:
    def __init__(
        self,
        _round: int,
        _max_round: int,
        _players: Dict[Team, object],
        _map: MapObject,
        _base: BaseObject,
        _tick_rate: float
    ):
        self.state = State.WAITING
        self.round = _round
        self.max_round = _max_round
        # { Team.ATTACKER: player, Team.DEFENDER: player }
        self.players = _players
        self.map = _map
        self.base = _base
        self.units: List[AttackObject] = []
        self.towers: List[DefenseObject] = []
        self.tick_rate = _tick_rate
        self._id_counter = 0

    def get_next_id(self):
        self._id_counter += 1
        return self._id_counter

    def start(self) -> None:
        self.state = State.PLAYING

    def game_loop(self, dt: float) -> None:
        if self.state != State.PLAYING:
            return
        self.update_units()
        self.update_towers()
        self.update_projectiles()
        self.check_round_end()
        self.check_game_over()
        self.broadcast_state()

    def update_units(self, dt: float) -> None:
        for unit in self.units[:]:  # copie pour suppression safe
            unit.move((unit.x, unit.y), dt, self.map)
            if unit.hp <= 0:
                self.units.remove(unit)

    def update_towers(self, dt: float) -> None:
        for tower in self.towers:
            tower.cooldown_remaining -= dt

            if tower.cooldown_remaining <= 0:
                target = self.find_target_for_tower(tower)

                if target:
                    target.get_attacked(tower.damage)
                    tower.cooldown_remaining = tower.attack_speed

    def update_projectiles(self, dt) -> None:
        return

    def find_target_for_tower(self, tower: DefenseObject):
        in_range = []

        for unit in self.units:
            dist = abs(unit.x - tower.x) + abs(unit.y - tower.y)
            if dist <= tower.attack_range:
                in_range.append(unit)
        if not in_range:
            return None
        return in_range[0]

    def check_round_end(self) -> None:
        if len(self.units) == 0:
            self.next_round()

    def check_game_over(self) -> None:
        if self.base.hp <= 0:
            self.end_game(Team.ATTACKER)

        elif self.round > self.max_round:
            self.end_game(Team.DEFENDER)

    def next_round(self) -> None:
        self.round += 1

        defender = self.players[Team.DEFENDER]
        defender.earn(50)  # bonus vague

    def end_game(self, winner: Team) -> None:
        self.state = State.GAME_OVER

        # à envoyer via websocket
        print(f"Winner: {winner}")

    def broadcast_state(self) -> None:
        state = self.to_dict()
        # branché plus tard avec socketio
        # socketio.emit("game_state", state)

    def to_dict(self) -> dict:
        return {
            "state": self.state.value,
            "round": self.round,
            "units": [u.to_dict() for u in self.units],
            "towers": [t.to_dict() for t in self.towers],
            "players": {
                team.value: player.to_dict()
                for team, player in self.players.items()
            },
            "base_hp": self.base.hp
        }

"""
start() — initialise la partie, passe state à "playing" , démarre la boucle
game_loop(dt) — appelée à chaque tick :
1. update_units(dt) — déplace les unités, gère les attaques
2. update_towers() — chaque tour cherche une cible et attaque
3. update_projectiles(dt) — déplace les projectiles
4. check_round_end() — vérifie si la vague est terminée
5. check_game_over() — vérifie les conditions de victoire/défaite
6. broadcast_state() — envoie l'état via WebSocket à tous les joueurs
Idées 4
next_round() — incrémente round , accorde le bonus d'or entre vagues
end_game(winner) — passe state à "game_over" , émet l'événement final
"""