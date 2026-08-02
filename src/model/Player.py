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
        self.player_life = self.player_max_life

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

    def check_collisions(self, enemies) -> list:
        """Detecta colisiones entre el jugador y los enemigos.

        Cuando un enemigo colisiona con el jugador y aún puede dañar
        (enemy.can_damage == True), la vida del jugador se reduce en
        enemy.damage y el enemigo pasa a can_damage = False para no
        seguir haciendo daño en colisiones posteriores (efecto "one shot").

        Args:
            enemies: Iterable de enemigos (lista, Group de pygame, etc.).

        Returns:
            list: Lista de enemigos que colisionaron en este ciclo.
        """
        collided_enemies = []
        for enemy in enemies:
            if py.sprite.collide_rect(self, enemy):
                collided_enemies.append(enemy)
                if enemy.can_damage:
                    self.player_life -= enemy.damage
                    enemy.can_damage = False
        return collided_enemies

    def draw_player(self, rectangle:py.Rect | None = None) -> None: 
        if rectangle == None:
            rectangle = self.rect
        # Actualizar y dibujar al jugador
        self.screen.blit(self.image, rectangle)
