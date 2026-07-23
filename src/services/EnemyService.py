import threading
from random import randint
from src.model.Enemy import Enemy
from pygame import Surface


class EnemyService:
    def __init__(self, screen):
        self.screen = screen
        self.screen: Surface
        self.enemiesCollection = []
        self._lock = threading.Lock()

    def new_enemy(self, posx, poy):
        return Enemy(self.screen, posx, poy)

    def draw_enemies(self):
        """Dibuja todos los enemigos en la pantalla. 
        Debe llamarse desde el game loop principal (síncrono)."""
        with self._lock:
            for enemy in self.enemiesCollection:
                enemy: Enemy
                enemy.draw_enemy()

    def test_spawn_enemies(self):
        """Genera 6 enemigos en posiciones aleatorias (síncrono)."""
        for i in range(6):
            ACT_enemy = self.new_enemy(
                randint(0, self.screen.get_width()),
                randint(0, self.screen.get_height())
            )
            with self._lock:
                self.enemiesCollection.append(ACT_enemy)
