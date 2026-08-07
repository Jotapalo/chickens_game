import pygame as py
from src.model.Config import EnemyConfig
from src.model.Enum import Enum
from src.model.LifeBar import LifeBar

class Enemy(py.sprite.Sprite):
    def __init__(self, screen, posx, posy, enemy_config: EnemyConfig) -> None:
        super().__init__()
        self.screen = screen
        self.speed = enemy_config.speed
        self.max_life = enemy_config.life
        self.life = enemy_config.life
        self.width, self.height = enemy_config.size
        self.lifeBar = LifeBar(screen, posx, posy, self.width, 10)
        self.enable_lifebar = True
        self.damage = enemy_config.damage
        self.xp = enemy_config.xp
        self.can_damage = True
        self.isAlive = True

        self.image = py.transform.scale(Enum.Image.Enemy, (self.width, self.height))
        self.rect = self.image.get_rect(center=(posx, posy))

    # Propiedades para mantener compatibilidad con código que usa .x y .y
    @property
    def x(self):
        return self.rect.centerx

    @x.setter
    def x(self, value):
        self.rect.centerx = value

    @property
    def y(self):
        return self.rect.centery

    @y.setter
    def y(self, value):
        self.rect.centery = value

    # Mantener compatibilidad con enemy_react (código externo que lo referencia)
    @property
    def enemy_react(self):
        return self.rect

    def draw_enemy(self) -> None: 
        # Actualizar y dibujar enemigos
        self.screen.blit(self.image, self.rect)
        # Sincronizar la barra de vida con la posición actual del enemigo (justo encima)
        if self.enable_lifebar:
            self.lifeBar.set_position(self.rect.x, self.rect.y)
            self.lifeBar.draw_life_bar()
        