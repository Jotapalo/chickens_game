import sys
import pygame as py
from src.levels.Level_1 import Level_1
from src.services.ShootService import ShootService
from src.services.PlayerMovementService import PlayerMovementService
from src.services.EnemyService import EnemyService
from src.config.PowerUpConfig import PowerUpConfig
from src.model.Player import Player
from src.model.Screen import Screen
from src.model.MessageOverlay import MessageOverlay
from src.model.Game import Game
from src.model.MainOverlay import MainOverlay
from src.model.EventGen import EventGen


GameInstance = Game()

# --- Leer argumentos key=value desde línea de comandos ---
def parse_key_value_args() -> dict[str, str]:
    """Convierte argv (ej: 'nivel=3 velocidad=5') en un diccionario."""
    return dict(arg.split('=', 1) for arg in sys.argv[1:] if '=' in arg)

args = parse_key_value_args()

parameters = {
    'level': int(args.get('level', '1')),
    "bullet_speed": int(args.get('bullet_speed', '20')),
    "debug": args.get('debug', 'false').lower() == 'true',
    "fps": int(args.get('fps', '100'))
}

for k, v in parameters.items():
    GameInstance.parameters[k] = v

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

GameInstance.mainScreen = screen
GameInstance.entities["player"] = player

# Servicios
ShootSVC = ShootService(GameInstance)
EnemySVC = EnemyService(GameInstance)

GameInstance.services["shoot_service"] = ShootSVC
GameInstance.services["enemy_service"] = EnemySVC


# Servicio de movimiento del jugador
player.suscribeMovementService(PlayerMovementService(player))

running = True
EventGenerator = EventGen(GameInstance)
EventGenerator.powerUp_CFG = PowerUpConfig(duration=15,
                                           fall_speed=2,
                                           rangex=[0, 900],
                                           rangey=20,
                                           damage=10,
                                           probability = 80)
EventGenerator.SetConfigPowerUp(5)

message_overlay = MessageOverlay(GameInstance)
GameInstance.layout["message_overlay"] = message_overlay

level_loaded = Level_1(GameInstance)
GameInstance.level = level_loaded

mainOverlay = MainOverlay(GameInstance)
GameInstance.layout["main_overlay"] = mainOverlay


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


    # Servicios
    player.PlayerMovementSVC.player_movement(screen=screen.surface)
    EnemySVC.move_enemies()
    level_loaded.shoot_manager()
    EventGenerator.checker()


    # Detectar
    bullet_collide = EnemySVC.check_collisions(ShootSVC.bulletsGroup, level_loaded)
    if bullet_collide > 0:
        if DEBUG:
            print(f"Colisiones detectadas en este frame: {bullet_collide}")

    # Zona de dibujado
    player.draw_player()
    ShootSVC.draw_bullets(screen=screen.surface)
    EnemySVC.draw_enemies()
    message_overlay.draw(screen.surface)
    mainOverlay.draw(screen.surface)

    # Actualizar pantalla y tasa de fotogramas
    py.display.flip()
    py.time.Clock().tick(FPS)
