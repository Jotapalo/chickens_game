import threading
from random import randint
from typing import Any
from src.model.Enemy import Enemy
from pygame import Surface


class EnemyService:
    def __init__(self, screen, enemies_speed) -> None:
        self.screen = screen
        self.screen: Surface
        self.enemiesCollection: list[Enemy] = []
        self._lock = threading.Lock()
        self.enemies_speed = enemies_speed

    def new_enemy(self, posx, posy):
        return Enemy(self.screen, posx, posy)

    def draw_enemies(self) -> None:
        """Dibuja todos los enemigos en la pantalla. 
        Debe llamarse desde el game loop principal (síncrono)."""
        with self._lock:
            for enemy in self.enemiesCollection:
                enemy: Enemy
                enemy.draw_enemy()

    def test_spawn_enemies(self) -> None: # Test de spawneo de enemigos temporal
        """Genera 6 enemigos en posiciones aleatorias (síncrono)."""
        coox = self.gen_coordinates_x(6, self.screen.get_width(), (25,75))

        for i in range(6):
            ACT_enemy = self.new_enemy(
                coox[i],
                randint(0, 10)
            )
            with self._lock:
                self.enemiesCollection.append(ACT_enemy)

    def move_enemies(self) -> None: # Simulacion temporal de fisicas
        for enemy in self.enemiesCollection:
            enemy.y += self.enemies_speed
            
    def check_collisions(self, bulletsList: list) -> int:
        """
        Verifica colisiones entre todos los enemigos y todas las balas.
        Cuando una bala colisiona con un enemigo, ambos son eliminados.
        
        Args:
            bulletsList: Lista de objetos Bullet a verificar
            
        Returns:
            int: Número de colisiones detectadas en este ciclo
        """
        collisions = 0
        with self._lock:
            # Iterar sobre copias para poder modificar las listas originales
            for enemy in self.enemiesCollection[:]:
                for bullet in bulletsList[:]:
                    if enemy.enemy_react.colliderect(bullet.bullet_react):
                        self.enemiesCollection.remove(enemy)
                        bulletsList.remove(bullet)
                        collisions += 1
                        break  # Salir del loop de balas, este enemigo ya no existe
        return collisions

    def gen_coordinates_x(self, num_enemies: int, screen_axis_size: int, range_coefficient: tuple[int, int]) -> list[int]:
        """Genera una lista de coordenadas con configuraciones personalizadas para la generacion de enemigos bajo
ciertos parametros, genera posiciones de acuerdo a columnas imaginarias sobre un eje especifico, con posibilidad
generar un patron de aleatoriedad entre posiciones de enemigos.

        Args:
            num_enemies (int): numero de coordenadas a generar
            screen_axis_size (int): numero en pixeles de el eje al que se quiere generar el patron
            range_coefficient (tuple[int, int]): coeficiente de aleatoriedad

        Returns:
            list: lista ordenada de coordenadas para posicionar enemigos.
        """        
        return [
            pos - randint(*(range_coefficient) if range_coefficient != None else 0) for pos in 
            [col*int(screen_axis_size/num_enemies) for col in 
             range(1,num_enemies+1)]
            ]