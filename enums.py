from enum import Enum

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