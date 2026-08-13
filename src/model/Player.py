from __future__ import annotations
import time
import pygame as py
from src.model.Enum import Enum
from src.services.ResourceService import ResourceService


class Player(py.sprite.Sprite):
    def __init__(self, screen=None) -> None:
        super().__init__()
        self.screen = screen
        self.image = ResourceService.BattheShip_collection[4]
        self.rect = self.image.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2))
        self.player_max_life = 100
        self.player_life = self.player_max_life
        self.can_damaged = True
        self.player_draw = True
        # Temporizador de invulnerabilidad basado en time.time() (sin hilos)
        self._invulnerable_until = 0.0

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

    def check_collisions(self, enemies) -> list:
        """Detecta colisiones entre el jugador y los enemigos.

        Cuando un enemigo colisiona con el jugador y aún puede dañar
        (enemy.can_damage == True), la vida del jugador se reduce en
        enemy.damage y el enemigo pasa a can_damage = False para no
        seguir haciendo daño en colisiones posteriores (efecto "one shot").

        La invulnerabilidad se gestiona con un temporizador basado en
        time.time() (sin crear hilos), comprobado en update_invulnerability().

        Args:
            enemies: Iterable de enemigos (lista, Group de pygame, etc.).

        Returns:
            list: Lista de enemigos que colisionaron en este ciclo.
        """
        collided_enemies = []
        for enemy in enemies:
            if py.sprite.collide_rect(self, enemy):
                collided_enemies.append(enemy)
                if self.can_damaged:
                    self.player_life -= enemy.damage
                    self.can_damaged = False
                    # Activar invulnerabilidad de 2 segundos (parpadeo)
                    self._invulnerable_until = time.time() + 2.0
                    self.player_draw = False
                return
        return collided_enemies

    def update_invulnerability(self) -> None:
        """Gestión del parpadeo de invulnerabilidad (llamar cada frame).

        Durante los primeros 2 segundos tras recibir daño, el jugador
        parpadea alternando player_draw. Al terminar el lapso, se restaura
        el dibujo normal y la capacidad de recibir daño.
        """
        if not self.can_damaged:
            remaining = self._invulnerable_until - time.time()
            if remaining <= 0:
                # Fin de la invulnerabilidad
                self.can_damaged = True
                self.player_draw = True
            else:
                # Parpadeo: alternar visibilidad con parpadeos rápidos
                self.player_draw = (int(remaining * 8) % 2) == 0

    def draw_player(self, rectangle: py.Rect | None = None) -> None:
        if rectangle is None:
            rectangle = self.rect
        # Actualizar y dibujar al jugador
        if self.player_draw:
            self.screen.blit(self.image, rectangle)
