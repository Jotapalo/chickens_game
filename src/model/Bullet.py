import pygame as py
import src.enum.resEnum as resEnum

class Bullet(py.Vector2):
    actual_ammo = 1

    def __init__(self, pos_x, pos_y, data):
        super().__init__(pos_x, pos_y)
        self.image = py.image.load(self.get_character(data))
        self.image = py.transform.scale(self.image, (40, 40))
        self.bullet_react = self.image.get_rect(center=self)

    def move_up(self, speed=5):
        self.y -= speed

    @staticmethod
    def get_character(data):
        if data == 1:
            return resEnum.BULLET_1
        elif data == 2:
            return resEnum.BULLET_2