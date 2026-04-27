from __future__ import annotations
from typing import Tuple, List
from enums import UnitType, TowerType, Placement
from game_map import MapObject
from game import GameObject
import math


class EntitiesObject:
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

class AttackObject(EntitiesObject):
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

    def move(self, path : Tuple[int, int], dt : float, _map : MapObject) -> None:
        self.x, self.y = path

        # Logique du mouvement selon speed et dt à ajouter

        if (self.x, self.y) == (_map.base.x, _map.base.y):
            _map.base.get_attacked(self.damage)


    def attack(self, target : List[DefenseObject], _map : MapObject) -> None:
        arr_coordinates = []
        for towers in target :
            arr_coordinates.append([towers.x, towers.y])
        nearest_coordinate = min(arr_coordinates, key=lambda c: math.sqrt((c[0] - self.x)**2 + (c[1] - self.y)**2))

        # dt et map à incorporer
        self.move(nearest_coordinate, dt=1.0, _map)


    def get_attacked(self, damage : int, game : GameObject, defender : DefenseObject) -> None:
        self.hp -= damage
        if self.hp <= 0:
            self.die(game, defender)


    # Méthode die à faire
    def die(self, game : GameObject, defender : DefenseObject ) -> None:
        game.destroy(self)
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

class DefenseObject(EntitiesObject):
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

    def upgrade(self) -> None:
        return

    def sell(self, _map : MapObject) -> None:
        return

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


