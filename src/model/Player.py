from __future__ import annotations
import pygame as py
from src.model.Enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.services.PlayerMovementService import PlayerMovementService

class Player(py.sprite.Sprite):
    def __init__(self, screen= None) -> None:
        super().__init__()
        self.screen = screen
        self.image = py.image.load(Enum.resourcePath.SHIP)
        self.image = py.transform.scale(self.image, (70, 70))
        self.rect = self.image.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2))
        self.PlayerMovementSVC: PlayerMovementService
        self.player_max_life = 100

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

    # Mantener compatibilidad con player_react (código externo que lo referencia)
    @property
    def player_react(self):
        return self.rect

    def suscribeMovementService(self, PlayerMovementService: PlayerMovementService) -> None:
        self.PlayerMovementSVC = PlayerMovementService

    def draw_player(self, rectangle:py.Rect | None = None) -> None: 
        if rectangle == None:
            rectangle = self.rect
        # Actualizar y dibujar al jugador
        self.screen.blit(self.image, rectangle)
