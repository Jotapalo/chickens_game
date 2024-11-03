import pygame as py
from random import randint as numero_aleatorio
import threading
import time

py.init()

# Setup window display info
width, height = 900, 600
screen = py.display.set_mode((width, height))
py.display.set_caption("Juego de Pausa")

# Load background image
image = py.image.load("P.JPG")

# Set pause
pause = False
font = py.font.Font(None, 36)
pause_text = font.render("Juego en Pausa", True, (255, 0, 0))
WHITE = (255, 255, 255)


class Player(py.Vector2):
    def __init__(self):
        super().__init__(screen.get_width() / 2, screen.get_height() / 2)
        self.image_player = py.image.load("pedorro.PNG")
        self.image_player = py.transform.scale(self.image_player, (70, 70))
        self.player_react = self.image_player.get_rect(center=self)


class Bullet(py.Vector2):
    def __init__(self, pos_x, pos_y, data):
        super().__init__(pos_x, pos_y)
        self.image = py.image.load(self.get_character(data))
        self.image = py.transform.scale(self.image, (40, 40))
        self.bullet_react = self.image.get_rect(center=self)

    def move_up(self, speed=5):
        self.y -= speed

    def get_character(self, data):
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
        global power_up_active, actual_ammo
        power_up_active = False
        print("El power-up ha expirado.")
        actual_ammo = 1

    @staticmethod
    def activate_power_up(duration=5):
        global power_up_active, actual_ammo
        power_up_active = True
        print("Power-up activado.")
        # Iniciar el temporizador para el power-up
        timer = TimerThread(duration=duration, callback=PowerUp.power_up_timeout)
        timer.start()
        actual_ammo = 2
        return timer  # Retornar el temporizador para controlarlo si es necesario


player = Player()
contador_bala = 0
list_of_bullets = []
list_of_power_ups = []
speed = 10
actual_ammo = 1
running = True
timer_paused = False

# Activar temporizador para power-up
timer = PowerUp.activate_power_up(10)

# Game loop
while running:
    for evento in py.event.get():
        if evento.type == py.QUIT:
            running = False
            timer.stop()
            py.quit()
            exit()
        elif evento.type == py.KEYDOWN and evento.key == py.K_ESCAPE:
            pause = not pause  # Alternar pausa
            if pause:
                timer.pause()
                print("Temporizador en pausa.")
            else:
                timer.resume()
                print("Temporizador reanudado.")

    if pause:
        # Si el juego está en pausa, mostrar el mensaje de pausa
        screen.fill(WHITE)
        screen.blit(pause_text, (width // 2 - pause_text.get_width() // 2, height // 2 - pause_text.get_height() // 2))
        py.display.flip()
        py.time.Clock().tick(30)  # Reducir la velocidad de actualización durante la pausa
        continue  # Saltar el resto de actualizaciones del juego

    # Incremento del contador de balas
    contador_bala += 1

    # Dibujar fondo
    screen.blit(py.transform.scale(image, (900, 600)), (0, 0))

    # Movimiento del jugador
    keys = py.key.get_pressed()
    if keys[py.K_RIGHT] or keys[py.K_d]:
        player.x += speed
    if keys[py.K_LEFT] or keys[py.K_a]:
        player.x -= speed
    if keys[py.K_UP] or keys[py.K_w]:
        player.y -= speed
    if keys[py.K_DOWN] or keys[py.K_s]:
        player.y += speed

    # Limitar el movimiento del jugador a la pantalla
    player.x = max(player.player_react.width // 2, min(player.x, width - player.player_react.width // 2))
    player.y = max(player.player_react.width // 2, min(player.y, height - player.player_react.width // 2))

    # Actualizar y dibujar al jugador
    player.player_react.center = (player.x, player.y)
    screen.blit(player.image_player, player.player_react)

    # Disparo de balas cada 20 frames
    if contador_bala >= 20:
        contador_bala = 0
        list_of_bullets.append(Bullet(player.x, player.y, data=actual_ammo))

    # Actualizar y dibujar cada proyectil
    for bullet in list_of_bullets[:]:
        bullet.move_up(speed=20)
        bullet.bullet_react.center = (bullet.x, bullet.y)
        screen.blit(bullet.image, bullet.bullet_react)

        if bullet.y < 0:
            list_of_bullets.remove(bullet)

    # Actualizar pantalla y tasa de fotogramas
    py.display.flip()
    py.time.Clock().tick(60)
