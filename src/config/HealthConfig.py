class HealthConfig:
    def __init__(self, rangex: list[int, int] | int = 100,
                 rangey: list[int, int] | int = 100,
                 fall_speed: int = 2,
                 heal_amount: int = 20,
                 probability: int = 30):# La probabilidad comprende un porcentaje de 0 a 100% de que un health aparezca
        self.fall_speed = fall_speed
        self.heal_amount = heal_amount
        self.x = rangex
        self.y = rangey
        self.probability = probability
