import threading
import pygame as py
import time
from src.model.Game import Game


class MessageOverlay:
    """Superficie transparente que se superpone al screen para mostrar mensajes.
    
    El hilo llamará a show() para activar el mensaje con una duración.
    El game loop principal llamará a draw() para renderizarlo sobre el screen.
    """
    def __init__(self, game_context: Game):
        self.width = game_context.mainScreen.width
        self.height = game_context.mainScreen.height
        # Superficie con canal alfa (transparencia)
        self.surface = py.Surface((self.width, self.height), py.SRCALPHA)
        self.active = False
        self._lock = threading.Lock()

    def show(self, text: str, duration: float):
        """Renderiza el mensaje y lo muestra durante 'duration' segundos (llamado desde el hilo)."""

        if text == "": return
        
        font = py.font.Font(None, 40)
        text_surface = font.render(text, True, (255, 255, 255))

        # Limpiar la superficie overlay (totalmente transparente)
        self.surface.fill((0, 0, 0, 0))

        # Fondo semitransparente detrás del texto
        padding_x, padding_y = 30, 15
        bg_rect = py.Rect(0, 0, text_surface.get_width() + padding_x * 2,
                          text_surface.get_height() + padding_y * 2)
        bg_rect.center = (self.width // 2, self.height // 2)
        py.draw.rect(self.surface, (0, 0, 0, 180), bg_rect, border_radius=12)

        # Texto centrado sobre el fondo
        text_rect = text_surface.get_rect(center=(self.width // 2, self.height // 2))
        self.surface.blit(text_surface, text_rect)

        # Marcar como activo y esperar
        with self._lock:
            self.active = True

        time.sleep(duration)

        # Desactivar
        with self._lock:
            self.active = False
            self.surface.fill((0, 0, 0, 0))

    def draw(self, screen_surface: py.Surface):
        """Dibuja el overlay sobre la pantalla si está activo (llamado desde el game loop)."""
        with self._lock:
            if self.active:
                screen_surface.blit(self.surface, (0, 0))

