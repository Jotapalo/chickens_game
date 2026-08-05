class EnemyConfig:
    def __init__(self, speed=1, life=100, size=(70, 70), damage=20):
        self.speed = speed
        self.life = life
        self.size = size
        self.damage = damage


class HealthConfig:
    def __init__(self, rangex: list[int, int] | int = 100,
                 rangey: list[int, int] | int = 100,
                 fall_speed: int = 2,
                 heal_amount: int = 20,
                 probability: int = 30):  # La probabilidad comprende un porcentaje de 0 a 100% de que un health aparezca
        self.fall_speed = fall_speed
        self.heal_amount = heal_amount
        self.x = rangex
        self.y = rangey
        self.probability = probability


class PowerUpConfig:
    def __init__(self, rangex: list[int, int] | int = 100,
                 rangey: list[int, int] | int = 100,
                 fall_speed: int = 2,
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
                 rangey: list[int, int] | int = 100,
                 fall_speed: int = 2,
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
