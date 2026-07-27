import threading
import time
from src.model.Screen import Screen
from src.model.MessageOverlay import MessageOverlay
from src.config.EnemyConfig import EnemyConfig
from src.services.EnemyService import EnemyService
from src.services.ShootService import ShootService
import pygame as py

class Level_1:
    """El nivel 1 consta de 3 stages, primero 3 enemigos con 5 de vida,
      segundo 5 enemigos con 10 de vida y tercero un enemigo con 30 de vida"""
    def __init__(self, enemySVC, shootSVC, screen: Screen, message_overlay: MessageOverlay):
        self.lock = False
        self.enemySVC: EnemyService = enemySVC
        self.shootSVC: ShootService = shootSVC
        self.screen = screen
        self.message_overlay = message_overlay
        self.enemyInfo = [
            (3, EnemyConfig(life=5), "Wave 2"),
            (5, EnemyConfig(life=10), "Boss"),
            (1, EnemyConfig(life=30, size=(200,200)), ""),
        ]
        self.waves_delay = 0.1

    def init_level(self):
        t = threading.Thread(target=self.run, daemon=True)
        t.start()

    def run(self):
        for iterator in range(len(self.enemyInfo)):
            self.enemySVC.test_spawn_enemies(*(self.enemyInfo[iterator]))
            self.wait_for_killed_enemies(0 if iterator == len(self.enemyInfo)-1 else self.waves_delay)
            if iterator < len(self.enemyInfo) - 1:
                self.message_overlay.show(self.enemyInfo[iterator][2], duration=2)

    def wait_for_killed_enemies(self, delay: int=1):
        while len(self.enemySVC.enemiesCollection) != 0:
            time.sleep(1)
        time.sleep(delay)

    def shoot_manager(self):
        self.shootSVC.shoot_checker()
        

