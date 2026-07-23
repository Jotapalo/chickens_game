import pygame as py
import src.enum.resEnum as resEnum

class Enemy(py.Vector2):
    def __init__(self, screen, posx, posy):
        super().__init__(posx, posy)
        self.screen = screen
        self.image_enemy = py.image.load(resEnum.ENEMY)
        self.image_enemy = py.transform.scale(self.image_enemy, (70, 70))
        self.enemy_react = self.image_enemy.get_rect(center=self)

    def draw_enemy(self): 
        # Actualizar y dibujar enemigos
        self.enemy_react.center = (self.x, self.y)
        self.screen.blit(self.image_enemy, self.enemy_react)