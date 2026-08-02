from __future__ import annotations
import pygame as py
from src.model.LifeBar import LifeBar
from src.model.Enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.model.Game import Game
    from src.model.Player import Player
    from src.model.Screen import Screen


class MainOverlay:
    def __init__(self, game_context: Game):
        self.screen: Screen = game_context.mainScreen
        self.player: Player = game_context.entities["player"]
        self.level = game_context.level

        # Barra de vida del jugador (esquina inferior izquierda)
        self.player_life_bar = LifeBar(self.screen.surface, 
                                       70,
                                       self.screen.height - 30,
                                       100,
                                       10,
                                       front_color=Enum.colorsMap.GREEN)

        self.player_life_bar.config_life(self.player.player_max_life, self.player.player_max_life)

        # === Nueva instancia de la imagen del jugador en la esquina inferior izquierda ===
        self.icon_image = py.image.load(Enum.resourcePath.SHIP)
        self.icon_image = py.transform.scale(self.icon_image, (40, 40))
        self.icon_rect = self.icon_image.get_rect()
        # Posicionar en el borde inferior izquierdo con un pequeño margen
        self.icon_rect.topleft = (20, self.screen.height - self.icon_rect.height - 10)

        # === Texto de puntaje para futuras implementaciones ===
        self.font_1 = py.font.SysFont("Arial", 30)
        self.surface_text_score = self.font_1.render(f"SCORE: {self.level.score}", True, Enum.colorsMap.WHITE)
        self.rect_text = self.surface_text_score.get_rect()
        self.rect_text.center = (self.screen.width//2, 20)

    def draw(self, screen_surface: py.Surface) -> None:
        """Dibuja el ícono del jugador y la barra de vida en la esquina inferior izquierda."""

        screen_surface.blit(self.icon_image, self.icon_rect)
        self.player_life_bar.config_life(self.player.player_life, self.player.player_max_life)
        self.player_life_bar.draw_life_bar()
        self.surface_text_score = self.font_1.render(f"SCORE: {self.level.score}", True, Enum.colorsMap.WHITE)
        self.screen.surface.blit(self.surface_text_score, self.rect_text)
