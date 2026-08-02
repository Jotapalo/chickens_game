import threading
import time
from typing import TYPE_CHECKING
from src.config.EnemyConfig import EnemyConfig
from src.model.Game import Game
from src.levels.Level import Level


if TYPE_CHECKING:
    from src.services.EnemyService import EnemyService
    from src.services.ShootService import ShootService

class Level_1(Level):
    """El nivel 1 consta de 3 stages, primero 3 enemigos con 5 de vida,
      segundo 5 enemigos con 10 de vida y tercero un enemigo con 30 de vida"""
    def __init__(self, game_context: Game):
        self.lock = False
        self.enemySVC: EnemyService = game_context.services["enemy_service"]
        self.shootSVC: ShootService = game_context.services["shoot_service"]
        self.screen = game_context.mainScreen
        self.message_overlay = game_context.layout["message_overlay"]
        self.game = game_context
        
        self.enemyInfo = [
            (3, EnemyConfig(life=5), "Wave 2"),
            (5, EnemyConfig(life=10), "Boss"),
            (1, EnemyConfig(life=30, size=(200,200)), ""),
        ]
        self.waves_delay = 2
        self.score = 0

    def init_level(self):
        t = threading.Thread(target=self.run, daemon=True)
        t.start()

    def run(self):
        for iterator in range(len(self.enemyInfo)):
            self.enemySVC.test_spawn_enemies(*(self.enemyInfo[iterator]))
            self.wait_for_killed_enemies(0 if iterator == len(self.enemyInfo)-1 else self.waves_delay)
            if iterator < len(self.enemyInfo) - 1:
                self.message_overlay.show(self.enemyInfo[iterator][2], duration=2)

        self.game.win = True

    def wait_for_killed_enemies(self, delay: int=1):
        while len(self.enemySVC.enemiesCollection) != 0:
            time.sleep(1)
        time.sleep(delay)

    def shoot_manager(self):
        self.shootSVC.shoot_checker()
        

