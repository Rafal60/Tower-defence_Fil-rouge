from enums import State
from typing import List
from models import MapObject, AttackObject, DefenseObject, player
from models import BaseObject


class GameObject:
    def __init__(self,
                 _round : int,
                 _max_round : int,
                 _player : dict,
                 _map : MapObject,
                 _base : BaseObject,
                 _units : List[AttackObject],
                 _towers : List[DefenseObject],
                 _tick_rate : float
                 ):
        self.state = State.WAITING
        self.round = _round
        self.max_round = _max_round
        self.player = player
        self.map = _map
        self.base = _base
        self.units = _units
        self.towers = _towers
        self.tick_rate = _tick_rate

    def start(self) -> None:
        self.state = State.PLAYING

    def game_loop(self, dt: float) -> None:
        self.update_units()
        self.update_towers()
        self.update_projectiles()
        self.check_round_end()
        self.check_game_over()
        self.broadcast_state()

    def update_units(self, dt) -> None:
        return

    def update_towers(self) -> None:
        return

    def update_projectiles(self, dt) -> None:
        return

    def check_round_end(self) -> None:
        return

    def check_game_over(self) -> None:
        return

    def broadcast_state(self) -> None:
        return

    def next_round(self) -> None:
        return

    def end_game(self, winner : str) -> None:
        return

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