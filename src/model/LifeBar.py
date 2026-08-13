import pygame
from src.model.Enum import Enum
from src.model.Bar import Bar

class LifeBar: 
    def __init__(self, screen: pygame.Surface, x: int, y:int, 
                 width: int, height: int,
                 bar_type: str):
        self.screen = screen
        self.total_bar = Bar(screen=screen, posx=x, posy=y, size_x=width, size_y=height, bar_type="empty")
        self.life_bar = Bar(screen=screen, posx=x, posy=y, size_x=width, size_y=height, bar_type=bar_type)

    def config_life(self, life, max_life):
        per: float = life/max_life
        if life < 0:
            life = 0
        if life > max_life:
            life = max_life
        self.life_bar.update_bar(self.total_bar.size_x * per)

    def set_position(self, x, y):
        """Fija la posición absoluta de la barra de vida."""
        self.total_bar.posx = x
        self.total_bar.posy = y
        self.life_bar.posx = x
        self.life_bar.posy = y
        
    def draw_life_bar(self):
        self.total_bar.draw()
        self.life_bar.draw()
