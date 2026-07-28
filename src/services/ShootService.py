import pygame as py
from src.model.Bullet import Bullet
from src.model.Player import Player

class ShootService:
    def __init__(self, bullet_speed, player: Player) -> None:
        self.__cooldown_counter = 0
        self.bulletsGroup = py.sprite.Group()
        self.bullet_speed = bullet_speed
        self.player = player
        
    bullet_damage = 1 # valor por defecto
    actual_ammo = 1 # valor por defecto

    @property
    def bulletsList(self):
        """Mantiene compatibilidad con código que usa bulletsList."""
        return self.bulletsGroup.sprites()

    def increment_counter (self) -> None:
        self.__cooldown_counter += 1

    def shoot_checker (self) -> None:
        # Disparo de balas cada 20 frames
        if self.__cooldown_counter >= 20:
            self.__cooldown_counter = 0
            new_bullet = Bullet(self.player.x, self.player.y,
                                data=ShootService.actual_ammo, 
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
