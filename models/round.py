from typing import List

from game import GameObject
from models import AttackObject


class RoundObject:
    def __init__(self, _round_number : int, _spawn_queue : List[dict], _spawn_timer : float, _is_finished : bool):
        self.round_number = _round_number
        self.spawn_queue = _spawn_queue
        self.spawn_timer = _spawn_timer
        self.is_finished = _is_finished

    def update(self, dt : float) -> None :
        self.spawn_timer -= dt
        if self.spawn_timer <= 0:


            # Gestion du spawn de la prochaine unité à faire
            self.spawn_queue.append(X)

    def spawn_next(self, game : GameObject, unit : AttackObject) -> None:
        game.units.append(unit)





'''
round_number — numéro de la vague
spawn_queue — liste ordonnée d'unités à faire apparaître [{ "type": "archer",
"delay": 1.5 }, ...]
spawn_timer — timer interne pour espacer les spawns
is_finished — True quand toutes les unités ont été envoyées et qu'il ne
reste plus d'unités vivantes
Méthodes :
update(dt) — décrémente spawn_timer , spawn la prochaine unité si le timer
atteint 0
spawn_next(game: GameObject) — crée l' AttackObject suivant et l'ajoute à
game.units
'''