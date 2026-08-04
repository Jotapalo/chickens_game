from __future__ import annotations
import time
from src.model.PowerUp import PowerUp
from src.model.Health import Health
from src.model.TimerThread import TimerThread
from src.config.PowerUpConfig import PowerUpConfig
from src.config.HealthConfig import HealthConfig
import threading
from random import randint
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.model.Game import Game

class EventGen:
    """Encargado de la generacion de eventos dentro del bucle del principal del juego
    """    
    def __init__(self, game_context: Game) -> None:
        self.init_time = time.perf_counter()
        self.powerUps: list[PowerUp] = list()
        self.healths: list[Health] = list()
        self.screen = game_context.mainScreen
        self.player = game_context.entities.get("player")
        self.player_service = game_context.services.get("player_service")
        self.powerUp_CFG = PowerUpConfig()
        self.health_CFG = HealthConfig()

        self.powerUpTrigger = False
        self.healthTrigger = False
        self.active_timers: list[TimerThread] = []

    def SetConfigPowerUp(self, delay: int):
        self.powerUp_delay = delay

    def setter_powerUpTrigger(self):
        time.sleep(2)
        self.powerUpTrigger = False

    def setter_healthTrigger(self):
        time.sleep(2)
        self.healthTrigger = False

    def pause_power_timers(self) -> None:
        """Pausa todos los temporizadores de PowerUp activos."""
        for timer in self.active_timers:
            timer.pause()

    def resume_power_timers(self) -> None:
        """Reanuda todos los temporizadores de PowerUp activos."""
        for timer in self.active_timers:
            timer.resume()

    def checker(self):
        current_delay = int(time.perf_counter() - self.init_time)

        if current_delay != 0 and (current_delay) % self.powerUp_delay == 0 and self.powerUpTrigger == False:
            if randint(0, 100) <= self.powerUp_CFG.probability : 
                new_powerup = PowerUp(self.powerUp_CFG)
                new_powerup.player_service = self.player_service
                self.powerUps.append(new_powerup)
                print("Power Up Spawned")
                self.powerUpTrigger=True

            threading.Thread(target=self.setter_powerUpTrigger, daemon=True).start()

        for power_up in self.powerUps:
                if power_up.update_and_draw(screen=self.screen.surface, player=self.player):
                    timer = power_up.activate_power_up()
                    self.active_timers.append(timer)
                    self.powerUps.remove(power_up)

        # Generación de Health: mismo rango que PowerUp, probabilidad más baja
        if current_delay != 0 and (current_delay) % self.powerUp_delay == 0 and self.healthTrigger == False:
            if randint(0, 100) <= self.health_CFG.probability:
                new_health = Health(self.health_CFG)
                self.healths.append(new_health)
                print("Health spawned")
                self.healthTrigger = True

            threading.Thread(target=self.setter_healthTrigger, daemon=True).start()

        for health in self.healths:
            if health.update_and_draw(screen=self.screen.surface, player=self.player):
                health.heal_player(self.player)
                self.healths.remove(health)

