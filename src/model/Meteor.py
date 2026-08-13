import time
import pygame as py
from src.services.ResourceService import ResourceService
from src.model.Config import MeteorConfig

class Meteor(py.sprite.Sprite):
    """Meteorito con animación de rotación.

    Usa la colección de frames pre-cargada en ResourceService.Asteroid_collection
    (spin-00.png ... spin-10.png) para animar el giro del asteroide.
    """
    # Velocidad de animación: cuántos frames se avanzan por draw (controla la
    # velocidad de giro). Se puede ajustar aquí o por instancia.
    frame_duration = 3

    def __init__(self, screen, meteor_CFG: MeteorConfig = None):
        super().__init__()

        if meteor_CFG is None:
            meteor_CFG = MeteorConfig.getRandomConfig(screen)

        self.degree = meteor_CFG.degree
        self.delta_x = meteor_CFG.delta_x
        self.delta_y = meteor_CFG.delta_y
        self.size = meteor_CFG.size
        self.damage = meteor_CFG.damage

        self._frame_index = 0
        self._frame_counter = 0
        self._hit_player = False

        # Frames de la animación (lista pre-cargada, reutilizada entre meteoritos).
        # Se aplican escalado y volteo según la dirección de movimiento para
        # que la animación se vea coherente con la trayectoria.
        self.frames = [
            py.transform.scale(frame, (self.size, self.size))
            for frame in ResourceService.Asteroid_collection
        ]
        """self.frames = [
            py.transform.flip(frame,
                              True if self.delta_x < 0 else False,
                              True if self.delta_y < 0 else False)
            for frame in self.frames
        ]"""
        for frame in self.frames:
            py.transform.rotate(frame, self.degree)

        self.image = self.frames[0]
        self.rect = self.image.get_rect(center=(meteor_CFG.posx, meteor_CFG.posy))

    def update(self) -> None:
        """Avanza la animación un frame (con control de velocidad)."""
        self._frame_counter += 1
        if self._frame_counter >= self.frame_duration:
            self._frame_counter = 0
            self._frame_index = (self._frame_index + 1) % len(self.frames)
            self.image = self.frames[self._frame_index]

    def draw(self, screen_surface):
        self.update()
        screen_surface.blit(self.image, self.rect)

    def check_player_collision(self, player) -> bool:
        """Detecta si este meteorito colisiona con el jugador.

        Si colisiona y el jugador puede recibir daño, le resta vida y activa
        la invulnerabilidad (mismo patrón que Player.check_collisions). El
        meteorito solo golpea una vez (flag _hit_player).

        Args:
            player: Instancia de Player.

        Returns:
            bool: True si el meteorito impactó al jugador (debe eliminarse).
        """
        if self._hit_player:
            return True

        if player is not None and py.sprite.collide_rect(self, player):
            collided = True
            if player.can_damaged:
                player.player_life -= self.damage
                player.can_damaged = False
                player._invulnerable_until = time.time() + 2.0
                player.player_draw = False
            self._hit_player = True
            return collided

        return False

    def draw_and_move(self, screen_surface: py.Surface, player=None) -> bool:
        self.rect.x += self.delta_x
        self.rect.y += self.delta_y
        self.draw(screen_surface=screen_surface)

        # Si colisionó con el jugador, devuelve True para que el llamador lo elimine.
        if self.check_player_collision(player):
            return True

        # Devuelve True si el meteorito salió de la pantalla (con margen del
        # tamaño del sprite) para que el llamador lo elimine de su lista.
        screen_w = screen_surface.get_width()
        screen_h = screen_surface.get_height()
        return (self.rect.right < -self.rect.width or
                self.rect.left > screen_w + self.rect.width or
                self.rect.bottom < -self.rect.height or
                self.rect.top > screen_h + self.rect.height)
