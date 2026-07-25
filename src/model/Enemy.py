import pygame as py
from src.config import EnemyConfig
import src.enum.resEnum as resEnum

class Enemy(py.Vector2):
    def __init__(self, screen, posx, posy, enemy_config: EnemyConfig) -> None:
        super().__init__(posx, posy)
        self.screen = screen
        self.speed = enemy_config.speed
        self.life = enemy_config.life
        self.size = enemy_config.size

        self.image_enemy = py.image.load(resEnum.ENEMY)
        self.image_enemy = py.transform.scale(self.image_enemy, (self.size[0], self.size[1]))
        self.enemy_react = self.image_enemy.get_rect(center=self)

    def draw_enemy(self) -> None: 
        # Actualizar y dibujar enemigos
        self.enemy_react.center = (self.x, self.y)
        self.screen.blit(self.image_enemy, self.enemy_react)