import sys
import pygame as py
from src.model.EventGen import EventGen
from src.levels.Level_1 import Level_1
from src.services.ShootService import ShootService
from src.services.PlayerMovementService import PlayerMovementService
from src.services.EnemyService import EnemyService
from src.config.PowerUpConfig import PowerUpConfig
from src.model.Player import Player
from src.model.Screen import Screen
from src.model.MessageOverlay import MessageOverlay


# --- Leer argumentos key=value desde línea de comandos ---
def parse_key_value_args():
    """Convierte argv (ej: 'nivel=3 velocidad=5') en un diccionario."""
    return dict(arg.split('=', 1) for arg in sys.argv[1:] if '=' in arg)

args = parse_key_value_args()

# Variables configurables con valores por defecto
LEVEL = int(args.get('level', '1'))
BULLET_SPEED = int(args.get('bullet_speed', '20'))
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
player = Player(screen=screen.surface)

# Servicios
ShootSVC = ShootService(BULLET_SPEED, player)
EnemySVC = EnemyService(screen=screen.surface)


# Servicio de movimiento del jugador
player.suscribeMovementService(PlayerMovementService(player))

running = True
EventGenerator = EventGen(screen=screen, player=player)
EventGenerator.powerUp_CFG = PowerUpConfig(duration=15,
                                           fall_speed=2,
                                           rangex=[0, 900],
                                           rangey=20,
                                           damage=10)
EventGenerator.SetConfigPowerUp(5)

message_overlay = MessageOverlay(width=screen.width, height=screen.height)
level_loaded = Level_1(EnemySVC, ShootSVC, screen=screen, message_overlay=message_overlay)

# Game loop
while running:
    for evento in py.event.get():
        if evento.type == py.QUIT:
            running = False
            py.quit()
            exit()
        elif evento.type == py.KEYDOWN and evento.key == py.K_ESCAPE:
            screen.pause = not screen.pause  # Alternar pausa
            if screen.pause:
                print("Temporizador en pausa.")
            else:
                print("Temporizador reanudado.")

    if screen.pause:
        screen.pause_protocol()
        continue  # Saltar el resto de actualizaciones del juego

    if level_loaded.lock == False:
        level_loaded.lock = True
        level_loaded.init_level()
    

    ShootSVC.increment_counter()

    # Dibujar fondo
    screen.draw_background()

    player.PlayerMovementSVC.player_movement(screen=screen.surface)
    EnemySVC.move_enemies()
    level_loaded.shoot_manager()

    EventGenerator.checker()

    # Zona de dibujado
    player.draw_player()
    ShootSVC.draw_bullets(screen=screen.surface)
    EnemySVC.draw_enemies()
    message_overlay.draw(screen.surface)

    # Detectar
    colisiones = EnemySVC.check_collisions(ShootSVC.bulletsGroup)
    if colisiones > 0:
        if DEBUG:
            print(f"Colisiones detectadas en este frame: {colisiones}")

    # Actualizar pantalla y tasa de fotogramas
    py.display.flip()
    py.time.Clock().tick(FPS)
