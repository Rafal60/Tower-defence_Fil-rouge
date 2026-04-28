from enum import Enum

class Team(Enum):
    ATTACKER = "attacker"
    DEFENDER = "defender"


class Placement(Enum):
    EDGE = "edge"
    PATH = "path"


class State(Enum):
    WAITING = "waiting"
    PLAYING = "playing"
    GAME_OVER = "game_over"


class UnitData:
    def __init__(self, price, hp, damage, attack_speed, range, reward, speed, is_melee):
        self.price = price
        self.hp = hp
        self.damage = damage
        self.attack_speed = attack_speed
        self.range = range
        self.reward = reward
        self.speed = speed
        self.is_melee = is_melee


class TowerData:
    def __init__(self, price, hp, damage, attack_speed, range, reward, duration, size, placement, cooldown):
        self.price = price
        self.hp = hp
        self.damage = damage
        self.attack_speed = attack_speed
        self.range = range
        self.reward = reward
        self.duration = duration
        self.size = size
        self.placement = placement
        self.cooldown = cooldown

class UnitType(Enum):
    MAGE = UnitData(
        price=10,
        hp=40,
        damage=8,
        attack_speed=1.5,
        attack_range=3,
        reward=5,
        speed=2,
        is_melee=False
    )

    SOLDAT = UnitData(
        price=30,
        hp=100,
        damage=12,
        attack_speed=1.0,
        attack_range=1,
        reward=10,
        speed=1,
        is_melee=True
    )

class TowerType(Enum):
    ARCHER = TowerData(
        price=10,
        hp=100,
        damage=10,
        attack_speed=1.0,
        attack_range=4,
        reward=5,
        duration=None,
        size=1,
        placement=Placement.EDGE,
        cooldown=0.0
    )

    CANNON = TowerData(
        price=20,
        hp=150,
        damage=25,
        attack_speed=2.0,
        attack_range=3,
        reward=10,
        duration=None,
        size=2,
        placement=Placement.EDGE,
        cooldown=0.0
    )

    FREEZE = TowerData(
        price=25,
        hp=80,
        damage=5,
        attack_speed=1.5,
        attack_range=3,
        reward=12,
        duration=10.0,
        size=1,
        placement=Placement.PATH,
        cooldown=0.0
    )