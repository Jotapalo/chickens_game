class PowerUpConfig:
    def __init__(self, rangex: list[int, int] | int = 100,
                 rangey: list[int, int] | int = 100,
                 fall_speed: int = 2,
                 duration: int = 20,
                 damage: int = 5):
        self.fall_speed = fall_speed
        self.duration = duration
        self.damage = damage
        self.x = rangex
        self.y = rangey
