from typing import List, Tuple
from enum import Enum
import json

class InsufficientFundsError(Exception):
    """Erreur levée quand le joueur n'a pas les fons pour payer quelque chose"""
    pass


class Team(Enum):
    ATTACKER = "attacker"
    DEFENDER = "defender"

class TowerType(Enum):
    ARCHER = "archer"
    CANNON = "cannon"
    FREEZE = "freeze"

class UnitType(Enum):
    MAGE = "mage"
    SOLDAT = "soldat"

class Placement(Enum):
    EDGE = "edge"
    PATH = "path"


class PlayerObject:
    def __init__(self, _id: int, _username : str, _gold : int, _team : Team):
        self.id = _id
        self.username = _username
        self.gold = _gold
        self.team = _team

    def can_afford(self, item_amount) -> bool:
        return item_amount <= self.gold

    def spend(self, amount) -> None:
        if not self.can_afford(amount):
            raise InsufficientFundsError("Le prix de l'entité que le joueur essaie de poser est supérieur à son argent possédé")
        self.gold -= amount

    def earn(self, amount) -> None:
        self.gold += amount

    def to_dict(self) -> dict:
        obj = {
            "id": self.id,
            "username": self.username,
            "gold": self.gold,
            "team": self.team
        }
        return obj

class BaseObject:
    def __init__(self, _test):
        test = _test

class DefenseObject:
    def __init__(self,
                 _id : int,
                 _type : TowerType,
                 _price : int,
                 _hp : int,
                 _max_hp : int,
                 _damage : int,
                 _duration : float | None,
                 _size : int,
                 _placement : Placement,
                 _attack_speed : float,
                 _attack_range : int,
                 _cooldown_remaining : float,
                 _reward : int,
                 _x : int,
                 _y : int,):
        self.id = _id
        self.type = _type
        self.price = _price
        self.hp = _hp
        self.max_hp = _max_hp
        self.damage = _damage
        self.duration = _duration
        self.size = _size
        self.placement = _placement
        self.attack_speed = _attack_speed
        self.attack_range = _attack_range
        self.cooldown_remaining = _cooldown_remaining
        self.reward = _reward
        self.x = _x
        self.y = _y

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


class AttackObject:
    def __init__(self,
                 _id : int,
                 _type : UnitType,
                 _price : int,
                 _hp : int,
                 _max_hp : int,
                 _damage : int,
                 _speed : int,
                 _is_melee : bool,
                 _attack_speed : float,
                 _attack_range : int,
                 _reward : int,
                 _waypoint_index : Tuple[int, int],
                 _x : int,
                 _y : int) -> None:
        self.id = _id
        self.type = _type
        self.price = _price
        self.hp = _hp
        self.max_hp = _max_hp
        self.damage = _damage
        self.speed = _speed
        self.is_melee = _is_melee
        self.attack_speed = _attack_speed
        self.attack_range = _attack_range
        self.reward = _reward
        self.waypoint_index = _waypoint_index
        self.x = _x
        self.y = _y

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



class MapObject:
    def __init__(self, _test):
        test = _test


class DefenderPlayer(PlayerObject):
    def __init__(self, _id, _username, _gold, _team,  _towers : List[DefenseObject], _base : BaseObject):
        super().__init__(_id, _username, _gold, _team)
        self.towers = _towers
        self.base = _base

    def place_tower(self, _tower_type : DefenseObject, _x : int, _y : int, _map : MapObject) -> None:
        if not self.can_afford(_tower_type.price) :
            return


        # Valeur de l'objet à changer
        new_def_obj = DefenseObject(1, TowerType.ARCHER, 1, 1, 1, 1, None, 1, Placement.EDGE, 1.0,1,1.0, 1, 1, 1)


        new_def_obj.deploy(_map)
        self.spend(_tower_type.price)

    def sell_tower(self, _tower : DefenseObject,_map : MapObject) -> None:
        self.earn(round(_tower.price * 0.7))
        _map.remove_tower(_tower)

    def upgrade_tower(self, _tower : DefenseObject) -> None:
        if not self.can_afford(_tower.price):
            return
        self.spend(_tower.price)
        _tower.upgrade()


class AttackerPlayer(PlayerObject):
    def __init__(self, _id, _username, _gold, _team,  _units_sent : List[AttackObject], _income_rate : int):
        super().__init__(_id, _username, _gold, _team)
        self.units_sent = _units_sent
        self.income_rate = _income_rate

    def send_unit(self, unit_type : UnitType, _map : MapObject ) -> None:
        return

    def collect_income(self, dt : float) -> None:
        self.earn(round(self.income_rate * dt))









