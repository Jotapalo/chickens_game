from __future__ import annotations
import pygame as py
from src.model.Enum import Enum
from random import randint
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.config.HealthConfig import HealthConfig

class Health(py.sprite.Sprite):
    def __init__(self, health_CFG: HealthConfig, screen=None) -> None:
        super().__init__()
        self.screen = screen
        self.health_CFG = health_CFG
        self.image = py.image.load(Enum.resourcePath.HEALTH)
        self.image = py.transform.scale(self.image, (40,40))

        # Si alguno de los rangos es lista entonces retorna un numero aleatorio en ese rango, si no entonces un entero
        rangex = randint(*self.health_CFG.x) if isinstance(self.health_CFG.x, list) else self.health_CFG.x
        rangey = randint(*self.health_CFG.y) if isinstance(self.health_CFG.y, list) else self.health_CFG.y
        self.rect = self.image.get_rect(center=(rangex, rangey))

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

    # Mantener compatibilidad con gem_react (código externo que lo referencia)
    @property
    def gem_react(self):
        return self.rect

    def move_down(self) -> None:
        self.rect.y += self.health_CFG.fall_speed

    def draw_health(self, screen=None) -> None:
        """Dibuja el Health en la pantalla.
        
        Args:
            screen: Superficie de pygame donde dibujar. Si no se proporciona,
                    usa la screen almacenada en el constructor.
        """
        target_screen = screen if screen is not None else self.screen
        if target_screen is None:
            raise ValueError("Se necesita una superficie de pygame para dibujar el Health.")
        target_screen.blit(self.image, self.rect)

    def check_player_collision(self, player) -> bool:
        """Comprueba si el Health colisiona con el jugador.
        
        Args:
            player: Objeto Player cuyo rect usamos para colisión
            
        Returns:
            bool: True si hay colisión, False en caso contrario.
        """
        return self.rect.colliderect(player.rect)

    def update_and_draw(self, screen, player) -> bool:
        """Mueve el Health hacia abajo, lo dibuja, y comprueba colisión con el jugador.
        
        Args:
            screen: Superficie de pygame donde dibujar.
            player: Objeto Player para detectar colisión.
            
        Returns:
            bool: True si el Health colisionó con el jugador, False en caso contrario.
        """
        self.move_down()
        self.draw_health(screen)
        return self.check_player_collision(player)

    def heal_player(self, player) -> None:
        """Cura al jugador la cantidad indicada en health_CFG.heal_amount (20 por defecto).
        
        La curación no puede superar la vida máxima del jugador (player_max_life).

        Args:
            player: Objeto Player al que se cura.
        """
        if player is None:
            return
        player.player_life = min(
            player.player_life + self.health_CFG.heal_amount,
            player.player_max_life
        )
        print(f"Salud recuperada: +{self.health_CFG.heal_amount} puntos")

