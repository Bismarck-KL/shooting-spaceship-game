# This file makes the enemies directory a Python package
from .enemy_base import Enemy
from .fast_enemy import FastEnemy
from .tank_enemy import TankEnemy
from .normal_enemy import NormalEnemy

__all__ = ['Enemy', 'FastEnemy', 'TankEnemy', 'NormalEnemy']

