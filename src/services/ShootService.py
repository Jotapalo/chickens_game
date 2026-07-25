from src.model.Bullet import Bullet
from src.model.Player import Player

class ShootService:
    def __init__(self, bullet_speed) -> None:
        self.__cooldown_counter = 0
        self.bulletsList = list()
        self.bullet_speed = bullet_speed

    def increment_counter (self) -> None:
        self.__cooldown_counter += 1

    def shoot_checker (self, player: Player) -> None:
        # Disparo de balas cada 20 frames
        if self.__cooldown_counter >= 20:
            self.__cooldown_counter = 0
            self.bulletsList.append(Bullet(player.x, player.y,
                                            data=Bullet.actual_ammo, bullet_speed=self.bullet_speed))
            
    def draw_bullets (self, screen) -> None: 
        # Actualizar y dibujar cada proyectil
        for bullet in self.bulletsList[:]:
            bullet: Bullet
            bullet.move_up()
            bullet.bullet_react.center = (bullet.x, bullet.y)
            screen.blit(bullet.image, bullet.bullet_react)
    
            if bullet.y < 0:
                self.bulletsList.remove(bullet)