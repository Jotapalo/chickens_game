import pygame as py
from utils import Player, PowerUp, Bullet

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

player = Player()
contador_bala = 0
list_of_bullets = []
list_of_power_ups = []
speed = 10
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
        list_of_bullets.append(Bullet(player.x, player.y, data=Bullet.actual_ammo))

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
