from typing import Literal

import pygame as py
from src.model.Enum import Enum

class Bullet(py.Vector2):
    def __init__(self, pos_x, pos_y, data, bullet_speed=5, damage=1) -> None:
        super().__init__(pos_x, pos_y)
        self.image = py.image.load(self.get_character(data))
        self.image = py.transform.scale(self.image, (40, 40))
        self.damage = damage
        self.bullet_react = self.image.get_rect(center=self)
        self.bullet_speed = bullet_speed

    def move_up(self) -> None:
        self.y -= self.bullet_speed

    @staticmethod
    def get_character(data) -> None | Literal['src/resources/bullet_1.PNG'] | Literal['src/resources/bullet_2.PNG']:
        if data == 1:
            return Enum.resourcePath.BULLET_1
        elif data == 2:
            return Enum.resourcePath.BULLET_2