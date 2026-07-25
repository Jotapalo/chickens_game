import sys
import pygame as py
from src.model.utils import PowerUp
from src.enum import colorsMap, resEnum 
from src.services.ShootService import ShootService
from src.services.PlayerMovementService import PlayerMovementService
from src.services.EnemyService import EnemyService
from src.model.Player import Player
from src.model.Screen import Screen


# --- Leer argumentos key=value desde línea de comandos ---
def parse_key_value_args():
    """Convierte argv (ej: 'nivel=3 velocidad=5') en un diccionario."""
    return dict(arg.split('=', 1) for arg in sys.argv[1:] if '=' in arg)

args = parse_key_value_args()

# Variables configurables con valores por defecto
LEVEL = int(args.get('level', '1'))
BULLET_SPEED = int(args.get('bullet_speed', '20'))
ENEMY_SPEED = int(args.get('enemy_speed', '1'))
DEBUG = args.get('debug', 'false').lower() == 'true'
FPS = int(args.get('fps', '100'))

print(f"Iniciando Chickens Game - Nivel {LEVEL}")
if DEBUG:
    print(f"Modo DEBUG activado")
    print(f"Set FPS: {FPS}")
# ---------------------------------------------------------


py.init()


# Setup window display info
screen = Screen(width=900, height=600)

# Servicios
ShootSVC = ShootService(BULLET_SPEED)
EnemySVC = EnemyService(screen=screen.surface, enemies_speed=ENEMY_SPEED)

player = Player(screen=screen.surface)

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
            screen.pause = not screen.pause  # Alternar pausa
            if screen.pause:
                timer.pause()
                print("Temporizador en pausa.")
            else:
                timer.resume()
                print("Temporizador reanudado.")

    if screen.pause:
        screen.pause_protocol()
        continue  # Saltar el resto de actualizaciones del juego

    ShootSVC.increment_counter()

    # Dibujar fondo
    screen.draw_background()

    player.PlayerMovementSVC.player_movement(screen=screen.surface)
    EnemySVC.move_enemies()

    ShootSVC.shoot_checker(player=player)

    # Zona de dibujado
    player.draw_player()
    ShootSVC.draw_bullets(screen=screen.surface)
    EnemySVC.draw_enemies()

    # Detectar y gestionar colisiones entre balas y enemigos
    colisiones = EnemySVC.check_collisions(ShootSVC.bulletsList)
    if colisiones > 0:
        if DEBUG:
            print(f"Colisiones detectadas en este frame: {colisiones}")

    # Actualizar pantalla y tasa de fotogramas
    py.display.flip()
    py.time.Clock().tick(FPS)
