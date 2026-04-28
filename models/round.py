from __future__ import annotations
from typing import TYPE_CHECKING,List

if TYPE_CHECKING:
    from game import GameObject

from .entities import UnitObject
from enums import UnitType


class RoundObject:
    def __init__(self, _round_number: int, _spawn_queue: List[dict], _spawn_timer: float):
        """
        Args:
            _round_number: numéro de la vague
            _spawn_queue: liste ordonnée d'unités à spawn [{"type": UnitType.SOLDAT, "delay": 1.5}, ...]
            _spawn_timer: temps initial avant le premier spawn
        """
        self.round_number = _round_number
        self.spawn_queue = _spawn_queue
        self.spawn_timer = _spawn_timer
        self.is_finished = False

    def update(self, dt: float, game: GameObject) -> None:
        """Appelée à chaque tick. Décrémente le timer et spawn quand il atteint 0."""
        if self.is_finished:
            return

        self.spawn_timer -= dt

        if self.spawn_timer <= 0 and self.spawn_queue:
            next_unit_data = self.spawn_queue.pop(0)
            self.spawn_next(game, next_unit_data)

            # Reset le timer avec le délai de la prochaine unité
            if self.spawn_queue:
                self.spawn_timer = self.spawn_queue[0].get("delay", 1.0)

        # La vague est "finie côté spawn" quand la queue est vide
        if not self.spawn_queue:
            self.is_finished = True

    def spawn_next(self, game: GameObject, unit_data: dict) -> None:
        """Crée l'unité et l'ajoute sur la carte via l'attaquant."""
        unit_type = unit_data["type"]
        game.attacker.send_unit(unit_type)