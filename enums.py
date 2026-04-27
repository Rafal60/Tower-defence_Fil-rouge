from enum import Enum

class Team(Enum):
    ATTACKER = "attacker"
    DEFENDER = "defender"


class Placement(Enum):
    EDGE = "edge"
    PATH = "path"


'''
On doit avoir tout ce qui à base data ( voir Notion et class)
TowerObject(1, tower_type, data.price, data.hp, data.damage, data.attack_speed, data.range, data.reward, x, y ,self.map, data.duration, data.size, data.placement, data.cooldown_remaining)
'''
class TowerType(Enum):
    ARCHER = 10
    CANNON = 20
    FREEZE = 25


'''
On doit avoir tout ce qui à base data ( voir Notion et class)
UnitObject(1, unit_type, data.price, data.hp, data.damage, data.attack_speed, data.range, data.reward, self.map.spawn.x,  self.map.spawn.y ,self.map, data.speed, data.is_melee, (1, 1))
'''
class UnitType(Enum):
    MAGE = 10
    SOLDAT = 30


class State(Enum):
    WAITING = "waiting"
    PLAYING = "playing"
    GAME_OVER = "game_over"
