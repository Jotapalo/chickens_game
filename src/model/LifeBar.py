import pygame
from src.model.Enum import Enum

class LifeBar(pygame.Vector2):
    def __init__(self, screen: pygame.Surface, x, y, width, height ):
        super().__init__(x, y)
        self.screen = screen
        self.total_bar = pygame.Rect(x, y, width, height)
        self.life_bar = pygame.Rect(x, y, width, height)

    def config_life(self, life, max_life):
        per: float = life/max_life
        self.life_bar.width = self.total_bar.width * per

    def set_position(self, x, y):
        """Fija la posición absoluta de la barra de vida."""
        self.total_bar.x = x
        self.total_bar.y = y
        self.life_bar.x = x
        self.life_bar.y = y
        
    def draw_life_bar(self):
        self.total_bar_react = pygame.draw.rect(surface=self.screen, 
                                               color=Enum.colorsMap.WHITE, 
                                               width=10, 
                                               rect=self.total_bar)
        self.life_bar_react = pygame.draw.rect(surface=self.screen, 
                                                       color=Enum.colorsMap.RED, 
                                                       width=10, 
                                                       rect=self.life_bar)

        