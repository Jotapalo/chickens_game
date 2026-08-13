import math

from src.model.Screen import Screen
from src.model.Game import Game
from random import randint

class EnemyConfig:
    def __init__(self, speed=1, life=100, size=(70, 70), damage=20, xp=10):
        self.speed = speed
        self.life = life
        self.size = size
        self.damage = damage
        self.xp = xp


class HealthConfig:
    def __init__(self, rangex: list[int, int] | int = 100,
                 rangey: list[int, int] | int = 0,
                 fall_speed: int = 1.5,
                 heal_amount: int = 20,
                 probability: int = 30):
        self.fall_speed = fall_speed
        self.heal_amount = heal_amount
        self.x = rangex
        self.y = rangey
        self.probability = probability

class MeteorConfig:
    def __init__(self, posx: int = 10,
                 posy: int = 10,
                 delta_x: int | float = 4,
                 delta_y: int | float = 4,
                 degree: int = 0,
                 size: int = 200,
                 damage: int = 20):
        self.posx = posx
        self.posy = posy
        self.delta_x = delta_x
        self.delta_y = delta_y
        self.degree = degree
        self.size = size
        self.damage = damage

    @classmethod
    def getRandomConfig(ctx, screen: Screen):
        max_x = screen.surface.get_width()
        duration = 2
        size_collection = [50, 75, 100, 115]

        init_x = -5 if randint(0,1) else max_x+5
        init_y = randint(0, 600)

        last_x = max_x+5 if init_x == -5 else -5
        last_y = randint(0, 600)

        dx = last_x - init_x
        dy = last_y - init_y

        degree = math.degrees(math.atan2(dy, dx))

        delta_time_x = dx / (Game.FPS * duration)
        delta_time_y = dy / (Game.FPS * duration)

        return MeteorConfig(posx=init_x, posy=init_y, delta_x=delta_time_x,
                            delta_y=delta_time_y, degree=degree, 
                            size=size_collection[randint(0, len(size_collection)-1)], 
                            damage=20)




class PowerUpConfig:
    def __init__(self, rangex: list[int, int] | int = 100,
                 rangey: list[int, int] | int = 0,
                 fall_speed: int = 1.5,
                 duration: int = 20,
                 damage: int = 5,
                 probability: int = 80):
        self.fall_speed = fall_speed
        self.duration = duration
        self.damage = damage
        self.x = rangex
        self.y = rangey
        self.probability = probability

class PowerUpMinigunConfig:
    def __init__(self, rangex: list[int, int] | int = 100,
                 rangey: list[int, int] | int = 0,
                 fall_speed: int = 1.5,
                 duration: int = 20,
                 fire_speed: int = 20,
                 probability: int = 80):
        self.fall_speed = fall_speed
        self.duration = duration
        self.fire_speed = fire_speed
        self.x = rangex
        self.y = rangey
        self.probability = probability

class Config:
    def __init__(self):
        pass
    enemy_CFG = EnemyConfig()
    health_CFG = HealthConfig()
    powerUp_CFG = PowerUpConfig()
