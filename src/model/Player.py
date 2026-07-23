import pygame as py
import src.enum.resEnum as resEnum
from src.services.PlayerMovementService import PlayerMovementService

class Player(py.Vector2):
    def __init__(self, screen):
        super().__init__(screen.get_width() / 2, screen.get_height() / 2)
        self.screen = screen
        self.image_player = py.image.load(resEnum.SHIP)
        self.image_player = py.transform.scale(self.image_player, (70, 70))
        self.player_react = self.image_player.get_rect(center=self)
        self.PlayerMovementSVC: PlayerMovementService

    def suscribeMovementService(self, PlayerMovementService: PlayerMovementService):
        self.PlayerMovementSVC = PlayerMovementService

    def draw_player(self): 
        # Actualizar y dibujar al jugador
        self.player_react.center = (self.x, self.y)
        self.screen.blit(self.image_player, self.player_react)