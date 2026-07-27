import threading
import time
import pygame as py
from src.services.ShootService import ShootService
from src.model.Bullet import Bullet
from src.model.Enum import Enum

power_up_active = False

class TimerThread(threading.Thread):
    def __init__(self, duration, callback, daemon: bool) -> None:
        super().__init__(daemon=daemon)
        self.duration = duration
        self.callback = callback
        self._pause_event = threading.Event()
        self._stop_event = threading.Event()
        self.remaining_time = duration

    def run(self) -> None:
        start_time = time.time()
        while self.remaining_time > 0:
            if self._stop_event.is_set():
                break
            if not self._pause_event.is_set():
                elapsed = time.time() - start_time
                self.remaining_time -= elapsed
                start_time = time.time()
                time.sleep(0.1)  # Pequeña pausa para reducir el consumo de CPU
            else:
                start_time = time.time()  # Resetear tiempo al pausar
        if self.remaining_time <= 0:
            self.callback()

    def pause(self) -> None:
        self._pause_event.set()

    def resume(self) -> None:
        self._pause_event.clear()

    def stop(self) -> None:
        self._stop_event.set()


class PowerUp(py.Vector2):
    def __init__(self, screen=None) -> None:
        super().__init__(100, 100)
        self.screen = screen
        self.image = py.image.load(Enum.resourcePath.POWER_UP)
        self.image = py.transform.scale(self.image, (80, 80))
        self.gem_react = self.image.get_rect(center=self)

    def move_down(self, speed=1) -> None:
        self.y += speed

    def draw_power_up(self, screen=None) -> None:
        """Dibuja el PowerUp en la pantalla.
        
        Args:
            screen: Superficie de pygame donde dibujar. Si no se proporciona,
                    usa la screen almacenada en el constructor.
        """
        target_screen = screen if screen is not None else self.screen
        if target_screen is None:
            raise ValueError("Se necesita una superficie de pygame para dibujar el PowerUp.")
        self.gem_react.center = (self.x, self.y)
        target_screen.blit(self.image, self.gem_react)

    def check_player_collision(self, player) -> bool:
        """Comprueba si el PowerUp colisiona con el jugador.
        
        Args:
            player: Objeto Player con un atributo player_react (pygame.Rect)
            
        Returns:
            bool: True si hay colisión, False en caso contrario.
        """
        return self.gem_react.colliderect(player.player_react)

    def update_and_draw(self, screen, player, speed=1) -> bool:
        """Mueve el PowerUp hacia abajo, lo dibuja, y comprueba colisión con el jugador.
        
        Args:
            screen: Superficie de pygame donde dibujar.
            player: Objeto Player para detectar colisión.
            speed: Velocidad de movimiento hacia abajo.
            
        Returns:
            bool: True si el PowerUp colisionó con el jugador, False en caso contrario.
        """
        self.move_down(speed)
        self.draw_power_up(screen)
        return self.check_player_collision(player)

    @staticmethod
    def power_up_timeout() -> None:
        global power_up_active
        power_up_active = False
        print("El power-up ha expirado.")
        ShootService.actual_ammo = 1
        ShootService.bullet_damage = 1


    @staticmethod
    def activate_power_up(duration=5):
        global power_up_active
        power_up_active = True
        print("Power-up activado.")
        # Iniciar el temporizador para el power-up
        timer = TimerThread(duration=duration, callback=PowerUp.power_up_timeout, daemon=True)
        timer.start()
        ShootService.actual_ammo = 2
        ShootService.bullet_damage = 5
        return timer  # Retornar el temporizador para controlarlo si es necesario

