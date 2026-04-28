from enum import Enum
from dataclasses import dataclass


class Team(Enum):
    ATTACKER = "attacker"
    DEFENDER = "defender"


class Placement(Enum):
    EDGE = "edge"
    PATH = "path"


@dataclass(frozen=True)
class TowerData:
    """Données de base pour un type de tour."""
    price: int
    hp: int
    damage: int
    attack_speed: float   # secondes entre chaque attaque
    range: int            # portée en cases
    reward: int           # or donné à l'attaquant si détruite
    duration: float | None  # durée de vie (None = permanente)
    size: int             # taille en cases (1 = 1x1)
    placement: "Placement"
    cooldown_remaining: float  # cooldown initial


class TowerType(Enum):
    #                     price  hp  dmg  atk_spd  range  reward  duration  size  placement       cooldown
    ARCHER = TowerData(    10,   50,  8,   1.0,     3,     5,     None,      1,   Placement.EDGE,  0.0)
    CANNON = TowerData(    20,   80,  25,  2.5,     2,     10,    None,      1,   Placement.EDGE,  0.0)
    FREEZE = TowerData(    25,   40,  0,   2.0,     3,     12,    None,      1,   Placement.EDGE,  0.0)


@dataclass(frozen=True)
class UnitData:
    """Données de base pour un type d'unité."""
    price: int
    hp: int
    damage: int
    attack_speed: float   # secondes entre chaque attaque
    range: int            # portée en cases
    reward: int           # or donné au défenseur si tuée
    speed: int            # vitesse de déplacement (cases/seconde)
    is_melee: bool


class UnitType(Enum):
    #                    price  hp   dmg  atk_spd  range  reward  speed  is_melee
    MAGE   = UnitData(   10,    60,   12,  1.5,     3,     8,      2,    False)
    SOLDAT = UnitData(   30,    150,  20,  1.0,     1,     15,     1,    True)


class State(Enum):
    WAITING = "waiting"
    PLAYING = "playing"
    GAME_OVER = "game_over"
