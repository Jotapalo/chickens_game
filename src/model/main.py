import sys
import pygame as py
from src.levels.Level_1 import Level_1
from src.services.ShootService import ShootService
from src.services.PlayerMovementService import PlayerMovementService
from src.services.EnemyService import EnemyService
from src.model.PowerUp import PowerUp
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
powerUps: list[PowerUp] = list()

# Servicios
ShootSVC = ShootService(BULLET_SPEED, player)
EnemySVC = EnemyService(screen=screen.surface)


# Servicio de movimiento del jugador
player.suscribeMovementService(PlayerMovementService(player))

running = True

powerUps.append(PowerUp())

level_loaded = Level_1(EnemySVC, ShootSVC)

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

    for power_up in powerUps:
        if power_up.update_and_draw(screen=screen.surface, player=player):
            power_up.activate_power_up()
            powerUps.remove(power_up)

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
