import threading
import time
from typing import TYPE_CHECKING
from src.config.EnemyConfig import EnemyConfig
from src.model.Game import Game
from src.levels.Level import Level


if TYPE_CHECKING:
    from src.services.EnemyService import EnemyService
    from src.services.PlayerService import PlayerService

class Level_1(Level):
    """El nivel 1 consta de 3 stages, primero 3 enemigos con 5 de vida,
      segundo 5 enemigos con 10 de vida y tercero un enemigo con 30 de vida"""
    def __init__(self, game_context: Game):
        self.lock = False
        self.enemySVC: EnemyService = game_context.services["enemy_service"]
        self.playerSVC: PlayerService = game_context.services["player_service"]
        self.screen = game_context.mainScreen
        self.message_overlay = game_context.layout["message_overlay"]
        self.game = game_context
        
        self.enemyInfo = [
            (3, EnemyConfig(life=5)),
            (5, EnemyConfig(life=10)),
            (1, EnemyConfig(life=500, size=(200,200)))
        ]
        
        self.waves_delay = 2
        self.score = 0

    def init_level(self):
        t = threading.Thread(target=self.run, daemon=True)
        t.start()

    def run(self):
        interview_msg = ["Wave 1", "Wave 2", "Boss"]
        msg_id = 0

        for iterator in range(len(self.enemyInfo)):
            self.message_overlay.show(interview_msg[iterator], duration=2)
            self.enemySVC.test_spawn_enemies(self.enemyInfo[iterator][0], self.enemyInfo[iterator][1])
            self.wait_for_killed_enemies(0 if iterator == len(self.enemyInfo)-1 else self.waves_delay)

        self.game.win = True

    def wait_for_killed_enemies(self, delay: int=1):
        while len(self.enemySVC.enemiesCollection) != 0:
            time.sleep(1)
        time.sleep(delay)

    def shoot_manager(self):
        self.playerSVC.shoot_checker()
        

