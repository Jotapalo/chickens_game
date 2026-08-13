from src.model.Enum import Enum
import pygame as py

class ResourceService:

    @classmethod
    def load(cls):
        bull1_rect = py.Rect(400, 254, 12, 18)
        bull2_rect = py.Rect(421, 254, 12, 18)

        bullet_spritesheet = py.image.load(Enum.resourcePath.BULLET_SPRITESHEET).convert_alpha()

        Bullet_1 = bullet_spritesheet.subsurface(bull1_rect)
        Bullet_2 = bullet_spritesheet.subsurface(bull2_rect)

        cls.Bullet_1 = py.transform.scale(Bullet_1, (12, 18)).convert_alpha()
        cls.Bullet_1.set_colorkey((0,0,0))

        cls.Bullet_2 = py.transform.scale(Bullet_2, (12, 18)).convert_alpha()
        cls.Bullet_2.set_colorkey((0,0,0))
    
        Player = py.image.load(Enum.resourcePath.SHIP)
        cls.Player = py.transform.scale(Player, (70, 70))
    
        Player_icon = py.image.load(Enum.resourcePath.SHIP)
        cls.Player_icon = py.transform.scale(Player_icon, (40, 40))
    
        cls.Enemy = py.image.load(Enum.resourcePath.ENEMY)
    
        PowerUpDamage_1 = py.image.load(Enum.resourcePath.POWER_UP)
        cls.PowerUpDamage_1 = py.transform.scale(PowerUpDamage_1, (40, 40))
    
        PowerUp_minigun = py.image.load(Enum.resourcePath.POWER_UP_MINIGUN)
        cls.PowerUp_minigun = py.transform.scale(PowerUp_minigun, (40, 40))
    
        RoastedChicken = py.image.load(Enum.resourcePath.ROASTED_CHICKEN)
        cls.RoastedChicken = py.transform.scale(RoastedChicken, (70,70))
    
        Saturn = py.image.load(Enum.resourcePath.SATURN)
        cls.Saturn = py.transform.scale(Saturn, (300, 300))
    
        Planet_1 = py.image.load(Enum.resourcePath.PLANET_1)
        cls.Planet_1 = py.transform.scale(Planet_1, (300, 300))
    
        Planet_2 = py.image.load(Enum.resourcePath.PLANET_2)
        cls.Planet_2 = py.transform.scale(Planet_2, (300, 300))
    
        cls.Asteroid_collection = []
        for i in range(11):
            cls.Asteroid_collection.append(
                py.image.load(Enum.resourcePath.ASTEROID_PATH+f"spin-{i:02d}.png")
            )
    
        cls.BattheShip_collection = []
        for i in range(1,10):
            cls.BattheShip_collection.append(
                py.transform.scale(py.image.load(Enum.resourcePath.BATTLE_SHIP_PATH+f"redfighter000{i}.png"), (80,80))  
                )

        cls.LifeBar_empty = {
            "empty_l" : py.image.load(Enum.resourcePath.EMPTY_LIFEBAR + "\\empty_l.png"),
            "empty_m" : py.image.load(Enum.resourcePath.EMPTY_LIFEBAR + "\\empty_m.png"),
            "empty_r" : py.image.load(Enum.resourcePath.EMPTY_LIFEBAR + "\\empty_r.png")
        }

        cls.LifeBar_player = {
            "player_l" : py.image.load(Enum.resourcePath.PLAYER_LIFEBAR + "\\player_l.png"),
            "player_m" : py.image.load(Enum.resourcePath.PLAYER_LIFEBAR + "\\player_m.png"),
            "player_r" : py.image.load(Enum.resourcePath.PLAYER_LIFEBAR + "\\player_r.png")
        }

        cls.LifeBar_enemy = {
            "enemy_l" : py.image.load(Enum.resourcePath.ENEMY_LIFEBAR + "\\enemy_l.png"),
            "enemy_m" : py.image.load(Enum.resourcePath.ENEMY_LIFEBAR + "\\enemy_m.png"),
            "enemy_r" : py.image.load(Enum.resourcePath.ENEMY_LIFEBAR + "\\enemy_r.png")
        }