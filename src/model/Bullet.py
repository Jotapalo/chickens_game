from typing import Literal

import pygame as py
from src.model.Enum import Enum

class Bullet(py.sprite.Sprite):
    def __init__(self, pos_x, pos_y, data, bullet_speed=5, damage=1) -> None:
        super().__init__()
        self.image = py.image.load(self.get_character(data))
        self.image = py.transform.scale(self.image, (40, 40))
        self.damage = damage
        self.rect = self.image.get_rect(center=(pos_x, pos_y))
        self.bullet_speed = bullet_speed

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

    # Mantener compatibilidad con bullet_react (código externo que lo referencia)
    @property
    def bullet_react(self):
        return self.rect

    def move_up(self) -> None:
        self.rect.y -= self.bullet_speed

    @staticmethod
    def get_character(data) -> None | Literal['src/resources/bullet_1.PNG'] | Literal['src/resources/bullet_2.PNG']:
        if data == 1:
            return Enum.resourcePath.BULLET_1
        elif data == 2:
            return Enum.resourcePath.BULLET_2
