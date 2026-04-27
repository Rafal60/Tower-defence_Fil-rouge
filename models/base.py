from enums import State
from game import GameObject


def destroy(game : GameObject = game) -> None:
    game.end_game("Attacker")


class BaseObject:
    def __init__(self,
                 _id : int,
                 _hp : int,
                 _max_hp : int,
                 _x : int,
                 _y : int,
                 ):
        self.id = _id
        self.hp = _hp
        self.max_hp = _max_hp
        self.x = _x
        self.y = _y

    def get_attacked(self, damage) -> None:
        self.hp -= damage
        if self.hp <= 0:
            destroy()



