import pygame as py

class PlayerMovementService:
    def __init__(self, player):
        self.player = player
        self.__player_speed = 10

    def player_movement(self, screen):
        # Movimiento del jugador
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

        