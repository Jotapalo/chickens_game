from __future__ import annotations
import threading
from random import randint
import pygame as py
from typing import TYPE_CHECKING

from src.config.EnemyConfig import EnemyConfig
from src.model.Enemy import Enemy
from pygame import Surface

if TYPE_CHECKING:
    from src.model.Game import Game

class EnemyService:
    def __init__(self, game_context: Game) -> None:
        self.screen: Surface = game_context.mainScreen.surface
        self._enemiesGroup = py.sprite.Group()
        self._lock = threading.Lock()

    @property
    def enemiesCollection(self):
        """Mantiene compatibilidad con código que usa enemiesCollection."""
        return list(self._enemiesGroup.sprites())

    def new_enemy(self, posx, posy, enemy_config: EnemyConfig):
        return Enemy(self.screen, posx, posy, enemy_config)

    def draw_enemies(self) -> None:
        """Dibuja todos los enemigos en la pantalla. 
        Debe llamarse desde el game loop principal (síncrono)."""
        with self._lock:
            for enemy in self._enemiesGroup.sprites():
                enemy: Enemy
                enemy.draw_enemy()

    def test_spawn_enemies(self, num_enemies, 
                           enemy_CFG: EnemyConfig = EnemyConfig(),
                           CF_range: tuple[int, int] = (0, 100)) -> None: # Test de spawneo de enemigos temporal
        """Genera enemigos en posiciones aleatorias (síncrono)."""
        coox = self.gen_coordinates_x(num_enemies, self.screen.get_width(), CF_range)

        for i in range(num_enemies):
            ACT_enemy = self.new_enemy(
                coox[i],
                randint(0, 10),
                enemy_config=enemy_CFG
            )
            with self._lock:
                self._enemiesGroup.add(ACT_enemy)

    def move_enemies(self) -> None: # Simulacion temporal de fisicas
        for enemy in self._enemiesGroup.sprites():
            enemy: Enemy
            enemy.y += enemy.speed

    def check_bottom_boundary(self) -> list[Enemy]:
        """Detecta qué enemigos han tocado el borde inferior de la pantalla.

        Un enemigo se considera "en el borde inferior" cuando el borde inferior
        de su rectángulo (rect.bottom) alcanza o supera la altura de la pantalla.

        Returns:
            list[Enemy]: Lista de enemigos que están tocando el borde inferior.
        """
        bottom_edge = self.screen.get_height()
        with self._lock:
            return [
                enemy for enemy in self._enemiesGroup.sprites()
                if enemy.rect.bottom >= bottom_edge
            ]

    def any_enemy_at_bottom(self) -> bool:
        """Indica si al menos un enemigo ha tocado el borde inferior de la pantalla.

        Returns:
            bool: True si existe algún enemigo tocando el borde inferior.
        """
        return len(self.check_bottom_boundary()) > 0

            
    def check_collisions(self, bullets_group: py.sprite.Group, level) -> int:
        """
        Verifica colisiones entre todos los enemigos y todas las balas.
        Cuando una bala colisiona con un enemigo, ambos son eliminados.
        Las balas colisionadas se eliminan automáticamente del grupo gracias a dokill2=True.
        
        Args:
            bullets_group: Grupo de pygame con objetos Bullet a verificar
            
        Returns:
            int: Número de colisiones detectadas en este ciclo
        """
        collisions = 0
        with self._lock:
            # groupcollide: dokill1=False (no matar enemigos automáticamente), dokill2=True (matar balas del grupo real)
            hits = py.sprite.groupcollide(self._enemiesGroup, bullets_group, False, True)
            for enemy, bullets in hits.items():
                for bullet in bullets: # Colision bala-enemigo detectada
                    enemy.life -= bullet.damage
                    enemy.lifeBar.config_life(enemy.life, enemy.max_life)
                    collisions += 1
                    level.score += bullet.damage
                    
                if enemy.life <= 0:
                    enemy.kill()
                    level.score += 10  # VALOR TEMPORAL, modificar con enemy.xp que se agregara proximamente
        return collisions

    def gen_coordinates_x(self, num_enemies: int, screen_axis_size: int, range_coefficient: tuple[int, int] = 0) -> list[int]:
        """Genera una lista de coordenadas con configuraciones personalizadas para la generacion de enemigos bajo
ciertos parametros, genera posiciones de acuerdo a columnas imaginarias sobre un eje especifico, con posibilidad
generar un patron de aleatoriedad entre posiciones de enemigos.

        Args:
            num_enemies (int): numero de coordenadas a generar
            screen_axis_size (int): numero en pixeles de el eje al que se quiere generar el patron
            range_coefficient (tuple[int, int]): coeficiente de aleatoriedad en porcentaje [ [0, 50],[50, 100] ]

        Returns:
            list: lista ordenada de coordenadas para posicionar enemigos.
        """        
        # variables de contabilizacion 
        size_per_col = screen_axis_size/num_enemies
        # col_end_points = list()
        col_start_points = list()
        final_coo = list()

        # Definir donde empieza cada columna en pixeles
        for col in range(1,num_enemies+1):
            # col_end_points.append(col*int(size_per_col))
            col_start_points.append(col*int(size_per_col) - size_per_col)

        # Agregar el coeficiente de cambio con un aleatorizamiento en el rango especificado
        for i in range(len(col_start_points)):
            percentage = randint(range_coefficient[0], range_coefficient[1]) / 100 if range_coefficient == tuple else 0.5
            final_coo.append(col_start_points[i] + 
                             size_per_col * percentage
                             )


        return final_coo
