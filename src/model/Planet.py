import pygame as py
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    ...

class Planet(py.sprite.Sprite):
    def __init__(self, image: py.Surface, posx, posy):
        super().__init__()
        self.image = image
        self.rect = image.get_rect(center=(posx, posy))

    def draw(self, screen_surface: py.Surface):
        screen_surface.blit(self.image, self.rect)

    def draw_and_move(self, screen_surface: py.Surface):
        self.draw(screen_surface=screen_surface)
        self.rect.y += 1