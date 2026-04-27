from __future__ import annotations
from typing import Tuple, List
from enums import UnitType, TowerType, Placement
from game_map import MapObject
import math

from models import AttackerPlayer, DefenderPlayer


class EntitiesObject:
    def __init__(self,
                 _id : int,
                 _type : UnitType | TowerType,
                 _price : int,
                 _hp : int,
                 _damage : int,
                 _attack_speed : float,
                 _attack_range : int,
                 _reward : int,
                 _x : int,
                 _y : int,
                 _map : MapObject
                 ) -> None:
        self.id = _id
        self.type = _type
        self.price = _price
        self.hp = _hp
        self.max_hp = _hp
        self.damage = _damage
        self.attack_speed = _attack_speed
        self.attack_range = _attack_range
        self.reward = _reward
        self.x = _x
        self.y = _y
        self.map = _map

class UnitObject(EntitiesObject):
    def __init__(self,
                 _id,
                 _type : UnitType,
                 _price,
                 _hp,
                 _damage,
                 _attack_speed,
                 _attack_range,
                 _reward,
                 _x,
                 _y,
                 _map,
                 _speed : int,
                 _is_melee : bool,
                 _waypoint_index : Tuple[int, int]
                 ) -> None:
        super().__init__(_id, _type, _price, _hp, _damage, _attack_speed, _attack_range, _reward, _x, _y, _map)
        self.speed = _speed
        self.is_melee = _is_melee
        self.waypoint_index = _waypoint_index

    def move(self, path : Tuple[int, int]) -> None:
        self.x, self.y = path
        if (self.x, self.y) == (self.map.base.x, self.map.base.y):
            self.map.base.get_attacked(self.damage)


    def attack(self) -> None:
        if [self.x, self.y] == self.map.base:
            self.map.base.get_attacked(self.damage)


    def get_attacked(self, damage : int, defender : DefenderPlayer = X) -> None:
        self.hp -= damage
        if self.hp <= 0:
            self.die(defender)


    def die(self, defender : DefenderPlayer) -> None:
        self.map.remove_unit(self)
        defender.earn(self.reward)

    def to_dict(self) -> dict:
        return {
            "id" : self.id,
            "type" : self.type,
            "price" : self.price,
            "hp" : self.hp,
            "max_hp" : self.max_hp,
            "damage" : self.damage,
            "attack_speed" : self.attack_speed,
            "attack_range" : self.attack_range,
            "reward" : self.reward,
            "x" : self.x,
            "y" : self.y,
            "speed" : self.speed,
            "is_melee" : self.is_melee,
            "waypoint_index" : self.waypoint_index
        }

class TowerObject(EntitiesObject):
    def __init__(self,
                 _id,
                 _type : TowerType,
                 _price,
                 _hp,
                 _damage,
                 _attack_speed,
                 _attack_range,
                 _reward,
                 _x,
                 _y,
                 _map,
                 _duration: float | None,
                 _size: int,
                 _placement: Placement,
                 _cooldown_remaining: float,
                 ) -> None:
        super().__init__(_id, _type, _price, _hp, _damage, _attack_speed, _attack_range, _reward, _x, _y, _map)
        self.duration = _duration
        self.size = _size
        self.placement = _placement
        self.cooldown_remaining = _cooldown_remaining

    def deploy(self, _map : MapObject) -> None:
        _map.add_tower(self)

    def attack(self, target : List[UnitObject]) -> None:
        arr_coordinates = []
        for unit in target:
            arr_coordinates.append([unit.x, unit.y])
        nearest_coordinate = min(arr_coordinates, key=lambda c: math.sqrt((c[0] - self.x) ** 2 + (c[1] - self.y) ** 2))
        for unit in target:
            if [unit.x, unit.y] == nearest_coordinate :
                unit.get_attacked(self.damage)

    def destroy(self) -> None:
        self.map.remove_tower(self)

    def upgrade(self) -> None:
        return

    def sell(self, defender : DefenderPlayer) -> None:
        defender.earn(round(self.price * 0.75))
        self.map.remove_tower(self)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "type": self.type,
            "price": self.price,
            "hp": self.hp,
            "max_hp": self.max_hp,
            "damage": self.damage,
            "attack_speed": self.attack_speed,
            "attack_range": self.attack_range,
            "reward": self.reward,
            "x": self.x,
            "y": self.y,
            "duration" : self.duration,
            "size" : self.size,
            "placement" : self.placement,
            "cooldown_remaining" : self.cooldown_remaining
        }

