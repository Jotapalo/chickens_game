import pygame
from src.model.Enum import Enum

class LifeBar(pygame.Vector2): 
    def __init__(self, screen: pygame.Surface, x: int, y:int, 
                 width: int, height: int,
                 front_color: tuple = Enum.colorsMap.RED,
                 background_color: tuple = Enum.colorsMap.WHITE):
        """Constructor de Barra de Vida generica para varias entidades

        Args:
            screen (pygame.Surface): superficie de dibujado
            x (int): coordenada x: empieza desde left y crece hacia right
            y (int): coordenada y: empieza desde top y crece hacia bottom
            width (int): ancho de la barra de vida
            height (_type_): alto de la barra de vida
        """        
        super().__init__(x, y)
        self.screen = screen
        self.total_bar = pygame.Rect(x, y, width, height)
        self.life_bar = pygame.Rect(x, y, width, height)
        self.front_color = front_color
        self.background_color = background_color

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
                                               color=self.background_color, 
                                               width=10, 
                                               rect=self.total_bar)
        self.life_bar_react = pygame.draw.rect(surface=self.screen, 
                                                       color=self.front_color, 
                                                       width=10, 
                                                       rect=self.life_bar)

        