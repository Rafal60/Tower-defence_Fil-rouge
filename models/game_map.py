
from __future__ import annotations
from typing import TYPE_CHECKING, List
if TYPE_CHECKING:
    from models import TowerObject, UnitObject, BaseObject

from typing import List, Tuple
from .map_def import DEFAULT_GRID_DEF, DEFAULT_WAYPOINTS, SPAWN_POS
 

class SpawnPoint:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
 
class MapObject:
    def __init__(
        self,
        _base: BaseObject,
        _units: List[UnitObject],
        _towers: List[TowerObject],
        _grid_def: List[List[str]] = None,
        _waypoints: List[Tuple[int, int]] = None,
        _spawn: SpawnPoint = None,
    ) -> None:
        self.base = _base
        self.units = _units
        self.towers = _towers
        self.grid_def = _grid_def or DEFAULT_GRID_DEF
        self.waypoints = _waypoints or DEFAULT_WAYPOINTS
        spawn_pos = SPAWN_POS if _spawn is None else (_spawn.x, _spawn.y)
        self.spawn = SpawnPoint(*spawn_pos)
 
    def add_tower(self, _tower: TowerObject) -> None:
        self.towers.append(_tower)
 
    def remove_tower(self, _tower: TowerObject) -> None:
        if _tower in self.towers:
            self.towers.remove(_tower)
 
    def spawn_unit(self, _unit: UnitObject) -> None:
        self.units.append(_unit)
 
    def remove_unit(self, _unit: UnitObject) -> None:
        if _unit in self.units:
            self.units.remove(_unit)
 
    def to_grid(self) -> List[List[dict]]:
        """
        Retourne un tableau 2D de cellules pour le frontend :
        [row][col] = { "type": "grass|path|spawn|base" }
        Les tours sont fusionnées dans la grille.
        """
        rows = len(self.grid_def)
        cols = len(self.grid_def[0])
 
        grid = [
            [{"type": self.grid_def[y][x]} for x in range(cols)]
            for y in range(rows)
        ]
 
        # Surcharger les cases avec les tours (elles ont déjà leur dict séparé,
        # mais on marque la case pour le CSS)
        for tower in self.towers:
            x, y = int(tower.x), int(tower.y)
            if 0 <= y < rows and 0 <= x < cols:
                grid[y][x]["type"] = "tower"
 
        return grid















