import pygame as py

class ColorsMap:
    RED = (255, 0, 0)
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)

class ResourcePath:
    BASE_PATH = "src/resources/"

    # Texturas
    BULLET_1 = BASE_PATH + "img/bullet_1.PNG"
    BULLET_2 = BASE_PATH + "img/bullet_2.PNG"
    FONT_1 = BASE_PATH + "img/space_font_1.jpg"
    FONT_2 = BASE_PATH + "img/space_font_2.png"
    FONT_3 = BASE_PATH + "img/space_font_3.jpg"
    POWER_UP = BASE_PATH + "img/power_up.PNG"
    POWER_UP_MINIGUN = BASE_PATH + "img/powerUp_minigun.PNG"
    SHIP = BASE_PATH + "img/ship.PNG"
    ENEMY = BASE_PATH + "img/enemy.PNG"
    HEALTH = BASE_PATH + "img/health.PNG"
    ROASTED_CHICKEN = BASE_PATH + "img/roasted_chicken.PNG"
    METEOR = BASE_PATH + "img/meteor.PNG"
    SATURN = BASE_PATH + "img/saturno.png"
    PLANET_1 = BASE_PATH + "img/planet_1.png"
    PLANET_2 = BASE_PATH + "img/planet_2.png"
    BOOM = BASE_PATH + "img/boom.png"

    # Estilos de palabras
    DEFAULT_FONT = BASE_PATH + "fonts/VeniteAdoremus-rgRBA.ttf"

    # Sonidos
    BUTTON_CLICK_SOUND = BASE_PATH + "sounds/button_sound.mp3"
    LEVEL_BACKGROUND_SOUND = BASE_PATH + "sounds/level_sound.mp3"
    POWER_UP_SOUND = BASE_PATH + "sounds/power_up_sound.mp3"
    SHOOT_SOUND = BASE_PATH + "sounds/shoot_sound.mp3"
    BOOM_SOUND = BASE_PATH + "sounds/boom_sound.mp3"
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

    RoastedChicken = py.image.load(ResourcePath.ROASTED_CHICKEN)
    RoastedChicken = py.transform.scale(RoastedChicken, (70,70))

    Meteor = py.image.load(ResourcePath.METEOR)
    Meteor = py.transform.scale(Meteor, (200, 200))

    Saturn = py.image.load(ResourcePath.SATURN)
    Saturn = py.transform.scale(Saturn, (300, 300))

    Planet_1 = py.image.load(ResourcePath.PLANET_1)
    Planet_1 = py.transform.scale(Planet_1, (300, 300))

    Planet_2 = py.image.load(ResourcePath.PLANET_2)
    Planet_2 = py.transform.scale(Planet_2, (300, 300))



class Enum:
    def __init__(self):
        pass
    colorsMap = ColorsMap()
    resourcePath = ResourcePath()
    Image = Img()
    