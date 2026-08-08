from __future__ import annotations
import pygame as py
from src.model.Enum import Enum
from src.model.TimerThread import TimerThread
from src.services.SoundService import SoundService
from random import randint
from typing import TYPE_CHECKING
from src.services.PlayerService import PlayerService

if TYPE_CHECKING:
    from src.model.Config import PowerUpConfig

class PowerUp(py.sprite.Sprite):
    power_up_active = False
    # Timer compartido a nivel de clase: siempre apunta al último temporizador
    # de daño activo. Así cualquier instancia puede extender/referenciar
    # el temporizador actual sin depender de un dict externo.
    timer: TimerThread | None = None

    def __init__(self, powerUp_CFG: PowerUpConfig, screen=None) -> None:
        super().__init__()
        self.screen = screen
        self.player_service: PlayerService | None = None
        self.image = Enum.Image.PowerUpDamage_1

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
        if self.rect.colliderect(player.rect):
            SoundService.play_power_up_sound()
            return True
        return False

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
        PowerUp.timer = None  # El timer terminó, lo limpiamos
        print("El power-up ha expirado.")
        if self.player_service:
            PlayerService.actual_ammo = 1
            PlayerService.bullet_damage = 1

    def activate_power_up(self):
        PowerUp.power_up_active = True
        print("Power-up activado.")
        if self.player_service:
            PlayerService.actual_ammo = 2
            PlayerService.bullet_damage = self.powerUp_CFG.damage

        # Siempre referenciamos el último timer de la clase.
        # Si sigue activo, lo extendemos; si no, creamos uno nuevo.
        if PowerUp.timer is not None:
            PowerUp.timer.extend(self.powerUp_CFG.duration)
            return PowerUp.timer

        # No hay timer activo: crear e iniciar uno nuevo y guardarlo en la clase
        PowerUp.timer = TimerThread(
            duration=self.powerUp_CFG.duration,
            callback=self.power_up_timeout,
            daemon=True,
        )
        PowerUp.timer.start()
        return PowerUp.timer
