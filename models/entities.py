from typing import Tuple
from enums import UnitType, TowerType, Placement
from game_map import MapObject
from game import GameObject

class BaseObject:
    def __init__(self,
                 _id : int,
                 _type : UnitType | TowerType,
                 _price : int,
                 _hp : int,
                 _max_hp : int,
                 _damage : int,
                 _attack_speed : float,
                 _attack_range : int,
                 _reward : int,
                 _x : int,
                 _y : int
                 ) -> None:
        self.id = _id
        self.type = _type
        self.price = _price
        self.hp = _hp
        self.max_hp = _max_hp
        self.damage = _damage
        self.attack_speed = _attack_speed
        self.attack_range = _attack_range
        self.reward = _reward
        self.x = _x
        self.y = _y

class AttackObject:
    def __init__(self,
                 _id,
                 _type : UnitType,
                 _price,
                 _hp,
                 _max_hp,
                 _damage,
                 _attack_speed,
                 _attack_range,
                 _reward,
                 _x,
                 _y,
                 _speed : int,
                 _is_melee : bool,
                 _waypoint_index : Tuple[int, int]
                 ) -> None:
        super().__init__(_id, _type, _price, _hp, _max_hp, _damage, _attack_speed, _attack_range, _reward, _x, _y)
        self.speed = _speed
        self.is_melee = _is_melee
        self.waypoint_index = _waypoint_index

    # Type de path à mettre
    def move(self, path, dt : float) -> None:
        return

    # Type de target à mettre
    def attack(self, target) -> None:
        return

    def get_attacked(self, damage : int) -> None:
        return

    def die(self, game : GameObject):
        return

    def to_dict(self) -> dict:
        return {}

class DefenseObject:
    def __init__(self,
                 _id,
                 _type : TowerType,
                 _price,
                 _hp,
                 _max_hp,
                 _damage,
                 _attack_speed,
                 _attack_range,
                 _reward,
                 _x,
                 _y,
                 _duration: float | None,
                 _size: int,
                 _placement: Placement,
                 _cooldown_remaining: float,
                 ) -> None:
        super().__init__(_id, _type, _price, _hp, _max_hp, _damage, _attack_speed, _attack_range, _reward, _x, _y)
        self.duration = _duration
        self.size = _size
        self.placement = _placement
        self.cooldown_remaining = _cooldown_remaining

    def deploy(self, _map : MapObject) -> None:
        return

    def attack(self, target : AttackObject) -> None:
        return

    def get_attacked(self, damage: int) -> None:
        return

    def destroy(self, _map : MapObject, game : GameObject) -> None:
        return

    # Type de path à mettre
    def upgrade(self) -> None:
        return

    def sell(self, _map : MapObject) -> None:
        return

    def to_dict(self) -> dict:
        return {}


