from typing import List
from models import TowerObject, UnitObject, BaseObject


class MapObject:
    def __init__(self, _base : BaseObject, _units : List[UnitObject], _towers : List[TowerObject]) -> None:
        self.base = _base
        self.units = _units
        self.towers = _towers

    def add_tower(self, _tower : TowerObject) -> None:
        self.towers.append(_tower)

    def remove_tower(self, _tower : TowerObject) -> None:
        self.towers.remove(_tower)

    def spawn_unit(self, _unit : UnitObject) -> None:
        self.units.append(_unit)

    def remove_unit(self, _unit : UnitObject) -> None:
        self.units.remove(_unit)
















