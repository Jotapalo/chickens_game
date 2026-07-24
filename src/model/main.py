import pygame as py
from src.model.utils import PowerUp
from src.enum import colorsMap, resEnum 
from src.services.ShootService import ShootService
from src.services.PlayerMovementService import PlayerMovementService
from src.services.EnemyService import EnemyService
from src.model.Player import Player


py.init()


# Setup window display info
width, height = 900, 600
screen = py.display.set_mode((width, height))
py.display.set_caption("Chickens Game")

# Servicios
ShootSVC = ShootService()
EnemySVC = EnemyService(screen=screen)

# Load background image
font_image = py.image.load(resEnum.FONT)

# Set pause
pause = False
font = py.font.Font(None, 36)
pause_text = font.render("Juego en Pausa", True, colorsMap.RED)

player = Player(screen=screen)

# Servicio de movimiento del jugador
player.suscribeMovementService(PlayerMovementService(player))

running = True

# Activar temporizador para power-up
timer = PowerUp.activate_power_up(10)

EnemySVC.test_spawn_enemies()

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
        screen.fill(colorsMap.WHITE)
        screen.blit(pause_text, (width // 2 - pause_text.get_width() // 2, height // 2 - pause_text.get_height() // 2))
        py.display.flip()
        py.time.Clock().tick(30)  # Reducir la velocidad de actualización durante la pausa
        continue  # Saltar el resto de actualizaciones del juego

    ShootSVC.increment_counter()

    # Dibujar fondo
    screen.blit(py.transform.scale(font_image, (900, 600)), (0, 0))

    player.PlayerMovementSVC.player_movement(screen=screen)
    EnemySVC.move_enemies()

    ShootSVC.shoot_checker(player=player)

    # Zona de dibujado
    player.draw_player()
    ShootSVC.draw_bullets(screen=screen)
    EnemySVC.draw_enemies()

    # Actualizar pantalla y tasa de fotogramas
    py.display.flip()
    py.time.Clock().tick(100)

