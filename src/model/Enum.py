import pygame as py

class ColorsMap:
    RED = (255, 0, 0)
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)

class ResourcePath: 
    BULLET_1 = "src/resources/bullet_1.PNG"
    BULLET_2 = "src/resources/bullet_2.PNG"
    FONT = "src/resources/font.JPG"
    POWER_UP = "src/resources/power_up.PNG"
    POWER_UP_MINIGUN = "src/resources/powerUp_minigun.PNG"
    SHIP = "src/resources/ship.PNG"
    ENEMY = "src/resources/enemy.PNG"
    HEALTH = "src/resources/health.PNG"
    DEFAULT_FONT = "src/fonts/VeniteAdoremus-rgRBA.ttf"
class Img:
    Bullet_1 = py.image.load(ResourcePath.BULLET_1)
    Bullet_1 = py.transform.scale(Bullet_1, (40, 40))

    Bullet_2 = py.image.load(ResourcePath.BULLET_2)
    Bullet_2 = py.transform.scale(Bullet_2, (40, 40))

    Player = py.image.load(ResourcePath.SHIP)
    Player = py.transform.scale(Player, (70, 70))

    Player_icon = py.image.load(ResourcePath.SHIP)
    Player_icon = py.transform.scale(Player_icon, (40, 40))

    Enemy = py.image.load(ResourcePath.ENEMY)

    PowerUpDamage_1 = py.image.load(ResourcePath.POWER_UP)
    PowerUpDamage_1 = py.transform.scale(PowerUpDamage_1, (40, 40))

    PowerUp_minigun = py.image.load(ResourcePath.POWER_UP_MINIGUN)
    PowerUp_minigun = py.transform.scale(PowerUp_minigun, (40, 40))

class Enum:
    def __init__(self):
        pass
    colorsMap = ColorsMap()
    resourcePath = ResourcePath()
    Image = Img()
    