from typing import TYPE_CHECKING
from src.model.Game import Game



if TYPE_CHECKING:
    from src.services.EnemyService import EnemyService
    from src.services.PlayerService import PlayerService
    from model import Screen
    from model.MessageOverlay import MessageOverlay
    from src.config.EnemyConfig import EnemyConfig

class Level:
    def __init__(self, game_context: Game):
        self.lock: bool
        self.enemySVC: EnemyService 
        self.playerSVC: PlayerService
        self.screen: Screen
        self.message_overlay: MessageOverlay
        
        self.enemyInfo: list[tuple[int, EnemyConfig, str]]
        self.waves_delay: int
        self.score:int 