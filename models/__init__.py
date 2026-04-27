__version__ = "1.0.2"
__author__ = "Kitsu"

from .player import AttackerPlayer, DefenderPlayer
from .game_map import MapObject
from .entities import DefenseObject, AttackObject
from .round import RoundObject
from .base import BaseObject

print("Initialisation du module de logique du jeu...")