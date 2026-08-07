import sys
import pygame as py
from src.levels.Level_1 import Level_1
from src.services.PlayerService import PlayerService
from src.services.EnemyService import EnemyService
from src.model.Config import PowerUpConfig, HealthConfig, PowerUpMinigunConfig
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
PlayerSVC = PlayerService(GameInstance)
EnemySVC = EnemyService(GameInstance)

GameInstance.services["player_service"] = PlayerSVC
GameInstance.services["enemy_service"] = EnemySVC

running = True
EventGenerator = EventGen(GameInstance)
EventGenerator.SetDelay(5)
EventGenerator.powerUp_CFG = PowerUpConfig(duration=15,
                                           fall_speed=1.5,
                                           rangex=[0, 900],
                                           rangey=0,
                                           damage=10,
                                           probability = 100)
EventGenerator.powerUpMinigun_CFG = PowerUpMinigunConfig(duration=5,
                                           fall_speed=1.5,
                                           rangex=[0, 900],
                                           rangey=0,
                                           fire_speed=7,
                                           probability = 100)
EventGenerator.health_CFG = HealthConfig(fall_speed=1.5,
                                         rangex=[0, 900],
                                         rangey=0,
                                         heal_amount=20,
                                         probability=20)


message_overlay = MessageOverlay(GameInstance)
GameInstance.layout["message_overlay"] = message_overlay

level_loaded = Level_1(GameInstance)
GameInstance.level = level_loaded

mainOverlay = MainOverlay(GameInstance)
GameInstance.layout["main_overlay"] = mainOverlay

# Game loop
while running:
    # Eventos
    for evento in py.event.get():
        if evento.type == py.QUIT:
            running = False
            py.quit()
            exit()
        elif evento.type == py.KEYDOWN and evento.key == py.K_ESCAPE:
            screen.pause = not screen.pause  # Alternar pausa
            if screen.pause:
                EventGenerator.pause_power_timers()   # Pausar contadores de PowerUp
            else:
                EventGenerator.resume_power_timers()  # Reanudar contadores de PowerUp

    # Handler en caso de victoria
    if GameInstance.win:
        screen.win_protocol()
        continue

    # Handler en caso de derrota
    if screen.game_over or player.player_life <= 0:
        screen.game_over_protocol()
        continue

    # Handler en caso de pausa
    if screen.pause:
        screen.pause_protocol()
        continue  # Saltar el resto de actualizaciones del juego

    # Cargador de nivel
    if level_loaded.lock == False:
        level_loaded.lock = True
        level_loaded.init_level()
    

    PlayerSVC.increment_counter()

    # Dibujar fondo
    screen.draw_background()


    # Servicios de movimiento
    PlayerSVC.player_movement()
    EnemySVC.move_enemies()

    # Servicios de disparo
    level_loaded.shoot_manager()

    # Servicio de items empaquetado
    EventGenerator.checker()

    # Detectar colisiones entre enemigos y balas
    EnemySVC.check_collisions(PlayerSVC.bulletsGroup, level_loaded)

    # Animacion de enemigos eliminados
    for chicken in EnemySVC.killed_enemies:
        chicken.draw()

    # Dibujar y limpiar las explosiones (boom) activas
    for boom in EnemySVC.booms[:]:
        boom.draw()
        if boom.finished:
            EnemySVC.booms.remove(boom)

    # Si el jugador puede ser dañado, verifica sus colisiones
    if player.can_damaged:
        player.check_collisions(EnemySVC.enemiesCollection)

    # Si los enemigos llegan al final de la pantalla se acaba
    if EnemySVC.any_enemy_at_bottom():
        screen.game_over = True
        continue

    # Zona de dibujado
    player.draw_player()
    PlayerSVC.draw_bullets(screen=screen.surface)
    EnemySVC.draw_enemies()
    message_overlay.draw(screen.surface)
    mainOverlay.draw(screen.surface)

    # Actualizar pantalla y tasa de fotogramas
    py.display.flip()
    py.time.Clock().tick(FPS)

