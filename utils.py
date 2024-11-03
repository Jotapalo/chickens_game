import pygame as py
import threading
import time
from random import randint as numero_aleatorio

power_up_active = False


class Player(py.Vector2):
    def __init__(self):
        from juego import screen
        super().__init__(screen.get_width() / 2, screen.get_height() / 2)
        self.image_player = py.image.load("pedorro.PNG")
        self.image_player = py.transform.scale(self.image_player, (70, 70))
        self.player_react = self.image_player.get_rect(center=self)


class Bullet(py.Vector2):
    actual_ammo = 1

    def __init__(self, pos_x, pos_y, data):
        super().__init__(pos_x, pos_y)
        self.image = py.image.load(self.get_character(data))
        self.image = py.transform.scale(self.image, (40, 40))
        self.bullet_react = self.image.get_rect(center=self)

    def move_up(self, speed=5):
        self.y -= speed

    @staticmethod
    def get_character(data):
        if data == 1:
            return "bullet_1.png"
        elif data == 2:
            return "bullet_2.png"


class TimerThread(threading.Thread):
    def __init__(self, duration, callback):
        super().__init__()
        self.duration = duration
        self.callback = callback
        self._pause_event = threading.Event()
        self._stop_event = threading.Event()
        self.remaining_time = duration

    def run(self):
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

    def pause(self):
        self._pause_event.set()

    def resume(self):
        self._pause_event.clear()

    def stop(self):
        self._stop_event.set()


class PowerUp(py.Vector2):
    def __init__(self):
        super().__init__(numero_aleatorio(25, 825), -1)
        self.image = py.image.load("power_up.png")
        self.image = py.transform.scale(self.image, (80, 80))
        self.gem_react = self.image.get_rect(center=self)

    def move_down(self, speed=1):
        self.y += speed

    @staticmethod
    def power_up_timeout():
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
