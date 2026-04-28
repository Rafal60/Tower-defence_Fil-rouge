from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game import GameObject


class BaseObject:
    def __init__(self,
                 _id: int,
                 _hp: int,
                 _max_hp: int,
                 _x: int,
                 _y: int,
                 ):
        self.id = _id
        self.hp = _hp
        self.max_hp = _max_hp
        self.x = _x
        self.y = _y

    def get_attacked(self, damage: int) -> None:
        self.hp -= damage
        # La vérification hp <= 0 est gérée par GameObject.check_game_over()
