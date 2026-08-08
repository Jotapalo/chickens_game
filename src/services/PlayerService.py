from __future__ import annotations
import pygame as py
from src.model.Bullet import Bullet
from src.model.Player import Player
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.model.Game import Game

class PlayerService:
    def __init__(self, game_context: Game) -> None:
        self.game_context = game_context
        self.screen = game_context.mainScreen
        self.sound_service = game_context.services.get("sound_service")
        self.__cooldown_counter = 0
        self.bulletsGroup = py.sprite.Group()
        self.bullet_speed = game_context.parameters.get("bullet_speed")
        self.cadence = 20 # Valor por defecto debe ser modificable a futuro
        self.player = game_context.entities.get("player")
        self.__player_speed = 10
    bullet_damage = 1 # valor por defecto
    actual_ammo = 1 # valor por defecto

    @property
    def bulletsList(self):
        """Mantiene compatibilidad con código que usa bulletsList."""
        return self.bulletsGroup.sprites()

    def player_movement(self) -> None:
        # Movimiento del jugador (antes PlayerMovementService, ahora encapsulado)
        screen = self.screen.surface
        keys = py.key.get_pressed()
        if keys[py.K_RIGHT] or keys[py.K_d]:
            self.player.x += self.__player_speed
        if keys[py.K_LEFT] or keys[py.K_a]:
            self.player.x -= self.__player_speed
        if keys[py.K_UP] or keys[py.K_w]:
            self.player.y -= self.__player_speed
        if keys[py.K_DOWN] or keys[py.K_s]:
            self.player.y += self.__player_speed

        # Limitar el movimiento del jugador a la pantalla
        self.player.x = max(self.player.player_react.width // 2,
                            min(self.player.x, screen.get_width() - self.player.player_react.width // 2))
        self.player.y = max(self.player.player_react.width // 2,
                            min(self.player.y, screen.get_height() - self.player.player_react.width // 2))

    def shoot_checker (self) -> None:
        self.__cooldown_counter += 1

        # Disparo de balas cada self.cadence frames
        if self.__cooldown_counter >= self.cadence:
            if self.sound_service == None:
                self.sound_service = self.game_context.services.get("sound_service")
            self.sound_service.play_shoot_sound()
            self.__cooldown_counter = 0
            new_bullet = Bullet(self.player.x, self.player.y,
                                data=PlayerService.actual_ammo, 
                                bullet_speed=self.bullet_speed,
                                damage=self.bullet_damage)
            self.bulletsGroup.add(new_bullet)

            
            
    def draw_bullets (self, screen) -> None: 
        # Actualizar y dibujar cada proyectil
        for bullet in self.bulletsGroup.sprites():
            bullet: Bullet
            bullet.move_up()
            screen.blit(bullet.image, bullet.rect)
    
            if bullet.rect.y < 0:
                bullet.kill()
