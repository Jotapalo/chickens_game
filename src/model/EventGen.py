from __future__ import annotations
import time
from src.model.PowerUp import PowerUp
from src.model.PowerUp_minigun import PowerUp_minigun
from src.model.Health import Health
from src.model.Config import PowerUpConfig, HealthConfig, PowerUpMinigunConfig
from src.model.Meteor import Meteor
from random import randint
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.model.Game import Game

class EventGen:
    """Encargado de la generacion de eventos dentro del bucle del principal del juego
    """
    def __init__(self, game_context: Game) -> None:
        self.powerUps: list[PowerUp | PowerUp_minigun] = list()
        self.healths: list[Health] = list()
        self.meteors: list[Meteor] = list()
        self.screen = game_context.mainScreen
        self.player = game_context.entities.get("player")
        self.player_service = game_context.player_service

        self.powerUp_CFG = PowerUpConfig()
        self.health_CFG = HealthConfig()
        self.powerUpMinigun_CFG = PowerUpMinigunConfig()

        self.powerUp_delay = 5  # Intervalo (segundos) entre cada intento de spawneo

        # Temporizadores acumulativos por tipo. Cada uno se reinicia tras cada
        # intento de spawneo (sin importar si la probabilidad fue favorable o no).
        self.powerUp_timer = 0.0
        self.powerUpMinigun_timer = 0.0
        self.health_timer = 0.0
        self.meteor_timer = 0.0
        self.planet_timer = 0.0

        # Marca de tiempo del último frame para calcular el delta real
        self._last_time = time.perf_counter()


    def SetDelay(self, delay: int):
        self.powerUp_delay = delay

    def pause_power_timers(self) -> None:
        """Pausa todos los temporizadores de PowerUp activos."""
        if PowerUp.timer is not None:
            PowerUp.timer.pause()
        if PowerUp_minigun.timer is not None:
            PowerUp_minigun.timer.pause()

    def resume_power_timers(self) -> None:
        """Reanuda todos los temporizadores de PowerUp activos."""
        if PowerUp.timer is not None:
            PowerUp.timer.resume()
        if PowerUp_minigun.timer is not None:
            PowerUp_minigun.timer.resume()


    def _try_spawn(self):
        """Comprueba la probabilidad de spawneo para cada tipo, cada
        self.powerUp_delay segundos. Si el rand no supera la probabilidad
        (resultado negativo), espera a la siguiente iteración para volver
        a preguntar."""
        # Power-up de daño
        if self.powerUp_timer >= self.powerUp_delay:
            self.powerUp_timer = 0.0  # se reinicia SIEMPRE tras el intento
            if randint(0, 100) <= self.powerUp_CFG.probability:
                new_powerup = PowerUp(self.powerUp_CFG)
                new_powerup.player_service = self.player_service
                self.powerUps.append(new_powerup)

        # Power-up minigun
        if self.powerUpMinigun_timer >= self.powerUp_delay:
            self.powerUpMinigun_timer = 0.0  # se reinicia SIEMPRE tras el intento
            if randint(0, 100) <= self.powerUpMinigun_CFG.probability:
                new_powerup = PowerUp_minigun(self.powerUpMinigun_CFG)
                new_powerup.player_service = self.player_service
                self.powerUps.append(new_powerup)

        # Power-up de vida (Health)
        if self.health_timer >= self.powerUp_delay:
            self.health_timer = 0.0  # se reinicia SIEMPRE tras el intento
            if randint(0, 100) <= self.health_CFG.probability:
                new_health = Health(self.health_CFG)
                self.healths.append(new_health)

        # Generacion de meteoritos
        if self.meteor_timer >= 7:
            self.meteor_timer = 0.0
            meteor = Meteor(self.screen)
            self.meteors.append(meteor)

        if self.planet_timer >= 10:
            self.planet_timer = 0.0
            self.screen.summon_planet(["saturn", "planet_1", "planet_2"][randint(0,2)],
                                        randint(50, 100) if randint(0, 1) == 1 else randint(800, 850),
                                        -300)

    def checker(self):
        # Calcular el delta de tiempo real transcurrido desde el último frame
        now = time.perf_counter()
        delta = now - self._last_time
        self._last_time = now

        # Acumular el tiempo transcurrido en cada temporizador
        self.powerUp_timer += delta
        self.powerUpMinigun_timer += delta
        self.health_timer += delta
        self.meteor_timer += delta
        self.planet_timer += delta

        # Intentar spawneo según probabilidad cada powerUp_delay segundos
        self._try_spawn()

        # Actualizar y dibujar los power-ups activos en pantalla.
        # Cada clase de power-up gestiona su propio timer de clase (el último
        # creado), por lo que al recolectar otro del mismo tipo mientras el
        # timer sigue activo, se EXTENDERÁ su duración automáticamente.
        # Se itera sobre una copia para poder eliminar de la lista con seguridad.
        for power_up in self.powerUps[:]:
            if power_up.update_and_draw(screen=self.screen.surface, player=self.player):
                power_up.activate_power_up()
                power_up.kill()
                self.powerUps.remove(power_up)
            elif power_up.rect.y >= 600:  # Salió de pantalla
                power_up.kill()
                self.powerUps.remove(power_up)


        # Actualizar y dibujar los healths activos en pantalla
        for health in self.healths[:]:
            if health.update_and_draw(screen=self.screen.surface, player=self.player):
                health.heal_player(self.player)
                health.kill()
                self.healths.remove(health)
            elif health.rect.y >= 600:  # Salió de pantalla
                health.kill()
                self.healths.remove(health)

        # Actualizar y mover los meteoritos. draw_and_move devuelve True cuando
        # el meteorito salió por completo de la pantalla o golpeó al jugador;
        # entonces lo eliminamos de la lista para liberar la referencia.
        for meteor in self.meteors[:]:
            withtout_limits = meteor.draw_and_move(self.screen.surface, player=self.player)
            if withtout_limits:
                self.meteors.remove(meteor)
