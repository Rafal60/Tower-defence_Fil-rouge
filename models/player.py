from typing import List
from exceptions import InsufficientFundsError
from enums import Team, UnitType, TowerType, Placement
from game_map import MapObject
from entities import UnitObject, TowerObject
from base import BaseObject


class PlayerObject:
    def __init__(self, _id: int, _username : str, _gold : int, _team : Team, _map : MapObject ) -> None:
        self.id = _id
        self.username = _username
        self.gold = _gold
        self.team = _team
        self.map = _map

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
    def __init__(self, _id, _username, _gold, _team, _map,  _units_sent : List[UnitObject], _income_rate : int):
        super().__init__(_id, _username, _gold, _team, _map)
        self.units_sent = _units_sent
        self.income_rate = _income_rate

    def send_unit(self, unit_type : UnitType) -> None:
        if not self.can_afford(unit_type.value) :
            return

        new_attack_obj = UnitObject(1, unit_type, 1, 1, 1, 1, 1.0, 1, 1, 1, 1,self.map, 1, True, (1,1))
        self.map.spawn_unit(new_attack_obj)

        self.spend(unit_type.value)

    def collect_income(self, dt : float) -> None:
        self.earn(round(self.income_rate * dt))


class DefenderPlayer(PlayerObject):
    def __init__(self, _id, _username, _gold, _team,  _towers : List[TowerObject], _base : BaseObject):
        super().__init__(_id, _username, _gold, _team)
        self.towers = _towers
        self.base = _base

    def place_tower(self, tower : TowerObject, x : int, y : int, _map : MapObject) -> None:
        if not self.can_afford(tower.price) :
            return


        # Valeur de l'objet à changer
        new_def_obj = TowerObject(1, TowerType.ARCHER, 1, 1, 1, 1, 1.0, 1, 1, x, y, None, 1, Placement.EDGE, 1.0)


        new_def_obj.deploy(_map)
        self.spend(tower.price)

    def sell_tower(self, tower : TowerObject,) -> None:
        self.earn(round(tower.price * 0.7))
        self.map.remove_tower(tower)

    def upgrade_tower(self, tower : TowerObject) -> None:
        if not self.can_afford(tower.price):
            return
        self.spend(tower.price)
        tower.upgrade()