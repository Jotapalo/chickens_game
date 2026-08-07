import math
import pygame as py
from src.model.Enum import Enum
from src.model.Config import MeteorConfig

class Meteor(py.sprite.Sprite):
    def __init__(self, screen, meteor_CFG: MeteorConfig = None):
        super().__init__()

        if meteor_CFG is None:
            meteor_CFG = MeteorConfig.getRandomConfig(screen)

        self.degree = meteor_CFG.degree
        self.delta_x = meteor_CFG.delta_x
        self.delta_y = meteor_CFG.delta_y
        self.image = py.transform.rotate(Enum.Image.Meteor, self.degree)
        self.image = py.transform.scale(self.image, (meteor_CFG.size, meteor_CFG.size))
        self.image = py.transform.flip(self.image, True if self.delta_x < 0 else False, True if self.delta_y < 0 else False)
        self.rect = self.image.get_rect(center=(meteor_CFG.posx, meteor_CFG.posy))

    def draw(self, screen_surface):
        screen_surface.blit(self.image, self.rect)

    def draw_and_move(self, screen_surface: py.Surface) -> bool:
        self.rect.x += self.delta_x
        self.rect.y += self.delta_y
        self.draw(screen_surface=screen_surface)

        # Devuelve True si el meteorito salió de la pantalla (con margen del
        # tamaño del sprite) para que el llamador lo elimine de su lista.
        screen_w = screen_surface.get_width()
        screen_h = screen_surface.get_height()
        return (self.rect.right < -self.rect.width or
                self.rect.left > screen_w + self.rect.width or
                self.rect.bottom < -self.rect.height or
                self.rect.top > screen_h + self.rect.height)
