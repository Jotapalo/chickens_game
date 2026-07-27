import pygame as py
from src.config import EnemyConfig
from src.model.Enum import Enum
from src.model.LifeBar import LifeBar

class Enemy(py.Vector2):
    def __init__(self, screen, posx, posy, enemy_config: EnemyConfig) -> None:
        super().__init__(posx, posy)
        self.screen = screen
        self.speed = enemy_config.speed
        self.max_life = enemy_config.life
        self.life = enemy_config.life
        self.width, self.height = enemy_config.size
        self.lifeBar = LifeBar(screen, posx, posy, self.width, 10)

        self.image_enemy = py.image.load(Enum.resourcePath.ENEMY)
        self.image_enemy = py.transform.scale(self.image_enemy, (self.width, self.height))
        self.enemy_react = self.image_enemy.get_rect(center=self)

    def draw_enemy(self) -> None: 
        # Actualizar y dibujar enemigos
        self.enemy_react.center = (self.x, self.y)
        self.screen.blit(self.image_enemy, self.enemy_react)
        # Sincronizar la barra de vida con la posición actual del enemigo (justo encima)
        self.lifeBar.set_position(self.x - self.width // 2, self.y - self.height)
        self.lifeBar.draw_life_bar()
        