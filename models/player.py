from typing import List
from exceptions import InsufficientFundsError
from enums import UnitType, Team, TowerType, Placement
from game_map import MapObject
from entities import BaseObject, AttackObject, DefenseObject


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

class AttackerPlayer(PlayerObject):
    def __init__(self, _id, _username, _gold, _team,  _units_sent : List[AttackObject], _income_rate : int):
        super().__init__(_id, _username, _gold, _team)
        self.units_sent = _units_sent
        self.income_rate = _income_rate

    def send_unit(self, unit_type : UnitType, _map : MapObject ) -> None:
        return

    def collect_income(self, dt : float) -> None:
        self.earn(round(self.income_rate * dt))


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