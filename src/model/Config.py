from src.model.Screen import Screen
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
                 probability: int = 30):  # La probabilidad comprende un porcentaje de 0 a 100% de que un health aparezca
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
                 size: int = 200):
        self.posx = posx
        self.posy = posy
        self.delta_x = delta_x
        self.delta_y = delta_y
        self.degree = degree
        self.size = size

    @classmethod
    def getRandomConfig(ctx, screen: Screen):
        max_x = screen.surface.get_width()
        max_y = screen.surface.get_height()

        coox = max_x if randint(0, 1) else 0
        cooy = max_y if randint(0, 1) else 0

        dx = -4 if coox == max_x else 4
        dy = -4 if cooy == max_y else 4

        size = randint(100, 300)
        print("Generated random MeteorConfig", coox, cooy, dx, dy)

        return MeteorConfig(posx=coox, posy=cooy, delta_x=dx, delta_y=dy, size=size)




class PowerUpConfig:
    def __init__(self, rangex: list[int, int] | int = 100,
                 rangey: list[int, int] | int = 0,
                 fall_speed: int = 1.5,
                 duration: int = 20,
                 damage: int = 5,
                 probability: int = 80):  # La probabilidad comprende un porcentaje de 0 a 100% de que un power up aparezca
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
                 probability: int = 80):  # La probabilidad comprende un porcentaje de 0 a 100% de que un power up aparezca
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
