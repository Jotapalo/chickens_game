from src.model.Bullet import Bullet
from src.model.Player import Player

class ShootService:
    def __init__(self):
        self.__cooldown_counter = 0
        self.bulletsList = list()

    def increment_counter (self):
        self.__cooldown_counter += 1

    def shoot_checker (self, player: Player):
        # Disparo de balas cada 20 frames
        if self.__cooldown_counter >= 20:
            self.__cooldown_counter = 0
            self.bulletsList.append(Bullet(player.x, player.y, data=Bullet.actual_ammo))
            
    def draw_bullets (self, screen): 
        # Actualizar y dibujar cada proyectil
        for bullet in self.bulletsList[:]:
            bullet.move_up(speed=20)
            bullet.bullet_react.center = (bullet.x, bullet.y)
            screen.blit(bullet.image, bullet.bullet_react)
    
            if bullet.y < 0:
                self.bulletsList.remove(bullet)