from __future__ import annotations
import pygame as py
from src.model.Enum import Enum
from src.model.TimerThread import TimerThread
from random import randint
from typing import TYPE_CHECKING
from src.services.ShootService import ShootService

if TYPE_CHECKING:
    from src.config.PowerUpConfig import PowerUpConfig
class PowerUp(py.sprite.Sprite):
    power_up_active = False
    def __init__(self, powerUp_CFG: PowerUpConfig, screen=None) -> None:
        super().__init__()
        self.screen = screen
        self.shoot_service: ShootService | None = None
        self.image = py.image.load(Enum.resourcePath.POWER_UP)
        self.image = py.transform.scale(self.image, (80, 80))

        self.powerUp_CFG = powerUp_CFG
        rangex = randint(*self.powerUp_CFG.x) if isinstance(self.powerUp_CFG.x, list) else self.powerUp_CFG.x
        rangey = randint(*self.powerUp_CFG.y) if isinstance(self.powerUp_CFG.y, list) else self.powerUp_CFG.y
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
        self.rect.y += self.powerUp_CFG.fall_speed

    def draw_power_up(self, screen=None) -> None:
        """Dibuja el PowerUp en la pantalla.
        
        Args:
            screen: Superficie de pygame donde dibujar. Si no se proporciona,
                    usa la screen almacenada en el constructor.
        """
        target_screen = screen if screen is not None else self.screen
        if target_screen is None:
            raise ValueError("Se necesita una superficie de pygame para dibujar el PowerUp.")
        target_screen.blit(self.image, self.rect)

    def check_player_collision(self, player) -> bool:
        """Comprueba si el PowerUp colisiona con el jugador.
        
        Args:
            player: Objeto Player cuyo rect usamos para colisión
            
        Returns:
            bool: True si hay colisión, False en caso contrario.
        """
        return self.rect.colliderect(player.rect)

    def update_and_draw(self, screen, player) -> bool:
        """Mueve el PowerUp hacia abajo, lo dibuja, y comprueba colisión con el jugador.
        
        Args:
            screen: Superficie de pygame donde dibujar.
            player: Objeto Player para detectar colisión.
            speed: Velocidad de movimiento hacia abajo.
            
        Returns:
            bool: True si el PowerUp colisionó con el jugador, False en caso contrario.
        """
        self.move_down()
        self.draw_power_up(screen)
        return self.check_player_collision(player)

    def power_up_timeout(self) -> None:
        PowerUp.power_up_active = False
        print("El power-up ha expirado.")
        if self.shoot_service:
            ShootService.actual_ammo = 1
            ShootService.bullet_damage = 1

    def activate_power_up(self):
        PowerUp.power_up_active = True
        print("Power-up activado.")
        # Iniciar el temporizador para el power-up
        timer = TimerThread(duration=self.powerUp_CFG.duration, callback=self.power_up_timeout, daemon=True)
        timer.start()
        if self.shoot_service:
            ShootService.actual_ammo = 2
            ShootService.bullet_damage = self.powerUp_CFG.damage
        return timer  # Retornar el temporizador para controlarlo si es necesario
