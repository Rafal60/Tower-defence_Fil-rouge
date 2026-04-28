from typing import List, Dict
from game import GameObject
from enums import UnitType
from models import AttackObject


class RoundObject:
    def __init__(
        self,
        _round_number: int,
        _spawn_queue: List[Dict],
    ):
        self.round_number = _round_number
        self.spawn_queue = _spawn_queue  # [{ "type": UnitType, "delay": float }]
        self.spawn_timer = 0.0
        self.is_finished = False

    def update(self, dt: float, game: GameObject) -> None:
        if self.is_finished:
            return
        self.spawn_timer -= dt

        if self.spawn_timer <= 0 and len(self.spawn_queue) > 0:
            next_spawn = self.spawn_queue.pop(0)
            unit_type: UnitType = next_spawn["type"]
            delay: float = next_spawn["delay"]
            self.spawn_next(game, unit_type)
            self.spawn_timer = delay

        if len(self.spawn_queue) == 0 and len(game.units) == 0:
            self.is_finished = True

    def spawn_next(self, game: GameObject, unit_type: UnitType) -> None:
        data = unit_type.value

        spawn_x, spawn_y = game.map.spawn_point

        unit = AttackObject(
            game.get_next_id(),
            unit_type,
            data.price,
            data.hp,
            data.hp,
            data.damage,
            data.attack_speed,
            data.attack_range,
            data.reward,
            spawn_x,
            spawn_y,
            data.speed,
            data.is_melee,
            (0, 0)
        )

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