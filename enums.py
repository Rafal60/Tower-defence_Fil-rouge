from enum import Enum

class Team(Enum):
    ATTACKER = "attacker"
    DEFENDER = "defender"

class Placement(Enum):
    EDGE = "edge"
    PATH = "path"

class TowerType(Enum):
    ARCHER = 10
    CANNON = 20
    FREEZE = 25

class UnitType(Enum):
    MAGE = 10
    SOLDAT = 30
