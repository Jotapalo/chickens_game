import time
from src.model.PowerUp import PowerUp
from src.config.PowerUpConfig import PowerUpConfig
import threading

class EventGen:
    # recibe de forma recursiva powerUp List pero posteriormente se tiene que encapsular este comportamiento en otra entidad como un servicio
    def __init__(self, screen, player) -> None:
        self.init_time = time.perf_counter()
        self.powerUps: list[PowerUp] = list()
        self.screen = screen
        self.player = player
        self.powerUp_CFG = PowerUpConfig()

        self.powerUpTrigger = False

    def SetConfigPowerUp(self, delay: int):
        self.powerUp_delay = delay

    def setter_powerUpTrigger(self):
        time.sleep(2)
        self.powerUpTrigger = False


    def checker(self):
        current_delay = int(time.perf_counter() - self.init_time)

        if current_delay != 0 and (current_delay) % self.powerUp_delay == 0 and self.powerUpTrigger == False:
            self.powerUps.append(PowerUp(self.powerUp_CFG))
            print("Spawned")
            self.powerUpTrigger=True

            t = threading.Thread(target=self.setter_powerUpTrigger, daemon=True)
            t.start()

        for power_up in self.powerUps:
                if power_up.update_and_draw(screen=self.screen.surface, player=self.player):
                    power_up.activate_power_up()
                    self.powerUps.remove(power_up)

