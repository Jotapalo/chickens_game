import pygame as py
import threading
import time
from random import randint
from src.model.Bullet import Bullet
from src.model.Enum import Enum

power_up_active = False
class TimerThread(threading.Thread):
    def __init__(self, duration, callback) -> None:
        super().__init__()
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
    def __init__(self) -> None:
        super().__init__(randint(25, 825), -1)
        self.image = py.image.load(Enum.resourcePath.POWER_UP)
        self.image = py.transform.scale(self.image, (80, 80))
        self.gem_react = self.image.get_rect(center=self)

    def move_down(self, speed=1) -> None:
        self.y += speed

    @staticmethod
    def power_up_timeout() -> None:
        global power_up_active
        power_up_active = False
        print("El power-up ha expirado.")
        Bullet.actual_ammo = 1

    @staticmethod
    def activate_power_up(duration=5):
        global power_up_active
        power_up_active = True
        print("Power-up activado.")
        # Iniciar el temporizador para el power-up
        timer = TimerThread(duration=duration, callback=PowerUp.power_up_timeout)
        timer.start()
        Bullet.actual_ammo = 2
        return timer  # Retornar el temporizador para controlarlo si es necesario
