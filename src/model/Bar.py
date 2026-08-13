from src.model.Enum import Enum
from src.services.ResourceService import ResourceService
import pygame as py

class Bar:
    def __init__(self, screen, posx, posy, size_x, size_y, bar_type: str):
        """Clase que representa una barra de progreso

        Args:
            bar_type (str): puede ser: 'empty', 'player' o 'enemy'
        """

        bar_left, bar_center, bar_right = None, None, None
        self.screen = screen
        self.posx = posx
        self.posy = posy
        self.size_x = size_x
        self.size_y = size_y

        match bar_type:
            case "player": 
                bar_left = ResourceService.LifeBar_player.get("player_l")
                bar_center = ResourceService.LifeBar_player.get("player_m")
                bar_right = ResourceService.LifeBar_player.get("player_r")
            case "enemy":
                bar_left = ResourceService.LifeBar_enemy.get("enemy_l")
                bar_center = ResourceService.LifeBar_enemy.get("enemy_m")
                bar_right = ResourceService.LifeBar_enemy.get("enemy_r")
            case "empty":
                bar_left = ResourceService.LifeBar_empty.get("empty_l")
                bar_center = ResourceService.LifeBar_empty.get("empty_m")
                bar_right = ResourceService.LifeBar_empty.get("empty_r")
            case _:
                print("Error en la carga de barra: Bar.py")

        center_width = size_x - bar_left.get_width()*2
        self.bar_left = py.transform.scale(bar_left, (bar_left.get_width(), size_y))
        self.bar_right = py.transform.scale(bar_right, (bar_right.get_width(), size_y))
        self.bar_center = py.transform.scale(bar_center, (center_width, size_y))

    def draw(self):
        last_x = self.posx

        self.screen.blit(self.bar_left, (last_x, self.posy))
        last_x += self.bar_left.get_width()

        self.screen.blit(self.bar_center, (last_x, self.posy))
        last_x += self.bar_center.get_width()

        self.screen.blit(self.bar_right, (last_x, self.posy))

    def update_bar(self, size_x):
        center_width = size_x - self.bar_left.get_width()*2
        if center_width < 0:
            center_width = 0
        self.bar_left = py.transform.scale(self.bar_left, (self.bar_left.get_width(), self.size_y))
        self.bar_right = py.transform.scale(self.bar_right, (self.bar_right.get_width(), self.size_y))
        self.bar_center = py.transform.scale(self.bar_center, (center_width, self.size_y))

        