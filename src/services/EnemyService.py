import threading
from random import randint
from src.config.EnemyConfig import EnemyConfig
from src.model.Enemy import Enemy
from pygame import Surface


class EnemyService:
    def __init__(self, screen) -> None:
        self.screen = screen
        self.screen: Surface
        self.enemiesCollection: list[Enemy] = []
        self._lock = threading.Lock()

    def new_enemy(self, posx, posy, enemy_config: EnemyConfig):
        return Enemy(self.screen, posx, posy, enemy_config)

    def draw_enemies(self) -> None:
        """Dibuja todos los enemigos en la pantalla. 
        Debe llamarse desde el game loop principal (síncrono)."""
        with self._lock:
            for enemy in self.enemiesCollection:
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
                self.enemiesCollection.append(ACT_enemy)

    def move_enemies(self) -> None: # Simulacion temporal de fisicas
        for enemy in self.enemiesCollection:
            enemy.y += enemy.speed
            
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