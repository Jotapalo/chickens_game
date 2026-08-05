from __future__ import annotations
import pygame as py
from src.model.LifeBar import LifeBar
from src.model.Enum import Enum
from src.services.PlayerService import PlayerService
from src.model.PowerUp_minigun import PowerUp_minigun
from src.model.PowerUp import PowerUp
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

        # === Nueva instancia de la imagen del jugador en la esquina inferior izquierda ===
        self.player_icon = Enum.Image.Player_icon
        self.player_icon_rect = self.player_icon.get_rect()
        # Posicionar en el borde inferior izquierdo con un pequeño margen
        self.player_icon_rect.topleft = (20, self.screen.height - self.player_icon_rect.height - 10)

        # Barra de vida del jugador (esquina inferior izquierda)
        self.player_life_bar = LifeBar(self.screen.surface, 
                                       70,
                                       self.screen.height - 30,
                                       100,
                                       10,
                                       front_color=Enum.colorsMap.GREEN)

        self.player_life_bar.config_life(self.player.player_max_life, self.player.player_max_life)


        # === Nueva instancia del Power Up activo de daño ===
        self.powerUp_icon = Enum.Image.PowerUpDamage_1
        self.powerUp_icon_rect = self.powerUp_icon.get_rect()
        self.powerUp_icon_rect.topleft = (20, self.player_icon_rect.y - 60)

        # == Nueva instancia del power Up activo de ametralladora
        self.powerUpMinigun_icon = Enum.Image.PowerUp_minigun
        self.powerUpMinigun_icon_rect = self.powerUp_icon.get_rect()
        self.powerUpMinigun_icon_rect.topleft = (20, self.powerUp_icon_rect.y - 60)


        # === Texto de puntaje ===
        self.font_1 = py.font.SysFont("arial", 30, bold=True)
        self.surface_text_score = self.font_1.render(f"SCORE: {self.level.score}", True, Enum.colorsMap.WHITE)
        self.rect_text = self.surface_text_score.get_rect()
        self.rect_text.center = (self.screen.width//2, 20)

        # Fondo oscuro detrás del score para que el texto blanco sea legible
        # sobre el fondo brillante (font.jpg) que se desplaza en cada frame.
        self.score_bg = py.Rect(0, 0, 0, 0)

    def draw(self, screen_surface: py.Surface) -> None:
        """Dibuja el ícono del jugador, la barra de vida y el puntaje actualizado."""

        # Dibujar Icono de Jugador
        screen_surface.blit(self.player_icon, self.player_icon_rect)

        # Dibujar Barra de vida
        self.player_life_bar.config_life(self.player.player_life, self.player.player_max_life)
        self.player_life_bar.draw_life_bar()

        # Dibujar power Up
        if PlayerService.actual_ammo != 1:
            screen_surface.blit(self.powerUp_icon, self.powerUp_icon_rect)
            damage_text = self.font_1.render(f"{int(PowerUp.timer.remaining_time)}", True, Enum.colorsMap.WHITE)
            damage_text_rect = damage_text.get_rect()
            damage_text_rect.topleft = (80, self.powerUp_icon_rect.y)
            screen_surface.blit(damage_text, damage_text_rect)

        if PowerUp_minigun.power_up_active:
            screen_surface.blit(self.powerUpMinigun_icon, self.powerUpMinigun_icon_rect)
            if not isinstance(PowerUp_minigun.timer, int):
                minigun_text = self.font_1.render(f"{int(PowerUp_minigun.timer.remaining_time)}", True, Enum.colorsMap.WHITE)
                minigun_text_rect = minigun_text.get_rect()
                minigun_text_rect.topleft = (80, self.powerUpMinigun_icon_rect.y)
                screen_surface.blit(minigun_text, minigun_text_rect)

        # Re-renderizar el puntaje con el valor actual y re-centrar el rect
        self.surface_text_score = self.font_1.render(f"SCORE: {self.level.score}", True, Enum.colorsMap.WHITE)
        self.rect_text = self.surface_text_score.get_rect()
        self.rect_text.center = (self.screen.width // 2, 20)

        # Panel de fondo para asegurar legibilidad del texto
        padding_x, padding_y = 12, 6
        self.score_bg = self.rect_text.inflate(padding_x * 2, padding_y * 2)
        py.draw.rect(screen_surface, (0, 0, 0), self.score_bg, border_radius=8)  # fondo negro
        # Contorno del texto para contrastar
        py.draw.rect(screen_surface, Enum.colorsMap.WHITE, self.score_bg, width=2, border_radius=8)
        screen_surface.blit(self.surface_text_score, self.rect_text)
